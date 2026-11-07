import json
import math
from collections import defaultdict

FILENAME = "customers.json"

def validate_customer(customer):
    problems = []

    if not isinstance(customer.get("name"), str):
        problems.append("Invalid customer name")

    account_number = customer.get("account_number")

    if not isinstance(account_number, str) or not account_number.strip():
        problems.append("Invalid account number")

    balance = customer.get("balance")

    if (
        isinstance(balance, bool)
        or not isinstance(balance, (int, float))
        or not math.isfinite(balance)
        or balance < 0
    ):
        problems.append("Invalid balance")

    transactions = customer.get("transactions")

    if not isinstance(transactions, list):
        problems.append("Transactions must be a list")

    return problems

def customer_fingerprint(customer):
    transactions = customer.get("transactions", [])

    return (
        customer.get("name"),
        customer.get("account_number"),
        customer.get("balance"),
        len(transactions),
        tuple(str(transaction) for transaction in transactions)
    )    

def validate_transaction(transaction):
    problems = []

    if not isinstance(transaction, dict):
        problems.append("Legacy transaction format")
        return problems

    transaction_type = transaction.get("transaction_type")
    amount = transaction.get("amount")
    status = transaction.get("status")

    if transaction_type not in (
        "DEPOSIT",
        "WITHDRAWAL",
        "TRANSFER"
    ):
        problems.append("Invalid transaction type")

    if (
        isinstance(amount, bool)
        or not isinstance(amount, (int, float))
        or not math.isfinite(amount)
        or amount <= 0
    ):
        problems.append("Invalid transaction amount")
    elif amount > 1_000_000:
        problems.append("Transaction amount exceeds practice limit")

    if status != "SUCCESS":
        problems.append("Transaction is not successful")

    return problems

def compare_customers(first, second):
    differences = []

    if first.get("name") != second.get("name"):
        differences.append("Name differs")

    if first.get("account_number") != second.get("account_number"):
        differences.append("Account number differs")

    if first.get("balance") != second.get("balance"):
        differences.append("Balance differs")

    first_transactions = first.get("transactions", [])
    second_transactions = second.get("transactions", [])

    if first_transactions == second_transactions:
        transaction_result = "Transactions identical"
    else:
        transaction_result = "Transactions differ"
        differences.append("Transaction history differs")

    if not differences:
        classification = "IDENTICAL"
    elif (
        first.get("name") == second.get("name")
        and first.get("account_number") == second.get("account_number")
    ):
        classification = "PARTIALLY MATCHING"
    else:
        classification = "DIFFERENT"

    return classification, differences, transaction_result    

with open(FILENAME, "r", encoding="utf-8") as file:
    customers = json.load(file)

accounts = defaultdict(list)

for customer in customers:
    account_number = str(customer.get("account_number", "")).strip()
    accounts[account_number].append(customer)

print("\n=== DRY-RUN CLEANUP PREVIEW ===")
print("Mode: READ ONLY")
print("No customer data will be changed.")

review_count = 0

for account_number, records in accounts.items():
    if len(records) == 2:
        classification, differences, transaction_result = compare_customers(
            records[0],
            records[1]
        )

        print("\n  === RECORD COMPARISON ===")
        print(f"  Classification: {classification}")
        print(f"  {transaction_result}")

        if differences:
            print("  Differences:")
            for difference in differences:
                print(f"    - {difference}")   
    if len(records) <= 1:
        continue

    review_count += 1

    print(f"\nAccount: {account_number}")
    print(f"Duplicate records found: {len(records)}")

    for index, customer in enumerate(records, start=1):
        balance = customer.get("balance")
        customer_problems = validate_customer(customer)

        transactions = customer.get("transactions", [])

        structured_count = sum(
            isinstance(transaction, dict)
            for transaction in transactions
        )

        legacy_count = sum(
            isinstance(transaction, str)
            for transaction in transactions
        )

        suspicious_amounts = []
        transaction_problems = []

        for transaction in transactions:
            t_problems = validate_transaction(transaction)
            if t_problems:
                transaction_problems.append({
                    "transaction": transaction,
                    "problems": t_problems
                })

        for transaction in transactions:
            if not isinstance(transaction, dict):
                continue

            amount = transaction.get("amount")

            if (
                isinstance(amount, bool)
                or not isinstance(amount, (int, float))
                or not math.isfinite(amount)
                or abs(amount) > 1_000_000
            ):
                suspicious_amounts.append(amount)

        print(f"  Record {index}:")
        print(f"    Name: {customer.get('name', 'Unknown')}")
        print(f"    Balance: {balance}")
        
        if customer_problems:
            print(f"    Validation problems: {customer_problems}")
        else:
            print("    Validation: PASS")

        print(f"    Structured transactions: {structured_count}")
        print(f"    Legacy transactions: {legacy_count}")
        print(f"    Suspicious amounts: {suspicious_amounts}")

        legacy_transactions = 0
        invalid_structured_transactions = 0

        for transaction in transactions:
            if not isinstance(transaction, dict):
                legacy_transactions += 1
                continue

            problems = validate_transaction(transaction)

            if problems:
                invalid_structured_transactions += 1

        if legacy_transactions > 0 or invalid_structured_transactions > 0:
            print("    Transaction validation: REVIEW REQUIRED")
            print(f"      Legacy transactions: {legacy_transactions}")
            print(
                f"      Invalid structured transactions: "
                f"{invalid_structured_transactions}"
            )
            print(
                f"      Suspicious amounts: "
                f"{len(suspicious_amounts)}"
            )
        else:
            print("    Transaction validation: PASS")

    print("  Proposed action: MANUAL REVIEW REQUIRED")
    print("  Automatic deletion: NOT PERMITTED")

print("\n=== SUMMARY ===")
print(f"Duplicate account numbers requiring review: {review_count}")
print("No records were deleted or modified.")

print("\n=== CUSTOMER FINGERPRINT TEST ===")

for account_number, records in accounts.items():
    if len(records) > 1:
        first_fingerprint = customer_fingerprint(records[0])
        second_fingerprint = customer_fingerprint(records[1])

        print(f"\nAccount: {account_number}")

        if first_fingerprint == second_fingerprint:
            print("Fingerprint result: IDENTICAL")
        else:
            print("Fingerprint result: DIFFERENT")

print("\nFingerprint test completed. No data was changed.")

def cleanup_candidate(first, second):
    reasons = []

    if first.get("name") != second.get("name"):
        reasons.append("Customer names differ")

    if first.get("account_number") != second.get("account_number"):
        reasons.append("Account numbers differ")

    if first.get("balance") != second.get("balance"):
        reasons.append("Balances differ")

    first_transactions = first.get("transactions", [])
    second_transactions = second.get("transactions", [])

    first_legacy = sum(
        isinstance(transaction, str)
        for transaction in first_transactions
    )

    second_legacy = sum(
        isinstance(transaction, str)
        for transaction in second_transactions
    )

    if first_legacy > 0 or second_legacy > 0:
        reasons.append("Legacy transactions exist")

    suspicious_found = False

    for transaction in first_transactions + second_transactions:
        if not isinstance(transaction, dict):
            continue

        amount = transaction.get("amount")

        if (
            isinstance(amount, (int, float))
            and not isinstance(amount, bool)
            and (
                not math.isfinite(amount)
                or amount > 1_000_000
            )
        ):
            suspicious_found = True

    if suspicious_found:
        reasons.append("Suspicious transaction amounts exist")

    if reasons:
        return False, reasons

    return True, ["No obvious conflicts detected"]
    print("\n=== CLEANUP CANDIDATE CHECK ===")

for account_number, records in accounts.items():
    if len(records) > 1:
        safe_candidate, reasons = cleanup_candidate(
            records[0],
            records[1]
        )

        print(f"\nAccount: {account_number}")

        if safe_candidate:
            print("Candidate status: POTENTIALLY SAFE FOR REVIEW")
        else:
            print("Candidate status: NOT SAFE FOR AUTOMATIC CLEANUP")

        for reason in reasons:
            print(f"  - {reason}")

print("\nCleanup candidate check completed. No data was changed.")


from datetime import datetime

report_filename = (
    "cleanup_audit_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".txt"
)

with open(report_filename, "w", encoding="utf-8") as report:
    report.write("BANKING SYSTEM - CLEANUP AUDIT REPORT\n")
    report.write("=" * 45 + "\n")
    report.write(f"Generated: {datetime.now().isoformat()}\n")
    report.write("Mode: READ ONLY\n\n")

    for account_number, records in accounts.items():
        if len(records) <= 1:
            continue

        report.write(f"Account: {account_number}\n")
        report.write(f"Duplicate records: {len(records)}\n")

        for index, customer in enumerate(records, start=1):
            report.write(f"\nRecord {index}\n")
            report.write(f"Name: {customer.get('name')}\n")
            report.write(f"Balance: {customer.get('balance')}\n")
            report.write(
                f"Transaction count: "
                f"{len(customer.get('transactions', []))}\n"
            )

        report.write("Decision: MANUAL REVIEW REQUIRED\n")
        report.write("-" * 45 + "\n\n")

    report.write("No customer data was modified.\n")

print(f"\nAudit report saved to: {report_filename}")
