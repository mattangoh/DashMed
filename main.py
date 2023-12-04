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
            pass
            
            while True:
                