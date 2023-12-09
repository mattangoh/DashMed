import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class BPSummary:
    """ BPSummary class to retrieve blood pressure data from database and plot graph. """
    def __init__(self, db, PatientId, user):
        self.db = db
        self.PatientId = PatientId
        self.table = f'"{PatientId}_BP"'
        self.user = user

    def table_exists(self):
        """ Check if the BP table for the patient exists in the database. """
        
        query = "SELECT * FROM sqlite_master WHERE type='table' AND name=?;"

        try:
            self.db.connect()
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self.PatientId + "_BP",))
            return cursor.fetchone() is not None
        
        except sql.Error as e:
            print(e)
            return False

        finally:
            self.db.close()

    def get_bp_data(self):
        """ Fetch the BP data for the patient from the database. """
        if not self.table_exists():
            print(f"No BP data table found for patient ID {self.PatientId}.")
            return None
        
        query = f'SELECT * FROM {self.table};'

        try:
            self.db.connect()
            cursor = self.db.conn.cursor()
            cursor.execute(query) 
            columns = [desc[0] for desc in cursor.description] # Fetch the column names
            bp_data = cursor.fetchall()

            df = pd.DataFrame(bp_data, columns=columns)
            return df
        
        except sql.Error as e:
            print(e)

        finally:
            self.db.close()

    def plot(self):
        """ Plot the BP data for the patient. """
        bp_data = self.get_bp_data()

        if self.user.role != 'Admin': # Will only show the bp graph if the user has an Admin role
            print('Access denied.')
            return
        
        else:
            if bp_data is not None:
            # Convert the Date column to datetime objects for plotting
                bp_data['Date'] = pd.to_datetime(bp_data['Date'])
                
                plt.figure(figsize=(14, 7))
                plt.plot(bp_data['Date'], bp_data['Resting Heart Rate'], label='Resting Heart Rate')
                plt.plot(bp_data['Date'], bp_data['Systolic Pressure'], label='Systolic Pressure')
                plt.plot(bp_data['Date'], bp_data['Diastolic Pressure'], label='Diastolic Pressure')

                plt.title(f'Blood Pressure Summary for Patient {self.PatientId}')
                plt.xlabel('Date')
                plt.ylabel('Values')
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.show()
