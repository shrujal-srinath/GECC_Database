# In api/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Max
from django.core.mail import send_mail
from .models import Player, PlayerTournamentStat, Tournament, PlayerEditRequest
from .serializers import (
    PlayerSerializer, PlayerTournamentStatSerializer, CareerStatsSerializer, TournamentSerializer,
    PlayerEditRequestSerializer
)

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    # 🚨 New custom action to handle edit requests
    @action(detail=True, methods=['post'], url_path='request-edit')
    def request_edit(self, request, pk=None):
        player = self.get_object()
        serializer = PlayerEditRequestSerializer(data={'player': player.id, 'proposed_changes': request.data})
        if serializer.is_valid():
            serializer.save()

            # 🚨 Send an email notification to the admin
            send_mail(
                'New Player Edit Request',
                f'A new edit request has been submitted for {player.name}. Please review it in the Django admin panel.',
                'noreply@yourdomain.com', # Replace with a valid sender email
                ['your-admin-email@example.com'], # Replace with your admin email
                fail_silently=False,
            )
            
            return Response(
                {'status': 'Edit request submitted for approval.'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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