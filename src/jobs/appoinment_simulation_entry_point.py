import time
from src.models.doctor import Doctor
from src.models.patient import Patient
from src.services.surgeries import Surgeries
from src.services.appointment import Appointment
from src.dbs.doctor_db_connection import DoctorDBConnection
from src.dbs.surgery_db_connection import SurgeryDBConnection
from src.dbs.patient_db_connection import PatientDBConnection
from src.dbs.appointment_db_connection import AppointmentDBConnection
from src.jobs.appointment_analysis_and_diagnosis import DiagnosisAgentSimulations

class AppointmentSimulations():
    def __init__(self):
        self.surgeries = Surgeries()
        self.appointment = Appointment()

    def create_patient_record(self):
        # Connect to relevant DBs
        surgery_db = SurgeryDBConnection()
        doctor_db = DoctorDBConnection()
        patient_db = PatientDBConnection()

        allocated_doctor = Doctor(doctor_db)
        allocated_doctor.select_doctor_record()

        surgery_db.add_to_patient_count(allocated_doctor.surgery_location)
        surgery_infection_rate = surgery_db.get_surgery_infection_status(allocated_doctor.surgery_location)
        patient = Patient(allocated_doctor, surgery_infection_rate, patient_db)

        # close open connection to db
        surgery_db.close()
        patient_db.close()

        return patient, allocated_doctor

    def run_single_simulation_of_appointment(self, patient, doctor):
        # Connect to relevant DBs
        appointment_db = AppointmentDBConnection()

        # Create the transcript for the appointment
        appointment_id = self.appointment.run_full_conversation(doctor, patient, appointment_db)

        # close open connection to db
        appointment_db.close()

        return appointment_id

    def run_full_simulation(self, number_of_appointments_to_simulate = 100):
        diagnosis_simulator = DiagnosisAgentSimulations()
        start_time_setup = time.time()

        print(f'Setup Complete in {time.time() - start_time_setup:.2f}s')
        start_time = time.time()
        for i in range(number_of_appointments_to_simulate):
            appointment_start_time = time.time()
            patient, doctor = sim.create_patient_record()
            appointment_id = sim.run_single_simulation_of_appointment(patient, doctor)
            appointment_end_time = time.time()
            appointment_duration = appointment_end_time - appointment_start_time

            diagnosis_start_time = time.time()
            try:
                diagnosis_simulator.get_diagnosis_agent_to_analyse_appointment(appointment_id)
            except Exception as e:
                print(e)
            diagnosis_duration = time.time() - diagnosis_start_time
            simulation_duration = time.time() - start_time
            print(
                f'Appointment Count: {i}, Appointment Duration: {appointment_duration:.2f}s, Diagnosis Duration: {diagnosis_duration:.2f}s, Simulation Duration: {simulation_duration:.2f}s')

if __name__ == '__main__':

    sim = AppointmentSimulations()

    # set up the simulation to run for the requirement number of appointments. NOTE: make sure that the
    # simulation has been set up correctly first using the Simulation Set Up.

    sim.run_full_simulation(
        number_of_appointments_to_simulate = 10
    )



