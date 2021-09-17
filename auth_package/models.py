import hashlib

from auth_package.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    salt = Column(String, unique=True, index=True)
    token = Column(String, unique=True, index=True)
    balance = Column(Integer, index=True)
    registration_time = Column(String, index=True)

    def credit(self, transaction):
        self.balance += transaction.sum_transaction
        return self.balance

    def debit(self, transaction):
        self.balance -= transaction.sum_transaction
        return self.balance


# Здесь должен быть еще пользователь в отношении которого была зарегестрирована транзакция
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    sum_transaction = Column(Integer, index=True)
    type_transaction = Column(String, index=True)
    date_and_time = Column(String, index=True)


def get_hash_password(password, salt):
    return hashlib.sha512(password.encode('utf-8') + salt).digest()
