from budget_app import storage
from budget_app.budget_manager import BudgetManager
from budget_app.app_window import BudgetApp


def main():
    manager = BudgetManager(storage)
    app = BudgetApp(manager)
    app.run()


if __name__ == "__main__":
    main()

