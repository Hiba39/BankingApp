from customer import Customer
from banking_service import (
    load_customers,
    save_customers,
    find_customer
)

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

def main():
    customers = load_customers()

    while True:
        print()
        print("================================")
        print("       OOP BANKING SYSTEM")
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
                continue

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

            print("Customer created successfully.")

        elif choice == "2":
            account_number = input("Enter account number: ")

            customer = find_customer(
                account_number,
                customers
            )

            if customer:
                print()
                print("===== CUSTOMER INFORMATION =====")
                customer.display_info()
                print("================================")
            else:
                print("Customer not found.")

        elif choice == "3":
            account_number = input("Enter account number: ")

            customer = find_customer(
                account_number,
                customers
            )

            if customer:
                amount = get_amount(
                    "Enter deposit amount: "
                )

                customer.deposit(amount)
                save_customers(customers)

            else:
                print("Customer not found.")

        elif choice == "4":
            account_number = input(
                "Enter account number: "
            )

            customer = find_customer(
                account_number,
                customers
            )

            if customer:
                amount = get_amount(
                    "Enter withdrawal amount: "
                )

                customer.withdraw(amount)
                save_customers(customers)

            else:
                print("Customer not found.")

        elif choice == "5":
            sender_account = input(
                "Enter sender account number: "
            )

            sender = find_customer(
                sender_account,
                customers
            )

            if not sender:
                print("Sender customer not found.")
                continue

            recipient_account = input(
                "Enter recipient account number: "
            )

            recipient = find_customer(
                recipient_account,
                customers
            )

            if not recipient:
                print("Recipient customer not found.")
                continue

            amount = get_amount(
                "Enter transfer amount: "
            )

            sender.transfer(recipient, amount)
            save_customers(customers)

        elif choice == "6":
            print()
            print("===== ALL CUSTOMERS =====")

            for customer in customers:
                print(
                    f"{customer.name} | "
                    f"{customer.account_number} | "
                    f"${customer.balance:.2f} | "
                    f"{customer.account_type}"
                )

            print("=========================")

        elif choice == "7":
            account_number = input(
                "Enter account number: "
            )

            customer = find_customer(
                account_number,
                customers
            )

            if customer:
                customer.show_transactions()
            else:
                print("Customer not found.")

        elif choice == "8":
            account_number = input(
                "Enter account number to delete: "
            )

            customer = find_customer(
                account_number,
                customers
            )

            if customer:
                customers.remove(customer)
                save_customers(customers)
                print("Customer deleted successfully.")
            else:
                print("Customer not found.")

        elif choice == "9":
            print(
                "Thank you for using the banking system."
            )
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main(