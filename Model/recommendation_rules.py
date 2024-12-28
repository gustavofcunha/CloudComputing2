import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import os

DATASET_PATHS = {
    "initial": "https://raw.githubusercontent.com/gustavofcunha/CloudComputing2/main/spotify/2023_spotify_ds1.csv",
    "songs": "https://raw.githubusercontent.com/gustavofcunha/CloudComputing2/main/spotify/2023_spotify_songs.csv"
}

RULES_FILE_PATH = "modelo/rules.pkl"

def load_and_transform_dataset(file_path):
    """Load and transform dataset into a list of transactions in one step."""
    df = pd.read_csv(file_path, usecols=['pid', 'track_uri'])
    transactions = df.groupby('pid')['track_uri'].apply(list).tolist()
    return df, transactions

def load_song_list(file_path):
    """Load song list to check for tracks outside original transactions."""
    df = pd.read_csv(file_path, usecols=['track_name', 'artist_name'])
    df['identifier'] = df['track_name'] + " - " + df['artist_name']
    return df['identifier'].tolist()

def find_most_popular_song(df):
    """Find the most popular song based on frequency in the dataset."""
    popular_song = df['track_uri'].value_counts().idxmax()
    return popular_song

def generate_rules(transactions, min_support=0.05, min_confidence=0.6):
    """Generate association rules from transactions."""
    _, rules = fpgrowth(transactions, minSupRatio=min_support, minConf=min_confidence)
    return rules

def transform_rules(rules, known_songs, most_popular_song):
    """
    Transform rules into the format expected by the server and include fallback rules.
    - Add rules for songs in `known_songs` that are missing from the transactions.
    """
    transformed_rules = [(list(rule[0]), list(rule[1])) 
                         for rule in rules if len(rule) == 3 and isinstance(rule[0], set) and isinstance(rule[1], set)]
    
    # Create fallback rules for songs not covered in the transactions
    fallback_rules = []
    for song in known_songs:
        if not any(song in rule[0] or song in rule[1] for rule in transformed_rules):
            fallback_rules.append(([song], [most_popular_song]))
    
    return transformed_rules + fallback_rules

def save_rules(rules, file_path):
    """Save generated rules to a pickle file in the correct format."""
    with open(file_path, 'wb') as f:
        pickle.dump(rules, f)

def main():
    initial_df, initial_transactions = load_and_transform_dataset(DATASET_PATHS["initial"])

    most_popular_song = find_most_popular_song(initial_df)

    known_songs = load_song_list(DATASET_PATHS["songs"])

    initial_rules = generate_rules(initial_transactions)
    transformed_initial_rules = transform_rules(initial_rules, known_songs, most_popular_song)
    save_rules(transformed_initial_rules, RULES_FILE_PATH)
    print(f"Rules saved to {RULES_FILE_PATH}")

if __name__ == "__main__":
    main()
