from rest_framework import serializers
from .models import Player, PlayerTournamentStat , Tournament


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
    batting = BattingStatsSerializer(source='*') # Use the nested serializer
    bowling = BowlingStatsSerializer(source='*') # Use the nested serializer
    player_name = serializers.CharField(source='player.name', read_only=True) # 👈 **THIS IS THE FIX**

    class Meta:
        model = PlayerTournamentStat
        # 👇 **'player_name' IS NOW ADDED HERE**
        fields = ['player_name', 'tournament_name', 'team_name', 'batting', 'bowling']

class PlayerSerializer(serializers.ModelSerializer):
    # This nests all of a player's stats directly into the player's API response
    stats = PlayerTournamentStatSerializer(many=True, read_only=True, source='playertournamentstat_set')

    class Meta:
        model = Player
        # 👇 ADDED batting_style and bowling_style
        fields = ['id', 'name', 'playing_role', 'batting_style', 'bowling_style', 'stats']


# --- Serializer for the Career Leaderboards ---

class CareerStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for aggregating player stats across all tournaments.
    """
    # Batting
    total_matches = serializers.IntegerField()
    total_runs = serializers.IntegerField()
    total_not_outs = serializers.IntegerField()
    total_fours = serializers.IntegerField()
    total_sixes = serializers.IntegerField()
    career_highest_score = serializers.IntegerField()

    # Bowling
    total_wickets = serializers.IntegerField()
    total_maidens = serializers.IntegerField()

    class Meta:
        model = Player
        fields = [
            'name', 'total_matches', 'total_runs', 'total_wickets',
            'career_highest_score', 'total_not_outs', 'total_fours',
            'total_sixes', 'total_maidens'
        ]