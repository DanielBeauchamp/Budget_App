import tkinter as tk


class BudgetApp:
    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Budget App - Version 2")

        self.build_ui()
        self.update_totals()

    def build_ui(self):
        # Amount input
        tk.Label(self.root, text="Amount:").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        # Category buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        for category in self.manager.data["limits"].keys():
            tk.Button(
                button_frame,
                text=category,
                width=15,
                command=lambda c=category: self.add_expense(c)
            ).pack(side=tk.LEFT, padx=5)

        # Limits section
        limits_frame = tk.LabelFrame(self.root, text="Category Limits")
        limits_frame.pack(pady=10, fill="x")

        self.limit_entries = {}

        for category in self.manager.data["limits"]:
            row = tk.Frame(limits_frame)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=category, width=15).pack(side=tk.LEFT)

            entry = tk.Entry(row, width=10)
            entry.insert(0, str(self.manager.data["limits"][category]))
            entry.pack(side=tk.LEFT)

            self.limit_entries[category] = entry

        tk.Button(
            limits_frame,
            text="Save Limits",
            command=self.save_limits
        ).pack(pady=5)

        # Totals
        self.totals_label = tk.Label(self.root, text="", justify=tk.LEFT)
        self.totals_label.pack(pady=10)

    def add_expense(self, category):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            return

        self.manager.add_expense(category, amount)
        self.amount_entry.delete(0, tk.END)
        self.update_totals()

    def save_limits(self):
        for category, entry in self.limit_entries.items():
            try:
                value = float(entry.get())
                self.manager.set_limit(category, value)
            except ValueError:
                continue

        self.update_totals()

    def update_totals(self):
        totals, status, total_spent, total_status = self.manager.calculate_status()
        total_limit = self.manager.get_total_limit()

        text = "Totals:\n"

        for category, total in totals.items():
            limit = self.manager.data["limits"][category]
            text += f"{category}: ${total:.2f} / ${limit:.2f}"

            if status[category] == "warning":
                text += "  (Warning)"
            elif status[category] == "exceeded":
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

        self.totals_label.config(text=text, fg=color)

    def run(self):
        self.root.mainloop()
