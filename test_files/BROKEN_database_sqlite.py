import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Fixing Directory to allow importing dashmed functions
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from dashmed.database.sqlite import *
from dashmed.database.role import *

# Unittest for sqlite.py
class TestSQLiteDB(unittest.TestCase):

    def setUp(self):
        # Using the mock test.db as we are mocking a connection
        self.sqlite = SQLiteDB('test.db')

    @patch('sqlite.sql.connect')
    def test_connect(self, mock_connect):
        self.sqlite.connect()
        mock_connect.assert_called_with('test.db') # Make sure its connecting to the right db

    @patch('sqlite.sql.connect')
    def test_initialize_db(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.sqlite.initialize_db()
        
        # Verify that _create_initial_tables is called
        self.assertTrue(mock_cursor.execute.called)
        mock_connection.close.assert_called_once()

    @patch('sqlite.sql.connect')
    def test_create_table(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        # Test with Admin user
        admin_user = Admin('admin_name', 'admin_password')
        create_table_sql = "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT)"
        self.sqlite.create_table(admin_user, create_table_sql)

        mock_cursor.execute.assert_called_with(create_table_sql)

    @patch('sqlite.sql.connect')
    def test_delete_table(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value
        # Test with Admin user
        admin_user = Admin('admin_name', 'admin_password')
        table_name = "test"
        self.sqlite.delete_table(admin_user, table_name)

        mock_cursor.execute.assert_called_with(f"DROP TABLE IF EXISTS {table_name}")

    @patch('sqlite.sql.connect')
    def test_show_tables(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = [('test1',), ('test2',)]

        admin_user = Admin('admin_name', 'admin_password')
        self.sqlite.show_tables(admin_user)

        mock_cursor.execute.assert_called_with("SELECT name FROM sqlite_master WHERE type='table';")

    @patch('sqlite.pd.read_csv')
    @patch('sqlite.sql.connect')
    def test_insert_csv_data(self, mock_connect, mock_read_csv):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value
        mock_df = MagicMock()
        mock_read_csv.return_value = mock_df

        admin_user = Admin('admin_name', 'admin_password')
        csv_file = 'patients.csv'
        self.sqlite.insert_csv_data(admin_user, csv_file)

        # Check if the correct methods are called on the mock DataFrame
        mock_df.to_sql.assert_called()

    @patch('sqlite.sql.connect')
    def test_authenticate_user(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchone.return_value = (1, 'admin_name', 30, 'Admin', 'admin_password')

        user = self.sqlite.authenticate_user('admin_name', 'admin_password')

        self.assertIsInstance(user, Admin)
        mock_cursor.execute.assert_called()
   
if __name__ == '__main__':
    unittest.main()
