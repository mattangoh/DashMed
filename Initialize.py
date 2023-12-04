import os
from dashmed.database.sqlite import SQLiteDB
from dashmed.database.role import *

def initialize_database():
    """Check if 'DashMed.db' exists and initialize it if not."""
    db_path = "DashMed.db"

    if os.path.exists(db_path):
        print(f"'{db_path}' already exists. Database initialization skipped.")
    else:
        db = SQLiteDB(db_path)
        db.initialize_db()
        print(f"Database '{db_path}' initialized.")
        
        user = Admin('Admin', 0) #check to make sure an administrator is trying to execute table generation.
        
        print("Inserting Toy Data")
        db.connect()
        db.insert_csv_data(user, 'patient_data/patients.csv')
        db.close()
        
        for filename in os.listdir('patient_data/patient_bp/'):
            if filename.endswith(".csv"):
                csv_file = os.path.join('patient_data/patient_bp/', filename)
                db.connect()
                db.insert_csv_data(user, csv_file)
                db.show_tables()
                db.close()

        print('Complete!')
        
if __name__ == "__main__":
    initialize_database()