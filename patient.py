from db_config import get_connection
import re
 
class Patient:
    def __init__(self, patient_id, name, age, gender, admission_date, contact_no):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.admission_date = admission_date
        self.contact_no = contact_no

# Data validation

    def add(self):
        # Validate Patient ID (integer)
        try:
            patient_id = int(self.patient_id)
            if patient_id <= 0:
                print("Invalid Patient ID. Must be a positive integer.")
                return
        except ValueError:
            print("Invalid Patient ID. Must be an integer.")
            return
     
        # Validate Name
        if not self.name or not self.name.replace(' ', '').isalpha():
            print("Invalid Name. Name must contain only letters and spaces.")
            return
     
        # Validate Age
        try:
            age = int(self.age)
            if age < 0 or age > 120:
                print("Invalid Age. Must be between 0 and 120.")
                return
        except ValueError:
            print("Invalid Age. Must be a number.")
            return
     
        # Validate Gender
        if self.gender not in ['M', 'F', 'Other']:
            print("Invalid Gender. Choose from M, F, Other.")
            return
     
        # Validate Admission Date using regex
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', self.admission_date):
            print("Invalid Admission Date. Use YYYY-MM-DD format.")
            return
     
        # Validate Contact Number
        if not self.contact_no.isdigit() or len(self.contact_no) < 10:
            print("Invalid Contact Number. Must be at least 10 digits.")
            return
     
        # Insert into DB
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO patients (patient_id, name, age, gender, admission_date, contact_no) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (patient_id, self.name, age, self.gender, self.admission_date, self.contact_no))
            conn.commit()
            print("Patient added successfully.")
        except Exception as e:
            print("Error adding patient:", e)
        finally:
            cursor.close()
            conn.close()
 
 
    def update(self):
        # Validate Patient ID (integer)
        try:
            patient_id = int(self.patient_id)
            if patient_id <= 0:
                print("Invalid Patient ID. Must be a positive integer.")
                return
        except ValueError:
            print("Invalid Patient ID. Must be an integer.")
            return
        
        if not self.name or not self.name.replace(' ', '').isalpha():
            print("Invalid Name.")
            return
        
        if not isinstance(self.age, int) or self.age <= 0 or self.age > 120:
            print("Invalid Age.")
            return
        
        if self.gender not in ['M', 'F', 'Other']:
            print("Invalid Gender. Choose from M, F, Other.")
            return
        
        try:
            import datetime
            datetime.datetime.strptime(self.admission_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid Admission Date. Use YYYY-MM-DD format.")
            return
        if not self.contact_no.isdigit() or len(self.contact_no) < 10:
            print("Invalid Contact Number.")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """UPDATE patients SET name=%s, age=%s, gender=%s, admission_date=%s, contact_no=%s WHERE patient_id=%s"""
            cursor.execute(sql, (self.name, self.age, self.gender, self.admission_date, self.contact_no, self.patient_id))
            conn.commit()
            print("Patient updated successfully.")
        except Exception as e:
            print("Error updating patient:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def delete(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM patients WHERE patient_id=%s"
            cursor.execute(sql, (patient_id,))
            conn.commit()
            print("Patient deleted successfully.")
        except Exception as e:
            print("Error deleting patient:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def view():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()
            print("patient_ID | Name | Age | Gender | Admission Date | Contact No")
            for row in rows:
                print(" | ".join(str(x) for x in row))
        except Exception as e:
            print("Error viewing patients:", e)
        finally:
            cursor.close()
            conn.close()
