import customtkinter as ctk
from tkinter import messagebox
import csv, os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FILE = "expenses.csv"

# Ensure file exists
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount", "Note"])

class ExpenseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("500x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # ---- Input Section ----
        self.category_label = ctk.CTkLabel(self, text="Category:")
        self.category_label.pack(pady=(20, 5))
        self.category_entry = ctk.CTkEntry(self, width=300)
        self.category_entry.pack()

        self.amount_label = ctk.CTkLabel(self, text="Amount:")
        self.amount_label.pack(pady=(15, 5))
        self.amount_entry = ctk.CTkEntry(self, width=300)
        self.amount_entry.pack()

        self.note_label = ctk.CTkLabel(self, text="Note:")
        self.note_label.pack(pady=(15, 5))
        self.note_entry = ctk.CTkEntry(self, width=300)
        self.note_entry.pack()

        self.add_btn = ctk.CTkButton(self, text="Add Expense", command=self.add_expense)
        self.add_btn.pack(pady=15)

        self.view_btn = ctk.CTkButton(self, text="View All Expenses", command=self.view_expenses)
        self.view_btn.pack(pady=5)

        self.chart_btn = ctk.CTkButton(self, text="Show Expense Chart", command=self.show_chart)
        self.chart_btn.pack(pady=5)

        self.clear_btn = ctk.CTkButton(self, text="Clear Fields", command=self.clear_fields)
        self.clear_btn.pack(pady=5)

        self.output = ctk.CTkTextbox(self, width=450, height=200)
        self.output.pack(pady=20)

    # ---- Add Expense ----
    def add_expense(self):
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()
        note = self.note_entry.get().strip()

        if not category or not amount:
            messagebox.showwarning("Warning", "Please enter category and amount!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, category, amount, note])

        messagebox.showinfo("Success", f"Added {category}: ₹{amount:.2f}")
        self.clear_fields()

    # ---- View All ----
    def view_expenses(self):
        try:
            df = pd.read_csv(FILE)
            if df.empty:
                self.output.delete("1.0", "end")
                self.output.insert("end", "No expenses found.")
                return
            self.output.delete("1.0", "end")
            total = df["Amount"].sum()
            self.output.insert("end", f"Total Expenses: ₹{total:.2f}\n\n")
            self.output.insert("end", df.to_string(index=False))
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("end", str(e))

    # ---- Chart ----
    def show_chart(self):
        try:
            df = pd.read_csv(FILE)
            if df.empty:
                messagebox.showinfo("Info", "No data to plot.")
                return
            category_sum = df.groupby("Category")["Amount"].sum()
            category_sum.plot(kind="bar", color="skyblue")
            plt.title("Expenses by Category")
            plt.xlabel("Category")
            plt.ylabel("Total Amount (₹)")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):
        self.category_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.note_entry.delete(0, "end")

if __name__ == "__main__":
    app = ExpenseApp()
    app.mainloop()
