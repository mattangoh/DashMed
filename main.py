from dashmed.database.sqlite import SQLiteDB
from dashmed.database.role import *

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
                        pass
                    
                    elif choice == '2':
                        pass
                    
                    elif choice == '3':
                        pass
                    
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