import unittest

from main import sign_up, sign_in
from user import User


class SignUp:

    def __init__(self, email, password, password_repeat):
        self.email = email
        self.password = password
        self.password_repeat: password_repeat


class AuthTest(unittest.TestCase):
    user1 = User("123d@gmail.com", "12345")

    def test_sign_up_first_reg(self):
        self.assertEqual(sign_up(SignUp("123d@gmail.com", "12345", "12345")),
                         {"callback": "Congratulations on your successful registration"})

    def test_sign_up_second_reg(self):
        self.assertEqual(sign_up(SignUp("123d@gmail.com", "12345", "12345")),
                         {"callback": "User is already registered"})

    def test_sign_up_empty_reg(self):
        self.assertEqual(sign_up(None),
                         {"callback": "Error"})

    def test_sign_in_empty(self):
        self.assertEqual(sign_in(None),
                         {"callback": "Error"})

    def test_sign_in_unregister_user(self):
        self.assertEqual(sign_in({"email": "13d@gmail.com", "password": "12345"}),
                         {'callback': 'User is not found. Register'})

    def test_user_balance(self, user=User("123d@gmail.com", "12345")):
        self.assertEqual(user.balance, 0)

    def test_user_credit(self, user=User("123d@gmail.com", "12345")):
        self.assertEqual(user.credit(1200).get("balance"), 1200)

    def test_user_debit_true(self, user=User("123d@gmail.com", "12345")):
        user.credit(1200)
        self.assertEqual(user.debit(1200).get("balance"), 0)

    def test_user_credit_false(self, user=User("123d@gmail.com", "12345")):
        user.credit(1200)
        self.assertEqual(user.debit(1300).get("balance"), 1200)


if __name__ == '__main__':
    unittest.main()
