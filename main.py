import hashlib
from uuid import UUID

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from user import User

app = FastAPI()
user_dict = {}
user_token = {}


class SignUp(BaseModel):
    email: str
    password: str
    password_repeat: str


# I assume the data was validated before sending
@app.post("/auth/sign_up")
def sign_up(data: SignUp):
    try:
        if data.email in user_dict.keys():
            return {"callback": "User is already registered"}
        else:
            user = User(data.email, data.password)
            user_dict[data.email] = user
            user_token[user.token] = user.email
            return {"callback": "Congratulations on your successful registration"}
    except AttributeError:
        return {"callback": "Error"}


@app.post("/auth/sign_in")
def sign_in(data: dict):
    try:
        if data["email"] not in user_dict.keys():
            return {"callback": "User is not found. Register"}
        else:
            user = user_dict[data["email"]]
            if get_hash_password(data["password"], user.salt) == user.password:
                return {"callback": user.token}
            else:
                return {"callback": "Wrong password"}
    except (TypeError, AttributeError):
        return {"callback": "Error"}


@app.get("/wallet/get_balance/{token}")
def get_balance(token: UUID):
    if token in user_token.keys():
        user = user_dict[user_token[token]]
        return {"balance": user.balance}
    else:
        return {"callback": "Not valid token"}


@app.get("/wallet/credit/{token}/{money}")
def credit(token: UUID, money: int):
    user = user_dict[user_token[token]]
    return user.credit(money)


@app.get("/wallet/debit/{token}/{money}")
def debit(token: UUID, money: int):
    user = user_dict[user_token[token]]
    return user.debit(money)


def get_hash_password(password, salt):
    return hashlib.sha512(password.encode('utf-8') + salt).digest()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
