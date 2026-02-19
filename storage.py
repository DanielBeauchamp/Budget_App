import json
import os

DATA_FILE = "budget.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "period": "2026-02",
            "expenses": [],
            "limits": {
                "Food": 150,
                "Transportation": 75,
                "Entertainment": 100,
                "Misc": 50
            }
        }

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
