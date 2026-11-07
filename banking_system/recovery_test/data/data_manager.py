import json
import math
import os
import shutil
from datetime import datetime

from models.customer import Customer
from models.transaction import Transaction

FILENAME = "customers.json"
BACKUP_FILENAME = "customers_backup.json"
TEMP_FILENAME = "customers.tmp"


def validate_customers(customers):
    for customer in customers:
        if not isinstance(customer.name, str) or not customer.name.strip():
            raise ValueError("Customer name cannot be empty.")

        if (
            not isinstance(customer.account_number, str)
            or not customer.account_number.isdigit()
        ):
            raise ValueError(
                f"Invalid account number for customer {customer.name}."
            )

        if not isinstance(customer.balance, (int, float)):
            raise ValueError(
                f"Invalid balance for account {customer.account_number}."
            )

        if not math.isfinite(customer.balance) or customer.balance < 0:
            raise ValueError(
                f"Invalid balance for account {customer.account_number}."
            )

def save_customers(customers):
    validate_customers(customers)
    data = []

    for customer in customers:
        transactions_data = []

        for transaction in customer.transactions:
            if isinstance(transaction, Transaction):
                transactions_data.append({
                    "transaction_type": transaction.transaction_type,
                    "account_number": transaction.account_number,
                    "amount": transaction.amount,
                    "status": transaction.status,
                    "description": transaction.description,
                    "timestamp": transaction.timestamp.isoformat()
                })
            else:
                # Preserve older transaction records stored as strings.
                transactions_data.append(transaction)

        data.append({
            "name": customer.name,
            "account_number": customer.account_number,
            "balance": customer.balance,
            "account_type": customer.account_type,
            "transactions": transactions_data
        })

    # Convert data to json string
    json_text = json.dumps(data, indent=4, allow_nan=False)

    # Step 3: Write to a temporary file first
    try:
        with open(TEMP_FILENAME, "w", encoding="utf-8") as file:
            file.write(json_text)
            file.flush()
            os.fsync(file.fileno())

        # Step 4: Back up the existing customer file
        if os.path.exists(FILENAME):
            shutil.copy2(FILENAME, BACKUP_FILENAME)

        # Step 5: Replace the main file only after the write succeeds
        os.replace(TEMP_FILENAME, FILENAME)

        print("Customers saved successfully.")

    except OSError as error:
        print("Error saving customers:", error)

        if os.path.exists(TEMP_FILENAME):
            try:
                os.remove(TEMP_FILENAME)
            except OSError:
                pass

        raise


def deserialize_customers(data):
    customers = []

    for item in data:
        customer = Customer(
            item["name"],
            item["account_number"],
            item["balance"],
            item["account_type"]
        )

        transactions = []

        for transaction_data in item.get("transactions", []):
            if isinstance(transaction_data, dict):
                transaction = Transaction(
                    transaction_type=transaction_data["transaction_type"],
                    account_number=transaction_data["account_number"],
                    amount=transaction_data["amount"],
                    status=transaction_data["status"],
                    description=transaction_data["description"]
                )

                timestamp = transaction_data.get("timestamp")

                if timestamp:
                    transaction.timestamp = datetime.fromisoformat(timestamp)

                transactions.append(transaction)
            else:
                # Keep older string-based transaction records.
                transactions.append(transaction_data)

        customer.transactions = transactions
        customers.append(customer)

    return customers





# def load_customers():
#     try:
#         with open(FILENAME, "r", encoding="utf-8") as file:
#             data = json.load(file)

#         customers = []

#         for item in data:
#             customer = Customer(
#                 item["name"],
#                 item["account_number"],
#                 item["balance"],
#                 item["account_type"]
#             )

#             transactions = []

#             for transaction_data in item.get("transactions", []):
#                 if isinstance(transaction_data, dict):
#                     transaction = Transaction(
#                         transaction_type=transaction_data["transaction_type"],
#                         account_number=transaction_data["account_number"],
#                         amount=transaction_data["amount"],
#                         status=transaction_data["status"],
#                         description=transaction_data["description"]
#                     )

#                     timestamp = transaction_data.get("timestamp")

#                     if timestamp:
#                         transaction.timestamp = datetime.fromisoformat(
#                             timestamp
#                         )

#                     transactions.append(transaction)
#                 else:
#                     # Keep older string-based transaction records.
#                     transactions.append(transaction_data)

#             customer.transactions = transactions
#             customers.append(customer)

#         print("Customers loaded successfully.")
#         return customers

#     except FileNotFoundError:
#         print("No customer file found.")
#         return []
#     except json.JSONDecodeError:
#         print("ERROR: customers.json is corrupted.")
#         print("Attempting to recover from backup...")

#         try:
#             with open(BACKUP_FILENAME, "r", encoding="utf-8") as file:
#                 backup_data = json.load(file)

#             customers = []

#             for item in backup_data:
#                 customer = Customer(
#                     item["name"],
#                     item["account_number"],
#                     item["balance"],
#                     item["account_type"]
#                 )

#                 transactions = []

#                 for transaction_data in item.get("transactions", []):
#                     if isinstance(transaction_data, dict):
#                         transaction = Transaction(
#                             transaction_type=transaction_data["transaction_type"],
#                             account_number=transaction_data["account_number"],
#                             amount=transaction_data["amount"],
#                             status=transaction_data["status"],
#                             description=transaction_data["description"]
#                         )

#                         timestamp = transaction_data.get("timestamp")

#                         if timestamp:
#                             transaction.timestamp = datetime.fromisoformat(
#                                 timestamp
#                             )

#                         transactions.append(transaction)

#                     else:
#                         transactions.append(transaction_data)

#                 customer.transactions = transactions
#                 customers.append(customer)

#             print("Backup loaded successfully.")
#             return customers

#         except FileNotFoundError:
#             print("ERROR: Backup file not found.")
#             return []

#         except json.JSONDecodeError:
#             print("ERROR: Backup file is also corrupted.")
#             return []    



def load_customers():
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        customers = deserialize_customers(data)
        print("Customers loaded successfully.")
        return customers

    except FileNotFoundError:
        print("No customer file found.")
        return []

    except json.JSONDecodeError:
        print("ERROR: customers.json is corrupted.")
        print("Attempting to recover from backup...")

        try:
            with open(BACKUP_FILENAME, "r", encoding="utf-8") as file:
                backup_data = json.load(file)

            customers = deserialize_customers(backup_data)

            # Restore the main file using the valid backup.
            with open(FILENAME, "w", encoding="utf-8") as file:
                json.dump(backup_data, file, indent=4, allow_nan=False)

            print("Backup loaded successfully.")
            print("Main customer file restored from backup.")
            return customers

        except FileNotFoundError:
            print("ERROR: Backup file not found.")
            return []

        except json.JSONDecodeError:
            print("ERROR: Backup file is also corrupted.")
            return []
