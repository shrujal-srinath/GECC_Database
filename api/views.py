from rest_framework import viewsets
from .models import Player
from .serializers import PlayerSerializer

# This is the only ViewSet we need now.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer