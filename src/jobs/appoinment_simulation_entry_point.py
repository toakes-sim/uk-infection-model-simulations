import time
from src.endpoints.endpoint_for_services import EndpointForServices

class AppointmentSimulations():
    def __init__(self):
        self.endpoints = EndpointForServices()

    def run_full_simulation(self, number_of_appointments_to_simulate=100):
        start_time = time.time()
        for i in range(number_of_appointments_to_simulate):
            appointment_start_time = time.time()
            patient, doctor = self.endpoints.create_patient_record()
            appointment_id = self.endpoints.run_single_simulation_of_appointment(patient, doctor)
            appointment_end_time = time.time()
            appointment_duration = appointment_end_time - appointment_start_time

            diagnosis_start_time = time.time()
            try:
                self.endpoints.get_diagnosis_agent_to_analyse_appointment(appointment_id)
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
        number_of_appointments_to_simulate = 1
    )



