from customer import save_customers, find_customer

def create_customer(customers):
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
    save_customers(customers)
    print("Customer created and saved successfully.")

def find_customer_details(customers):
    account_number = input("Enter account number: ")
    found_customer = find_customer(account_number, customers)

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

def deposit(customers):
    account_number = input("Enter account number: ")
    found_customer = find_customer(account_number, customers)

    if found_customer:
        amount = float(input("Enter deposit amount: "))
        if amount > 0:
            found_customer["balance"] += amount
            save_customers(customers)
            print("Deposit successful.")
            print("New Balance:", found_customer["balance"])
        else:
            print("Amount must be greater than zero.")
    else:
        print("Customer not found.")

def withdraw(customers):
    account_number = input("Enter account number: ")
    found_customer = find_customer(account_number, customers)

    if found_customer:
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
        elif amount > found_customer["balance"]:
            print("Insufficient balance.")
        else:
            found_customer["balance"] -= amount
            save_customers(customers)
            print("Withdrawal successful.")
            print("New Balance:", found_customer["balance"])
    else:
        print("Customer not found.")

def view_customers(customers):
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

def delete_customer(customers):
    account_number = input("Enter account number to delete: ")
    found_customer = find_customer(account_number, customers)

    if found_customer:
        customers.remove(found_customer)
        save_customers(customers)
        print("Customer deleted successfully.")
    else:
        print("Customer not found.")