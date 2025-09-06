from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlayerViewSet, PlayerTournamentStatViewSet, CareerStatsViewSet, TournamentViewSet
)

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'stats', PlayerTournamentStatViewSet)
router.register(r'career-stats', CareerStatsViewSet, basename='career-stats')
router.register(r'tournaments', TournamentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]