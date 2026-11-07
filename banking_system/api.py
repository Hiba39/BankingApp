from math import isfinite
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from data.data_manager import load_customers, save_customers
from models.customer import Customer
from models.transaction import Transaction


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    account_number: str = Field(pattern=r"^\d{8}$")
    balance: float = Field(ge=0, le=1_000_000_000)
    account_type: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Customer name cannot be empty.")
        return value

    @field_validator("account_type")
    @classmethod
    def validate_account_type(cls, value):
        value = value.strip().lower()
        if value not in ("saving", "current"):
            raise ValueError("Account type must be 'saving' or 'current'.")
        return value


class DepositAccountRequest(BaseModel):
    account_number: str = Field(pattern=r"^\d{8}$")
    amount: float = Field(gt=0, le=1_000_000)

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if not isfinite(value):
            raise ValueError("Deposit amount must be finite.")
        return value


class WithdrawalAccountRequest(BaseModel):
    account_number: str = Field(pattern=r"^\d{8}$")
    amount: float = Field(gt=0, le=1_000_000)

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if not isfinite(value):
            raise ValueError("Withdrawal amount must be finite.")
        return value
class TransferRequest(BaseModel):
    sender_account: str = Field(pattern=r"^\d{8}$")
    recipient_account: str = Field(pattern=r"^\d{8}$")
    amount: float = Field(gt=0, le=1_000_000)

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if not isfinite(value):
             raise ValueError("Transfer amount must be finite.")
        return value    


class DepositRequest(BaseModel):
    current_balance: float = Field(ge=0, le=1_000_000_000)
    deposit_amount: float = Field(gt=0, le=1_000_000)


app = FastAPI(title="My Banking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Welcome to My Banking API!",
        "status": "running"
    }


@app.get("/hello")
def say_hello():
    return {
        "message": "Hello, Adrian!",
        "lesson": "My first API"
    }


@app.get("/accounts/demo")
def demo_account():
    return {
        "account_number": "00123456",
        "customer_name": "Demo Customer",
        "balance": 5000.00,
        "currency": "ETB"
    }


@app.post("/deposit-demo")
def deposit_demo(request: DepositRequest):
    if not isfinite(request.current_balance):
        return {"error": "Balance must be finite."}

    if not isfinite(request.deposit_amount):
        return {"error": "Deposit amount must be finite."}

    new_balance = request.current_balance + request.deposit_amount

    if not isfinite(new_balance) or new_balance > 1_000_000_000:
        return {"error": "Resulting balance exceeds the permitted limit."}

    return {
        "current_balance": request.current_balance,
        "deposit_amount": request.deposit_amount,
        "new_balance": new_balance,
        "currency": "ETB",
        "mode": "DEMO ONLY"
    }


@app.get("/customers")
def get_customers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=100),
    sort_by: str = Query(default="name"),
    order: str = Query(default="asc"),
    account_type: str | None = Query(default=None)
):
    customers = load_customers()
    allowed_fields = ("name", "balance", "account_number")

    sort_by = sort_by.strip().lower()
    order = order.strip().lower()

    if sort_by not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be name, balance, or account_number."
        )

    if order not in ("asc", "desc"):
        raise HTTPException(
            status_code=400,
            detail="order must be asc or desc."
        )

    if account_type is not None:
        account_type = account_type.strip().lower()
        if account_type not in ("saving", "current"):
            raise HTTPException(
                status_code=400,
                detail="account_type must be saving or current."
            )
        customers = [
            customer
            for customer in customers
            if customer.account_type.strip().lower() == account_type
        ]

    if sort_by == "name":
        customers.sort(
            key=lambda customer: customer.name.casefold(),
            reverse=(order == "desc")
        )
    elif sort_by == "balance":
        customers.sort(
            key=lambda customer: customer.balance,
            reverse=(order == "desc")
        )
    else:
        customers.sort(
            key=lambda customer: customer.account_number,
            reverse=(order == "desc")
        )

    total_records = len(customers)
    total_pages = (total_records + page_size - 1) // page_size

    start = (page - 1) * page_size
    page_customers = customers[start:start + page_size]

    result = []
    for customer in page_customers:
        result.append({
            "name": customer.name,
            "account_number": customer.account_number,
            "balance": customer.balance,
            "account_type": customer.account_type
        })

    return {
        "total_records": total_records,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "sort_by": sort_by,
        "order": order,
        "account_type_filter": account_type,
        "customers_on_this_page": len(result),
        "customers": result
    }


@app.get("/customers/search")
def search_customers(
    name: str | None = Query(default=None, min_length=1),
    account_type: str | None = Query(default=None),
):
    customers = load_customers()

    if name is None and account_type is None:
        raise HTTPException(
            status_code=400,
            detail="Provide a name or account_type to search."
        )

    search_name = name.strip().casefold() if name else None
    search_type = account_type.strip().lower() if account_type else None

    if search_name == "":
        raise HTTPException(
            status_code=400,
            detail="Search name cannot be empty."
        )

    if search_type is not None and search_type not in ("saving", "current"):
        raise HTTPException(
            status_code=400,
            detail="Account type must be 'saving' or 'current'."
        )

    matches = []
    for customer in customers:
        name_matches = (
            search_name is None
            or search_name in customer.name.casefold()
        )
        type_matches = (
            search_type is None
            or search_type == customer.account_type.strip().lower()
        )

        if name_matches and type_matches:
            matches.append({
                "name": customer.name,
                "account_number": customer.account_number,
                "balance": customer.balance,
                "account_type": customer.account_type
            })

    return {
        "results_count": len(matches),
        "customers": matches
    }


@app.get("/customers/{account_number}")
def get_customer_by_account(account_number: str):
    customers = load_customers()
    matches = []

    for customer in customers:
        if customer.account_number == account_number:
            matches.append({
                "name": customer.name,
                "account_number": customer.account_number,
                "balance": customer.balance,
                "account_type": customer.account_type
            })

    if len(matches) == 0:
        return {
            "message": "Customer not found",
            "account_number": account_number
        }

    return {
        "matches_found": len(matches),
        "customers": matches
    }


@app.post("/customers", status_code=201)
def create_customer(request: CustomerCreate):
    if not isfinite(request.balance):
        raise HTTPException(
            status_code=422,
            detail="Balance must be a finite number."
        )

    customers = load_customers()

    for customer in customers:
        if customer.account_number == request.account_number:
            raise HTTPException(
                status_code=409,
                detail="This account number already exists."
            )

    new_customer = Customer(
        name=request.name.strip(),
        account_number=request.account_number,
        balance=request.balance,
        account_type=request.account_type
    )

    customers.append(new_customer)

    try:
        save_customers(customers)
    except (OSError, ValueError) as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not save customer: {error}"
        ) from error

    return {
        "message": "Customer created successfully.",
        "customer": {
            "name": new_customer.name,
            "account_number": new_customer.account_number,
            "balance": new_customer.balance,
            "account_type": new_customer.account_type
        }
    }


@app.get("/dashboard/summary")
def dashboard_summary():
    customers = load_customers()

    total_balance = 0.0
    savings_accounts = 0
    current_accounts = 0

    for customer in customers:
        if (
            isinstance(customer.balance, bool)
            or not isinstance(customer.balance, (int, float))
            or not isfinite(customer.balance)
            or customer.balance < 0
        ):
            raise HTTPException(
                status_code=500,
                detail="Invalid balance found in customer data."
            )

        total_balance += customer.balance
        account_type = customer.account_type.strip().lower()

        if account_type == "saving":
            savings_accounts += 1
        elif account_type == "current":
            current_accounts += 1

    if not isfinite(total_balance):
        raise HTTPException(
            status_code=500,
            detail="Total balance calculation is invalid."
        )

    return {
        "total_customer_records": len(customers),
        "total_balance": round(total_balance, 2),
        "savings_accounts": savings_accounts,
        "current_accounts": current_accounts,
        "currency": "ETB"
    }


@app.get("/customers/{account_number}/transactions")
def get_customer_transactions(account_number: str):
    customers = load_customers()
    matches = [
        customer
        for customer in customers
        if customer.account_number == account_number
    ]

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="Customer account not found."
        )

    if len(matches) > 1:
        raise HTTPException(
            status_code=409,
            detail="Multiple records use this account number. Transaction history is ambiguous."
        )

    customer = matches[0]
    transactions = []

    for transaction in customer.transactions:
        if isinstance(transaction, str):
            transactions.append({
                "transaction_type": "LEGACY",
                "description": transaction
            })
        else:
            transactions.append({
                "transaction_type": transaction.transaction_type,
                "account_number": transaction.account_number,
                "amount": transaction.amount,
                "status": transaction.status,
                "description": transaction.description,
                "timestamp": transaction.timestamp.isoformat()
            })

    return {
        "customer_name": customer.name,
        "account_number": customer.account_number,
        "transaction_count": len(transactions),
        "transactions": transactions
    }


@app.post("/accounts/deposit")
def deposit_to_account(request: DepositAccountRequest):
    customers = load_customers()
    matches = [
        customer
        for customer in customers
        if customer.account_number == request.account_number
    ]

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="Customer account not found."
        )

    if len(matches) > 1:
        raise HTTPException(
            status_code=409,
            detail="Duplicate account records found. Deposit cancelled."
        )

    customer = matches[0]

    if (
        isinstance(customer.balance, bool)
        or not isinstance(customer.balance, (int, float))
        or not isfinite(customer.balance)
        or customer.balance < 0
    ):
        raise HTTPException(
            status_code=409,
            detail="Customer balance is invalid. Deposit cancelled."
        )

    old_balance = customer.balance
    new_balance = old_balance + request.amount

    if not isfinite(new_balance) or new_balance > 1_000_000_000:
        raise HTTPException(
            status_code=422,
            detail="Resulting balance exceeds the permitted limit."
        )

    transaction = Transaction(
        transaction_type="DEPOSIT",
        account_number=customer.account_number,
        amount=request.amount,
        status="SUCCESS",
        description="Deposit through banking dashboard"
    )

    customer.transactions.append(transaction)
    customer.balance = new_balance

    try:
        save_customers(customers)
    except (OSError, ValueError, TypeError) as error:
        customer.balance = old_balance
        customer.transactions.pop()
        raise HTTPException(
            status_code=500,
            detail="Could not save the deposit."
        ) from error

    return {
        "message": "Deposit completed successfully.",
        "account_number": customer.account_number,
        "customer_name": customer.name,
        "deposit_amount": request.amount,
        "previous_balance": old_balance,
        "new_balance": new_balance,
        "transaction_type": transaction.transaction_type,
        "status": transaction.status,
        "timestamp": transaction.timestamp.isoformat(),
        "currency": "ETB"
    }


@app.post("/accounts/withdraw")
def withdraw_from_account(request: WithdrawalAccountRequest):
    customers = load_customers()
    matches = [
        customer
        for customer in customers
        if customer.account_number == request.account_number
    ]

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="Customer account not found."
        )

    if len(matches) > 1:
        raise HTTPException(
            status_code=409,
            detail="Duplicate account records found. Withdrawal cancelled."
        )

    customer = matches[0]

    if (
        isinstance(customer.balance, bool)
        or not isinstance(customer.balance, (int, float))
        or not isfinite(customer.balance)
        or customer.balance < 0
    ):
        raise HTTPException(
            status_code=409,
            detail="Customer balance is invalid. Withdrawal cancelled."
        )

    old_balance = customer.balance

    if request.amount > old_balance:
        raise HTTPException(
            status_code=409,
            detail="Insufficient balance. Withdrawal cancelled."
        )

    new_balance = old_balance - request.amount

    if not isfinite(new_balance) or new_balance < 0:
        raise HTTPException(
            status_code=422,
            detail="Resulting balance would be invalid."
        )

    transaction = Transaction(
        transaction_type="WITHDRAWAL",
        account_number=customer.account_number,
        amount=request.amount,
        status="SUCCESS",
        description="Withdrawal through banking dashboard"
    )

    customer.balance = new_balance
    customer.transactions.append(transaction)

    try:
        save_customers(customers)
    except (OSError, ValueError, TypeError) as error:
        customer.balance = old_balance
        customer.transactions.pop()
        raise HTTPException(
            status_code=500,
            detail="Could not save the withdrawal."
        ) from error

    return {
        "message": "Withdrawal completed successfully.",
        "account_number": customer.account_number,
        "customer_name": customer.name,
        "withdrawal_amount": request.amount,
        "previous_balance": old_balance,
        "new_balance": new_balance,
        "transaction_type": transaction.transaction_type,
        "status": transaction.status,
        "timestamp": transaction.timestamp.isoformat(),
        "currency": "ETB"
    }

@app.post("/accounts/transfer")
def transfer_between_accounts(request: TransferRequest):
    customers = load_customers()

    # Find sender and recipient
    sender_matches = [
        c for c in customers
        if c.account_number == request.sender_account
    ]
    recipient_matches = [
        c for c in customers
        if c.account_number == request.recipient_account
    ]

    if request.sender_account == request.recipient_account:
        raise HTTPException(
            status_code=400,
            detail="Sender and recipient must be different accounts."
        )

    if not sender_matches:
        raise HTTPException(status_code=404, detail="Sender account not found.")

    if not recipient_matches:
        raise HTTPException(status_code=404, detail="Recipient account not found.")

    if len(sender_matches) > 1 or len(recipient_matches) > 1:
        raise HTTPException(status_code=409, detail="Duplicate account numbers found.")

    sender = sender_matches[0]
    recipient = recipient_matches[0]

    # Validate balances
    for customer in (sender, recipient):
        balance = customer.balance
        if (
            isinstance(balance, bool)
            or not isinstance(balance, (int, float))
            or not isfinite(balance)
            or balance < 0
        ):
            raise HTTPException(
                status_code=400,
                detail="An account has an invalid balance."
            )

    if sender.balance < request.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance."
        )

    new_sender_balance = sender.balance - request.amount
    new_recipient_balance = recipient.balance + request.amount

    if (
        not isfinite(new_sender_balance)
        or not isfinite(new_recipient_balance)
        or new_recipient_balance > 1_000_000_000
    ):
        raise HTTPException(
            status_code=400,
            detail="Transfer would exceed the permitted balance."
        )

    # Save the original state for rollback if saving fails
    old_sender_balance = sender.balance
    old_recipient_balance = recipient.balance
    old_sender_transactions = list(sender.transactions)
    old_recipient_transactions = list(recipient.transactions)

    try:
        sender.balance = new_sender_balance
        recipient.balance = new_recipient_balance

        sender.transactions.append(
            Transaction(
                "TRANSFER",
                sender.account_number,
                request.amount,
                "SUCCESS",
                f"Transfer to {recipient.account_number}"
            )
        )

        recipient.transactions.append(
            Transaction(
                "TRANSFER",
                recipient.account_number,
                request.amount,
                "SUCCESS",
                f"Transfer from {sender.account_number}"
            )
        )

        save_customers(customers)

    except (OSError, ValueError, TypeError) as error:
        sender.balance = old_sender_balance
        recipient.balance = old_recipient_balance
        sender.transactions = old_sender_transactions
        recipient.transactions = old_recipient_transactions

        raise HTTPException(
            status_code=500,
            detail="Transfer could not be saved."
        ) from error

    return {
        "message": "Transfer completed successfully.",
        "sender_account": sender.account_number,
        "recipient_account": recipient.account_number,
        "amount": request.amount,
        "sender_new_balance": sender.balance,
        "recipient_new_balance": recipient.balance,
        "status": "SUCCESS",
        "currency": "ETB"
    }
