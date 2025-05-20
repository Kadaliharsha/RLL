from db_config import get_connection
from service import ServiceUsageDB
import re
import datetime
 
class Bill:
    def __init__(self, bill_id, patient_id, billing_date=None):
        self.bill_id = bill_id
        self.patient_id = patient_id
        self.billing_date = billing_date or datetime.date.today().strftime("%Y-%m-%d")
 
    def add(self):
        # Data validation
        if not self.bill_id or not isinstance(self.bill_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.bill_id):
            print("Invalid Bill ID. It must be alphanumeric (no spaces or special characters).")
            return
 
        if not self.patient_id or not isinstance(self.patient_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.patient_id):
            print("Invalid Patient ID. It must be alphanumeric (no spaces or special characters).")
            return
 
        try:
            datetime.datetime.strptime(self.billing_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid Billing Date. Use YYYY-MM-DD format.")
            return
 
        # Fetch all services used by this patient from temp_service_usage
        services = ServiceUsageDB.get_services_for_patient(self.patient_id)
        if not services:
            print("No services to bill for this patient.")
            return
 
        # Calculate total amount
        total_amount = sum(float(s[2]) for s in services)  # s[2] is cost
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Check patient exists
            cursor.execute("SELECT 1 FROM patients WHERE patient_id=%s", (self.patient_id,))
            if cursor.fetchone() is None:
                print("Patient ID does not exist.")
                return
 
            # Insert bill
            sql = "INSERT INTO billing (bill_id, patient_id, total_amount, billing_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (self.bill_id, self.patient_id, total_amount, self.billing_date))
            conn.commit()
            print(f"Bill added successfully. Total amount: {total_amount}")
 
            # (Optional) Insert service details into a billed_services table for record-keeping
            # for s in services:
            #     cursor.execute(
            #         "INSERT INTO billed_services (bill_id, service_id, service_name, cost) VALUES (%s, %s, %s, %s)",
            #         (self.bill_id, s[0], s[1], s[2])
            #     )
            # conn.commit()
 
        except Exception as e:
            print("Error adding bill:", e)
        finally:
            cursor.close()
            conn.close()
 
        # Clear temp service usage for this patient
        ServiceUsageDB.clear_services_for_patient(self.patient_id)
 
    def update(self):
        # Data validation (same as add)
        if not self.bill_id or not isinstance(self.bill_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.bill_id):
            print("Invalid Bill ID. It must be alphanumeric (no spaces or special characters).")
            return
 
        if not self.patient_id or not isinstance(self.patient_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.patient_id):
            print("Invalid Patient ID. It must be alphanumeric (no spaces or special characters).")
            return
 
        try:
            datetime.datetime.strptime(self.billing_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid Billing Date. Use YYYY-MM-DD format.")
            return
 
        # Fetch all services used by this patient from temp_service_usage
        services = ServiceUsageDB.get_services_for_patient(self.patient_id)
        if not services:
            print("No services to bill for this patient.")
            return
 
        # Calculate total amount
        total_amount = sum(float(s[2]) for s in services)  # s[2] is cost
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Check patient exists
            cursor.execute("SELECT 1 FROM patients WHERE patient_id=%s", (self.patient_id,))
            if cursor.fetchone() is None:
                print("Patient ID does not exist.")
                return
 
            # Update bill
            sql = "UPDATE billing SET patient_id=%s, total_amount=%s, billing_date=%s WHERE bill_id=%s"
            cursor.execute(sql, (self.patient_id, total_amount, self.billing_date, self.bill_id))
            conn.commit()
            if cursor.rowcount == 0:
                print("Bill ID not found.")
            else:
                print("Bill updated successfully. Total amount:", total_amount)
 
        except Exception as e:
            print("Error updating bill:", e)
        finally:
            cursor.close()
            conn.close()
 
        # Clear temp service usage for this patient
        ServiceUsageDB.clear_services_for_patient(self.patient_id)
 
    @staticmethod
    def delete(bill_id):
        if not bill_id or not isinstance(bill_id, str) or not re.match(r'^[A-Za-z0-9]+$', bill_id):
            print("Invalid Bill ID. It must be alphanumeric (no spaces or special characters).")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM billing WHERE bill_id=%s"
            cursor.execute(sql, (bill_id,))
            conn.commit()
            if cursor.rowcount == 0:
                print("Bill ID not found.")
            else:
                print("Bill deleted successfully.")
        except Exception as e:
            print("Error deleting bill:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def view():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM billing")
            rows = cursor.fetchall()
            print("ID | Patient ID | Total Amount | Billing Date")
            for row in rows:
                print(" | ".join(str(x) for x in row))
        except Exception as e:
            print("Error viewing bills:", e)
        finally:
            cursor.close()
            conn.close()
 
