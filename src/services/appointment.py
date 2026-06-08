import os
import ast
import pathlib
from src.endpoints.endpoint_for_databases import EndpointForDatabases

class Appointment():
    def __init__(self):
        self.storage_location = os.environ['STORAGE_LOCATION']
        self.endpoints = EndpointForDatabases()

    def run_full_conversation(self, doctor, patient):

        surgery_location = doctor.surgery_location

        message_history = patient.submit_initial_request()
        for i in range(2):
            message_history = doctor.submit_requests(message_history)
            message_history = patient.submit_further_requests(message_history)

        message_history = doctor.submit_final_request(message_history)

        appointment_id = self.endpoints.add_record_of_appointment_to_db(patient.patient_id, doctor.doctor_id, surgery_location)

        with open(f'{self.storage_location}/appointment_{appointment_id}.txt', 'w') as f:
            for line in message_history:
                f.write(f"{line}\n")

        return appointment_id

    def get_appointment_history(self, appointment_id):
        with open(f'{self.storage_location}/appointment_{appointment_id}.txt', 'r') as f:
            transcript = f.read()
            f.close()
            transcript = transcript.split('\n')
            patient_prompt = transcript[0]
            patient_prompt = ast.literal_eval(patient_prompt)['content'].split('\n')[1:-1]
            transcript = transcript[1:-1]
            readable_transcript = []
            for i in range(len(transcript)):
                if i % 2 == 0:
                    readable_transcript.append({"speaker": "Doctor", "text": f"{transcript[i][29:-2]}"})
                else:
                    readable_transcript.append({"speaker": "Patient", "text": f"{transcript[i][34:-2]}"})

        return [readable_transcript, patient_prompt]

    def get_patient_record_for_appointment(self, appointment_id):
        appointment_data = self.endpoints.get_record_of_appointment(appointment_id)
        patient_data = self.endpoints.get_record_of_patient(appointment_data['patient_id'])
        return patient_data