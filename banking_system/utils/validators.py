# import math

# def get_positive_amount(message):
#     while True:
#         try:
#             amount = float(input(message))
#         if not math.isfinite(amount):
#             print("Amount must be a valid, finite number.")
#             continue

#             if amount <= 0:
#                 print("Amount must be greater than zero.")
#                 continue

#             return amount

#         except ValueError:
#             print("Invalid amount. Please enter a number.")


# def get_account_number(message):
#     while True:
#         account_number = input(message).strip()

#         if account_number == "":
#             print("Account number cannot be empty.")
#             continue
#         if not account_number.isdigit():
#             print("Account number must be contain digits only.")
#             continue

#         return account_number




import math


def get_positive_amount(message):
    while True:
        try:
            amount = float(input(message))

            if not math.isfinite(amount):
                print("Amount must be a finite number.")
                continue

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")


def get_account_number(message):
    while True:
        account_number = input(message).strip()

        if account_number == "":
            print("Account number cannot be empty.")
            continue

        if not account_number.isdigit():
            print("Account number must contain digits only.")
            continue

        return account_number


def get_customer_name(message):
    while True:
        name = input(message).strip()

        if name == "":
            print("Customer name cannot be empty.")
            continue

        return name


def get_initial_balance(message):
    while True:
        try:
            balance = float(input(message))

            if balance < 0:
                print("Initial balance cannot be negative.")
                continue

            return balance

        except ValueError:
            print("Invalid amount. Enter a numeric value.")

def get_account_type(message):
    valid_types = {
        "saving": "Saving",
        "current": "Current"
    }

    while True:
        account_type = input(message).strip().lower()

        if account_type in valid_types:
            return valid_types[account_type]

        print("Invalid account type. Enter Saving or Current.")
