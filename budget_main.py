import tkinter as tk
import json
import os

# -----------------------------
# Configuration
# -----------------------------

CATEGORIES = ["Food", "Transportation", "Entertainment", "Misc"]
DATA_FILE = "budget.json"
CATEGORY_LIMITS = {
    "Food": 150,
    "Transportation": 75,
    "Entertainment": 100,
    "Misc": 50
}

TOTAL_LIMIT = 300
WARNING_THRESHOLD = 0.8


# -----------------------------
# Data Handling
# -----------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "expenses": [],
            "limits": {
                "Food": 150,
                "Transportation": 75,
                "Entertainment": 100,
                "Misc": 50
            }
        }

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    if "limits" not in data:
        data["limits"] = {
            "Food": 150,
            "Transportation": 75,
            "Entertainment": 100,
            "Misc": 50
        }

    return data


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

data = load_data()

# -----------------------------
# Logic
# -----------------------------

def save_limits():
    for category, entry in limit_entries.items():
        try:
            value = float(entry.get())
            if value >= 0:
                data["limits"][category] = value
        except ValueError:
            continue  # Ignore bad input

    save_data(data)
    update_totals()


def calculate_status(totals):
    status = {}

    for category, spent in totals.items():
        limit = data["limits"].get(category, 0)
        ratio = spent / limit if limit > 0 else 0

        if ratio >= 1:
            status[category] = "exceeded"
        elif ratio >= WARNING_THRESHOLD:
            status[category] = "warning"
        else:
            status[category] = "normal"

    total_spent = sum(totals.values())
    total_limit = get_total_limit()
    total_ratio = total_spent / total_limit if total_limit > 0 else 0

    if total_ratio >= 1:
        total_status = "exceeded"
    elif total_ratio >= WARNING_THRESHOLD:
        total_status = "warning"
    else:
        total_status = "normal"

    return status, total_spent, total_status


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

def get_total_limit():
    return sum(data["limits"].values())


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

limits_frame = tk.LabelFrame(root, text="Category Limits")
limits_frame.pack(pady=10, fill="x")

limit_entries = {}

for category in CATEGORIES:
    row = tk.Frame(limits_frame)
    row.pack(fill="x", pady=2)

    label = tk.Label(row, text=category, width=15, anchor="w")
    label.pack(side=tk.LEFT)

    entry = tk.Entry(row, width=10)
    entry.insert(0, str(data["limits"][category]))
    entry.pack(side=tk.LEFT)

    limit_entries[category] = entry

save_limits_button = tk.Button(
    limits_frame,
    text="Save Limits",
    command=save_limits
)
save_limits_button.pack(pady=5)


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
    status, total_spent, total_status = calculate_status(totals)
    total_limit = get_total_limit()

    text = "Totals:\n"

    for category, total in totals.items():
        limit = data["limits"][category]
        cat_status = status[category]

        text += f"{category}: ${total:.2f} / ${limit:.2f}"

        if cat_status == "warning":
            text += "  (Warning)"
        elif cat_status == "exceeded":
            text += "  (Exceeded)"

        text += "\n"

    text += f"\nOverall: ${total_spent:.2f} / ${total_limit:.2f}"

    color = "black"
    if total_status == "warning":
        color = "orange"
        text += "  (Warning)"
    elif total_status == "exceeded":
        color = "red"
        text += "  (Exceeded)"

    totals_label.config(text=text, fg=color)



update_totals()

root.mainloop()
