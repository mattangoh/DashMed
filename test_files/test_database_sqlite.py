import sys
import os
import unittest
import sqlite3 as sql

# Fixing Directory to allow importing dashmed functions
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importing dashmed 

from dashmed.database.sqlite import *

class TestSQLiteDB(unittest.TestCase):

    def setUp(self):
        """Set up a test database."""
        self.db = SQLiteDB(':memory:')  # Using an in-memory database for testing
        self.db.connect()

    def test_connect(self):
        """Test if the connection is established."""
        self.assertIsNotNone(self.db.conn)

    def tearDown(self):
        """Close the database connection."""
        self.db.close()

if __name__ == '__main__':
    unittest.main()