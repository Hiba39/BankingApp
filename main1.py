from customer import load_customers
from banking import (
    create_customer,
    find_customer_details,
    deposit,
    withdraw,
    view_customers,
    delete_customer
)

def main():
    # Load customers when the program starts
    customers = load_customers()

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
            create_customer(customers)
        elif choice == "2":
            find_customer_details(customers)
        elif choice == "3":
            deposit(customers)
        elif choice == "4":
            withdraw(customers)
        elif choice == "5":
            view_customers(customers)
        elif choice == "6":
            delete_customer(customers)
        elif choice == "7":
            print("Thank you for using the banking system.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()