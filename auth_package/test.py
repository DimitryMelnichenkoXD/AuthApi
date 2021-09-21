import unittest

from auth_package.main import sign_up, sign_in
from auth_package.schemas import *


class AuthTest(unittest.TestCase):

    async def test_sign_up_first_reg(self):
        user = UserCreate(email="123456098@gmail.com", password="12345", password_repeat="12345")
        self.assertEqual(await sign_up(user),
                         {"callback": "Congratulations on your successful registration"})

    async def test_sign_up_second_reg(self):
        user = UserCreate(email="123456098@gmail.com", password="12345", password_repeat="12345")
        self.assertEqual(await sign_up(user),
                         {"callback": "User is already registered"})

    async def test_sign_up_empty_reg(self):
        self.assertEqual(await sign_up(None),
                         {"callback": "Error"})

    async def test_sign_in_empty(self):
        self.assertEqual(await sign_in(None),
                         {"callback": "Error"})

    async def test_sign_in_unregister_user(self):
        user = UserCreate(email="1111@gmail.com", password="12345", password_repeat="12345")
        self.assertEqual(await sign_in(user),
                         {'callback': 'User is not found. Register'})

    # def test_user_balance(self):
    #     token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoiMTIzNDU2NzgwQGdtYWlsLmNvbSJ9.WFzUDz2OlTSBzGoMDm9DeLjCWte8Mt6yWzM0vCUqREM" \
    #     self.assertEqual(user.balance, 0)
    #
    # def test_user_credit(self, user=User("123d@gmail.com", "12345")):
    #     self.assertEqual(user.credit(1200).get("balance"), 1200)
    #
    # def test_user_debit_true(self, user=User("123d@gmail.com", "12345")):
    #     user.credit(1200)
    #     self.assertEqual(user.debit(1200).get("balance"), 0)
    #
    # def test_user_credit_false(self, user=User("123d@gmail.com", "12345")):
    #     user.credit(1200)
    #     self.assertEqual(user.debit(1300).get("balance"), 1200)


if __name__ == '__main__':
    unittest.main()
