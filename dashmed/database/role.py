class User:
    """A class representing a general user."""
    def __init__(self, name, age, password):
        """Initialize a new User instance."""
        self.name = name
        self.age = age
        self.password = password

    def display(self):
        """Display the user's details."""
        print(f'Name: {self.name}\nAge: {self.age}')

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

# Example usage
try:
    admin1 = Admin("Jane", 35)
    admin1.display()
except ValueError as e:
    print(e)

try:
    scribe1 = Scribe("John", 30)
    scribe1.display()
except ValueError as e:
    print(e)
