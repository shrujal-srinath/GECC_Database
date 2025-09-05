from rest_framework import serializers
from .models import Player, PlayerTournamentStat, Tournament

class PlayerTournamentStatSerializer(serializers.ModelSerializer):
    # Include the tournament's name for easy display
    tournament_name = serializers.CharField(source='tournament.name', read_only=True)
    
    class Meta:
        model = PlayerTournamentStat
        fields = [
            'tournament_name', 'matches_played', 'runs_scored', 
            'balls_faced', 'highest_score', 'batting_average', 
            'batting_strike_rate', 'overs_bowled', 'runs_conceded', 
            'wickets_taken', 'bowling_average', 'economy_rate', 'bowling_strike_rate'
        ]

class PlayerSerializer(serializers.ModelSerializer):
    # This nests all of a player's stats directly into the player's API response
    stats = PlayerTournamentStatSerializer(many=True, read_only=True, source='playertournamentstat_set')

    class Meta:
        model = Player
        fields = ['id', 'name', 'playing_role', 'batting_style', 'bowling_style', 'stats']