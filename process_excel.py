import pandas as pd
import os
import re
import numpy as np

# --- CONFIGURATION ---
EXCEL_FOLDER_PATH = os.path.expanduser("~/Desktop/excel_data")
BATTING_FILENAME = "Batting 1_merged.xlsx"
BOWLING_FILENAME = "bowling 1 june _merged.xlsx"
OUTPUT_CSV_PATH = "master_stats.csv"

# --- Column mapping to standardize all variations ---
# 👇 UPDATED to include all new columns
COLUMN_MAP = {
    'Player Name': 'player_name', 'Team Name': 'team_name', 'Mat': 'matches_played',
    'Inns': 'innings', 'Runs': 'runs_scored', 'Balls': 'balls_faced',
    'Highest': 'highest_score', 'N/O': 'not_outs', 'Avg': 'batting_average',
    'SR': 'batting_strike_rate', '4s': 'fours', '6s': 'sixes', '50s': 'fifties',
    '100s': 'hundreds', 'Overs': 'overs_bowled', 'Wickets': 'wickets_taken',
    'Econ': 'economy_rate', 'Maidens': 'maidens', 'Batting Hand': 'batting_style',
    'Bowling Style': 'bowling_style'
}
BOWLING_RENAME_MAP = {
    'runs_scored': 'runs_conceded',
    'batting_average': 'bowling_average',
    'batting_strike_rate': 'bowling_strike_rate'
}

def find_header_row(df_head):
    for i, row in df_head.iterrows():
        if 'Player Name' in row.values:
            return i
    return 0

def clean_player_name(name):
    if isinstance(name, str):
        return " ".join(name.strip().split()).title()
    return name

def process_excel_file(filepath, is_bowling=False):
    xls = pd.ExcelFile(filepath)
    all_sheets_data = []
    for sheet_name in xls.sheet_names:
        match = re.search(r'(\d+)', sheet_name)
        if not match:
            continue
        tournament_id = int(match.group(1))
        header_row_index = find_header_row(pd.read_excel(xls, sheet_name=sheet_name, header=None, nrows=5))
        df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_index)
        df.rename(columns=COLUMN_MAP, inplace=True)
        if is_bowling:
            df.rename(columns=BOWLING_RENAME_MAP, inplace=True)
        df['tournament_id'] = tournament_id
        df['player_name'] = df['player_name'].apply(clean_player_name)
        all_sheets_data.append(df)
    return pd.concat(all_sheets_data, ignore_index=True)

def main():
    """Main function to run the entire process."""
    batting_filepath = os.path.join(EXCEL_FOLDER_PATH, BATTING_FILENAME)
    bowling_filepath = os.path.join(EXCEL_FOLDER_PATH, BOWLING_FILENAME)

    batting_df = process_excel_file(batting_filepath, is_bowling=False)
    bowling_df = process_excel_file(bowling_filepath, is_bowling=True)

    print("\nMerging batting and bowling data...")
    final_df = pd.merge(batting_df, bowling_df, on=['player_name', 'tournament_id'], how='outer', suffixes=('_bat', '_bowl'))

    # Combine columns that might appear in both files
    for col in ['matches_played', 'team_name', 'batting_style', 'bowling_style']:
        col_bat, col_bowl = f'{col}_bat', f'{col}_bowl'
        if col_bat in final_df.columns and col_bowl in final_df.columns:
            # Fill missing values from one column with values from the other
            final_df[col] = final_df[col_bat].fillna(final_df[col_bowl])
        elif col_bat in final_df.columns:
            final_df[col] = final_df[col_bat]
        elif col_bowl in final_df.columns:
            final_df[col] = final_df[col_bowl]
            
    if 'highest_score_bat' in final_df.columns:
        final_df.rename(columns={'highest_score_bat': 'highest_score'}, inplace=True)

    # 👇 This list now defines everything we want to keep
    final_columns_order = [
        'player_name', 'tournament_id', 'team_name', 'batting_style', 'bowling_style',
        'matches_played', 'runs_scored', 'balls_faced', 'highest_score', 'not_outs',
        'fours', 'sixes', 'fifties', 'hundreds', 'batting_average', 'batting_strike_rate',
        'overs_bowled', 'runs_conceded', 'wickets_taken', 'maidens', 'bowling_average',
        'economy_rate', 'bowling_strike_rate'
    ]

    final_df_filtered = final_df[[col for col in final_columns_order if col in final_df.columns]]
    final_df_filtered = final_df_filtered.replace({np.nan: None})
    final_df_filtered.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"\n✅ Success! All data processed and saved to '{OUTPUT_CSV_PATH}'.")

if __name__ == "__main__":
    main()