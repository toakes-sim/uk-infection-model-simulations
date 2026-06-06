import mysql.connector
import uuid
import os

class AppointmentDBConnection():
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user=os.environ['MYSQLUSERNAME'],
            password=os.environ['MYSQLPASSWORD'],
            host='localhost',
            database='national_health_monitoring')
        self.cursor = self.cnx.cursor(dictionary=True)
        # Try and create the relevant table if it does not exist
        try:
            query = ("CREATE TABLE IF NOT EXISTS appointmentsdb ("
                     "appointment_id VARCHAR(255) PRIMARY KEY, "
                     "patient_id VARCHAR(255), "
                     "doctor_id VARCHAR(255), "
                     "surgery_location VARCHAR(255))")
            # set the appointments db up
            self.cursor.execute(query)

            self.cnx.commit()

        except mysql.connector.Error as err:
            print(err)

    def add_record_of_appointment(self, patient_id, doctor_id, surgery_location):
        appointment_id = self.generate_uuid()
        query = ("INSERT INTO appointmentsdb ("
                 "appointment_id , "
                 "patient_id, "
                 "doctor_id, "
                 "surgery_location) "
                 "VALUES (%s, %s, %s, %s)")
        appointment_data = (
            appointment_id,
            patient_id,
            doctor_id,
            surgery_location)
        self.cursor.execute(query, appointment_data)
        self.cnx.commit()
        return appointment_id

    def get_record_of_appointment(self, appointment_id):
        query = "SELECT * FROM appointmentsdb WHERE appointment_id = %s"
        self.cursor.execute(query, (appointment_id,))
        results = self.cursor.fetchall()
        return results

    def get_list_of_appointments(self):
        query = "SELECT appointment_id FROM appointmentsdb "
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def select_list_of_all_undiagnosed_appointments(self):
        query = ("SELECT appointment_id FROM appointmentsdb "
                 "where appointment_id not in (select appointment_id from diagnosisdb)")
        self.cursor.execute(query,)
        results = self.cursor.fetchall()
        return results

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    def close(self):
        self.cnx.close()
