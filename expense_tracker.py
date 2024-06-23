from expense import Expense
from user import User, register_user, login_user
import calendar
import datetime

def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    
    user = user_authentication()
    
    if user:
        expense = get_user_expense()
        save_expense_to_file(expense, expense_file_path, user.username)
        summarize_expenses(expense_file_path, user)

def user_authentication():
    while True:
        print("1. Register")
        print("2. Login")
        choice = input("Select an option: ")
        
        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            income = float(input("Enter your income: "))
            register_user(username, password, income)
            print("User registered successfully! Please log in.")
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = login_user(username, password)
            if user:
                print(f"Welcome back, {user.username}!")
                return user
            else:
                print("Invalid credentials. Please try again.")
        else:
            print("Invalid option. Please try again.")

def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

def save_expense_to_file(expense: Expense, expense_file_path, username):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, expense.name, expense.amount, expense.category])

def summarize_expenses(expense_file_path, user):
    print(f"🎯 Summarizing User Expense")
    expenses = []
    with open(expense_file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == user.username:
                expense_name, expense_amount, expense_category = row[1], row[2], row[3]
                line_expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                )
                expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = user.income - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()
