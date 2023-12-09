import sys
import os
import unittest
from unittest.mock import MagicMock, patch, call

# Fixing Directory to allow importing dashmed functions
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from dashmed.dash.display import *

# Testing PatientSummary
class TestPatientSummary(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.PatientId = '12345'
        self.ptsum = PatientSummary(self.mock_db, self.PatientId)

    @patch('dashmed.dash.display.PatientSummary.patient_exists')
    def test_patient_exists(self, mock_patient_exists):
        # If the patient does exist
        mock_patient_exists.return_value = True
        exists = self.ptsum.patient_exists()
        self.assertTrue(exists)

    @patch('dashmed.dash.display.PatientSummary.patient_exists')
    def test_patient_not_exists(self, mock_patient_exists):
        # If the patient does not exist
        mock_patient_exists.return_value = False
        exists = self.ptsum.patient_exists()
        self.assertFalse(exists)
    
    def test_patient_exists_sql_error(self):
        # Test for SQL error handling
        self.mock_db.connect.side_effect = sql.Error("SQL Error")
        exists = self.ptsum.patient_exists()
        self.assertFalse(exists)

    @patch('dashmed.dash.display.PatientSummary.patient_exists')
    def test_getdata(self, mock_patient_exists):
        mock_patient_exists.return_value = True
        self.mock_db.conn.cursor().fetchone.return_value = ["data1", "data2", "data3"] # Example data retrieval

        expected_data = ["data1", "data2", "data3"]
        patient_data = self.ptsum.getdata()
        self.assertEqual(patient_data, expected_data)

    @patch('dashmed.dash.display.PatientSummary.patient_exists')
    def test_getdata_invalid_patient(self, mock_patient_exists):
        # Setup patient_exists to return False for invalid patient
        mock_patient_exists.return_value = False

        patient_data = self.ptsum.getdata()
        self.assertIsNone(patient_data)

    def tearDown(self): 
        self.mock_db.reset_mock()
        self.PatientId = None
        self.ptsum = None

# Testing Dashboard class
class TestDashboard(unittest.TestCase):

    def setUp(self):
        self.mock_summary = MagicMock()
        self.mock_user = MagicMock()

    @patch('dashmed.dash.display.PatientSummary')
    @patch('dashmed.database.role.Admin')
    @patch('builtins.print')
    def test_display_dash_admin(self, mock_print, MockUser, MockSummary):
        # Setting up mock user and summary
        mock_user = MockUser.return_value
        mock_user.role = 'Admin'
        mock_summary = MockSummary.return_value
        mock_summary.getdata.return_value = ["P123", "John", "Doe", "Address", "123456", "M", "01-01-2001", 30, "Related", "History", "Medication"]
        
        dashboard = Dashboard(mock_summary, mock_user)
        dashboard.display_dash()
        mock_print.assert_called_with("-------------------------------------")

    @patch('dashmed.dash.display.PatientSummary')
    @patch('dashmed.database.role.Scribe')
    @patch('builtins.print')
    def test_display_dash_scribe(self, mock_print, MockUser, MockSummary):
        mock_user = MockUser.return_value
        mock_user.role = 'Scribe'
        dashboard = Dashboard(MockSummary.return_value, mock_user)
        dashboard.display_dash()
        mock_print.assert_called_with("Access denied.") # Should not work

    @patch('dashmed.dash.display.PatientSummary')
    @patch('dashmed.database.role.Admin')
    @patch('builtins.print')
    def test_display_dash_print(self, mock_print, MockUser, MockSummary):
        mock_user = MockUser.return_value
        mock_user.role = 'Admin'
        mock_summary = MockSummary.return_value
        complete_patient_data = ["P321", "Jane", "Doe", "123 Main St", "123-456-7890", "M", "01-01-1980", 40, "None", "No medical history", "No medication"]
        mock_summary.getdata.return_value = complete_patient_data

        dashboard = Dashboard(mock_summary, mock_user)
        dashboard.display_dash()

        # Check that all patient information is printed correctly
        expected_print_calls = [
            call('Patient Dashboard'),
            call('-------------------------------------'),
            call('Patient ID: P321'),
            call('First name: Jane'),
            call('Last name: Doe'),
            call('Address: 123 Main St'),
            call('Phone: 123-456-7890'),
            call('Sex: M'),
            call('Brithdate: 01-01-1980'),
            call('Age: 40'),
            call('Related patients: None'),
            call('Medical history: No medical history'),
            call('Medication: No medication'),
            call('-------------------------------------')
        ]
        mock_print.assert_has_calls(expected_print_calls)
    
    def tearDown(self): 
        self.mock_summary.reset_mock()
        self.mock_user.reset_mock()
    
if __name__ == '__main__':
    unittest.main()