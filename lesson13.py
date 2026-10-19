import json

customers = [
    {
        "name": "Adrian",
        "account_number": "00123456",
        "balance": 18000.0,
        "account_type": "Savings"
    },
    {
        "name": "Abdi",
        "account_number": "00123457",
        "balance": 8500.0,
        "account_type": "Savings"
    },
    {
        "name": "Aman",
        "account_number": "00123444",
        "balance": 1800.0,
        "account_type": "Savings"
    }
]

# SAVE customers to JSON
with open("customers.json", "w") as file:
    json.dump(customers, file, indent=4)

print("Customers saved successfully.")

# READ customers from JSON
with open("customers.json", "r") as file:
    customers = json.load(file)

print("Customers loaded successfully.")

# Display customers
for customer in customers:
    print()
    print("Name:", customer["name"])
    print("Account Number:", customer["account_number"])
    print("Balance:", customer["balance"])
    print("Account Type:", customer["account_type"])