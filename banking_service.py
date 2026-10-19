import json
from customer import Customer

FILENAME = "customers.json"


def save_customers(customers):
    data = [customer.to_dict() for customer in customers]

    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)


def load_customers():
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)

        customers = []

        for item in data:
            customer = Customer.from_dict(item)
            customers.append(customer)

        return customers

    except FileNotFoundError:
        return []


def find_customer(account_number, customers):
    for customer in customers:
        if customer.account_number == account_number:
            return customer

    return None