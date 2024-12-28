import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import os
from datetime import datetime

DATASET_PATHS = {
    "initial": "https://raw.githubusercontent.com/gustavofcunha/CloudComputing2/main/spotify/2023_spotify_ds1.csv"
}

RULES_FILE_PATH = "/modelo/data/rules.pkl"
#RULES_FILE_PATH = "/home/gustavocunha/TP-2/rules.pkl"

VERSION = 1.0
DATE = datetime.now().strftime("%d-%m-%Y")

def load_and_transform_dataset(file_path):
    df = pd.read_csv(file_path, usecols=['pid', 'track_name'])
    transactions = df.groupby('pid')['track_name'].apply(list).tolist()
    return transactions

def generate_rules(transactions, min_support=0.05, min_confidence=0.4):
    """Generate association rules from transactions."""
    _, rules = fpgrowth(transactions, minSupRatio=min_support, minConf=min_confidence)
    return rules

def save_rules(rules, file_path):
    pickle_data = {
        "rules": rules,
        "version": VERSION,
        "date": DATE
    }

    with open(file_path, 'wb') as f:
        pickle.dump(pickle_data, f)

def main():
    initial_transactions = load_and_transform_dataset(DATASET_PATHS["initial"])

    initial_rules = generate_rules(initial_transactions)
    
    save_rules(initial_rules, RULES_FILE_PATH)
    print(f"Rules saved to {RULES_FILE_PATH}")

if __name__ == "__main__":
    main()
