from rest_framework import viewsets
from django.db.models import Sum, Max
from .models import Player, PlayerTournamentStat, Tournament
from .serializers import (
    PlayerSerializer, PlayerTournamentStatSerializer, CareerStatsSerializer, TournamentSerializer
)

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

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
            total_matches=Sum('playertournamentstat__matches_played'),
            total_runs=Sum('playertournamentstat__runs_scored'),
            total_wickets=Sum('playertournamentstat__wickets_taken'),
            career_highest_score=Max('playertournamentstat__highest_score'),
            total_not_outs=Sum('playertournamentstat__not_outs'),
            total_fours=Sum('playertournamentstat__fours'),
            total_sixes=Sum('playertournamentstat__sixes'),
            total_maidens=Sum('playertournamentstat__maidens')
        ).order_by('-total_runs')