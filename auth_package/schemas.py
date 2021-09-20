from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    password_repeat: str


class UserLogIn(BaseModel):
    email: str
    password: str


class NewTransaction(BaseModel):
    sum_transaction: float
    type_transaction: str


class TransactionResult(BaseModel):
    status: str


class BalanceResult(BaseModel):
    email: str
    balance: float


class UserResponse(BaseModel):
    email: str
    token: str
