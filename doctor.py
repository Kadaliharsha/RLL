import re
from db_config import get_connection
 
class Doctor:
    def __init__(self, doctor_id, name, specialization, contact_no):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.contact_no = contact_no
 
    def add(self):
        # Enhanced Data validation
        if not self.doctor_id or not isinstance(self.doctor_id, str) or not re.match(r'^(?=.*[A-Za-z])[A-Za-z0-9]+$', self.doctor_id):
            print("Invalid Doctor ID. It must be alphanumeric and contain at least one letter (no spaces or special characters).")
            return
        if not self.name or not all(x.isalpha() or x.isspace() for x in self.name):
            print("Invalid Name. Only letters and spaces allowed.")
            return
        if not self.specialization or not all(x.isalpha() or x.isspace() for x in self.specialization):
            print("Invalid Specialization. Only letters and spaces allowed.")
            return
        if not self.contact_no.isdigit() or len(self.contact_no) < 10:
            print("Invalid Contact Number. Only digits allowed, minimum 10 digits.")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO doctors (doctor_id, name, specialization, contact_no) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (self.doctor_id, self.name, self.specialization, self.contact_no))
            conn.commit()
            print("Doctor added successfully.")
        except Exception as e:
            print("Error adding doctor:", e)
        finally:
            cursor.close()
            conn.close()
 
    def update(self):
        # Enhanced Data validation (same as add)
        if not self.doctor_id or not isinstance(self.doctor_id, str) or not re.match(r'^(?=.*[A-Za-z])[A-Za-z0-9]+$', self.doctor_id):
            print("Invalid Doctor ID. It must be alphanumeric and contain at least one letter (no spaces or special characters).")
            return
        if not self.name or not all(x.isalpha() or x.isspace() for x in self.name):
            print("Invalid Name. Only letters and spaces allowed.")
            return
        if not self.specialization or not all(x.isalpha() or x.isspace() for x in self.specialization):
            print("Invalid Specialization. Only letters and spaces allowed.")
            return
        if not self.contact_no.isdigit() or len(self.contact_no) < 10:
            print("Invalid Contact Number. Only digits allowed, minimum 10 digits.")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "UPDATE doctors SET name=%s, specialization=%s, contact_no=%s WHERE doctor_id=%s"
            cursor.execute(sql, (self.name, self.specialization, self.contact_no, self.doctor_id))
            conn.commit()
            if cursor.rowcount == 0:
                print("Doctor ID not found.")
            else:
                print("Doctor updated successfully.")
        except Exception as e:
            print("Error updating doctor:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def delete(doctor_id):
        if not doctor_id or not isinstance(doctor_id, str) or not re.match(r'^(?=.*[A-Za-z])[A-Za-z0-9]+$', doctor_id):
            print("Invalid Doctor ID. It must be alphanumeric and contain at least one letter (no spaces or special characters).")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM doctors WHERE doctor_id=%s"
            cursor.execute(sql, (doctor_id,))
            conn.commit()
            if cursor.rowcount == 0:
                print("Doctor ID not found.")
            else:
                print("Doctor deleted successfully.")
        except Exception as e:
            print("Error deleting doctor:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def view():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM doctors")
            rows = cursor.fetchall()
            print("ID | Name | Specialization | Contact No")
            for row in rows:
                print(" | ".join(str(x) for x in row))
        except Exception as e:
            print("Error viewing doctors:", e)
        finally:
            cursor.close()
            conn.close()
 
