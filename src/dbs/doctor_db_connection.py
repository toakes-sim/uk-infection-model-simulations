from src.dbs.base_db_connection import BaseDBConnection

class DoctorDBConnection(BaseDBConnection):
    def __init__(self):
        super().__init__()
        # Try and create the relevant table if it does not exist
        try:
            query = ("CREATE TABLE IF NOT EXISTS doctordb ("
                     "doctor_id VARCHAR(255) PRIMARY KEY, "
                     "surgery_location VARCHAR(255), "
                     "doctor_persona VARCHAR(255), "
                     "first_name VARCHAR(255), "
                     "last_name VARCHAR(255))")
            # set the doctor db up
            self.cursor.execute(query)
            self.cnx.commit()

        except self.connector.Error as err:
            print(err)

    def add_record_of_doctor(self, surgery_location, doctor_persona, name):
        doctor_id = self.generate_uuid()
        query = ("INSERT INTO doctordb ("
                 "doctor_id, "
                 "surgery_location, "
                 "doctor_persona, "
                 "first_name, "
                 "last_name) "
                 "VALUES (%s, %s, %s, %s, %s)")
        doctor_data = (
            doctor_id,
            surgery_location,
            doctor_persona,
            name[0],
            name[1])
        self.cursor.execute(query, doctor_data)
        self.cnx.commit()
        return doctor_id

    def get_random_record_of_doctor(self):
        query = "SELECT * FROM doctordb ORDER BY rand() LIMIT 1"
        self.cursor.execute(query,)
        results = self.cursor.fetchall()[0]
        return results['doctor_id'], results['surgery_location'], results['doctor_persona']
