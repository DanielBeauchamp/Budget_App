import tkinter as tk
from tkinter import messagebox


class BudgetApp:
    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Budget App - Version 2")

        self.build_ui()
        self.update_totals()

    def build_ui(self):
        # Period display
        self.period_label = tk.Label(
            self.root,
            text=f"Period {self.manager.data['current_period']}",
            font=("Arial", 14, "bold")
        )
        self.period_label.pack(pady=5)

        # New Period button
        tk.Button(
            self.root,
            text="Start New Period",
            command=self.confirm_new_period
        ).pack(pady=2)

        tk.Button(
        self.root,
        text="View History",
        command=self.open_history_viewer
    ).pack(pady=2)
        
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

    def open_history_viewer(self):
        history = self.manager.data["history"]

        if not history:
            messagebox.showinfo("No History", "No past periods to display yet.")
            return

        # Create a child window
        viewer = tk.Toplevel(self.root)
        viewer.title("Period History")

        # Period selector
        tk.Label(viewer, text="Select Period:", font=("Arial", 11)).pack(pady=5)

        period_numbers = [f"Period {entry['period']}" for entry in history]
        selected_period = tk.StringVar(viewer)
        selected_period.set(period_numbers[-1])  # default to most recent

        dropdown = tk.OptionMenu(
            viewer,
            selected_period,
            *period_numbers,
            command=lambda _: update_history_display()
        )
        dropdown.pack()

        # Display area
        history_label = tk.Label(viewer, text="", justify=tk.LEFT, font=("Courier", 10))
        history_label.pack(padx=20, pady=10)

        def update_history_display():
            # Find the selected period entry
            period_num = int(selected_period.get().split()[1])
            entry = next(e for e in history if e["period"] == period_num)

            totals = self.manager.get_period_summary(entry)
            limits = entry["limits"]
            total_spent = sum(totals.values())
            total_limit = sum(limits.values())

            text = f"Period {period_num} Summary\n"
            text += "-" * 30 + "\n"

            for category, total in totals.items():
                limit = limits.get(category, 0)
                text += f"{category}: ${total:.2f} / ${limit:.2f}\n"

            text += "-" * 30 + "\n"
            text += f"Overall: ${total_spent:.2f} / ${total_limit:.2f}\n"

            if not entry["expenses"]:
                text += "\n(No expenses recorded)"

            history_label.config(text=text)

        # Populate on open
        update_history_display()

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

    def confirm_new_period(self):
        confirm = tk.messagebox.askyesno(
            "Start New Period",
            f"End Period {self.manager.data['current_period']} and start a new one?\n"
            "Current expenses will be archived."
        )
        if confirm:
            self.manager.reset_period()
            self.period_label.config(
                text=f"Period {self.manager.data['current_period']}"
            )
            self.update_totals()

    def run(self):
        self.root.mainloop()
