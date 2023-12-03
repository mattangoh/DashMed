import sqlite3 as sql

class SQLiteDB:
    
    def __init__(self, db):
        self.db = db
        self.conn = None
        
    def connect(self):
        """Create a database connection to the SQLite database."""
        try:
            self.conn = sql.connect(self.db)
        except sql.Error as e:
            print(e)
            
    def create_table(self, create_table_sql):
        """Create a table from the create_table_sql statement."""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            print("Table created successfully")
        except sql.Error as e:
            print(e)
    
    def delete_table(self, table_name):
        """Delete a table from the database."""
        try:
            c = self.conn.cursor()
            c.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Table {table_name} deleted successfully")
        except sql.Error as e:
            print(e)
    
    def show_tables(self):
        """Display all tables in the database."""
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
            
    def insert_csv_data(self, csv_file):
        """
        Add data from a CSV file to a table in the database.
        """
        # Derive table name from the CSV file name (excluding the extension)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        
        df = pd.read_csv(csv_file)

        if table_name == 'patients':
        # Insert the data into the table, create the table if it doesn't exist for patients since it has a primary key
            df.to_sql(table_name, self.conn, if_exists='append', index=False)

            print(f"Data from {csv_file} added to {table_name} table.")
        
        # replace data if it exists for BP csv files since there is no primary key?
        else:
            df.to_sql(table_name, self.conn, if_exists='replace', index=False)

            print(f"Data from {csv_file} added to {table_name} table.")
