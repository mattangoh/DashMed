import sys
import os
from unittest.mock import patch
import unittest
import sqlite3 as sql

# Fixing Directory to allow importing dashmed functions
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importing dashmed 

from dashmed.database.role import *
from dashmed.database.sqlite import *

class TestUserSubclasses(unittest.TestCase):

    @patch('builtins.input', return_value='admin123')
    def test_admin_init_correct_password(self, mock_input):
        """Test Admin initialization with the correct password."""
        admin = Admin('AdminUser', 30, 'adminpass')
        self.assertEqual(admin.role, 'Admin')

    @patch('builtins.input', return_value='wrongpassword')
    def test_scribe_init_incorrect_password(self, mock_input):
        """Test Scribe initialization with an incorrect password."""
        with self.assertRaises(ValueError):
            Scribe('ScribeUser', 25, 'scribepass')

    @patch('builtins.input', return_value='scribe123')
    def test_scribe_init_correct_password(self, mock_input):
        """Test Scribe initialization with the correct password."""
        scribe = Scribe('ScribeUser', 25, 'scribepass')
        self.assertEqual(scribe.role, 'Scribe')
        
class TestCreateUserFunction(unittest.TestCase):

    @patch('builtins.input', side_effect=['John Doe', '30', 'admin', 'admin123'])
    @patch('getpass.getpass', return_value='user_password')
    def test_create_admin_user(self, mock_getpass, mock_input):
        """Test the create_user function for creating an admin user."""
        user = create_user()
        self.assertIsInstance(user, Admin)
        self.assertEqual(user.name, 'John Doe')

    @patch('builtins.input', side_effect=['Jane Doe', '30', 'scribe', 'scribe123'])
    @patch('getpass.getpass', return_value='user_password')
    def test_create_scribe_user(self, mock_getpass, mock_input):
        """Test the create_user function for creating an admin user."""
        user = create_user()
        self.assertIsInstance(user, Scribe)
        self.assertEqual(user.name, 'Jane Doe')
    

if __name__ == '__main__':
    unittest.main()
