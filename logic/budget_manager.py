WARNING_THRESHOLD = 0.8
CATEGORIES = ["Food", "Transportation", "Entertainment", "Misc"]


class BudgetManager:
    def __init__(self, storage):
        self.storage = storage
        self.data = self.storage.load_data()

    # -----------------------------
    # Expense Logic
    # -----------------------------

    def add_expense(self, category, amount):
        self.data["expenses"].append({
            "category": category,
            "amount": amount
        })
        self.storage.save_data(self.data)

    def reset_period(self, new_period):
        self.data["period"] = new_period
        self.data["expenses"] = []
        self.storage.save_data(self.data)

    # -----------------------------
    # Limits
    # -----------------------------

    def set_limit(self, category, value):
        if value >= 0:
            self.data["limits"][category] = value
            self.storage.save_data(self.data)

    def get_total_limit(self):
        return sum(self.data["limits"].values())

    # -----------------------------
    # Calculations
    # -----------------------------

    def calculate_totals(self):
        totals = {category: 0 for category in CATEGORIES}

        for expense in self.data["expenses"]:
            totals[expense["category"]] += expense["amount"]

        return totals

    def calculate_status(self):
        totals = self.calculate_totals()
        status = {}

        for category, spent in totals.items():
            limit = self.data["limits"].get(category, 0)
            ratio = spent / limit if limit > 0 else 0

            if ratio >= 1:
                status[category] = "exceeded"
            elif ratio >= WARNING_THRESHOLD:
                status[category] = "warning"
            else:
                status[category] = "normal"

        total_spent = sum(totals.values())
        total_limit = self.get_total_limit()
        total_ratio = total_spent / total_limit if total_limit > 0 else 0

        if total_ratio >= 1:
            total_status = "exceeded"
        elif total_ratio >= WARNING_THRESHOLD:
            total_status = "warning"
        else:
            total_status = "normal"

        return totals, status, total_spent, total_status
