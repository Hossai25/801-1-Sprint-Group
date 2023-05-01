import unittest
from django.test import TestCase
from TAScheduler.models import User, PublicInfo, PrivateInfo
from typing import Dict
from unittest.mock import patch, MagicMock

from classes.account import create_account, delete_account


class TestCreateAccount(TestCase):
    '''tests whether the create_account function creates a new user, public info and private info object
    correctly when provided with a valid dictionary containing all required fields.'''

    @patch('TAScheduler.models.User.objects.create')
    @patch('TAScheduler.models.PublicInfo.objects.create')
    @patch('TAScheduler.models.PrivateInfo.objects.create')
    def test_create_account_success(self, mock_private_info, mock_public_info, mock_user_create):
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'account_type': 'T',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        mock_user_create.return_value = MagicMock(pk=1)
        create_account(data)
        mock_user_create.assert_called_once_with(email='test@example.com', password='password123', account_type='T')
        mock_public_info.assert_called_once_with(user_id=1, first_name='John', last_name='Doe')
        mock_private_info.assert_called_once_with(user_id=1)

    '''Tests whether the create_account function returns None when required fields are missing.'''

    @patch('TAScheduler.models.User.objects.create')
    def test_create_account_missing_fields(self, mock_user_create):
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'account_type': 'T',
        }
        result = create_account(data)
        self.assertIsNone(result)
        mock_user_create.assert_not_called()

    '''Tests whether the create_account function returns None when a user with the same email already 
    exists in the database.'''

    @patch('TAScheduler.models.User.objects.create')
    def test_create_account_existing_user(self, mock_user_create):
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'account_type': 'T',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        mock_user_create.side_effect = Exception('duplicate key value violates unique constraint')
        result = create_account(data)
        self.assertIsNone(result)
        mock_user_create.assert_called_once_with(email='test@example.com', password='password123', account_type='T')


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
