from money import Monetary


class Account:

    def __init__(self, owner_first_name, owner_last_name, owner_address, ban, balance=None):
        self.owner_first_name = owner_first_name
        self.owner_last_name = owner_last_name
        self.owner_address = owner_address
        self.ban = ban
        self.balance = balance if balance is not None else Monetary(0, "PLN")

    def __repr__(self):
        return f"Account {self.ban}, balance {self.balance}"
