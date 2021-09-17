import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from auth_package.crud import create_transactions, update_user, create_user
from auth_package import crud, models, schemas
from auth_package.database import SessionLocal, engine

from auth_package.models import get_hash_password

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Создание сесси
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# I assume the data was validated before sending
@app.post("/auth/sign_up")
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        db_user = create_user(db, user)
        return schemas.UserResponse(email=db_user.email, token=db_user.token)


@app.post("/auth/sign_in")
def sign_in(user: schemas.UserLogIn, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        return schemas.UserResponse(email="User is not found.", token="Null")
    else:
        if db_user.password == get_hash_password(user.password, db_user.salt):
            return schemas.UserResponse(email=db_user.email, token=db_user.token)
        else:
            return schemas.UserResponse(email=db_user.email, token="Wrong password")


@app.get("/wallet/get_balance/{token}")
def get_balance(token: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_token(db, token=token)
    if db_user is None:
        return schemas.BalanceResult(email="User is not found", balance="Wrong token")
    else:
        return schemas.BalanceResult(email=db_user.email, balance=db_user.balance)


@app.post("/wallet/credit/{token}")
def credit(token: str, new_transaction: schemas.NewTransaction, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_token(db, token=token)
    if db_user is None:
        return schemas.TransactionResult(email="User is not found", balance="Wrong token")
    else:
        db_user = update_user(db, db_user.email, db_user.credit(new_transaction))
        db_transactions = create_transactions(db, new_transaction, db_user.id)
        return schemas.TransactionResult(status="OK")


@app.post("/wallet/debit/{token}")
def debit(token: str, new_transaction: schemas.NewTransaction, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_token(db, token=token)
    if db_user is None:
        return schemas.TransactionResult(email="User is not found", balance="Wrong token")
    else:
        db_user = update_user(db, db_user.email, db_user.debit(new_transaction))
        db_transactions = create_transactions(db, new_transaction, db_user.id)
        return schemas.TransactionResult(status="OK")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app)


