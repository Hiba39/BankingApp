import json

FILENAME = "customers.json"

class Customer:
    def __init__(self, name, account_number, balance, account_type, transactions=None):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.account_type = account_type
        self.transactions = transactions if transactions is not None else []

    def to_dict(self):
        """Converts the Customer object into a dictionary for JSON storage."""
        return {
            "name": self.name,
            "account_number": self.account_number,
            "balance": self.balance,
            "account_type": self.account_type,
            "transactions": self.transactions
        }

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposit: +${amount:.2f}")
            print("Deposit successful.")
            print("New Balance:", self.balance)
        else:
            print("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
        elif amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -${amount:.2f}")
            print("Withdrawal successful.")
            print("New Balance:", self.balance)

    def transfer(self, other_customer, amount):
        if amount <= 0:
            print("Transfer amount must be greater than zero.")
        elif amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            other_customer.balance += amount
            self.transactions.append(f"Transfer to {other_customer.name}: -${amount:.2f}")
            other_customer.transactions.append(f"Transfer from {self.name}: +${amount:.2f}")
            print("Transfer successful.")
            print("Transferred:", amount)
            print("From:", self.name)
            print("To:", other_customer.name)

    def display_info(self):
        print("Name:", self.name)
        print("Account:", self.account_number)
        print("Balance:", self.balance)
        print("Account Type:", self.account_type)

    def check_balance(self):
        print(f"Current balance: ${self.balance:.2f}")

    def show_transactions(self):
        print()
        print(f"===== TRANSACTION HISTORY FOR {self.name.upper()} =====")
        if len(self.transactions) == 0:
            print("No transactions yet.")
        else:
            for transaction in self.transactions:
                print(transaction)
        print("==================================================")


def save_customers(customers):
    """Converts list of Customer objects to dictionaries and saves to JSON."""
    data = [customer.to_dict() for customer in customers]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)


def load_customers():
    """Loads JSON data and re-creates live Customer objects."""
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
            customers = []
            for item in data:
                customer = Customer(
                    name=item["name"],
                    account_number=item["account_number"],
                    balance=item["balance"],
                    account_type=item["account_type"],
                    transactions=item.get("transactions", [])
                )
                customers.append(customer)
            return customers
    except FileNotFoundError:
        default_customers = [
            Customer("Adrian", "00123456", 18000.0, "Savings", ["Account Created: Initial Balance $18000.00"]),
            Customer("Abdi", "00123457", 8500.0, "Savings", ["Account Created: Initial Balance $8500.00"]),
            Customer("Aman", "00123383", 11000.0, "Savings", ["Account Created: Initial Balance $11000.00"])
        ]
        save_customers(default_customers)
        return default_customers


def find_customer(account_number, customers):
    for customer in customers:
        if customer.account_number == account_number:
            return customer
    return None


def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount < 0:
                print("Amount cannot be negative.")
            else:
                return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")


# --- MAIN PROGRAM LOOP ---
def main():
    customers = load_customers()

    while True:
        print()
        print("================================")
        print("      OOP BANKING SYSTEM")
        print("================================")
        print("1. Create Customer")
        print("2. Find Customer")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. View All Customers")
        print("7. View Transaction History")
        print("8. Delete Customer")
        print("9. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter customer name: ")
            account_number = input("Enter account number: ")

            if find_customer(account_number, customers):
                print("Account number already exists.")
            else:
                account_type = input("Enter account type: ")
                balance = get_amount("Enter initial balance: ")

                new_customer = Customer(
                    name,
                    account_number,
                    balance,
                    account_type,
                    [f"Account Created: Initial Balance ${balance:.2f}"]
                )
                customers.append(new_customer)
                save_customers(customers)
                print("Customer created and saved successfully!")

        elif choice == "2":
            acc_num = input("Enter account number: ")
            cust = find_customer(acc_num, customers)
            if cust:
                print()
                print("===== CUSTOMER INFORMATION =====")
                cust.display_info()
                print("================================")
            else:
                print("Customer not found.")

        elif choice == "3":
            acc_num = input("Enter account number: ")
            cust = find_customer(acc_num, customers)
            if cust:
                amount = get_amount("Enter deposit amount: ")
                cust.deposit(amount)
                save_customers(customers)
            else:
                print("Customer not found.")

        elif choice == "4":
            acc_num = input("Enter account number: ")
            cust = find_customer(acc_num, customers)
            if cust:
                amount = get_amount("Enter withdrawal amount: ")
                cust.withdraw(amount)
                save_customers(customers)
            else:
                print("Customer not found.")

        elif choice == "5":
            from_acc = input("Enter your account number (Sender): ")
            sender = find_customer(from_acc, customers)
            if sender:
                to_acc = input("Enter recipient account number: ")
                recipient = find_customer(to_acc, customers)
                if recipient:
                    amount = get_amount("Enter transfer amount: ")
                    sender.transfer(recipient, amount)
                    save_customers(customers)
                else:
                    print("Recipient customer not found.")
            else:
                print("Sender customer not found.")

        elif choice == "6":
            print()
            print("===== ALL CUSTOMERS =====")
            for cust in customers:
                print(f"{cust.name} | {cust.account_number} | ${cust.balance:.2f} | {cust.account_type}")
            print("=========================")

        elif choice == "7":
            acc_num = input("Enter account number to view history: ")
            cust = find_customer(acc_num, customers)
            if cust:
                cust.show_transactions()
            else:
                print("Customer not found.")

        elif choice == "8":
            acc_num = input("Enter account number to delete: ")
            cust = find_customer(acc_num, customers)
            if cust:
                customers.remove(cust)
                save_customers(customers)
                print("Customer deleted successfully.")
            else:
                print("Customer not found.")

        elif choice == "9":
            print("Thank you for using the banking system.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()