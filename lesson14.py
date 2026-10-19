import json

try:
    with open("customers.json", "r") as file:
        customers = json.load(file)
except FileNotFoundError:
    customers = [
        {
            "name": "Adrian",
            "account_number": "00123456",
            "balance": 18000.0,
            "account_type": "Savings"
        },
        {
            "name": "Abdi",
            "account_number": "00123457",
            "balance": 8500.0,
            "account_type": "Savings"
        },
        {
            "name": "Aman",
            "account_number": "00123444",
            "balance": 1800.0,
            "account_type": "Savings"
        }
    ]
    with open("customers.json", "w") as file:
        json.dump(customers, file, indent=4)

def save_customers():
    with open("customers.json", "w") as file:
        json.dump(customers, file, indent=4)

while True:
    print()
    print("================================")
    print("        BANKING SYSTEM")
    print("================================")
    print("1. Create Customer")
    print("2. Find Customer")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. View All Customers")
    print("6. Delete Customer")
    print("7. Exit")
    print("================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter customer name: ")
        account_number = input("Enter account number: ")
        account_type = input("Enter account type: ")
        balance = float(input("Enter initial balance: "))

        new_customer = {
            "name": name,
            "account_number": account_number,
            "balance": balance,
            "account_type": account_type
        }

        customers.append(new_customer)
        save_customers()
        print("Customer created successfully.")

    elif choice == "2":
        account_number = input("Enter account number: ")
        found_customer = None

        for customer in customers:
            if customer["account_number"] == account_number:
                found_customer = customer
                break

        if found_customer:
            print()
            print("===== CUSTOMER INFORMATION =====")
            print("Name:", found_customer["name"])
            print("Account:", found_customer["account_number"])
            print("Balance:", found_customer["balance"])
            print("Account Type:", found_customer["account_type"])
            print("================================")
        else:
            print("Customer not found.")

    elif choice == "3":
        account_number = input("Enter account number: ")
        found_customer = None

        for customer in customers:
            if customer["account_number"] == account_number:
                found_customer = customer
                break

        if found_customer:
            amount = float(input("Enter deposit amount: "))

            if amount > 0:
                found_customer["balance"] += amount
                save_customers()
                print("Deposit successful.")
                print("New Balance:", found_customer["balance"])
            else:
                print("Amount must be greater than zero.")
        else:
            print("Customer not found.")

    elif choice == "4":
        account_number = input("Enter account number: ")
        found_customer = None

        for customer in customers:
            if customer["account_number"] == account_number:
                found_customer = customer
                break

        if found_customer:
            amount = float(input("Enter withdrawal amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
            elif amount > found_customer["balance"]:
                print("Insufficient balance.")
            else:
                found_customer["balance"] -= amount
                save_customers()
                print("Withdrawal successful.")
                print("New Balance:", found_customer["balance"])
        else:
            print("Customer not found.")

    elif choice == "5":
        print()
        print("===== ALL CUSTOMERS =====")

        for customer in customers:
            print(
                customer["name"],
                "|",
                customer["account_number"],
                "|",
                customer["balance"],
                "|",
                customer["account_type"]
            )

        print("=========================")

    elif choice == "6":
        account_number = input("Enter account number to delete: ")
        found_customer = None

        for customer in customers:
            if customer["account_number"] == account_number:
                found_customer = customer
                break

        if found_customer:
            customers.remove(found_customer)
            save_customers()
            print("Customer deleted successfully.")
        else:
            print("Customer not found.")

    elif choice == "7":
        print("Thank you for using the banking system.")
        break

    else:
        print("Invalid choice.")