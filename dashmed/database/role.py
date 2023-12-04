import getpass
import dashmed.database.sqlite
import sqlite3 as sql

class User:
    """A class representing a general user."""
    def __init__(self, name, age, password):
        """Initialize a new User instance."""
        self.name = name
        self.age = age
        self.password = password
        self.role = None

    def display(self):
        """Display the user's details."""
        print(f'Name: {self.name}\nAge: {self.age}')

    def add_to_database(self, db):
        """Add user details to the users table in the database."""
        insert_sql = """
        INSERT INTO users (name, age, role, password) VALUES (?, ?, ?, ?);
        """
        try:
            db.connect(self)
            c = db.conn.cursor()
            c.execute(insert_sql, (self.name, self.age, self.role, self.password))
            db.conn.commit()
            print(f"User {self.name} added to the database.")
        except sql.Error as e:
            print(e)
        finally:
            db.close(self)

class Admin(User):
    """A class representing an Admin user, inheriting from User."""
    admin_password = "admin123"  # Preset password for demonstration

    def __init__(self, name, age, role='Admin'):
        """Initialize a new Admin instance, requiring password verification."""
        password = input("Enter password for Admin: ")
        if password == Admin.admin_password:
            super().__init__(name, age, password)
            self.role = role
        else:
            raise ValueError("Incorrect password for Admin role.")

    def display(self):
        """Display the admin user's details along with their role."""
        super().display()
        print(f'Role: {self.role}')

class Scribe(User):
    """A class representing a Scribe user, inheriting from User."""
    scribe_password = "scribe123"  # Preset password for demonstration

    def __init__(self, name, age, role='Scribe'):
        """Initialize a new Scribe instance, requiring password verification."""
        password = input("Enter password for Scribe: ")
        if password == Scribe.scribe_password:
            super().__init__(name, age, password)
            self.role = role
        else:
            raise ValueError("Incorrect password for Scribe role.")

    def display(self):
        """Display the scribe user's details along with their role."""
        super().display()
        print(f'Role: {self.role}')

def create_user():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    password = getpass.getpass("Enter your password: ")  # Secure password input

    role = input("Enter your role (Admin/Scribe/User): ").lower()
    if role == 'admin':
        try:
            return Admin(name, age, password)
        except ValueError as e:
            print(e)
            return None
    elif role == 'scribe':
        try:
            return Scribe(name, age, password)
        except ValueError as e:
            print(e)
            return None
    else:
        return User(name, age, password)
