class PatientSummary():
    """ Summary class to retrieve patient data from an input patient ID. """
    
    def __init__(self, db, PatientId):
        self.db = db
        self.PatientId = PatientId

    def patient_exists(self):
        """ Check if the patient ID number does exist in the database. """

        query = 'SELECT COUNT(*) FROM patients WHERE PatientId = ?'  # Placeholder added

        try:
            self.db.connect()
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self.PatientId,))  # Correctly binding the patient ID
            result = cursor.fetchone()
            return result[0] > 0
        
        except sql.Error as e:
            print(e)
            return False

        finally:
            self.db.close()

    def getdata(self):
        """ Return the row containing the patient information as a list. """
        if not self.patient_exists():
            print("Patient ID not valid. Please input valid patient ID.")
            return

        query = 'SELECT * FROM patients WHERE PatientId = ?'  # Placeholder added

        try:
            self.db.connect()
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self.PatientId,))  # Correctly binding the patient ID
            patient_data = [n for n in cursor.fetchone()]
            
            return patient_data
        
        except sql.Error as e:
            print(e)

        finally:
            self.db.close()

class Dashboard:

    def __init__(self, summary):
        """ Initialize with a Summary object """
        self.summary = summary

    def display_dash(self):
        """ Display the patient data in a simple dashboard format. """
        patient_data = self.summary.getdata()
        
        PatientId, FirstName, LastName, Address, Phone, Sex, Birthdate, Age, RelatedPatients, MedicalHistory, Medication = patient_data

        # Simple dashboard display
        print("Patient Dashboard")
        print("-------------------------------------")
        print(f"Patient ID: {PatientId}")
        print(f"First name: {FirstName}")
        print(f"Last name: {LastName}")
        print(f"Address: {Address}")
        print(f"Phone: {Phone}")
        print(f"Sex: {Sex}")
        print(f"Brithdate: {Birthdate}")
        print(f"Age: {Age}")
        print(f"Related patients: {RelatedPatients}")
        print(f"Medical history: {MedicalHistory}")
        print(f"Medication: {Medication}")
        print("-------------------------------------")

