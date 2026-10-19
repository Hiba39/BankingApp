
class Customer:
    def __init__(self, name, account_number, balance, account_type, transactions=None):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.account_type = account_type
        self.transactions = transactions if transactions is not None else []

    def to_dict(self):
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
            self.transactions.append(
                f"Deposit: +${amount:.2f}"
            )
            print("Deposit successful.")
            print("New Balance:", self.balance)
        else:
            print("Amount must be greater than zero.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")

        elif amount > self.balance:
            print("Insufficient balance.")

        else:
            self.balance -= amount
            self.transactions.append(
                f"Withdrawal: -${amount:.2f}"
            )
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

            self.transactions.append(
                f"Transfer to {other_customer.name}: -${amount:.2f}"
            )

            other_customer.transactions.append(
                f"Transfer from {self.name}: +${amount:.2f}"
            )

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
        print(
            f"===== TRANSACTION HISTORY FOR "
            f"{self.name.upper()} ====="
        )

        if len(self.transactions) == 0:
            print("No transactions yet.")

        else:
            for transaction in self.transactions:
                print(transaction)

        print("==================================================")

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["account_number"],
            data["balance"],
            data["account_type"],
            data.get("transactions", [])
        )