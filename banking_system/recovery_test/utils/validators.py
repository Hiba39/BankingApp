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
