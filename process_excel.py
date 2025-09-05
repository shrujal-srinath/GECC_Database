import pandas as pd
import os
import re

# --- CONFIGURATION ---
EXCEL_FOLDER_PATH = os.path.expanduser("~/Desktop/excel_data")
BATTING_FILENAME = "Batting 1_merged.xlsx"
BOWLING_FILENAME = "bowling 1 june _merged.xlsx"
OUTPUT_CSV_PATH = "master_stats.csv"

# --- Column mapping to standardize all variations ---
COLUMN_MAP = {
    'Player Name': 'player_name', 'Mat': 'matches_played', 'Inns': 'innings',
    'Runs': 'runs_scored', 'Balls': 'balls_faced', 'Highest': 'highest_score',
    'N/O': 'not_outs', 'NIO': 'not_outs', 'Avg': 'batting_average', 'SR': 'batting_strike_rate',
    'Overs': 'overs_bowled', 'Wickets': 'wickets_taken', 'Econ': 'economy_rate',
}
BOWLING_RENAME_MAP = {
    'runs_scored': 'runs_conceded',
    'batting_average': 'bowling_average',
    'batting_strike_rate': 'bowling_strike_rate'
}

def find_header_row(df_head):
    """Finds the actual header row in the first few lines of a sheet."""
    for i, row in df_head.iterrows():
        if 'Player Name' in row.values:
            return i
    return 0

def clean_player_name(name):
    """Standardizes player names."""
    if isinstance(name, str):
        return " ".join(name.strip().split()).title()
    return name

def process_excel_file(filepath, is_bowling=False):
    """Reads all sheets from a single Excel file and returns a list of dataframes."""
    print(f"Processing {'Bowling' if is_bowling else 'Batting'} file: {os.path.basename(filepath)}...")
    xls = pd.ExcelFile(filepath)
    all_sheets_data = []

    for sheet_name in xls.sheet_names:
        # Extract tournament ID from sheet name like "Table 1", "Table 12"
        match = re.search(r'(\d+)', sheet_name)
        if not match:
            continue
        tournament_id = int(match.group(1))

        # Find the header row to handle inconsistent starting rows
        header_row_index = find_header_row(pd.read_excel(xls, sheet_name=sheet_name, header=None, nrows=5))
        df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_index)

        # Standardize column names
        df.rename(columns=COLUMN_MAP, inplace=True)
        if is_bowling:
            df.rename(columns=BOWLING_RENAME_MAP, inplace=True)

        df['tournament_id'] = tournament_id
        df['player_name'] = df['player_name'].apply(clean_player_name)

        all_sheets_data.append(df)
        print(f"  - Successfully processed Tournament {tournament_id} from sheet '{sheet_name}'")

    return pd.concat(all_sheets_data, ignore_index=True)

def main():
    """Main function to run the entire process."""
    batting_filepath = os.path.join(EXCEL_FOLDER_PATH, BATTING_FILENAME)
    bowling_filepath = os.path.join(EXCEL_FOLDER_PATH, BOWLING_FILENAME)

    batting_df = process_excel_file(batting_filepath, is_bowling=False)
    bowling_df = process_excel_file(bowling_filepath, is_bowling=True)

    print("\nMerging batting and bowling data...")
    # Merge the two master dataframes
    final_df = pd.merge(batting_df, bowling_df, on=['player_name', 'tournament_id'], how='outer')

    # Clean up and fill missing values
    final_df.fillna(0, inplace=True)

    # Select and order final columns for the database
    final_columns = [
        'player_name', 'tournament_id', 'matches_played_x', 'runs_scored', 
        'balls_faced', 'highest_score', 'not_outs_x', 'batting_average', 
        'batting_strike_rate', 'overs_bowled', 'runs_conceded', 'wickets_taken', 
        'bowling_average', 'economy_rate', 'bowling_strike_rate'
    ]
    # Rename merged columns (like 'matches_played_x')
    final_df.rename(columns={'matches_played_x': 'matches_played', 'not_outs_x': 'not_outs'}, inplace=True)

    # Filter for columns that actually exist to prevent errors
    existing_cols = [col for col in final_df.columns if col in final_columns]
    final_df = final_df[existing_cols]

    final_df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"\n✅ Success! All data processed and saved to '{OUTPUT_CSV_PATH}'.")

if __name__ == "__main__":
    main()