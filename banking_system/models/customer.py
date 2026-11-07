import math
from exceptions import (
    InsufficientBalanceError,
    InvalidAmountError,
    SameAccountTransferError
)
from models.transaction import Transaction


class Customer:

    def __init__(self, name, account_number, balance, account_type):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.account_type = account_type
        self.transactions = []

    def display_info(self):
        print()
        print("===== CUSTOMER INFORMATION =====")
        print("Name:", self.name)
        print("Account:", self.account_number)
        print("Balance:", self.balance)
        print("Account Type:", self.account_type)
        print("================================")

    def check_balance(self):
        print(f"Current balance: ${self.balance:.2f}")

    def deposit(self, amount):
        if(
            isinstance(amount, bool)
            or not isinstance(amount, (int, float))
        ):
            raise InvalidAmountError("Deposit amount must be a valid number.")

    
        if not math.isfinite(amount) or amount <= 0:
            raise InvalidAmountError(
                "Deposit amount must be a finite number greater than zero."
            )
        
        if amount > 1_000_000:
            raise InvalidAmountError("Deposit amount exceeds the practice limit of 1,000,000.")

        new_balance = self.balance + amount
        if not math.isfinite(new_balance):
            raise InvalidAmountError("This deposit would create an invalid balance.")

        if (
            isinstance(self.balance, bool)
            or not isinstance(self.balance, (int, float))
            or not math.isfinite(self.balance)
            or self.balance <0
        ):
            raise InvalidAmountError("Account balance is invalid. please contact support.")
                

        self.balance = new_balance

        transaction = Transaction(
            transaction_type="DEPOSIT",
            account_number=self.account_number,
            amount=amount,
            status="SUCCESS",
            description="Cash deposit"
        )
        self.transactions.append(transaction)

        # print("Deposit successful.")
        # print(f"New Balance: ${self.balance:.2f}")
        return True

    def withdraw(self, amount):
        if(
            isinstance(amount,bool)
            or not isinstance(amount,(int, float))
        ):
           raise InvalidAmountError("Withdrawal amount must be a valid number.")

        if not math.isfinite(amount) or amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be a finite number greater than zero.")

        if amount > 1_000_000:
            raise InvalidAmountError("Withdrawal amount exceeds the practice limit of 1,000,000.")

        if (
            isinstance(self.balance,bool)
            or not isinstance(self.balance,(int, float))
            or not math.isfinite(self.balance)
            or self.balance < 0
        ):
            raise InvalidAmountError("Account balance is invalid. please contact support.")

        # if not math.isfinite(self.balance) or self.balance < 0:
        #     raise InvalidAmountError("Account balance is invalid. Please contact support.")

        if amount > self.balance:
            raise InsufficientBalanceError("Insufficient balance.")

        new_balance = self.balance - amount

        if not math.isfinite(new_balance) or new_balance < 0:
            raise InvalidAmountError("The resulting balance would be invalid.")

        self.balance = new_balance

        transaction = Transaction(
            transaction_type="WITHDRAWAL",
            account_number=self.account_number,
            amount=amount,
            status="SUCCESS",
            description="Cash withdrawal"
        )
        self.transactions.append(transaction)

        # print("Withdrawal successful.")
        # print(f"New Balance: ${self.balance:.2f}")
        return True

    def transfer(self, other_customer, amount):
        # Robust comparison using string casting and strip to prevent bypasses
        if str(self.account_number).strip() == str(other_customer.account_number).strip():
            raise SameAccountTransferError("Cannot transfer money to the same account.")
            
        if not math.isfinite(amount) or amount <= 0:
            raise InvalidAmountError("Transfer amount must be a finite number greater than zero.")

        if not math.isfinite(self.balance) or self.balance < 0:
            raise InvalidAmountError("Account balance is invalid. Please contact support.")
        if not math.isfinite(other_customer.balance) or other_customer.balance < 0:
            raise InvalidAmountError("Recipient accounr balance is invalid.")
        if amount > self.balance:
            raise InsufficientBalanceError("Insufficient balance.")

        new_balance = self.balance - amount
        if not math.isfinite(new_balance) or new_balance < 0:
            raise InvalidAmountError("The resulting balance would be invalid.")
        new_balance = self.balance - amount
        recipient_new_balance = other_customer.balance + amount
        if not math.isfinite(new_balance) or new_balance < 0:
            raise InvalidAmountError("The sender's resulting balance would be invalid.")
        if not math.isfinite(recipient_new_balance):
            raise InvalidAmountError("The recipient's resulting balance would be invalid.")

        # self.balance = new_balance
        # other_customer.balance = recipient_new_balance

        sender_transaction = Transaction(
            transaction_type="TRANSFER",
            account_number=self.account_number,
            amount=amount,
            status="SUCCESS",
            description=f"Transfer to {other_customer.name}"
        )

        recipient_transaction = Transaction(
            transaction_type="TRANSFER",
            account_number=other_customer.account_number,
            amount=amount,
            status="SUCCESS",
            description=f"Transfer from {self.name}"
        )
        self.balance = new_balance
        other_customer.balance = recipient_new_balance
        self.transactions.append(sender_transaction)
        other_customer.transactions.append(recipient_transaction)

        print("Transfer successful.")
        print(f"Transferred: ${amount:.2f}")
        print(f"From: {self.name}")
        print(f"To: {other_customer.name}")

        return True

    def show_transactions(self):
        print()
        print("===== TRANSACTION HISTORY =====")

        if len(self.transactions) == 0:
            print("No transactions yet.")
        else:
            for transaction in self.transactions:
                if isinstance(transaction, str):
                    print(transaction)
                else:
                    transaction.display()  

        print("===============================")