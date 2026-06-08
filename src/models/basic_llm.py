import os
from ast import literal_eval
from openai import OpenAI

class BasicLLM():
    def __init__(self, ):
        self.client = OpenAI(base_url=os.environ['OLLAMA_IP'], api_key='ollama')
        self.model = 'llama3.2'

    def create_list_british_names_for_doctors(self, number_of_names):
        attempts = 0
        names = []
        while len(names) < number_of_names and attempts < 100:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[{'role': 'user', 'content': f'Give me a list of {number_of_names} British names (first and last) in the format of a python list with no other characters. Only output the list itself'}],
                    model=self.model,
                )
                results = literal_eval(chat_completion.choices[0].message.content)
                if isinstance(results, list):
                    for result in results:
                        try:
                            test_name = result.split(' ')
                            if len(test_name) == 2:
                                names.append(result)
                        except:
                            pass
                    names = list(set(names))
            except Exception as e:
                attempts += 1
                if attempts == 1:
                    print("generating doctor names")
                print(f'failed attempts {attempts}, names {len(names)}')

        return names