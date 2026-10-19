customers = [
    {
        "name": "Adrian",
        "account_number": "00123456",
        "balance": 13000.0,
        "account_type": "Savings"
    },
    {
        "name": "Abdi",
        "account_number": "00123457",
        "balance": 8500.0,
        "account_type": "Savings"
    },

    {   "name": "Tola",
        "account_number": "00123453",
        "balance": 9500.0,
        "account_type": "Savings"

    }
]

account_number = input("Enter account number: ")

found = False

for customer in customers:
    if customer["account_number"] == account_number:
        found = True

        print()
        print("===== CUSTOMER FOUND =====")
        print("Name:", customer["name"])
        print("Account:", customer["account_number"])
        print("Balance:", customer["balance"])
        print("account_type:", customer["account_type"])
        print("==========================")

        deposit = float(input("Enter deposit amount: "))

        if deposit > 0:
           customer["balance"] += deposit
           print("Deposit successful.")
           print("New Balance:", customer["balance"])
        else:
           print("Deposit must be greater than zero.")

if not found:
    print("Customer not found.")