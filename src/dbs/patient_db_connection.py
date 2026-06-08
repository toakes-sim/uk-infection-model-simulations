from src.dbs.base_db_connection import BaseDBConnection

class PatientDBConnection(BaseDBConnection):
    def __init__(self):
        super().__init__()
        # Try and create the relevant table if it does not exist
        try:
            query = ("CREATE TABLE IF NOT EXISTS patientdb ("
                     "patient_id VARCHAR(255) PRIMARY KEY, "
                     "surgery_location VARCHAR(255), "
                     "doctor_id VARCHAR(255), "
                     "patient_age INT, "
                     "patient_persona VARCHAR(510), "
                     "infection_status VARCHAR(255))")
            # set the patients db up
            self.cursor.execute(query)
            self.cnx.commit()

        except self.connector.Error as err:
            print(err)

    def add_record_of_patient(self, surgery_location, doctor_id, patient_age, patient_persona, infection_status):
        patient_id = self.generate_uuid()
        query = ("INSERT INTO patientdb ("
                 "patient_id, "
                 "surgery_location, "
                 "doctor_id, "
                 "patient_age, "
                 "patient_persona, "
                 "infection_status) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        patient_data = (
            patient_id,
            surgery_location,
            doctor_id,
            patient_age,
            patient_persona,
            infection_status)
        self.cursor.execute(query, patient_data)
        self.cnx.commit()
        return patient_id

    def get_record_of_patient(self, patient_id):
        query = "SELECT * FROM patientdb WHERE patient_id = %s"
        self.cursor.execute(query, (patient_id,))
        results = self.cursor.fetchall()
        return results