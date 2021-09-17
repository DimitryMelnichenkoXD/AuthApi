import hashlib

from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from . import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.token == token).first()


def create_user(db: Session, user: schemas.UserCreate):
    salt = uuid4().bytes
    db_user = models.User(email=user.email,
                          password=hashlib.sha512(user.password.encode('utf-8') + salt).digest(),
                          salt=salt,
                          token=str(uuid4()),
                          balance=0,
                          registration_time=str(datetime.time))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, email: str, balance: int):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    db_user.balance = balance
    db.commit()
    return db_user


def get_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.User.id == user_id).all()


def create_transactions(db: Session, new_transactions: schemas.NewTransaction, user_id: int):
    db_transactions = models.Transaction(user_id=user_id,
                                         sum_transaction=new_transactions.sum_transaction,
                                         type_transaction=new_transactions.type_transaction,
                                         date_and_time=str(datetime.time))
    db.add(db_transactions)
    db.commit()
    return db_transactions
