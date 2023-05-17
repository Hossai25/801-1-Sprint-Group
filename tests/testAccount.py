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
from classes.account import create_account, delete_account, Account


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
        newAccount = create_account(data)
        self.assertIsInstance(newAccount,Account)

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

    def test_valid_login(self):
    # Test case 1: Valid email and password

        email_attempt = "test@example.com"
        password_attempt = "password123"
    #    self.assertEqual(account.valid_login(email_attempt,password_attempt),True)

    # Test case 2: Invalid email
        self.assertEqual(account.valid_login("invalid@example.com", password_attempt),False)

    # Test case 3: Invalid password

        self.assertEqual(account.valid_login(email_attempt, "wrongpassword"),False)

    def test_editAccountReturnOnSuccess(self):
        user_model = User.objects.create(email="1", password="1", account_type="ta")
        PublicInfo.objects.create(first_name="1", last_name="1", office_hours="1", user_id=user_model)
        PrivateInfo.objects.create(address="1", phone_number="1", user_id=user_model)
        data = {
            'first_name': '2',
            'last_name': '2',
            'address': '2',
            'phone_number': '2',
            'office_hours': '2'
        }
        result = account.edit_account(user_model.pk, data)
        self.assertIsInstance(result, Account)

    def test_editAccountReturnOnFailure(self):
        data = {
            'first_name': '2',
            'last_name': '2',
            'address': '2',
            'phone_number': '2',
            'office_hours': '2'
        }
        result = account.edit_account(1, data)
        self.assertIsNone(result)

    def test_editAccountModelsUpdate(self):
        user_model = User.objects.create(email="1", password="1", account_type="ta")
        PublicInfo.objects.create(first_name="1", last_name="1", office_hours="1", user_id=user_model)
        PrivateInfo.objects.create(address="1", phone_number="1", user_id=user_model)
        data = {
            'first_name': '2',
            'last_name': '2',
            'address': '1',
            'phone_number': '2',
            'office_hours': '2'
        }
        result = account.edit_account(user_model.pk, data)
        self.assertIsInstance(result, Account)


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
