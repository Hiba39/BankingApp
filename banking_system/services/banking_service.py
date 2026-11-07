import math
from exceptions import SameAccountTransferError

class BankingService:

    def __init__(self, customers):
        self.customers = customers

    def find_customer(self, account_number):
        for customer in self.customers:
            if str(customer.account_number).strip() == str(account_number).strip():
                return customer
        return None
    
    def account_exists(self, account_number):
        account_number = str(account_number).strip()

        for customer in self.customers:
            if str(customer.account_number).strip() == account_number:
                return True

        return False
    
    def deposit(self, account_number, amount):
        customer = self.find_customer(account_number)

        if customer is None:
            print("Customer not found.")
            return False

        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            print("Deposit amount must be a valid number.")
            return False    
        
        if not math.isfinite(amount):
            print("Deposit amount must be finite.")
            return False

        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return False

        if amount > 1_000_000:
            print("Deposit amount exceeds the practice limit of 1,000,000.")
            return False

        new_balance = customer.balance + amount    
        if not math.isfinite(new_balance):
            print("Deposit would produce an invalid balance.")
            return False

        customer.deposit(amount)
        return True    

    def withdraw(self, account_number, amount):
        customer = self.find_customer(account_number)

        if customer is None:
            print("Customer not found.")
            return False

        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            print("Withdrawal amount must be a valid number.")
            return False

        if not math.isfinite(amount):
            print("Withdrawal amount must be finite.")
            return False

        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return False

        if amount > 1_000_000:
            print("Withdrawal amount exceeds the practice limit of 1,000,000.")
            return False

        if amount > customer.balance:
            print("Insufficient balance.")
            return False

        return customer.withdraw(amount)

    def transfer(self, sender_account, recipient_account, amount):
        # Validate same account transfer upfront with string casting and stripping
        if str(sender_account).strip() == str(recipient_account).strip():
            raise SameAccountTransferError("Cannot transfer money to the same account.")

        sender = self.find_customer(sender_account)
        recipient = self.find_customer(recipient_account)

        if sender is None:
            print("Sender customer not found.")
            return False

        if recipient is None:
            print("Recipient customer not found.")
            return False

        return sender.transfer(recipient, amount)

    def show_all_customers(self):
        print()
        print("===== ALL CUSTOMERS =====")

        if not self.customers:
            print("No customers found.")
        else:
            for customer in self.customers:
                print(
                    customer.name,
                    "|",
                    customer.account_number,
                    "|",
                    f"${customer.balance:.2f}",
                    "|",
                    customer.account_type
                )

        print("=========================")