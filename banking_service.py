# # import json
# # from customer import Customer

# # FILENAME = "customers.json"


# # def save_customers(customers):
# #     data = [customer.to_dict() for customer in customers]

# #     with open(FILENAME, "w") as file:
# #         json.dump(data, file, indent=4)


# # def load_customers():
# #     try:
# #         with open(FILENAME, "r") as file:
# #             data = json.load(file)

# #         customers = []

# #         for item in data:
# #             customer = Customer.from_dict(item)
# #             customers.append(customer)

# #         return customers

# #     except FileNotFoundError:
# #         return []


# # def find_customer(account_number, customers):
# #     for customer in customers:
# #         if customer.account_number == account_number:
# #             return customer

# #     return None






















# from customer import Customer
# import json


# FILENAME = "customers.json"


# class BankingService:

#     def __init__(self):
#         self.customers = []
#         self.load_customers()

#     # =========================
#     # DATA MANAGEMENT
#     # =========================

#     def save_customers(self):
#         data = [customer.to_dict() for customer in self.customers]

#         with open(FILENAME, "w") as file:
#             json.dump(data, file, indent=4)

#     def load_customers(self):
#         try:
#             with open(FILENAME, "r") as file:
#                 data = json.load(file)

#             self.customers = [
#                 Customer.from_dict(item)
#                 for item in data
#             ]

#         except FileNotFoundError:
#             self.customers = []

#     # =========================
#     # CUSTOMER MANAGEMENT
#     # =========================

#     def find_customer(self, account_number):

#         for customer in self.customers:
#             if customer.account_number == account_number:
#                 return customer

#         return None

#     def create_customer(
#         self,
#         name,
#         account_number,
#         account_type,
#         balance
#     ):

#         if self.find_customer(account_number):
#             return False, "Account number already exists."

#         customer = Customer(
#             name,
#             account_number,
#             balance,
#             account_type,
#             [
#                 f"Account Created: "
#                 f"Initial Balance ${balance:.2f}"
#             ]
#         )

#         self.customers.append(customer)
#         self.save_customers()

#         return True, "Customer created successfully."

#     def delete_customer(self, account_number):

#         customer = self.find_customer(account_number)

#         if not customer:
#             return False, "Customer not found."

#         self.customers.remove(customer)
#         self.save_customers()

#         return True, "Customer deleted successfully."

#     # =========================
#     # BANKING OPERATIONS
#     # =========================

#     def deposit(self, account_number, amount):

#         customer = self.find_customer(account_number)

#         if not customer:
#             return False, "Customer not found."

#         if amount <= 0:
#             return False, "Amount must be greater than zero."

#         customer.deposit(amount)
#         self.save_customers()

#         return True, "Deposit successful."

#     def withdraw(self, account_number, amount):

#         customer = self.find_customer(account_number)

#         if not customer:
#             return False, "Customer not found."

#         if amount <= 0:
#             return False, "Amount must be greater than zero."

#         if amount > customer.balance:
#             return False, "Insufficient balance."

#         customer.withdraw(amount)
#         self.save_customers()

#         return True, "Withdrawal successful."

#     def transfer(
#         self,
#         sender_account,
#         recipient_account,
#         amount
#     ):

#         sender = self.find_customer(sender_account)
#         recipient = self.find_customer(recipient_account)

#         if not sender:
#             return False, "Sender customer not found."

#         if not recipient:
#             return False, "Recipient customer not found."

#         if sender_account == recipient_account:
#             return False, "Cannot transfer to the same account."

#         if amount <= 0:
#             return False, "Transfer amount must be greater than zero."

#         if amount > sender.balance:
#             return False, "Insufficient balance."

#         sender.transfer(recipient, amount)

#         self.save_customers()

#         return True, "Transfer successful."