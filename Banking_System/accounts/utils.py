import random


def generate_account_data(data):
    random.seed(random.randint(300, 800))

    account_data = {
        "account_no": 30097 * 10 ** 7 + int(random.random() * 10 ** 7),
        "account_holder_name": data["account_holder_name"],
        "account_type": data["account_type"],
        "fathers_name": data["fathers_name"],
        "address": data["address"],
        "identity_proof": int(data["identity_proof"]),
        "contact": data["contact"],
        "has_debit_card": bool(data["has_debit_card"]),
        "balance": float(0),
        "user": {
            "username": str(data["account_holder_name"]).split()[0] + str(int(random.random() * 10**5)),
            "password": str(data["account_holder_name"]).split()[0] + str(int(random.random() * 10**5))
        }
    }

    return account_data
