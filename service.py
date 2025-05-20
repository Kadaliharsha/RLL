from db_config import get_connection
import re
 
class Service:
    def __init__(self, service_id, service_name, cost):
        self.service_id = service_id
        self.service_name = service_name
        self.cost = cost

    def __repr__(self):
        return f"{self.service_name} (ID: {self.service_id}, Cost: {self.cost})"
 
    def add(self):
        # Data validation
        if not self.service_id or not isinstance(self.service_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.service_id):
            print("Invalid Service ID. It must be alphanumeric (no spaces or special characters).")
            return
        if not self.service_name or not re.match(r'^[A-Za-z0-9\s\-_]+$', self.service_name):
            print("Invalid Service Name.")
            return
        
        try:
            cost_val = float(self.cost)
            if cost_val < 0 or cost_val > 5000:
                print("Cost must be between 0 and 5000.")
                return
        except ValueError:
            print("Invalid Cost. Enter a valid number.")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO services (service_id, service_name, cost) VALUES (%s, %s, %s)"
            cursor.execute(sql, (self.service_id, self.service_name, self.cost))
            conn.commit()
            print("Service added successfully.")
        except Exception as e:
            print("Error adding service:", e)
        finally:
            cursor.close()
            conn.close()
 
    def update(self):
        # Data validation (same as add)
        if not self.service_id or not isinstance(self.service_id, str) or not re.match(r'^[A-Za-z0-9]+$', self.service_id):
            print("Invalid Service ID. It must be alphanumeric (no spaces or special characters).")
            return
        if not self.service_name or not re.match(r'^[A-Za-z0-9\s\-\_]+$', self.service_name):
            print("Invalid Service Name.")
            return
        try:
            cost_val = float(self.cost)
            if cost_val < 0 or cost_val > 5000:
                print("Cost must be between 0 and 5000.")
                return
        except ValueError:
            print("Invalid Cost. Enter a valid number.")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "UPDATE services SET service_name=%s, cost=%s WHERE service_id=%s"
            cursor.execute(sql, (self.service_name, self.cost, self.service_id))
            conn.commit()
            if cursor.rowcount == 0:
                print("Service ID not found.")
            else:
                print("Service updated successfully.")
        except Exception as e:
            print("Error updating service:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def delete(service_id):
        if not service_id or not isinstance(service_id, str) or not re.match(r'^[A-Za-z0-9]+$', service_id):
            print("Invalid Service ID. It must be alphanumeric (no spaces or special characters).")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM services WHERE service_id=%s"
            cursor.execute(sql, (service_id,))
            conn.commit()
            if cursor.rowcount == 0:
                print("Service ID not found.")
            else:
                print("Service deleted successfully.")
        except Exception as e:
            print("Error deleting service:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def view():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM services")
            rows = cursor.fetchall()
            print("ID | Name | Cost")
            for row in rows:
                print(" | ".join(str(x) for x in row))
        except Exception as e:
            print("Error viewing services:", e)
        finally:
            cursor.close()
            conn.close()
 
class ServiceUsageDB:
    @staticmethod
    def add_service_for_patient(patient_id, service):
        # Data validation
        if not re.match(r'^[A-Za-z0-9]+$', patient_id):
            print("Invalid Patient ID.")
            return
        if not re.match(r'^[A-Za-z0-9]+$', service.service_id):
            print("Invalid Service ID.")
            return
        if not re.match(r'^[A-Za-z0-9\s\-_]+$', service.service_name):
            print("Invalid Service Name.")
            return
        try:
            cost = float(service.cost)
            if cost < 0 or cost > 5000:
                print("Invalid Cost.")
                return
        except ValueError:
            print("Invalid Cost.")
            return
 
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO temp_service_usage (patient_id, service_id, service_name, cost) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (patient_id, service.service_id, service.service_name, service.cost))
            conn.commit()
            print(f"Added {service.service_name} (ID: {service.service_id}, Cost: {service.cost}) for patient {patient_id}")
        except Exception as e:
            print("Error adding service usage:", e)
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def get_services_for_patient(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "SELECT service_id, service_name, cost FROM temp_service_usage WHERE patient_id=%s"
            cursor.execute(sql, (patient_id,))
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error fetching services:", e)
            return []
        finally:
            cursor.close()
            conn.close()
 
    @staticmethod
    def clear_services_for_patient(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM temp_service_usage WHERE patient_id=%s"
            cursor.execute(sql, (patient_id,))
            conn.commit()
            print(f"Cleared services for patient {patient_id}")
        except Exception as e:
            print("Error clearing services:", e)
        finally:
            cursor.close()
            conn.close()
 
