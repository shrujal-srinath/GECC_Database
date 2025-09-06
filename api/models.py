from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    # 👇 ADDED/UPDATED THESE FIELDS FOR THE PLAYER PROFILE
    playing_role = models.CharField(max_length=50, blank=True, null=True)
    batting_style = models.CharField(max_length=50, blank=True, null=True)
    bowling_style = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.year})"

class PlayerTournamentStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100, blank=True, null=True) # 👈 ADDED

    # Batting Stats
    matches_played = models.IntegerField(default=0, null=True, blank=True)
    runs_scored = models.IntegerField(default=0, null=True, blank=True)
    balls_faced = models.IntegerField(default=0, null=True, blank=True)
    highest_score = models.IntegerField(default=0, null=True, blank=True)
    not_outs = models.IntegerField(default=0, null=True, blank=True) # 👈 ADDED
    fours = models.IntegerField(default=0, null=True, blank=True) # 👈 ADDED
    sixes = models.IntegerField(default=0, null=True, blank=True) # 👈 ADDED
    fifties = models.IntegerField(default=0, null=True, blank=True) # 👈 ADDED
    hundreds = models.IntegerField(default=0, null=True, blank=True) # 👈 ADDED
    batting_average = models.FloatField(null=True, blank=True)
    batting_strike_rate = models.FloatField(null=True, blank=True)

    # Bowling Stats
    overs_bowled = models.FloatField(null=True, blank=True)
    runs_conceded = models.IntegerField(default=0, null=True, blank=True)
    wickets_taken = models.IntegerField(default=0, null=True, blank=True)
    maidens = models.IntegerField(default=0, null=True, blank=True) # 👈 ADDED
    bowling_average = models.FloatField(null=True, blank=True)
    economy_rate = models.FloatField(null=True, blank=True)
    bowling_strike_rate = models.FloatField(null=True, blank=True)
    # We can add best_bowling_figures later if needed

    def __str__(self):
        return f"{self.player.name}'s stats for {self.tournament.name}"

# We are no longer using these models, but it's safe to leave them for now
class Match(models.Model):
    date = models.DateField()
    venue = models.CharField(max_length=100)
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    winner_name = models.CharField(max_length=100, blank=True)

class BattingPerformance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    runs_scored = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)

class BowlingPerformance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    overs_bowled = models.FloatField(default=0.0)
    runs_conceded = models.IntegerField(default=0)
    wickets_taken = models.IntegerField(default=0)