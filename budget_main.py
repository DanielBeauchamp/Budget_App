import tkinter as tk
import json
import os

# -----------------------------
# Configuration
# -----------------------------

CATEGORIES = ["Food", "Transportation", "Entertainment", "Misc"]
DATA_FILE = "budget.json"

# -----------------------------
# Data Handling
# -----------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"expenses": []}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

data = load_data()

# -----------------------------
# Logic
# -----------------------------

def add_expense(category):
    try:
        amount = float(amount_entry.get())
    except ValueError:
        return  # Invalid input, silently ignore for now

    expense = {
        "amount": amount,
        "category": category
    }

    data["expenses"].append(expense)
    save_data(data)

    amount_entry.delete(0, tk.END)
    update_totals()

def calculate_totals():
    totals = {category: 0 for category in CATEGORIES}
    for expense in data["expenses"]:
        totals[expense["category"]] += expense["amount"]
    return totals

# -----------------------------
# UI
# -----------------------------

root = tk.Tk()
root.title("Budget App - Version 0")

# Amount input
amount_label = tk.Label(root, text="Amount:")
amount_label.pack()

amount_entry = tk.Entry(root)
amount_entry.pack()

# Category buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

for category in CATEGORIES:
    button = tk.Button(
        button_frame,
        text=category,
        width=15,
        command=lambda c=category: add_expense(c)
    )
    button.pack(side=tk.LEFT, padx=5)

# Totals display
totals_label = tk.Label(root, text="", justify=tk.LEFT)
totals_label.pack(pady=10)

def update_totals():
    totals = calculate_totals()
    text = "Totals:\n"
    for category, total in totals.items():
        text += f"{category}: ${total:.2f}\n"
    totals_label.config(text=text)

update_totals()

root.mainloop()
