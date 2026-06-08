from src.dbs.base_db_connection import BaseDBConnection

class SurgeryDBConnection(BaseDBConnection):
    def __init__(self):
        super().__init__()
        # Try and create the relevant table if it does not exist
        try:
            query = ("CREATE TABLE IF NOT EXISTS surgerydb ("
                     "surgery_location VARCHAR(255) PRIMARY KEY, "
                     "surgery_latitude DECIMAL(10,3), "
                     "surgery_longitude DECIMAL(10,3), "
                     "patient_count INT, "
                     "doctor_count INT,  "
                     "surgery_infection_status DECIMAL(10,3))")
            # set the surgery db up
            self.cursor.execute(query)
            self.cnx.commit()

        except self.connector.Error as err:
            print(err)

    def check_surgery(self, surgery_location):
        query = "SELECT * FROM surgerydb WHERE surgery_location = %s"
        self.cursor.execute(query, (surgery_location,))
        results = self.cursor.fetchall()
        return results

    def check_if_surgery_exists_create_one_if_it_does_not(self, surgery_details, surgery_infection_status):
        surgery_location = surgery_details[0]
        surgery_latitude = surgery_details[1]
        surgery_longitude = surgery_details[2]
        results = self.check_surgery(surgery_location)
        if len(results) == 0:
            patient_count = 0
            doctor_count = 0
            query = ("INSERT INTO surgerydb ("
                     "surgery_location, "
                     "surgery_latitude, "
                     "surgery_longitude, "
                     "patient_count, "
                     "doctor_count, "
                     "surgery_infection_status) "
                     "VALUES (%s, %s, %s, %s, %s, %s)")
            surgery_data = (
                surgery_location,
                surgery_latitude,
                surgery_longitude,
                patient_count,
                doctor_count,
                surgery_infection_status)
            self.cursor.execute(query, surgery_data)
            self.cnx.commit()

        else:
            patient_count = results[0]['patient_count']
            doctor_count = results[0]['doctor_count']

        return patient_count, doctor_count

    def add_to_patient_count(self, surgery_location):
        query = "UPDATE surgerydb SET patient_count = patient_count + 1 WHERE surgery_location = %s"
        self.cursor.execute(query, (surgery_location,))
        self.cnx.commit()

    def add_to_doctor_count(self, surgery_location):
        query = "UPDATE surgerydb SET doctor_count = doctor_count + 1 WHERE surgery_location = %s"
        self.cursor.execute(query, (surgery_location,))
        self.cnx.commit()

    def get_list_of_surgery_locations(self):
        query = "SELECT surgery_location FROM surgerydb"
        self.cursor.execute(query)
        results = [x['surgery_location'] for x in self.cursor.fetchall()]
        return results

    def get_surgery_infection_status(self, surgery_location):
        query = "SELECT surgery_infection_status FROM surgerydb WHERE surgery_location = %s"
        self.cursor.execute(query, (surgery_location,))
        results = [float(x['surgery_infection_status']) for x in self.cursor.fetchall()]
        return results[0]