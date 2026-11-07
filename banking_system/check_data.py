
import json
import math
import shutil
from datetime import datetime
from collections import defaultdict

FILENAME = "customers.json"
MAX_TEST_AMOUNT = 1_000_000

with open(FILENAME, "r", encoding="utf-8") as file:
    customers = json.load(file)

accounts = defaultdict(list)

for customer in customers:
    account_number = str(customer.get("account_number", ""))
    accounts[account_number].append(customer)

print("\n=== DATA INTEGRITY REPORT ===")

# 1. Check duplicate accounts
for account_number, records in accounts.items():
    if len(records) > 1:
        print(
            f"DUPLICATE: Account {account_number} "
            f"has {len(records)} records."
        )

# 2. Check balances and transaction amounts
for customer in customers:
    name = customer.get("name", "Unknown")
    account_number = str(customer.get("account_number", ""))

    balance = customer.get("balance")

    if (
        isinstance(balance, bool)
        or not isinstance(balance, (int, float))
        or not math.isfinite(balance)
        or balance < 0
    ):
        print(
            f"INVALID BALANCE: {name}, "
            f"account {account_number}, value={balance}"
        )

    for transaction in customer.get("transactions", []):
        # Older transactions may be stored as strings.
        if not isinstance(transaction, dict):
            continue

        amount = transaction.get("amount")

        if (
            isinstance(amount, bool)
            or not isinstance(amount, (int, float))
            or not math.isfinite(amount)
            or amount < 0
        ):
            print(
                f"INVALID TRANSACTION AMOUNT: {name}, "
                f"account {account_number}, value={amount}"
            )
        elif amount > MAX_TEST_AMOUNT:
            print(
                f"SUSPICIOUS TRANSACTION AMOUNT: {name}, "
                f"account {account_number}, value={amount}"
            )

print("\nIntegrity check completed. No data was changed.")


print("\n=== DUPLICATE ACCOUNT INVESTIGATION ===")

for account_number, records in accounts.items():
    if len(records) > 1:
        print(f"\nAccount number: {account_number}")

        for index, customer in enumerate(records, start=1):
            transactions = customer.get("transactions", [])

            print(f"  Record {index}")
            print(f"    Name: {customer.get('name', 'Unknown')}")
            print(f"    Balance: {customer.get('balance')}")
            print(f"    Transaction count: {len(transactions)}")

print("\nInvestigation report completed. No data was changed.")


print("\n=== DUPLICATE BALANCE COMPARISON ===")

for account_number, records in accounts.items():
    if len(records) > 1:
        balances = [
            customer.get("balance")
            for customer in records
        ]

        print(f"\nAccount: {account_number}")
        print(f"Balances: {balances}")

        if all(balance == balances[0] for balance in balances):
            print("Result: All balances match.")
        else:
            print("Result: Balances differ. Further investigation needed.")

print("\n=== TRANSACTION HISTORY INSPECTION ===")

for account_number, records in accounts.items():
    if len(records) > 1:
        print(f"\nAccount: {account_number}")

        for index, customer in enumerate(records, start=1):
            print(f"\n  Record {index}: {customer.get('name')}")

            for transaction in customer.get("transactions", []):
                if isinstance(transaction, dict):
                    print(
                        "    Type:", transaction.get("transaction_type"),
                        "| Amount:", transaction.get("amount"),
                        "| Status:", transaction.get("status")
                    )
                else:
                    print("    Legacy transaction:", transaction)

print("\nTransaction inspection completed. No data was changed.")


print("\n=== DUPLICATE ACCOUNT SUMMARY ===")

for account_number, records in accounts.items():
    if len(records) > 1:
        print(f"\nAccount: {account_number}")

        for index, customer in enumerate(records, start=1):
            transactions = customer.get("transactions", [])

            dictionary_count = sum(
                isinstance(transaction, dict)
                for transaction in transactions
            )

            legacy_count = sum(
                isinstance(transaction, str)
                for transaction in transactions
            )

            print(
                f"Record {index}: "
                f"Balance={customer.get('balance')}, "
                f"Total transactions={len(transactions)}, "
                f"Structured={dictionary_count}, "
                f"Legacy={legacy_count}"
            )

print("\nSummary completed. No data was changed.")


print("\n=== TRANSACTION LIMIT CHECK ===")

for customer in customers:
    for transaction in customer.get("transactions", []):
        if not isinstance(transaction, dict):
            continue

        amount = transaction.get("amount")

        if (
            isinstance(amount, (int, float))
            and not isinstance(amount, bool)
            and abs(amount) > MAX_TEST_AMOUNT
        ):
            print(
                f"REVIEW: {customer.get('name')} "
                f"| Account: {customer.get('account_number')} "
                f"| Type: {transaction.get('transaction_type')} "
                f"| Amount: {amount}"
            )

print("\nTransaction limit check completed. No data was changed.")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_filename = f"customers_backup_{timestamp}.json"

shutil.copy2(FILENAME, backup_filename)

print(f"\nBackup created: {backup_filename}")


print("\n=== STRUCTURED TRANSACTION RECONCILIATION ===")

for account_number, records in accounts.items():
    if len(records) > 1:
        print(f"\nAccount: {account_number}")

        for index, customer in enumerate(records, start=1):
            transactions = customer.get("transactions", [])

            structured = [
                transaction
                for transaction in transactions
                if isinstance(transaction, dict)
            ]

            net_total = 0.0

            for transaction in structured:
                amount = transaction.get("amount")
                transaction_type = transaction.get("transaction_type")

                if (
                    isinstance(amount, (int, float))
                    and not isinstance(amount, bool)
                    and math.isfinite(amount)
                    and transaction_type in ("DEPOSIT", "WITHDRAWAL")
                ):
                    if transaction_type == "DEPOSIT":
                        net_total += amount
                    else:
                        net_total -= amount

            print(f"  Record {index}")
            print(f"    Current balance: {customer.get('balance')}")
            print(f"    Structured transactions: {len(structured)}")
            print(f"    Deposit/withdrawal net total: {net_total}")

print("\nReconciliation report completed. No data was changed.")


print("\n=== TRANSFER TRANSACTION INSPECTION ===")

for account_number, records in accounts.items():
    if len(records) > 1:
        for index, customer in enumerate(records, start=1):
            for transaction in customer.get("transactions", []):
                if (
                    isinstance(transaction, dict)
                    and transaction.get("transaction_type") == "TRANSFER"
                ):
                    print(
                        f"Account: {account_number} | "
                        f"Record: {index} | "
                        f"Amount: {transaction.get('amount')} | "
                        f"Description: {transaction.get('description')} | "
                        f"Status: {transaction.get('status')}"
                    )

print("\nTransfer inspection completed. No data was changed.")

print("\n=== FULL TRANSFER RECORDS ===")

for customer in customers:
    for transaction in customer.get("transactions", []):
        if (
            isinstance(transaction, dict)
            and transaction.get("transaction_type") == "TRANSFER"
        ):
            print(
                f"\nAccount: {customer.get('account_number')}"
            )
            print(transaction)

print("\nFull transfer inspection completed. No data was changed.")


from datetime import datetime

print("\n=== TRANSFER PAIR MATCHING ===")

transfers = []

for customer in customers:
    for transaction in customer.get("transactions", []):
        if (
            isinstance(transaction, dict)
            and transaction.get("transaction_type") == "TRANSFER"
            and transaction.get("status") == "SUCCESS"
        ):
            transfers.append({
                "account": str(customer.get("account_number")),
                "amount": transaction.get("amount"),
                "description": transaction.get("description", ""),
                "timestamp": transaction.get("timestamp", "")
            })

matched = set()

for i, first in enumerate(transfers):
    if i in matched:
        continue

    for j in range(i + 1, len(transfers)):
        if j in matched:
            continue

        second = transfers[j]

        if first["account"] == second["account"]:
            continue

        if first["amount"] != second["amount"]:
            continue

        if not (
            ("to " in first["description"].lower()
             and "from " in second["description"].lower())
            or
            ("from " in first["description"].lower()
             and "to " in second["description"].lower())
        ):
            continue

        try:
            time1 = datetime.fromisoformat(first["timestamp"])
            time2 = datetime.fromisoformat(second["timestamp"])
        except (ValueError, TypeError):
            continue

        difference = abs((time1 - time2).total_seconds())

        if difference <= 1:
            print(
                f"Possible match: {first['account']} <-> "
                f"{second['account']} | Amount: {first['amount']} | "
                f"Time difference: {difference:.6f} seconds"
            )
            matched.update((i, j))
            break

print("\nTransfer matching completed. No data was changed.")
