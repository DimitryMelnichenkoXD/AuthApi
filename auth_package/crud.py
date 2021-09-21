import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime
from sqlalchemy import select
from . import models, schemas
import jwt


async def get_user_by_email(session: AsyncSession, email: str) -> models.User:
    stmt = select(models.User).where(models.User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_token(session: AsyncSession, token: str) -> models.User:
    stmt = select(models.User).where(models.User.token == token)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_user(session: AsyncSession, user: schemas.UserCreate):
    salt = uuid4().hex
    db_user = models.User(email=user.email,
                          password=hashlib.sha512(user.password.encode('utf-8') + salt.encode("utf-8")).hexdigest(),
                          salt=salt,
                          token=jwt.encode({"some": user.email}, salt, algorithm="HS256"),
                          balance=0.0,
                          registration_time=str(datetime.now()))
    session.add(db_user)
    await session.commit()
    return db_user


async def update_user(session: AsyncSession, email: str, balance: int):
    stmt = select(models.User).where(models.User.email == email)
    result = await session.execute(stmt)
    db_user = result.scalars().first()
    db_user.balance = balance
    await session.commit()
    return db_user


async def get_transactions(session: AsyncSession, user_id: int) -> models.Transaction:
    stmt = select(models.Transaction).where(models.Transaction.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_transactions(session: AsyncSession, new_transactions: schemas.NewTransaction, user_id: int):
    db_transactions = models.Transaction(user_id=user_id,
                                         sum_transaction=new_transactions.sum_transaction,
                                         type_transaction=new_transactions.type_transaction,
                                         date_and_time=str(datetime.time))
    session.add(db_transactions)
    await session.commit()
    return db_transactions
