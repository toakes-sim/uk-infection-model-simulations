from src.dbs.base_db_connection import BaseDBConnection

class DiagnosisDBConnection(BaseDBConnection):
    def __init__(self):
        super().__init__()
        # Try and create the relevant table if it does not exist
        try:
            query = ("CREATE TABLE IF NOT EXISTS diagnosisdb ("
                     "appointment_id VARCHAR(255) PRIMARY KEY, "
                     "actual_patient_symptom_list VARCHAR(255), "
                     "actual_patient_infection_status VARCHAR(255), "
                     "inferred_patient_symptom_list VARCHAR(255), "
                     "inferred_patient_infection_status VARCHAR(255), "
                     "diagnosis_summary VARCHAR(510))")
            # set the diagnosis db up
            self.cursor.execute(query)

            self.cnx.commit()

        except self.connector.Error as err:
            print(err)

    def add_record_of_diagnosis(self, diagnosis_details):
        query = ("INSERT INTO diagnosisdb ("
                 "appointment_id, "
                 "actual_patient_symptom_list, "
                 "actual_patient_infection_status, "
                 "inferred_patient_symptom_list, "
                 "inferred_patient_infection_status, "
                 "diagnosis_summary) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        diagnosis_data = (diagnosis_details['appointment_id'],
                          str(diagnosis_details['actual_patient_symptom_list']),
                          diagnosis_details['actual_patient_infection_status'],
                          str(diagnosis_details['inferred_patient_symptom_list']),
                          diagnosis_details['inferred_patient_infection_status'],
                          diagnosis_details['diagnosis_summary'])
        self.cursor.execute(query, diagnosis_data)
        self.cnx.commit()

    def check_if_diagnosis_exist(self, appointment_id):
        query = "SELECT * FROM diagnosisdb WHERE appointment_id = %s"
        self.cursor.execute(query, (appointment_id,))
        results = self.cursor.fetchall()
        if len(results) > 0:
            return 'exist'
        else:
            return 'deos not exist'