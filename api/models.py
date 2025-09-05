
from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)
    playing_role = models.CharField(max_length=50)
    batting_style = models.CharField(max_length=50, blank=True)
    bowling_style = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
    
# new model for match and induvidul performance 

class Match(models.Model):
    date = models.DateField()
    venue = models.CharField(max_length=100)
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    winner_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.team1_name} vs {self.team2_name} on {self.date}"

class BattingPerformance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    runs_scored = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.name}: {self.runs_scored} ({self.balls_faced}) in Match {self.match.id}"

class BowlingPerformance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    overs_bowled = models.FloatField(default=0.0)
    runs_conceded = models.IntegerField(default=0)
    wickets_taken = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.name}: {self.wickets_taken} wickets for {self.runs_conceded} in Match {self.match.id}"
    
    
# ... (Keep your existing Player, Match, etc. models at the top) ...

# new addition made for player stats 

class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.year})"

# ... (CHANGED BELOW TO ALLOW NULL) ...

class PlayerTournamentStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    # Batting Stats
    matches_played = models.IntegerField(default=0, null=True, blank=True)
    runs_scored = models.IntegerField(default=0, null=True, blank=True)
    balls_faced = models.IntegerField(default=0, null=True, blank=True)
    highest_score = models.IntegerField(default=0, null=True, blank=True)
    batting_average = models.FloatField(null=True, blank=True)
    batting_strike_rate = models.FloatField(null=True, blank=True)

    # Bowling Stats
    overs_bowled = models.FloatField(null=True, blank=True)
    runs_conceded = models.IntegerField(default=0, null=True, blank=True)
    wickets_taken = models.IntegerField(default=0, null=True, blank=True)
    bowling_average = models.FloatField(null=True, blank=True)
    economy_rate = models.FloatField(null=True, blank=True)
    bowling_strike_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.name}'s stats for {self.tournament.name}"