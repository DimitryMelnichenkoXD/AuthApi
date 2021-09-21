import uvicorn
import asyncio

from fastapi import FastAPI, HTTPException

from auth_package.crud import create_transactions, update_user, create_user
from auth_package import crud, models, schemas, database

from auth_package.models import get_hash_password

# asyncio.run(init_models())
app = FastAPI()


# I assume the data was validated before sending
@app.post("/auth/sign_up")
async def sign_up(user: schemas.UserCreate):
    async with database.async_session() as session:
        db_user = await crud.get_user_by_email(session, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            db_user = await create_user(session, user)
            return schemas.UserResponse(email=db_user.email, token=db_user.token)


@app.post("/auth/sign_in")
async def sign_in(user: schemas.UserLogIn):
    async with database.async_session() as session:
        db_user = await crud.get_user_by_email(session, email=user.email)
        if db_user is None:
            return schemas.UserResponse(email="User is not found.", token="Null")
        else:
            if db_user.password == get_hash_password(user.password, db_user.salt):
                return schemas.UserResponse(email=db_user.email, token=db_user.token)
            else:
                return schemas.UserResponse(email=db_user.email, token="Wrong password")


@app.get("/wallet/get_balance/{token}")
async def get_balance(token: str):
    async with database.async_session() as session:
        db_user = await crud.get_user_by_token(session, token=token)
        if db_user is None:
            return schemas.BalanceResult(email="User is not found", balance="Wrong token")
        else:
            return schemas.BalanceResult(email=db_user.email, balance=db_user.balance)


@app.post("/wallet/credit/{token}")
async def credit(token: str, new_transaction: schemas.NewTransaction):
    async with database.async_session() as session:
        db_user = await crud.get_user_by_token(session, token=token)
        if db_user is None:
            return schemas.TransactionResult(email="User is not found", balance="Wrong token")
        else:
            db_user = await update_user(session, db_user.email, db_user.credit(new_transaction))
            db_transactions = await create_transactions(session, new_transaction, db_user.id)
            return schemas.TransactionResult(status="OK")


@app.post("/wallet/debit/{token}")
async def debit(token: str, new_transaction: schemas.NewTransaction):
    async with database.async_session() as session:
        db_user = await crud.get_user_by_token(session, token=token)
        if db_user is None:
            return schemas.TransactionResult(email="User is not found", balance="Wrong token")
        else:
            db_user = await update_user(session, db_user.email, db_user.debit(new_transaction))
            db_transactions = await create_transactions(session, new_transaction, db_user.id)
            return schemas.TransactionResult(status="OK")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app)


