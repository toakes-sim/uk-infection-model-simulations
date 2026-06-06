import os
import random
from math import floor
from openai import OpenAI
from src.services.symptoms import Symptoms

class Patient():
    def __init__(self, allocated_doctor, surgery_infection_rate, patient_db):
        self.client = OpenAI(base_url=os.environ['OLLAMA_IP'], api_key='ollama')
        self.model = 'llama3.2'
        self.patient_db = patient_db
        self.create_patient_record(allocated_doctor, surgery_infection_rate)

    def create_patient_persona(self, patient_symptom_list, symptoms_service):
        base_context = 'You are a patient going to the doctor. You have a list of symptoms as follows:'
        for patient_symptom in patient_symptom_list:
            base_context = base_context + f'\n{symptoms_service.get_symptom_details(patient_symptom)[0]}'

        if "Ears fall off" in patient_symptom_list:
            base_context = base_context + '\nYou are extremely worried you may have been infected by a deadly virus'
        elif "Red Ear Boils" in patient_symptom_list or "Coughing Blood" in patient_symptom_list:
            base_context = base_context + '\nYou are very worried you may have been infected by a virus going around'
        else:
            base_context = base_context + '\nYou are worried you may have picked something up'

        return base_context

    def create_patient_record(self, allocated_doctor, surgery_infection_rate):

        patient_age = random.randint(20, 80)
        age_risk_factor = floor(patient_age/10)

        random_number_for_infection_status = random.uniform(0,1)
        if random_number_for_infection_status*age_risk_factor < surgery_infection_rate:
            infection_status = 'infected'
        else:
            infection_status = 'uninfected'

        symptoms_service = Symptoms()
        patient_symptom_list = []

        for symptom_count in range(random.randint(1,4)):
            patient_symptom_list.append(symptoms_service.randomly_sample_symptom_given_infection_status(infection_status))

        patient_symptom_list = list(set(patient_symptom_list))

        self.persona = self.create_patient_persona(patient_symptom_list, symptoms_service)

        self.patient_id = self.patient_db.add_record_of_patient(allocated_doctor.surgery_location,
                                              allocated_doctor.doctor_id,
                                              patient_age,
                                              self.persona,
                                              infection_status)

    def submit_initial_request(self):

        patient_system_prompt = {'role': 'system', 'content': self.persona}
        initial_prompt_default_from_doctor = {'role': 'user', 'content': 'How can I help you today?'}

        message_history = [patient_system_prompt , initial_prompt_default_from_doctor]

        chat_completion = self.client.chat.completions.create(
            messages=message_history,
            model=self.model,
        )
        message_history = [*message_history, {'role':'assistant','content': chat_completion.choices[0].message.content}]

        return message_history

    def submit_further_requests(self, message_history):
        chat_completion = self.client.chat.completions.create(
            messages=message_history,
            model=self.model,
        )
        message_history = [*message_history, {'role':'assistant','content': chat_completion.choices[0].message.content}]

        return message_history
