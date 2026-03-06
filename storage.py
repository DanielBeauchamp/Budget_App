import json
import os

DATA_FILE = "budget.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "current_period": 1,
            "expenses": [],
            "limits": {
                "Food": 150,
                "Transportation": 75,
                "Entertainment": 100,
                "Misc": 50
            },
            "history": []
        }

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    if "current_period" not in data:
        data["current_period"] = 1
    if "history" not in data:
        data["history"] = []

    return data

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)