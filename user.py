import hashlib
from datetime import datetime
from uuid import uuid4


class User:
    def __init__(self, email, password):
        self.email = email
        self.salt = uuid4().bytes
        self.password = hashlib.sha512(password.encode('utf-8') + self.salt).digest()
        self.token = uuid4()
        self.balance = 0
        self.registration_time = datetime.time

    def credit(self, money):
        self.balance += money
        return {"callback": "Money has been successfully credited", "balance": self.balance}

    def debit(self, money):
        if self.balance - money < 0:
            return {"callback": "The transaction was not completed due to insufficient funds", "balance": self.balance}
        else:
            self.balance -= money
            return {"callback": "Money was successfully debited", "balance": self.balance}
