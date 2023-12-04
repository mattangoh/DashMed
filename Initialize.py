import os
from dashmed.database.sqlite import SQLiteDB

def initialize_database():
    db_path = "DashMed.db"

    if os.path.exists(db_path):
        print(f"'{db_path}' already exists. Database initialization Failed.")
    else:
        db = SQLiteDB(db_path)
        db.initialize_db()
        print(f"Database '{db_path}' initialized.")

if __name__ == "__main__":
    initialize_database()