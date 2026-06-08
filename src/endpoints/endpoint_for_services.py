import time
import math
from src.models.doctor import Doctor
from src.models.patient import Patient
from src.models.basic_llm import BasicLLM
from src.services.symptoms import Symptoms
from src.services.surgeries import Surgeries
from src.services.appointment import Appointment
from src.models.diagnosis_agent import DiagnosisAgent
from src.endpoints.endpoint_for_databases import EndpointForDatabases


class EndpointForServices():
    def __init__(self):
        self.symptom_service = Symptoms()
        self.surgery_service = Surgeries()
        self.appointment_service = Appointment()
        self.endpoints = EndpointForDatabases()
        self.basic_llm = BasicLLM()

    def create_list_british_names_for_doctors(self, number_of_names = 200):
        return self.basic_llm.create_list_british_names_for_doctors(number_of_names)

    def get_list_of_surgery_locations(self):
        return self.surgery_service.get_city_locations()

    def check_if_surgery_exists_create_one_if_it_does_not(self, surgery, epicentre_details):
        # Calculate distance from epicenter of infection zone
        surgery_distance_to_infection_epicenter = math.sqrt(
            (epicentre_details['infection_center_latitude'] - surgery[1]) ** 2 + (epicentre_details['infection_center_longitude'] - surgery[2]) ** 2)
        # Calculate the strength of the infection based on the distance to epicenter with a cut of infection defined by infection radius.
        surgery_infection_status = max(
            (epicentre_details['infection_center_radius'] - surgery_distance_to_infection_epicenter) / epicentre_details['infection_center_radius'], 0)
        self.endpoints.check_if_surgery_exists_create_one_if_it_does_not(surgery, surgery_infection_status)

    def create_doctor_record(self, surgery, doctor_name):
        new_doctor = Doctor()
        new_doctor.set_doctor_name(doctor_name.split(' '))
        new_doctor.create_doctor_record(surgery)
        self.endpoints.add_to_doctor_count_to_db(surgery[0])

    def create_patient_record(self):

        allocated_doctor = Doctor()
        allocated_doctor.select_doctor_record()

        self.endpoints.add_to_patient_count_to_db(allocated_doctor.surgery_location)
        surgery_infection_rate = self.endpoints.get_surgery_infection_status(allocated_doctor.surgery_location)
        patient = Patient(allocated_doctor, surgery_infection_rate)

        return patient, allocated_doctor

    def run_single_simulation_of_appointment(self, patient, doctor):

        # Create the transcript for the appointment
        appointment_id = self.appointment_service.run_full_conversation(doctor, patient)
        print(appointment_id)
        return appointment_id

    def get_diagnosis_agent_to_analyse_appointment(self, appointment_id):

        diagnosis_agent = DiagnosisAgent()
        diagnosis = self.endpoints.check_if_diagnosis_exist(appointment_id)
        diagnosis_attempts = 0

        if diagnosis != 'exist':
            appointment_data = self.appointment_service.get_appointment_history(appointment_id)
            actual_patient_symptom_list = self.symptom_service.get_list_of_symptoms_from_symptom_description(appointment_data[1])

            patient_data = self.appointment_service.get_patient_record_for_appointment(appointment_id)
            actual_patient_infection_status = patient_data['infection_status']

            inferred_patient_symptom_list = []
            while not inferred_patient_symptom_list and diagnosis_attempts < 5:
                diagnosis_agent.determine_symptoms_from_appointment_transcript(appointment_data[0])
                inferred_patient_symptom_list = diagnosis_agent.current_patient_symptom_list
                diagnosis_attempts += 1

            inferred_patient_infection_status = diagnosis_agent.determine_chance_of_infection_given_list_of_symptoms(inferred_patient_symptom_list)

            if inferred_patient_infection_status > 0.75:
                inferred_infection_status = 'infected'
            else:
                inferred_infection_status = 'not infected'

            diagnosis_summary = diagnosis_agent.summaries_diagnosis_of_patient(inferred_patient_symptom_list, inferred_infection_status)
            diagnosis_details = {
                'appointment_id': appointment_id,
                'actual_patient_symptom_list':actual_patient_symptom_list,
                'actual_patient_infection_status':actual_patient_infection_status,
                'inferred_patient_symptom_list':inferred_patient_symptom_list,
                'inferred_patient_infection_status':inferred_patient_infection_status,
                'diagnosis_summary':diagnosis_summary[:255]
            }
            print(diagnosis_details)

            self.endpoints.add_record_of_diagnosis_to_db(diagnosis_details)

        if diagnosis_attempts >= 5:
            print('Diagnosis failed')

    def run_through_all_appointments_and_diagnose(self):
        list_of_appointments = self.endpoints.get_list_of_all_undiagnosed_appointments()
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
