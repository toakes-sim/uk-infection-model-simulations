from src.dbs.doctor_db_connection import DoctorDBConnection
from src.dbs.surgery_db_connection import SurgeryDBConnection
from src.dbs.patient_db_connection import PatientDBConnection
from src.dbs.diagnosis_db_connection import DiagnosisDBConnection
from src.dbs.appointment_db_connection import AppointmentDBConnection

class EndpointForDatabases():
    def __init__(self):
        pass

    def add_to_doctor_count_to_db(self, surgery):
        surgery_db = SurgeryDBConnection()
        surgery_db.add_to_doctor_count(surgery)
        surgery_db.close()

    def add_to_patient_count_to_db(self, surgery_location):
        surgery_db = SurgeryDBConnection()
        surgery_db.add_to_patient_count(surgery_location)
        surgery_db.close()

    def add_record_of_diagnosis_to_db(self, diagnosis_details):
        diagnosis_db = DiagnosisDBConnection()
        diagnosis_db.add_record_of_diagnosis(diagnosis_details)
        diagnosis_db.close()

    def add_record_of_patient_to_db(self, surgery_location, doctor_id, patient_age, persona, infection_status):
        patient_db = PatientDBConnection()
        patient_id = patient_db.add_record_of_patient(surgery_location,
                                              doctor_id,
                                              patient_age,
                                              persona,
                                              infection_status)
        patient_db.close()
        return patient_id

    def add_record_of_doctor_to_db(self, surgery_location, persona, name):
        doctors_db = DoctorDBConnection()
        doctor_id = doctors_db.add_record_of_doctor(surgery_location, persona, name)
        doctors_db.close()
        return doctor_id

    def add_record_of_appointment_to_db(self, patient_id, doctor_id, surgery_location):
        appointment_db = AppointmentDBConnection()
        appointment_id = appointment_db.add_record_of_appointment(patient_id, doctor_id, surgery_location)
        appointment_db.close()
        return appointment_id

    def get_random_record_of_doctor(self):
        doctors_db = DoctorDBConnection()
        doctor_id, surgery_location, persona = doctors_db.get_random_record_of_doctor()
        doctors_db.close()
        return doctor_id, surgery_location, persona

    def get_surgery_infection_status(self, surgery_location):
        surgery_db = SurgeryDBConnection()
        surgery_infection_rate = surgery_db.get_surgery_infection_status(surgery_location)
        surgery_db.close()
        return surgery_infection_rate

    def get_record_of_appointment(self, appointment_id):
        appointment_db = AppointmentDBConnection()
        appointment_data = appointment_db.get_record_of_appointment(appointment_id)[0]
        appointment_db.close()
        return appointment_data

    def get_list_of_all_undiagnosed_appointments(self):
        appointment_db = AppointmentDBConnection()
        list_of_appointments = appointment_db.select_list_of_all_undiagnosed_appointments()
        appointment_db.close()
        return list_of_appointments

    def get_record_of_patient(self, patient_id):
        patient_db = PatientDBConnection()
        patient_data = patient_db.get_record_of_patient(patient_id)[0]
        patient_db.close()
        return patient_data

    def check_if_diagnosis_exist(self, appointment_id):
        diagnosis_db = DiagnosisDBConnection()
        diagnosis = diagnosis_db.check_if_diagnosis_exist(appointment_id)
        diagnosis_db.close()
        return diagnosis

    def check_if_surgery_exists_create_one_if_it_does_not(self, surgery, surgery_infection_status):
        surgery_db = SurgeryDBConnection()
        surgery_db.check_if_surgery_exists_create_one_if_it_does_not(surgery, surgery_infection_status)
        surgery_db.close()

