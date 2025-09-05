import csv
from django.core.management.base import BaseCommand
from api.models import Player, Tournament, PlayerTournamentStat
import pandas as pd # 👈 THE FIX IS HERE

def to_int(value):
    """Helper function to safely convert a value to an integer, returning None on failure."""
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None

def to_float(value):
    """Helper function to safely convert a value to a float, returning None on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

class Command(BaseCommand):
    help = 'Imports player tournament stats from master_stats.csv'

    def handle(self, *args, **kwargs):
        csv_file_path = 'master_stats.csv'
        self.stdout.write(f"Starting import from {csv_file_path}...")

        PlayerTournamentStat.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all existing tournament stats."))

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                stats_created = 0

                for row in reader:
                    player_name = row.get('player_name')
                    if not player_name or pd.isna(player_name):
                        continue

                    player, _ = Player.objects.get_or_create(name=player_name.strip())

                    tournament_id = to_int(row.get('tournament_id'))
                    if tournament_id is None:
                        continue

                    tournament, _ = Tournament.objects.get_or_create(
                        name=f"Tournament {tournament_id}",
                        defaults={'year': 2024}
                    )

                    PlayerTournamentStat.objects.create(
                        player=player,
                        tournament=tournament,
                        matches_played=to_int(row.get('matches_played')),
                        runs_scored=to_int(row.get('runs_scored')),
                        balls_faced=to_int(row.get('balls_faced')),
                        highest_score=to_int(row.get('highest_score')),
                        batting_average=to_float(row.get('batting_average')),
                        batting_strike_rate=to_float(row.get('batting_strike_rate')),
                        overs_bowled=to_float(row.get('overs_bowled')),
                        runs_conceded=to_int(row.get('runs_conceded')),
                        wickets_taken=to_int(row.get('wickets_taken')),
                        bowling_average=to_float(row.get('bowling_average')),
                        economy_rate=to_float(row.get('economy_rate')),
                        bowling_strike_rate=to_float(row.get('bowling_strike_rate')),
                    )
                    stats_created += 1

            self.stdout.write(self.style.SUCCESS(f"\nImport complete! All rows processed."))
            self.stdout.write(self.style.SUCCESS(f"  - Stats Records Created: {stats_created}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: The file '{csv_file_path}' was not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))