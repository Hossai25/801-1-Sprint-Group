#<<<<<<< HEAD
#=======
from django.test import TestCase
#>>>>>>> main
from TAScheduler.models import User, PublicInfo, PrivateInfo
from typing import Dict
#from unittest.mock import patch, MagicMock

#<<<<<<< HEAD
from classes import account


class TestCreateAccount(TestCase):


    """tests whether the create_account function creates a new user, public info and private info object
    correctly when provided with a valid dictionary containing all required fields."""
#=======
from classes.account import create_account, delete_account


class TestCreateAccount(TestCase):
    '''tests whether the create_account function creates a new user, public info and private info object
    correctly when provided with a valid dictionary containing all required fields.'''

#>>>>>>> main

    def test_create_account_success(self):
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'account_type': 'T',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        create_account(data)

    '''Tests whether the create_account function returns None when required fields are missing.'''

    def test_create_account_missing_fields(self):
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'account_type': 'T',
        }
        result = create_account(data)
        self.assertIsNone(result)

    '''Tests whether the create_account function returns None when a user with the same email already 
    exists in the database.'''
#add user model,

    def test_create_account_existing_user(self):
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'account_type': 'T',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        data2 = {
            'email': 'test@example.com',
            'password': 'password123',
            'account_type': 'T',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        example = account.create_account(data)
        result = account.create_account(data2)
        self.assertEqual(result, None)


#<<<<<<< HEAD
def test_has_required_fields():
    # Test case 1: All required fields are present
    data1 = {
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'password123',
        'user_type': 'admin',
        'account_type': 'premium'
    }
    assert __has_required_fields(data1) == True

    # Test case 2: Missing required fields
    data2 = {
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'user_type': 'admin',
        'account_type': 'premium'
    }
    assert __has_required_fields(data2) == False

    # Test case 3: Empty dictionary
    data3 = {}
    assert __has_required_fields(data3) == False

def test_valid_login():
    # Test case 1: Valid email and password
    with patch("module.get_user_model") as mock_get_user_model:
        mock_user = MagicMock()
        mock_user.password = "password123"
        mock_get_user_model.return_value = mock_user

        assert valid_login("test@example.com", "password123") == True

    # Test case 2: Invalid email
    with patch("module.get_user_model") as mock_get_user_model:
        mock_get_user_model.return_value = None

        assert valid_login("invalid@example.com", "password123") == False

    # Test case 3: Invalid password
    with patch("module.get_user_model") as mock_get_user_model:
        mock_user = MagicMock()
        mock_user.password = "password123"
        mock_get_user_model.return_value = mock_user

        assert valid_login("test@example.com", "wrongpassword") == False

#=======
class TestDeleteAccount(TestCase):
    def test_userModelRemoved(self):
        user_model = User.objects.create(email="test_email")
        delete_account(user_model.pk)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email="test_email")

    def test_publicInfoModelRemoved(self):
        user_model = User.objects.create(email="test_email")
        PublicInfo.objects.create(first_name="test", user_id=user_model)
        delete_account(user_model.pk)
        with self.assertRaises(PublicInfo.DoesNotExist):
            PublicInfo.objects.get(first_name="test")

    def test_privateInfoModelRemoved(self):
        user_model = User.objects.create(email="test_email")
        PrivateInfo.objects.create(address="test", user_id=user_model)
        delete_account(user_model.pk)
        with self.assertRaises(PrivateInfo.DoesNotExist):
            PrivateInfo.objects.get(address="test")

    def test_trueOnSuccess(self):
        user_model = User.objects.create(email="test_email")
        self.assertTrue(delete_account(user_model.pk))

    def test_falseOnFailure(self):
        user_model = User.objects.create(email="test_email")
        primary_key = user_model.pk
        user_model.delete()
        self.assertFalse(delete_account(primary_key))
#>>>>>>> main
