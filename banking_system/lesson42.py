import json
import math

def show_account_audit(customer):
    print("-" * 40)
    print(f"Account Number: {customer['account_number']}")
    print(f"Customer Name: {customer['name']}")
    print(f"Balance: ${customer['balance']:.2f}")
    print(f"Transactions: {len(customer['transactions'])}")
    print("-" * 40)


def load_customers(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            customers = json.load(file)

        if not isinstance(customers, list):
            print("Error: Customer data must be a list.")
            return None

        return customers

    except FileNotFoundError:
        print(f"Error: File '{filename}' was not found.")
        return None

    except json.JSONDecodeError:
        print(f"Error: File '{filename}' contains invalid JSON.")
        return None

    except OSError as error:
        print(f"Error reading file: {error}")
        return None


def validate_customer_record(customer):
    if not isinstance(customer, dict):
        return False, "Customer record must be a dictionary."

    required_fields = [
        "name",
        "account_number",
        "balance",
        "transactions"
    ]

    for field in required_fields:
        if field not in customer:
            return False, f"Missing field: {field}"

    if not isinstance(customer["name"], str) or not customer["name"].strip():
        return False, "Customer name is invalid."

    if not isinstance(customer["account_number"], str):
        return False, "Account number must be a string."

    balance = customer["balance"]

    if isinstance(balance, bool) or not isinstance(balance, (int, float)):
        return False, "Balance must be numeric."

    if not math.isfinite(balance):
        return False, "Balance must be finite."

    if balance < 0:
        return False, "Balance cannot be negative."

    if not isinstance(customer["transactions"], list):
        return False, "Transactions must be a list."

    return True, "Record structure is valid."


def validate_transaction_record(transaction):
    if isinstance(transaction, str):
        return True, "Legacy text transaction; review format"

    if not isinstance(transaction, dict):
        return False, "Transaction must be text or a dictionary"

    required_fields = [
        "transaction_type",
        "amount"
    ]

    for field in required_fields:
        if field not in transaction:
            return False, f"Missing transaction field: {field}"

    transaction_type = transaction["transaction_type"]
    amount = transaction["amount"]

    allowed_types = {"DEPOSIT", "WITHDRAWAL", "TRANSFER"}

    if transaction_type not in allowed_types:
        return False, "Unknown transaction type"

    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return False, "Transaction amount must be numeric"

    if not math.isfinite(amount) or amount <= 0:
        return False, "Amount must be finite and positive"

    return True, "Structured transaction is valid"


def validate_account_number(account_number):
    if not isinstance(account_number, str):
        return False

    if len(account_number) != 8:
        return False

    if not account_number.isdigit():
        return False

    return True


def show_audit_summary(customers):
    account_counts = {}
    invalid_count = 0

    for customer in customers:
        account_number = customer["account_number"]

        account_counts[account_number] = (
            account_counts.get(account_number, 0) + 1
        )

        if not validate_account_number(account_number):
            invalid_count += 1

    duplicate_accounts = sum(
        1 for count in account_counts.values() if count > 1
    )

    print("\nFINAL AUDIT SUMMARY")
    print("=" * 40)
    print(f"Total records: {len(customers)}")
    print(f"Unique account numbers: {len(account_counts)}")
    print(f"Duplicate account numbers: {duplicate_accounts}")
    print(f"Records needing format review: {invalid_count}")


def save_audit_summary(customers):
    account_counts = {}
    invalid_count = 0

    for customer in customers:
        account_number = customer["account_number"]

        account_counts[account_number] = (
            account_counts.get(account_number, 0) + 1
        )

        if not validate_account_number(account_number):
            invalid_count += 1

    duplicate_accounts = sum(
        1 for count in account_counts.values() if count > 1
    )

    report = (
        "BANKING SYSTEM - AUDIT SUMMARY\n"
        + "=" * 40 + "\n"
        + f"Total records: {len(customers)}\n"
        + f"Unique account numbers: {len(account_counts)}\n"
        + f"Duplicate account numbers: {duplicate_accounts}\n"
        + f"Records needing format review: {invalid_count}\n"
        + "\nNo customer data was modified.\n"
    )

    with open("lesson42_audit_report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    print("\nAudit report saved to lesson42_audit_report.txt")


# === Main Execution ===
if __name__ == "__main__":
    customers = load_customers("customers.json")
    if customers is None:
        raise SystemExit("Audit stopped because customer data could not be loaded.")

    print(f"Total customer records: {len(customers)}")

    unique_accounts = set()
    account_counts = {}

    for customer in customers:
        account_number = customer["account_number"]
        unique_accounts.add(account_number)

        if account_number in account_counts:
            account_counts[account_number] += 1
        else:
            account_counts[account_number] = 1

    print(f"Unique account numbers: {len(unique_accounts)}")

    print("\nDUPLICATE ACCOUNT REPORT")
    print("=" * 40)

    for account_number, count in account_counts.items():
        if count > 1:
            print(f"Account: {account_number} | Records: {count}")

    print("\nAUDIT COMPLETE — NO DATA MODIFIED")

    print("\nACCOUNT NUMBER VALIDATION")
    print("=" * 40)

    for customer in customers:
        account_number = customer["account_number"]
        name = customer["name"]

        if validate_account_number(account_number):
            print(f"VALID: {account_number} | {name}")
        else:
            print(f"REVIEW: {account_number} | {name}")

    show_audit_summary(customers)
    save_audit_summary(customers)

    print("\nCUSTOMER RECORD STRUCTURE CHECK")
    print("=" * 40)

    for customer in customers:
        is_valid, message = validate_customer_record(customer)
        account_number = customer.get("account_number", "UNKNOWN")

        if is_valid:
            print( f"VALID: {account_number} | "f"{message} | Balance: ${customer['balance']:.2f}")
        else:
            print(f"REVIEW: {account_number} | {message}")
    
print("\nTRANSACTION VALIDATION REPORT")
print("=" * 40)

for customer in customers:
    account_number = customer.get("account_number", "UNKNOWN")

    for index, transaction in enumerate(
        customer.get("transactions", []), start=1
    ):
        is_valid, message = validate_transaction_record(transaction)

        if not is_valid:
            print(
                f"REVIEW: {account_number} | "
                f"Transaction {index} | {message}"
            )
        elif isinstance(transaction, str):
            print(
                f"LEGACY: {account_number} | "
                f"Transaction {index} | {message}"
            )

print("\nTransaction audit complete. No data modified.")
