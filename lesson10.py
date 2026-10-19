customer = {
    "name": "Adrian",
    "account_number": "00123456",
    "balance": 13000.0,
    "account_type": "Savings",
    "transactions": [
        "Deposit: +$5000.00",
        "Withdrawal: -$2000.00"
    ]
}

print(customer["name"])
print(customer["account_number"])
print(customer["balance"])
print(customer["account_type"])
for transaction in customer["transactions"]:
    print(transaction)