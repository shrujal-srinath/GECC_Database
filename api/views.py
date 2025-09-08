from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Max, F
from django.db.models.functions import Coalesce
from .models import Player, PlayerTournamentStat, Tournament
from .serializers import (
    PlayerSerializer, PlayerTournamentStatSerializer, CareerStatsSerializer, TournamentSerializer, TopPerformerSerializer
)

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @action(detail=True, methods=['get'])
    def career_summary(self, request, pk=None):
        player_queryset = Player.objects.filter(pk=pk).annotate(
            total_matches=Coalesce(Sum('playertournamentstat__matches_played'), 0),
            total_runs=Coalesce(Sum('playertournamentstat__runs_scored'), 0),
            total_wickets=Coalesce(Sum('playertournamentstat__wickets_taken'), 0),
            career_highest_score=Max('playertournamentstat__highest_score'),
            total_not_outs=Coalesce(Sum('playertournamentstat__not_outs'), 0),
            total_fours=Coalesce(Sum('playertournamentstat__fours'), 0),
            total_sixes=Coalesce(Sum('playertournamentstat__sixes'), 0),
            total_maidens=Coalesce(Sum('playertournamentstat__maidens'), 0)
        )
        try:
            player = player_queryset.get()
        except Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        career_stats_serializer = CareerStatsSerializer(player)
        player_serializer = PlayerSerializer(player)
        
        response_data = {
            'id': player_serializer.data['id'],
            'name': player_serializer.data['name'],
            'playing_role': player_serializer.data['playing_role'],
            'batting_style': player_serializer.data['batting_style'],
            'bowling_style': player_serializer.data['bowling_style'],
            'stats': player_serializer.data['stats'],
            'career_summary': career_stats_serializer.data
        }

        return Response(response_data)


class PlayerTournamentStatViewSet(viewsets.ModelViewSet):
    queryset = PlayerTournamentStat.objects.all()
    serializer_class = PlayerTournamentStatSerializer
    filterset_fields = ['tournament']

class TournamentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tournament.objects.all().order_by('id')
    serializer_class = TournamentSerializer

class CareerStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This view provides aggregated career stats for each player.
    """
    serializer_class = CareerStatsSerializer

    def get_queryset(self):
        return Player.objects.annotate(
            total_matches=Coalesce(Sum('playertournamentstat__matches_played'), 0),
            total_runs=Coalesce(Sum('playertournamentstat__runs_scored'), 0),
            total_wickets=Coalesce(Sum('playertournamentstat__wickets_taken'), 0),
            career_highest_score=Coalesce(Max('playertournamentstat__highest_score'), 0),
            total_not_outs=Coalesce(Sum('playertournamentstat__not_outs'), 0),
            total_fours=Coalesce(Sum('playertournamentstat__fours'), 0),
            total_sixes=Coalesce(Sum('playertournamentstat__sixes'), 0),
            total_fifties=Coalesce(Sum('playertournamentstat__fifties'), 0),
            total_hundreds=Coalesce(Sum('playertournamentstat__hundreds'), 0),
            total_overs_bowled=Coalesce(Sum('playertournamentstat__overs_bowled'), 0),
            total_runs_conceded=Coalesce(Sum('playertournamentstat__runs_conceded'), 0),
            total_maidens=Coalesce(Sum('playertournamentstat__maidens'), 0)
        ).order_by(F('total_runs').desc(nulls_last=True))

class TopPerformersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = TopPerformerSerializer

    def get_queryset(self):
        return Player.objects.annotate(
            total_matches=Coalesce(Sum('playertournamentstat__matches_played'), 0),
            total_runs=Coalesce(Sum('playertournamentstat__runs_scored'), 0),
            career_highest_score=Coalesce(Max('playertournamentstat__highest_score'), 0),
            total_wickets=Coalesce(Sum('playertournamentstat__wickets_taken'), 0),
            total_fours=Coalesce(Sum('playertournamentstat__fours'), 0),
            total_sixes=Coalesce(Sum('playertournamentstat__sixes'), 0),
            total_fifties=Coalesce(Sum('playertournamentstat__fifties'), 0),
            total_hundreds=Coalesce(Sum('playertournamentstat__hundreds'), 0),
            total_maidens=Coalesce(Sum('playertournamentstat__maidens'), 0)
        )

    @action(detail=False, methods=['get'])
    def top_batsman(self, request):
        top_batsman = self.get_queryset().order_by(F('total_runs').desc(nulls_last=True)).first()
        serializer = self.get_serializer(top_batsman)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_bowler(self, request):
        top_bowler = self.get_queryset().order_by(F('total_wickets').desc(nulls_last=True)).first()
        serializer = self.get_serializer(top_bowler)
        return Response(serializer.data)