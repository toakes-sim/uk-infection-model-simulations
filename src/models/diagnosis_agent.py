import os
import ast
from openai import OpenAI
from src.services.symptoms import Symptoms

class DiagnosisAgent:
    def __init__(self):
        self.symptom_service = Symptoms()
        self.client = OpenAI(base_url=os.environ['OLLAMA_IP'], api_key='ollama')
        self.model = 'llama3-groq-tool-use'
        self.temperature = 0.2
        self.get_symptom_likelihood()
        self.set_prompt_parameters()
        self.get_list_of_agent_tools()

    def get_symptom_likelihood(self):

        self.normalised_likelihood_of_symptom_if_infected = {item[0]: item[1] for item in self.symptom_service.get_normalised_symptom_likelihood_for_infected('infected')}
        self.normalised_likelihood_of_symptom_if_not_infected = {item[0]: item[1] for item in self.symptom_service.get_normalised_symptom_likelihood_for_infected('not infected')}

    def set_prompt_parameters(self):

        prompt = '''
        You are a doctor in a UK based GP surgery who's job it is to read transcripts of appointment between a patients and 
        doctors and identify what symptoms are discussed. There is a potential infection going around the UK. 
        '''

        self.diagnosis_agent_system_prompt = {'role': 'system', 'content': prompt}

    def handel_tool_cals(self, message):
        responses = []
        try:
            for tool_call in message.tool_calls:
                if tool_call.function.name == "add_patient_symptom_to_list":
                    arguments = ast.literal_eval(tool_call.function.arguments)
                    symptoms = arguments.get('symptoms')
                    add_symptom_to_list = self.add_patient_symptom_to_list(symptoms)
                    responses.append({"role": "tool", "content": add_symptom_to_list, "tool_call_id": tool_call.id})

            return responses
        except:
            return "tool call failed"

    def get_list_of_agent_tools(self):
        add_symptom = {
            "type": "function",
            "name": "add_patient_symptom_to_list",
            "description": "Store symptoms found in patient transcript.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symptoms": {
                        "type": "string",
                        "description": "A full list of symptoms mentioned in the transcript from the list of possible symptoms, e.g. Sneezing",
                        "enum": self.symptom_service.list_of_symptoms
                    },
                },
                "required": ["symptoms"],
            }
        }

        self.list_of_tools = [{"type": "function", "function": add_symptom}]

    def add_patient_symptom_to_list(self, identified_symptoms):
        tool_response = ""

        if isinstance(identified_symptoms, list):
            for symptom in identified_symptoms:
                if symptom in self.current_patient_symptom_list:
                    tool_response += f"Patient symptom {symptom} is identified. "
                elif symptom in self.symptom_service.list_of_symptoms:
                    tool_response += f"Added patient symptom {symptom} to list of symptoms. Continue to check for more symptoms. "
                    self.current_patient_symptom_list.append(symptom)
        return tool_response

    def determine_symptoms_from_appointment_transcript(self, appointment_transcript):

        self.current_patient_symptom_list = []

        prompt = '''
        I am about to give you an appointment transcript. Using the list of symptoms you know try and identify 
        which symptoms are present in the transcript and store the symptoms using a tool. Make a note of any identified symptoms with a tool. 
        The transcript is as follows: 
        '''

        prompt += str(appointment_transcript)

        prompt += f' make sure the symptoms you send to the tool are from the symptom list {str(self.symptom_service.list_of_symptoms)}'

        messages = [self.diagnosis_agent_system_prompt, {'role': 'user', 'content': prompt}]

        response = self.client.chat.completions.create(messages=messages, model=self.model, temperature=self.temperature, tools=self.list_of_tools)

        while response.choices[0].finish_reason == 'tool_calls':
            message = response.choices[0].message
            responses = self.handel_tool_cals(message)
            messages.append(message)
            messages.extend(responses)
            response = self.client.chat.completions.create(messages=messages, model=self.model, temperature=self.temperature, tools=self.list_of_tools)

        chat_output = response.choices[0].message.content

        return chat_output

    def determine_chance_of_infection_given_list_of_symptoms(self, patient_symptom_list):

        product_of_probability_of_infected = 1
        product_of_probability_of_not_infected = 1

        for symptom in patient_symptom_list:

            product_of_probability_of_infected *= self.normalised_likelihood_of_symptom_if_infected.get(symptom, 0)
            product_of_probability_of_not_infected *= self.normalised_likelihood_of_symptom_if_not_infected.get(symptom, 0)

        normalised_probability_of_being_infected = product_of_probability_of_infected/(product_of_probability_of_infected + product_of_probability_of_not_infected)

        return normalised_probability_of_being_infected

    def summaries_diagnosis_of_patient(self, list_of_inferred_symptoms, inferred_infection_status):

        prompt = f'Please summaries in a few short sentences (up to 400 characters) the diagnosis of this patient where the identified symptoms are {list_of_inferred_symptoms}, '

        prompt += f'and the patient is deemed to be {inferred_infection_status}.'

        messages = [self.diagnosis_agent_system_prompt, {'role': 'user', 'content': prompt}]

        response = self.client.chat.completions.create(messages=messages, model=self.model, temperature=self.temperature, tools=self.list_of_tools)

        return response.choices[0].message.content

