import sqlite3 as sql
import os
import pandas as pd
from dashmed.database.role import *

class SQLiteDB:
    
    def __init__(self, db):
        self.db = db
        self.conn = None
    
    def _role_check(self, user, allowed_roles):
        """Check if the user's role is in the list of allowed roles and raise an error if not."""
        if user.role not in allowed_roles:
            raise PermissionError(f"Access denied: {user.role} role does not have permission for this action.")
                
    def connect(self):
        """Create a database connection to the SQLite database."""
        try:
            self.conn = sql.connect(self.db)
        except sql.Error as e:
            print(e)
    
    def initialize_db(self):
        """Initialize the database with default tables and configurations."""
        self.connect()
        self._create_initial_tables()
        self.close()
        print("Database initialized.")

    def _create_initial_tables(self):
        """Create initial tables in the database."""
        # Example: Creating a sample table. You can add your own table creation logic here.
        patients = """
                    CREATE TABLE IF NOT EXISTS patients (
                    PatientId integer PRIMARY KEY,
                    FirstName text NOT NULL,
                    LastName text NOT NULL,
                    Address text NOT NULL,
                    Phone text NOT NULL,
                    Sex text NOT NULL,
                    Birthdate date NOT NULL,
                    Age integer NOT NULL,
                    RelatedPatients text,
                    MedicalHistory text,
                    Medication text  
                    );
                    """
        users_table = """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        role TEXT NOT NULL,
                        password TEXT NOT NULL
                    );
                    """
        try:
            c = self.conn.cursor()
            c.execute(patients)
            c.execute(users_table)
        except sql.Error as e:
            print(e)
           
    def create_table(self, user, create_table_sql):
        """Create a table from the create_table_sql statement."""
        self._role_check(user, ['Admin', 'Scribe'])
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            print("Table created successfully")
        except sql.Error as e:
            print(e)
    
    def delete_table(self, user, table_name):
        """Delete a table from the database."""
        self._role_check(user, ['Admin'])
        try:
            c = self.conn.cursor()
            c.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Table {table_name} deleted successfully")
        except sql.Error as e:
            print(e)
    
    def show_tables(self, user):
        """Display all tables in the database."""
        self._role_check(user, ['Admin'])
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        try:
            c = self.conn.cursor()
            c.execute(query)
            tables = c.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        except sql.Error as e:
            print(e)
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            
    def insert_csv_data(self, user, csv_file):
        """Add data from a CSV file to a table in the database."""
        self._role_check(user, ['Admin', 'Scribe'])
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        
        df = pd.read_csv(csv_file)

        if table_name == 'patients':  # Insert the data into the table, create the table if it doesn't exist for patients since it has a primary key
            df.to_sql(table_name, self.conn, if_exists='append', index=False)
        else: # replace data if it exists for BP csv files since there is no primary key?
            df.to_sql(table_name, self.conn, if_exists='replace', index=False)

        print(f"Data from {csv_file} added to {table_name} table.")

    def authenticate_user(self, name, password):
        """Authenticate a user based on username and password."""
        select_sql = """
        SELECT id, name, age, role, password FROM users WHERE name = ?;
        """
        try:
            self.connect()
            c = self.conn.cursor()
            c.execute(select_sql, (name,))
            user_data = c.fetchone()
            
            if user_data and user_data[4] == password:
                print(f"Login successful for {user_data[1]}.")
                
                if user_data[3] == 'Admin':
                    return Admin(user_data[1], user_data[2], user_data[4])
                elif user_data[3] == 'Scribe':
                    return Scribe(user_data[1], user_data[2], user_data[4])
                else:
                    return User(user_data[1], user_data[2], user_data[4])
            else:
                print("Login failed. Please check your username and password.")
                return None
        except sql.Error as e:
            print(e)
            return None
        finally:
            self.close()