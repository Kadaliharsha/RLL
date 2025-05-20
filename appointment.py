from db_config import get_connection
import re
import datetime
 
class Appointment:
    def __init__(self, appt_id, patient_id, doctor_id, date, diagnosis):
        self.appt_id = appt_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.diagnosis = diagnosis
 
    def add(self):
        # Data validation
        if not self.appt_id or not isinstance(self.appt_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.appt_id):
            print("Invalid Appointment ID. It must be alphanumeric (no spaces or special characters).")
            return
        if not self.patient_id or not isinstance(self.patient_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.patient_id):
            print("Invalid Patient ID. It must be alphanumeric (no spaces or special characters).")
            return
        if not self.doctor_id or not isinstance(self.doctor_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.doctor_id):
            print("Invalid Doctor ID. It must be alphanumeric (no spaces or special characters).")
            return
        try:
            datetime.datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            print("Invalid Date. Use YYYY-MM-DD format.")
            return
        if not self.diagnosis or not all(x.isalpha() or x.isspace() for x in self.diagnosis):
            print("Invalid Diagnosis. Only letters and spaces allowed.")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Check patient exists
            cursor.execute("SELECT 1 FROM patients WHERE patient_id=%s", (self.patient_id,))
            if cursor.fetchone() is None:
                print("Patient ID does not exist.")
                return
            # Check doctor exists
            cursor.execute("SELECT 1 FROM doctors WHERE doctor_id=%s", (self.doctor_id,))
            if cursor.fetchone() is None:
                print("Doctor ID does not exist.")
                return
            # Insert appointment
            sql = "INSERT INTO appointments (appt_id, patient_id, doctor_id, date, diagnosis) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.appt_id, self.patient_id, self.doctor_id, self.date, self.diagnosis))
            conn.commit()
            print("Appointment added successfully.")
        except Exception as e:
            print("Error adding appointment:", e)
        finally:
            cursor.close()
            conn.close()
 
    def update(self):
        # Data validation (same as add)
        if not self.appt_id or not isinstance(self.appt_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.appt_id):
            print("Invalid Appointment ID. It must be alphanumeric (no spaces or special characters).")
            return
        if not self.patient_id or not isinstance(self.patient_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.patient_id):
            print("Invalid Patient ID. It must be alphanumeric (no spaces or special characters).")
            return
        if not self.doctor_id or not isinstance(self.doctor_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.doctor_id):
            print("Invalid Doctor ID. It must be alphanumeric (no spaces or special characters).")
            return
        try:
            datetime.datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            print("Invalid Date. Use YYYY-MM-DD format.")
            return
        if not self.diagnosis or not all(x.isalpha() or x.isspace() for x in self.diagnosis):
            print("Invalid Diagnosis. Only letters and spaces allowed.")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Check patient exists
            cursor.execute("SELECT 1 FROM patients WHERE patient_id=%s", (self.patient_id,))
            if cursor.fetchone() is None:
                print("Patient ID does not exist.")
                return
            # Check doctor exists
            cursor.execute("SELECT 1 FROM doctors WHERE doctor_id=%s", (self.doctor_id,))
            if cursor.fetchone() is None:
                print("Doctor ID does not exist.")
                return
            # Update appointment
            sql = "UPDATE appointments SET patient_id=%s, doctor_id=%s, date=%s, diagnosis=%s WHERE appt_id=%s"
            cursor.execute(sql, (self.patient_id, self.doctor_id, self.date, self.diagnosis, self.appt_id))
            conn.commit()
            if cursor.rowcount == 0:
                print("Appointment ID not found.")
            else:
                print("Appointment updated successfully.")
        except Exception as e:
            print("Error updating appointment:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def delete(appt_id):
        if not appt_id or not isinstance(appt_id, str) or not re.match(r'^[A-Za-z0-9]+$', appt_id):
            print("Invalid Appointment ID. It must be alphanumeric (no spaces or special characters).")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM appointments WHERE appt_id=%s"
            cursor.execute(sql, (appt_id,))
            conn.commit()
            if cursor.rowcount == 0:
                print("Appointment ID not found.")
            else:
                print("Appointment deleted successfully.")
        except Exception as e:
            print("Error deleting appointment:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def view():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM appointments")
            rows = cursor.fetchall()
            print("ID | Patient ID | Doctor ID | Date | Diagnosis")
            for row in rows:
                print(" | ".join(str(x) for x in row))
        except Exception as e:
            print("Error viewing appointments:", e)
        finally:
            cursor.close()
            conn.close()
            
    def filter_appointments():
        conn=get_connection()
        cursor=conn.cursor()
        try:
            start_date = input("Enter start date(YYYY-MM-DD): ")
            end_date=input("Enter end date(YYYY-MM-DD):")
            cursor.execute("SELECT * FROM appointments WHERE date BETWEEN %s and %s",(start_date,end_date))
            for row in cursor.fetchall():
                print(row)
        except Exception as e:
            print("ERROR!!! Couldnt fetch appointments for given dates!",e)
        finally:
            cursor.close()
            conn.close()
 
