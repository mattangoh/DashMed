# DashMed 🩺
***
A Python package that imports patient data from .csv files into a SQLite database, creates a dashboard displaying patient data with a graph of blood pressure over time, and manages user roles with varying permissions for data access and modification.

![Link to Pypi Package:](https://pypi.org/project/DashMed/)

![DashMed Actions](https://github.com/mattangoh/DashMed/actions/workflows/python-app.yml/badge.svg)

## Table of Contents 📜

1. [Introduction to DashMed](#1-introduction-to-dashmed)<br>
    1.1. [Repository Components](#11-repository-components)<br>
2. [Subpackages & Modules](#2-subpackages--modules)<br>
    2.1. [The `sqlite` Module](#21-the-sqlite-module-)<br>
    2.2. [The `role` Module](#22-the-role-module-)<br>
    2.3. [The `display` Module](#23-the-display-module-)<br>
    2.4. [The `bpgraph` Module](#24-the-bpgraph-module-)<br>
3. [How to Use DashMed](#3-user-guide)<br>
***
# 1. Introduction to DashMed

DashMed is a straightforward and easy-to-use software tool made for doctors and staff in medical offices. It combines the power of SQLite databases with simple dashboard tools in one package. With DashMed, healthcare workers can quickly import patient data from .csv files into a database and then view this information on user-friendly dashboards. DashMed includes a feature to create blood pressure trend graphs, making it easier for medical staff to track and understand changes in a patient's health over time. Additionally, this package includes features to control who can see or change patient information, protecting patient privacy. 

**DashMed aims to make it easier for healthcare professionals to access and use patient data effectively in their day-to-day work.**

#### 1.1 Repository Components

1. **`dashmed` package**
    - `dash` subpackage
        - `bpgraph.py`
        - `display.py`
    - `database` subpackage
        - `role.py`
        - `sqlite.py`
2. `patient_data` folder that contains the toy data (ie. example patient data) as raw .csv files
3. `test files`
    - `DashMed_test.ipynb` which contains testing of the module features
4. `HowToGuide.ipynb` containing the template to use the package
5. `Initialize.py` initializes the database infrastructure to accomodate the example data
6. `main.py` sets up the user interface for DashMed. This is what allows users to directly use the package.
7. `requirements.txt` includes the package dependencies to have before using DashMed

***

# 2. Subpackages & Modules

DashMed is structured into two distinct subpackages: `dash` and `database`. 

The **`database`** subpackage is designed to handle all aspects of database management, including initialization, modification, and user role creation, along with defining specific permissions for each role. **`database`** consists of two modules, `role` and `sqlite`, to accomplish this.

On the other hand, **`dash`** is focused on retrieving data from the database in accordance with user input and permissions, and is responsible for generating blood pressure graphs and dashboards. **`dash`** also consists of two modules, `display` and `bpgraph` to create the dashboard and blood pressure graph, respectively.

#### 2.1 The `sqlite` Module 🗄️

This module includes the import of `sqlite3`, `os`, and `pandas`, and also references `dashmed.database.role`. 

**SQLiteDB Class**:
   - This class encapsulates all the necessary functions for database initialization and manipulation.
###### SQLiteDB Functions

1. `def __init__(self, db)`: Initializes the `SQLiteDB` class instance.
   - `self`: Reference to the class instance.
   - `db`: The database connection string or path.

2. `def _role_check(self, user, allowed_roles)`: Verifies if a user's role is allowed for specific database operations.
   - `self`: Reference to the class instance.
   - `user`: The user object, likely containing user credentials and role information.
   - `allowed_roles`: A list of roles permitted to perform the operation.

3. `def connect(self)`: Establishes a connection to the SQLite database.
   - `self`: Reference to the class instance.

4. `def initialize_db(self)`: Sets up the initial structure of the database.
   - `self`: Reference to the class instance.

5. `def _create_initial_tables(self)`: Creates the initial tables in the database.
   - `self`: Reference to the class instance.

6. `def create_table(self, table_definition)`: Allows for the creation of new tables.
   - `self`: Reference to the class instance.
   - `table_definition`: SQL command for table creation.

7. `def delete_table(self, table_name)`: Enables the deletion of tables.
   - `self`: Reference to the class instance.
   - `table_name`: Name of the table to be deleted.

8. `def show_tables(self)`: Lists all tables in the database.
   - `self`: Reference to the class instance.

9. `def close(self)`: Closes the database connection.
   - `self`: Reference to the class instance.

10. `def insert_csv_data(self, table_name, csv_file_path)`: Inserts data from a CSV file into a specified table.
    - `self`: Reference to the class instance.
    - `table_name`: The table into which the data will be inserted.
    - `csv_file_path`: Path to the CSV file containing the data.

11. `def authenticate_user(self, user)`: Handles user authentication.
    - `self`: Reference to the class instance.
    - `user`: The user object for authentication, likely containing credentials and roles.

#### 2.2 The `role` Module 👤
This module includes the import of `getpass`, `sqlite3`, and also references `dashmed.database.sqlite`. This module contains 3 classes which establish user roles and permissions.

1. **class User**:
   - This class is the base class for user roles and does not inherit from other classes. It defines common attributes or methods shared across `Admin` and `Scribe` roles.

2. **class Admin(User)**:
   - Inherits from the `User` class. The `Admin` class defines attributes and methods specific to administrative users, such as enhanced permissions or administrative functionalities.

3. **class Scribe(User)**:
   - Inherits from the `User` class. Tailored for users with scribe-specific roles, it includes permissions and methods for data entry or record keeping.

###### Functions in Each Class

#### User Class
1. `def __init__(self, role_name, permissions)`: Initializes a `User` instance.
    - `self`: Reference to the class instance.
    - `role_name`: Name of the user role.
    - `permissions`: Set of permissions for this role.
2. `def display(self)`: Displays the user role's details.
    - `self`: Reference to the class instance.
3. `def add_to_database(self, db_connection)`: Adds the role to the database.
    - `self`: Reference to the class instance.
    - `db_connection`: Database connection for the operation.

#### Admin Class
- Inherits all methods from the `User` class. Includes an `admin_password` attribute to store the password that admin users must use to verify their roles. Admins have full access to the patient dashboards, blood pressure graphs, and database modification controls.
- Typically the role of doctors, nurses and other medical staff.

#### Scribe Class
- Inherits all methods from the `User` class. Includes an `scribe_password` attribute to store the password that scribe users must use to verify their roles. Scribes do not have permission to view patient dashboards nor the blood pressure graphs. They can only input and create new data for the database.
- Typically for office staff, such as the scribes, clerks and receptionists.

#### 2.2 The `display` Module 🖥️
This module contains 2 classes to retrieve patient data from the database and produce a string formatted dashboard.

1. **PatientSummary Class**:
   - This class is designed to retrieve patient data using a patient ID.
###### PatientSummary Functions
- `def __init__(self, db, PatientId)`: Initializes the `PatientSummary` instance.
    - `self`: Reference to the class instance.
    - `db`: Database connection object.
    - `PatientId`: The ID of the patient.
- `def patient_exists(self)`: Checks if a patient exists in the database.
    - `self`: Reference to the class instance.
- `def getdata(self)`: Retrieves the patient's data from the database.
    - `self`: Reference to the class instance.

2. **Dashboard Class**:
   - This class displays patient data in a dashboard format.
###### Dashboard Functions
- `def __init__(self, summary, user)`: Initializes the `Dashboard` instance.
    - `self`: Reference to the class instance.
    - `summary`: A `PatientSummary` object.
    - `user`: The user object, which includes role information.
- `def display_dash(self)`: Displays the patient data on a dashboard, accessible only by users with an 'Admin' role.
    - `self`: Reference to the class instance.

#### 2.4 The `bpgraph` Module 📈
This module includes the import of `matplotlib.pyplot`, `pandas` and `datetime`. The `BPSummary` class is used here to retrieve blood pressure data from the database and create a line plot.

**BPSummary Class**:
   - A class designed for blood pressure data management and visualization.
###### BPSummary Functions
- `def __init__(self, db, patient_id)`: Initializes the `BPSummary` instance.
    - `self`: Reference to the class instance.
    - `db`: Database connection object.
    - `patient_id`: The ID of the patient.
- `def table_exists(self)`: Checks if the blood pressure data table exists in the database.
    - `self`: Reference to the class instance.
- `def get_bp_data(self)`: Retrieves blood pressure data for a specific patient.
    - `self`: Reference to the class instance.
- `def plot(self)`: Plots the blood pressure data for visualization.
    - `self`: Reference to the class instance.

***
# 3. User Guide
### How to use DashMed?
For demonstration, the files `Initialize.py` and `main.py` in conjunction with the contents of the `patient_data` folder are required. We'll be executing the program in Terminal.

1. **`Initialize.py`**
This file is responsible for setting up or initializing the environment in which the Python application runs. It configures database connections, initializes application parameters, and sets up necessary data structures. This file prepares the application state before the main functionality starts.

2. **`main.py`**
This file is where the main execution flow of the program is defined. This file includes the setup of the application environment, the invocation of primary functions or classes, and the integration of different components of the application.

3. **`patient_data`**
This contains all the example patient data as .csv files which will be used as input into the database when using DashMed.

###### ***NOTE: The `Initialize.py` and `main.py` are programmed to accomodate .csv files that are exactly in the format of the example data given in `patient_data`. Those files and the DashMed modules may have to have some changes done to work with .csv files that have a different format.***

### Tutorial

1. Open Terminal and first ensure that you have Python installed.
![Alt text](/README_images/image-11.png)
Also ensure that you are in the proper directory where your DashMed repository is.

2. Type `python Initialize.py` to run `Initialize.py`.
![Alt text](/README_images/imagee.png)

3. It will then prompt for an **admin password**. This feature is to ensure that only admin users (whom should know the password) can initiate the database creation. In our program, the password is **admin123**.
![Alt text](/README_images/image1.png)
*Note that to change this password it would require changing it directly in `role.py`.*
This should be the final output:
![Alt text](/README_images/image2.png)

4. Type `python main.py` to run `main.py`.
![Alt text](/README_images/image.png)

5. As soon as that is run, it will print options for the user. Since we are running DashMed for the first time and have only just initialized the database, we do not have any user information stored in there, either. 
So we need to make one!
![Alt text](/README_images/image-1.png)
Input '1' to create a new user.
![Alt text](/README_images/image-2.png)
Enter in your name.
![Alt text](/README_images/image-3.png)
Then enter in your age.
![Alt text](/README_images/image-4.png)
Input a user password of your choice.
![Alt text](/README_images/image-5.png)

6. Enter your role. In this case, its admin. Enter in the admin password again.
![Alt text](/README_images/image-7.png)

7. Afterwards, the same set of options will show up. Now that we have user, we can login! It will ask you to enter in your name and password to login. Once again, you will have to enter in the admin password.
![Alt text](/README_images/image-8.png)
![Alt text](/README_images/image-9.png)
![Alt text](/README_images/image-10.png)

8. Another set of options will pop up. We can enter in '1' to view a patient dashboard. The program will prompt for a patient ID. Let's use **23989**. Now we can view the patient dashboard and we have permission to do so as admin.
![Alt text](/README_images/imageu.png)
![Alt text](/README_images/image-12.png)

9. The option menu will pop back up again. Let's look at the blood pressure graph of patient **30111**.
![Alt text](/README_images/image-13.png)
![Alt text](/README_images/image-14.png)

10. Let's finish up by logging out. The option menu will pop back up and we can enter '4' to logout, then '3' to exit DashMed.
![Alt text](/README_images/image-15.png)

This is an example of an Admin user, but what about for the Scribe user? Say we have **Matthew** saved as a Scribe user in the database already.

*Note that to create a Scribe user, we need to enter the password **scribe123**, similar to **admin123**.*

1. Login as Matthew with the scribe password.
![Alt text](/README_images/image-16.png)

2. Let's try to view the patient dashboard for patient **97021**. We can see that access was denied since scribes are not permitted to view the dashboards.
![Alt text](/README_images/image-17.png)

3. Similarly with blood pressure graphs.
![Alt text](/README_images/image-18.png)

Scribe users can add new data, though! (Option 3).

### Using `HowToGuide.ipynb`
You can run DashMed in the Jupyter Notebook `HowToGuide.ipynb` as well and run the cells to achieve the same process. This file provides a step-by-step guide to demonstrate how to use DashMed.