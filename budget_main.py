import storage
from budget_manager import BudgetManager
from app_window import BudgetApp


def main():
    manager = BudgetManager(storage)
    app = BudgetApp(manager)
    app.run()


if __name__ == "__main__":
    main()
