from app.models import User
import unittest

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user = User(password = 'example')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password = 'example')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password = 'example')
        self.assertTrue(user.verify_password('example'))
        self.assertFalse(user.verify_password('example2'))

    def test_password_salts_are_random(self):
        user = User(password='example')
        user2 = User(password='example')
        self.assertTrue(user.password_hash != user2.password_hash)