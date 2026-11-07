
from datetime import datetime
from uuid import uuid4


class Transaction:
    def __init__(
        self,
        transaction_type,
        account_number,
        amount,
        status,
        description,
        reference=None
    ):
        self.transaction_type = transaction_type
        self.account_number = account_number
        self.amount = amount
        self.status = status
        self.description = description
        self.timestamp = datetime.now()

        # Generate a unique reference if one was not provided
        self.reference = reference or f"TRX-{uuid4().hex[:12].upper()}"

    def to_dict(self):
        return {
            "transaction_type": self.transaction_type,
            "account_number": self.account_number,
            "amount": self.amount,
            "status": self.status,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "reference": self.reference
        }
