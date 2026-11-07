from models.customer import Customer
from exceptions import (
    InsufficientBalanceError,
    InvalidAmountError,
    SameAccountTransferError
)
from data.data_manager import save_customers, load_customers
from services.banking_service import BankingService
# from utils.validators import get_positive_amount, get_account_number,get_customer_name
from utils.validators import (get_positive_amount, get_account_number, get_customer_name,get_initial_balance,get_account_type
)

def main():
    customers = load_customers()
    service = BankingService(customers)

    while True:
        print()
        print("================================")
        print("        OOP BANKING SYSTEM      ")
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

        # CREATE CUSTOMER
        if choice == "1":
            name = get_customer_name("Enter customer name: ")
            account_number = get_account_number("Enter account number: ")
            account_type = get_account_type("Enter account type: ")

            # try:
            #     balance = float(input("Enter initial balance: "))
            # except ValueError:
            #     print("Invalid amount.")
            #     continue
            balance = get_initial_balance("Enter initial balance: ")
            # existing_customer = service.find_customer(account_number)

            # if existing_customer:
            #     print("Account number already exists.")
            #     continue
            if service.account_exists(account_number):
                print("Account number already exists. Choose a different number.")
                continue    

            customer = Customer(
                name,
                account_number,
                balance,
                account_type
            )

            customer.transactions.append(
                f"Account Created: Initial Balance ${balance:.2f}"
            )

            customers.append(customer)
            save_customers(customers)
            print("Customer created successfully.")

        # FIND CUSTOMER
        elif choice == "2":
            account_number = input("Enter account number: ")
            customer = service.find_customer(account_number)

            if customer:
                customer.display_info()
            else:
                print("Customer not found.")

        # DEPOSIT
        elif choice == "3":
            account_number = get_account_number("Enter account number: ")
            customer = service.find_customer(account_number)

            if customer:
                try:
                    amount = get_positive_amount("Enter deposit amount: ")
                    previous_balance = customer.balance
                    previous_transactions = customer.transactions.copy()
                    
                    success = service.deposit(account_number, amount)
                    if success:
                        try:
                            save_customers(customers)
                            print("Deposit successful.")
                            print(f"New Balance: ${customer.balance:.2f}")
                        except (OSError, ValueError, TypeError) as error:
                            customer.balance = previous_balance
                            customer.transactions = previous_transactions
                            print("Deposit was not saved. The account was restored.")
                            print("Save error:", error)
                    # if success:
                    #     try:
                    #         raise OSError("TEST ERROR: simulated save failure")
                    #     except (OSError, ValueError, TypeError) as error:
                    #         customer.balance = previous_balance
                    #         customer.transactions = previous_transactions
                    #         print("Deposit was not saved. The account was restored.")
                    #         print("save error:", error)   
                            
                except InvalidAmountError as error:
                    print(error)
            else:
                print("Customer not found.")

        # WITHDRAW
        elif choice == "4":
            account_number = get_account_number("Enter account number: ")
            customer = service.find_customer(account_number)

            if customer:
                try:
                    amount = get_positive_amount("Enter withdrawal amount: ")
                    previous_balance = customer.balance
                    previous_transactions = customer.transactions.copy()

                    success = service.withdraw(account_number, amount)
                    if success:
                        try:
                            save_customers(customers)
                            print("withdrawal successful.")
                            print(f"New Balance: ${customer.balance:.2f}")
                        except (OSError, ValueError, TypeError) as error:
                            customer.balance = previous_balance
                            customer.transactions = previous_transactions
                            print("Withdrawal was not saved. The account was restored.")
                            print("Save error:", error)
                except (InsufficientBalanceError, InvalidAmountError) as error:
                    print(error)
            else:
                print("Customer not found.")

        # TRANSFER
        elif choice == "5":
            sender_account = get_account_number("Enter sender account number: ")
            receiver_account = get_account_number("Enter recipient account number: ")
            
            try:
                amount = get_positive_amount("Enter transfer amount: ")
                
                sender = service.find_customer(sender_account)
                recipient = service.find_customer(receiver_account)

                if sender and recipient:
                    sender_prev_balance = sender.balance
                    recipient_prev_balance = recipient.balance
                    sender_prev_txns = sender.transactions.copy()
                    recipient_prev_txns = recipient.transactions.copy()

                    success = service.transfer(
                        sender_account,
                        receiver_account,
                        amount
                    )
                    if success:
                        try:
                            save_customers(customers)
                            # raise OSError("TEST ERROR: Simulated transfer save failure")
                            print("Transfer successful.")
                            print(f"Sender balace: "f"${sender.balance:.2f}")
                            print(f"Recepient balance: "f"${recipient.balance:.2f}")
                        except (OSError, ValueError, TypeError) as error:
                            sender.balance = sender_prev_balance
                            recipient.balance = recipient_prev_balance
                            sender.transactions = sender_prev_txns
                            recipient.transactions = recipient_prev_txns
                            print("Transfer was not saved. Accounts were restored.")
                            print("Save error:", error)
                else:
                    if not sender:
                        print("Sender account not found.")
                    if not recipient:
                        print("Recipient account not found.")                
            except (InsufficientBalanceError, InvalidAmountError, SameAccountTransferError) as error:
                print(error)

        # VIEW ALL CUSTOMERS
        elif choice == "6":
            service.show_all_customers()

        # TRANSACTION HISTORY
        elif choice == "7":
            account_number = get_account_number("Enter account number: ")
            customer = service.find_customer(account_number)

            if customer:
                customer.show_transactions()
            else:
                print("Customer not found.")

        # DELETE CUSTOMER
        elif choice == "8":
            account_number = get_account_number("Enter account number to delete: ")
            customer = service.find_customer(account_number)

            if customer:
                customers.remove(customer)
                save_customers(customers)
                print("Customer deleted successfully.")
            else:
                print("Customer not found.")

        # EXIT
        elif choice == "9":
            save_customers(customers)
            print("Thank you for using the banking system.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()