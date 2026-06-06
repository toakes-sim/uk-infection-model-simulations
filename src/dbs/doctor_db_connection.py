import mysql.connector
import uuid
import os

class DoctorDBConnection():
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user=os.environ['MYSQLUSERNAME'],
            password=os.environ['MYSQLPASSWORD'],
            host='localhost',
            database='national_health_monitoring')
        self.cursor = self.cnx.cursor(dictionary=True)
        # Try and create the relevant table if it does not exist
        try:
            query = ("CREATE TABLE IF NOT EXISTS doctordb ("
                     "doctor_id VARCHAR(255) PRIMARY KEY, "
                     "surgery_location VARCHAR(255), "
                     "doctor_persona VARCHAR(255))")
            # set the doctor db up
            self.cursor.execute(query)
            self.cnx.commit()

        except mysql.connector.Error as err:
            print(err)

    def add_record_of_doctor(self, surgery_location, doctor_persona):
        doctor_id = self.generate_uuid()
        query = ("INSERT INTO doctordb ("
                 "doctor_id, "
                 "surgery_location, "
                 "doctor_persona) "
                 "VALUES (%s, %s, %s)")
        doctor_data = (
            doctor_id,
            surgery_location,
            doctor_persona)
        self.cursor.execute(query, doctor_data)
        self.cnx.commit()
        return doctor_id

    def get_random_record_of_doctor(self):
        query = "SELECT * FROM doctordb ORDER BY rand() LIMIT 1"
        self.cursor.execute(query,)
        results = self.cursor.fetchall()[0]
        return results['doctor_id'], results['surgery_location'], results['doctor_persona']

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    def close(self):
        self.cnx.close()