import sys
sys.path.append("../util/*")
sys.path.append("../db/*")
from db.ConnectionManager import ConnectionManager
import pymssql

class Appointment:
    def __init__(self, Time, Caregiver, Patient, Vaccine):
        self.time = Time
        self.caregiver = Caregiver
        self.patient = Patient
        self.vaccine = Vaccine
            

    def get_username(self):
        return self.username

    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_appointment = "INSERT INTO Appointment VALUES (%d, %s, %s, %s, %s, %d)"
        try:
            cursor.execute("SELECT count(*) AS aid FROM Appointment")
            for row in cursor:
                aid = int(row[0]) + 1
            cursor.execute(add_appointment, (aid, self.time, self.caregiver, self.patient, self.vaccine, 0))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()
        return aid