import os
from openai import OpenAI
from src.endpoints.endpoint_for_databases import EndpointForDatabases

class Doctor:
    def __init__(self):
        self.client = OpenAI(base_url=os.environ['OLLAMA_IP'], api_key='ollama')
        self.model = 'llama3.2'
        self.endpoints = EndpointForDatabases()

    def set_doctor_name(self, name):
        self.name = name

    def set_other_prompt_parameters(self):
        self.doctor_system_prompt = {'role': 'system', 'content': self.persona}
        self.doctor_final_system_prompt = {'role': 'system',
                                           'content': self.persona + ' This is the last response before the end of the appointment. The patient will respond one final time.'}

    def create_doctor_record(self, surgery_location):
        self.persona = 'You are a doctor working in the Uk. You have some patients coming to see you with various ailments. You must diagnose them quickly.'
        self.surgery_location = surgery_location
        self.doctor_id = self.endpoints.add_record_of_doctor_to_db(self.surgery_location, self.persona, self.name)
        self.set_other_prompt_parameters()

    def select_doctor_record(self):
        self.doctor_id, self.surgery_location, self.persona = self.endpoints.get_random_record_of_doctor()
        self.set_other_prompt_parameters()

    def doctor_message_history(self, message_history, final_response = False):
        doctor_history = []
        for entry in message_history:
            if entry['role'] == 'system':
                if final_response:
                    doctor_history.append(self.doctor_final_system_prompt)
                else:
                    doctor_history.append(self.doctor_system_prompt)
            elif entry['role'] == 'user':
                doctor_history.append({'role':'assistant', 'content': entry['content']})
            elif entry['role'] == 'assistant':
                doctor_history.append({'role':'user', 'content': entry['content']})
        return doctor_history

    def submit_requests(self, message_history):

        chat_completion = self.client.chat.completions.create(
            messages=self.doctor_message_history(message_history),
            model=self.model,
        )
        return [*message_history, {'role': 'user', 'content': chat_completion.choices[0].message.content}]

    def submit_final_request(self, message_history):

        chat_completion = self.client.chat.completions.create(
            messages=self.doctor_message_history(message_history, True),
            model=self.model,
        )
        return [*message_history, {'role': 'user', 'content': chat_completion.choices[0].message.content}]
