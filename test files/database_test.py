# Testing the database subpackage
### The password for admin is 'admin123' and for scribe is 'scribe123' ###

from dashmed.database import sqlite, role

# Initialize the test database using sqlite
test = sqlite.SQLiteDB('test.db')

# Initialize the users
admin1 = role.Admin('Shayla', 22)
scribe1 = role.Scribe('Matthew', 23)

try:
    # Connect and initialize the database
    test.initialize_db()
    test.connect()

    # Insert CSV data as scribe
    try:
        test.insert_csv_data(scribe1, 'patient_data/patients.csv') 
    except PermissionError:
        print('Wrongful permission denial.')

    # Show tables as admin
    try:
        test.show_tables(admin1)
    except PermissionError:
        print('Wrongful permission denial.')

    # Delete table as scribe (should fail)
    try:
        test.delete_table(scribe1, 'patients')
    except PermissionError:
        print('Scribe does not have permission to delete tables.')
# Raise other errors if they appear
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    test.close()

#################### Expected Output ###########################
# Database initialized.
# Data from patient_data/patients.csv added to patients table.
# Tables in the database:
# patients
# users
# sqlite_sequence
# Scribe does not have permission to delete tables.

# Note that the sqlite_sequence is a default table when using SQLite