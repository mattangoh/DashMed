import sys
import os
from unittest.mock import Mock, MagicMock, patch
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
    def test_admin_init_incorrect_password(self, mock_input):
        """Test Scribe initialization with an incorrect password."""
        with self.assertRaises(ValueError):
            Admin('ScribeUser', 25, 'scribepass')

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
    
    @patch('builtins.input', side_effect=['Will Smith', '35', 'user'])
    @patch('getpass.getpass', return_value='user_password')
    def test_create_user(self, mock_getpass, mock_input):
        """Test the create_user function for creating an admin user."""
        user = create_user()
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, 'Will Smith')    

class TestAddToDataBase(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = MagicMock()
        self.user = User("John", 30, "password123", "Admin")
    
    def test_add_to_database_success(self):
        # Simulate a successful database operation
        self.mock_db.conn.cursor().execute.return_value = True
        self.user.add_to_database(self.mock_db)
        
        # Assertions
        self.mock_db.connect.assert_called_once()
        self.mock_db.conn.cursor().execute.assert_called_once()
        self.mock_db.conn.commit.assert_called_once()
        self.mock_db.close.assert_called_once()
    
    def test_add_to_database_failure(self):
        # Simulate a database error
        self.mock_db.conn.cursor().execute.side_effect = sql.Error("Failed to insert")
        
        self.user.add_to_database(self.mock_db)

        # Assertions
        self.mock_db.connect.assert_called_once()
        self.mock_db.conn.cursor().execute.assert_called_once()
        self.mock_db.conn.rollback.assert_called_once()
        self.mock_db.close.assert_called_once()
    
    def tearDown(self):
        self.mock_db.reset_mock()


if __name__ == '__main__':
    unittest.main()
