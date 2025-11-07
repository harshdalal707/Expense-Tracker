import csv
from datetime import datetime

FILENAME = "expenses.csv"

# Create file if not exists
def init_file():
    try:
        with open(FILENAME, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Note"])
    except FileExistsError:
        pass

def add_expense():
    category = input("Enter category (e.g. food, travel, shopping): ")
    amount = float(input("Enter amount spent: "))
    note = input("Enter a short note (optional): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, note])
    print("✅ Expense added successfully!\n")

def view_expenses():
    try:
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            total = 0
            print("\n📘 Your Expenses:")
            print("-" * 50)
            for row in reader:
                print(f"{row[0]} | {row[1]} | ₹{row[2]} | {row[3]}")
                total += float(row[2])
            print("-" * 50)
            print(f"💰 Total Spent: ₹{total}\n")
    except FileNotFoundError:
        print("⚠️ No expenses recorded yet.\n")

def main():
    init_file()
    while True:
        print("==== Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("👋 Exiting... Have a great day!")
            break
        else:
            print("❌ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()

