from rest_framework import serializers
from .models import Player, PlayerTournamentStat, Tournament


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name']

# --- Nested Serializers for Cleanliness ---

class BattingStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerTournamentStat
        fields = [
            'matches_played', 'runs_scored', 'balls_faced', 'highest_score', 'not_outs',
            'fours', 'sixes', 'fifties', 'hundreds', 'batting_average', 'batting_strike_rate'
        ]

class BowlingStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerTournamentStat
        fields = [
            'overs_bowled', 'runs_conceded', 'wickets_taken', 'maidens',
            'bowling_average', 'economy_rate', 'bowling_strike_rate'
        ]

# --- Main Serializer for Player Detail Page ---

class PlayerTournamentStatSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source='tournament.name', read_only=True)
    team_name = serializers.CharField()
    batting = BattingStatsSerializer(source='*')
    bowling = BowlingStatsSerializer(source='*')
    player_name = serializers.CharField(source='player.name', read_only=True)

    class Meta:
        model = PlayerTournamentStat
        fields = ['player_name', 'tournament_name', 'team_name', 'batting', 'bowling']

class PlayerSerializer(serializers.ModelSerializer):
    stats = PlayerTournamentStatSerializer(many=True, read_only=True, source='playertournamentstat_set')

    class Meta:
        model = Player
        fields = ['id', 'name', 'playing_role', 'batting_style', 'bowling_style', 'stats']


# --- Serializer for the Career Leaderboards & Top Performers ---

class CareerStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for aggregating player stats across all tournaments.
    """
    class Meta:
        model = Player
        fields = '__all__'

class TopPerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'