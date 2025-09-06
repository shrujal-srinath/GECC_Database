import csv
from django.core.management.base import BaseCommand
from api.models import Player, Tournament, PlayerTournamentStat
import pandas as pd

def to_int(value):
    """Helper function to safely convert a value to an integer, returning None on failure."""
    try:
        # Handle cases where value might be None or empty string
        if value is None or value == '':
            return None
        return int(float(value))
    except (ValueError, TypeError):
        return None

def to_float(value):
    """Helper function to safely convert a value to a float, returning None on failure."""
    try:
        if value is None or value == '':
            return None
        return float(value)
    except (ValueError, TypeError):
        return None

class Command(BaseCommand):
    help = 'Imports player tournament stats from master_stats.csv'

    def handle(self, *args, **kwargs):
        csv_file_path = 'master_stats.csv'
        self.stdout.write(f"Starting import from {csv_file_path}...")

        # Clear only the stats, not the players or tournaments, to preserve IDs
        PlayerTournamentStat.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all existing tournament stats."))

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                stats_created = 0
                players_updated = 0

                for row in reader:
                    player_name = row.get('player_name')
                    if not player_name or pd.isna(player_name):
                        continue

                    # Get or create the player
                    player, created = Player.objects.get_or_create(name=player_name.strip())

                    # --- NEW: Update Player profile info if available ---
                    player_updated_flag = False
                    if row.get('batting_style') and not player.batting_style:
                        player.batting_style = row['batting_style']
                        player_updated_flag = True
                    if row.get('bowling_style') and not player.bowling_style:
                        player.bowling_style = row['bowling_style']
                        player_updated_flag = True
                    
                    if player_updated_flag:
                        player.save()
                        players_updated += 1


                    tournament_id = to_int(row.get('tournament_id'))
                    if tournament_id is None:
                        continue
                    
                    # Use a consistent year for now
                    tournament, _ = Tournament.objects.get_or_create(
                        id=tournament_id,
                        defaults={'name': f"Tournament {tournament_id}", 'year': 2024}
                    )
                    
                    # Create the detailed stat record
                    PlayerTournamentStat.objects.create(
                        player=player,
                        tournament=tournament,
                        team_name=row.get('team_name'),
                        matches_played=to_int(row.get('matches_played')),
                        runs_scored=to_int(row.get('runs_scored')),
                        balls_faced=to_int(row.get('balls_faced')),
                        highest_score=to_int(row.get('highest_score')),
                        not_outs=to_int(row.get('not_outs')),
                        fours=to_int(row.get('fours')),
                        sixes=to_int(row.get('sixes')),
                        fifties=to_int(row.get('fifties')),
                        hundreds=to_int(row.get('hundreds')),
                        batting_average=to_float(row.get('batting_average')),
                        batting_strike_rate=to_float(row.get('batting_strike_rate')),
                        overs_bowled=to_float(row.get('overs_bowled')),
                        runs_conceded=to_int(row.get('runs_conceded')),
                        wickets_taken=to_int(row.get('wickets_taken')),
                        maidens=to_int(row.get('maidens')),
                        bowling_average=to_float(row.get('bowling_average')),
                        economy_rate=to_float(row.get('economy_rate')),
                        bowling_strike_rate=to_float(row.get('bowling_strike_rate')),
                    )
                    stats_created += 1

            self.stdout.write(self.style.SUCCESS(f"\nImport complete! All rows processed."))
            self.stdout.write(self.style.SUCCESS(f"  - Stats Records Created: {stats_created}"))
            self.stdout.write(self.style.SUCCESS(f"  - Player Profiles Updated: {players_updated}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: The file '{csv_file_path}' was not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))