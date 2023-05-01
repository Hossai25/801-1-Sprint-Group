import unittest
from unittest import TestCase
from TAScheduler.models import User, PublicInfo, PrivateInfo
from typing import Dict
from unittest.mock import patch, MagicMock

from classes.account import create_account, __has_required_fields, valid_login


class TestCreateAccount(TestCase):


    """tests whether the create_account function creates a new user, public info and private info object
    correctly when provided with a valid dictionary containing all required fields."""
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

