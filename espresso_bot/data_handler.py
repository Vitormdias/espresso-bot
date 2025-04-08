import json
import os

def load_history(db_path):
    try:
        with open(db_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_entry(data, db_path):
    history = load_history(db_path)
    history.append(data)
    with open(db_path, "w") as f:
        json.dump(history, f, indent=2)
