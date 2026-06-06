import time
from src.services.symptoms import Symptoms
from src.services.appointment import Appointment
from src.models.diagnosis_agent import DiagnosisAgent
from src.dbs.patient_db_connection import PatientDBConnection
from src.dbs.diagnosis_db_connection import DiagnosisDBConnection
from src.dbs.appointment_db_connection import AppointmentDBConnection

class DiagnosisAgentSimulations():

    def __init__(self):
        self.appointment_service = Appointment()
        self.diagnosis_agent = DiagnosisAgent()
        self.symptom_service = Symptoms()

    def get_patient_record_for_appointment(self, appointment_id):
        appointment_db = AppointmentDBConnection()
        patient_db = PatientDBConnection()
        appointment_data = appointment_db.get_record_of_appointment(appointment_id)[0]
        patient_data = patient_db.get_record_of_patient(appointment_data['patient_id'])[0]

        # close open connection to db
        appointment_db.close()
        patient_db.close()

        return patient_data

    def get_diagnosis_agent_to_analyse_appointment(self, appointment_id):

        diagnosis_db = DiagnosisDBConnection()

        diagnosis = diagnosis_db.check_if_diagnosis_exist(appointment_id)

        diagnosis_attempts = 0

        if diagnosis != 'exist':
            appointment_data = self.appointment_service.get_appointment_history(appointment_id)
            actual_patient_symptom_list = self.symptom_service.get_list_of_symptoms_from_symptom_description(appointment_data[1])

            patient_data = self.get_patient_record_for_appointment(appointment_id)
            actual_patient_infection_status = patient_data['infection_status']

            inferred_patient_symptom_list = []
            while not inferred_patient_symptom_list and diagnosis_attempts < 5:
                self.diagnosis_agent.determine_symptoms_from_appointment_transcript(appointment_data[0])
                inferred_patient_symptom_list = self.diagnosis_agent.current_patient_symptom_list
                diagnosis_attempts += 1

            inferred_patient_infection_status = self.diagnosis_agent.given_list_of_symptoms_determine_chance_of_infection(inferred_patient_symptom_list)

            if inferred_patient_infection_status > 0.75:
                inferred_infection_status = 'infected'
            else:
                inferred_infection_status = 'not infected'

            diagnosis_summary = self.diagnosis_agent.summaries_diagnosis_of_patient(inferred_patient_symptom_list, inferred_infection_status)
            diagnosis_details = {
                'appointment_id': appointment_id,
                'actual_patient_symptom_list':actual_patient_symptom_list,
                'actual_patient_infection_status':actual_patient_infection_status,
                'inferred_patient_symptom_list':inferred_patient_symptom_list,
                'inferred_patient_infection_status':inferred_patient_infection_status,
                'diagnosis_summary':diagnosis_summary[:255]
            }

            diagnosis_db.add_record_of_diagnosis(diagnosis_details)

            # close open connection to db
            diagnosis_db.close()

        if diagnosis_attempts >= 5:
            print('Diagnosis failed')

    def run_through_all_appointments_and_diagnose(self):
        appointment_db = AppointmentDBConnection()
        list_of_appointments = appointment_db.select_list_of_all_undiagnosed_appointments()
        initial_start_time = time.time()
        appointment_tally_total = len(list_of_appointments)
        appointment_tally = 0
        for appointment_id in list_of_appointments:
            start_time = time.time()
            try:
                self.get_diagnosis_agent_to_analyse_appointment(appointment_id['appointment_id'])
            except Exception as e:
                print(e)
            appointment_tally +=1
            print('appointment {}/{} time taken to analyse appointment: {:.2f}. total time taken: {:.2f}'.format(appointment_tally, appointment_tally_total, time.time() - start_time, time.time() - initial_start_time))
