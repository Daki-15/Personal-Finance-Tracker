import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description, DATE_FORMAT
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "transactions.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            data_frame = pd.DataFrame(columns=cls.COLUMNS)
            data_frame.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry  = {
            "date" : date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("\n\n")
        print("*"*28)
        print("| Entry added successfully |")
        print("*"*28)
    @classmethod
    def get_transactions(cls, start_date, end_data):
        data_frame = pd.read_csv(cls.CSV_FILE)

        data_frame["date"] = pd.to_datetime(data_frame["date"], format=DATE_FORMAT)
        start_date = datetime.strptime(start_date, DATE_FORMAT)
        end_data = datetime.strptime(end_data, DATE_FORMAT)

        mask = (data_frame["date"] >= start_date) & (data_frame["date"] <= end_data)
        filtered_data_frame = data_frame.loc[mask]

        if filtered_data_frame.empty:
            print("No transaction in the given data range")
        else:
            print(f"Transations from {start_date.strftime(DATE_FORMAT)} to {end_data.strftime(DATE_FORMAT)}")
            print(
                filtered_data_frame.to_string(
                    formatters={"date": lambda x: x.strftime(DATE_FORMAT)}, index=False
                    )
                )
            total_income = filtered_data_frame[filtered_data_frame["category"] == "Income"]["amount"].sum()
            total_expense = filtered_data_frame[filtered_data_frame["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"MNet Savings: {(total_income - total_expense):.2f}")

        return filtered_data_frame


def add():
    CSV.initialize_csv()
    Date = get_date("Enter the date of transaction (YYYY-MM-DD) or `enter` for todat's day: ", allow_default=True)
    Amount = get_amount()
    Category = get_category()
    Description = get_description()

    CSV.add_entry(date=Date, amount=Amount, category=Category, description=Description if Description != "" else "None")

def plot_transactions(data_frame):
    data_frame.set_index('date', inplace=True)

    income_df = (
        data_frame[data_frame["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(data_frame.index, fill_value = 0)
    )

    expense_df = (
        data_frame[data_frame["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(data_frame.index, fill_value = 0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expanse", color="r")

    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expanse Over Time")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a data range")
        print("3. Exit")

        choice = input("\nEnter your choice (1 - 3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date(YYYY-MM-DD): ")
            end_date = get_date("Enter the end date(YYYY-MM-DD): ")

            Data_Frame = CSV.get_transactions(start_date=start_date, end_data=end_date)
            
            if input("Do you want to see a plot? (y/n)").lower() == "y":
                plot_transactions(data_frame=Data_Frame)
        elif choice == "3":
            print("Exiting....")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()