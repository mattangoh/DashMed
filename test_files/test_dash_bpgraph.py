import sys
import os
import unittest
from unittest.mock import Mock, MagicMock, patch

# Fixing Directory to allow importing dashmed functions
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from dashmed.dash.bpgraph import *

# Testing the BPSummary class
class TestBPSummary(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()
        self.PatientId = "12345" # Example patient ID
        self.mock_user = Mock()
        self.bpsum = BPSummary(self.mock_db, self.PatientId, self.mock_user)

    def test_table_exists_true(self): # If the table does exist
        self.mock_db.connect.return_value = None
        self.mock_db.conn.cursor.return_value.fetchone.return_value = True
        self.assertTrue(self.bpsum.table_exists())

    def test_get_bp_data(self):
        # Test fetching BP data
        self.mock_db.connect.return_value = None
        self.mock_db.conn.cursor.return_value.execute.return_value = None
        # Example of rows retrieved from bp data (two tuples)
        self.mock_db.conn.cursor.return_value.fetchall.return_value = [('2001-01-01', 60, 120, 80), ('2023-01-02', 69, 130, 85)]
        self.mock_db.conn.cursor.return_value.description = [('Date',), ('Resting Heart Rate',), ('Systolic Pressure',), ('Diastolic Pressure',)]

        bp_data = self.bpsum.get_bp_data()
        self.assertIsNotNone(bp_data)
        self.assertEqual(len(bp_data), 2) # Ensure that we are retrieving the 2 tuples

        # Test when no data is available
        self.mock_db.conn.cursor.return_value.fetchall.return_value = []
        no_data = self.bpsum.get_bp_data()
        self.assertTrue(no_data.empty)

    @patch('matplotlib.pyplot.show')
    def test_plot(self, mock_plot):
        # Have get_bp_data return a dataframe
        self.bpsum.get_bp_data = MagicMock(return_value=pd.DataFrame([('2001-01-01', 60, 120, 80), ('2023-01-02', 69, 130, 85)], columns=['Date', 'Resting Heart Rate', 'Systolic Pressure', 'Diastolic Pressure']))

        # Test with Admin user
        self.mock_user.role = 'Admin'
        self.bpsum.plot()
        mock_plot.assert_called()

        mock_plot.reset_mock() # Reset the mock

        # Test with Scribe user
        self.mock_user.role = 'Scribe'
        self.bpsum.plot()
        mock_plot.assert_not_called()

if __name__ == '__main__':
    unittest.main()