from dashmed.database.sqlite import SQLiteDB
from dashmed.database.role import *
from dashmed.dash.display import *
from dashmed.dash.bpgraph import *

print('Welcome to Dashmed.')

while True:
        print("\n1. Create new user\n2. Login to existing user\n3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            user = create_user()
            user.add_to_database(db = SQLiteDB("DashMed.db"))

        elif choice == '2':
            name = input("Enter your name: ")
            password = getpass.getpass("Enter your password: ")
            db = SQLiteDB("DashMed.db")
            user = db.authenticate_user(name, password)
            
            if user:
                while True:
                    print("\n1. View Patient Summary\n2. View Patient BP data\n3. Add new Data\n4. Exit")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        db = SQLiteDB("DashMed.db")
                        pid = input('Input a patient ID:')
                        dashboard = Dashboard(PatientSummary(db, pid), user)
                        dashboard.display_dash()
                    
                    elif choice == '2':
                        db = SQLiteDB("DashMed.db")
                        pid = input('Input a patient ID:')
                        bp = BPSummary(db, pid, user)
                        bp.plot()
                    
                    elif choice == '3':
                        path_to_csv = input('Enter the Path to your CSV file: ')

                        try:
                            db = SQLiteDB('Dashmed.db')
                            db.connect()
                            db.insert_csv_data(user, path_to_csv)
                        except Exception as e:
                            print(f"An error occurred: {e}")
                        finally:
                            db.close()
                            
                    elif choice == '4':
                        print("Logging Out")
                        break
                    
                    else:
                        print('Invalid input.')
                    
        elif choice == '3':
            print("Exiting Dashmed.")
            break
        
        else:
            print('Invalid Input.')