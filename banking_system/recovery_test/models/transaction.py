from datetime import datetime


class Transaction:

    def __init__(self, transaction_type, account_number, amount, status, description):
        self.transaction_type = transaction_type
        self.account_number = account_number
        self.amount = amount
        self.status = status
        self.description = description
        self.timestamp = datetime.now()
    def to_dict(self):
        return{
            "transcation_type": self.transaction_type,
            "account_number": self.account_number,
            "amount": self.amount,
            "status": self.status,
            "description": self.description,
            "timestamp": self.timestamp.isoformat()
        }
    def display(self):
        print()
        print("===== TRANSACTION =====")
        print("Type:", self.transaction_type)
        print("Account:", self.account_number)
        print("Amount:", f"${self.amount:.2f}")
        print("Status:", self.status)
        print("Description:", self.description)
        print("Date:", self.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        print("=======================")