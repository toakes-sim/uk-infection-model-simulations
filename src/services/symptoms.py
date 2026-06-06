import pathlib
import json
import os
import random


class Symptoms():

    def __init__(self):
        self.get_list_of_symptoms_details()

    def get_list_of_symptoms_details(self):

        with open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'Symptom Book for Infectious Deseases.txt'), newline='') as f:
            raw_text_data = json.load(f)

        self.list_of_symptom_details = raw_text_data['list_of_all_known_symptoms']
        self.list_of_symptoms = [symptom['symptom_name'] for symptom in self.list_of_symptom_details]

    def get_symptom_details(self, symptom_name):
        return [symptom_information['symptom_description'] for symptom_information in self.list_of_symptom_details if symptom_information['symptom_name'] in symptom_name]

    def randomly_sample_symptom_given_infection_status(self, infection_status):

        symptom_likelihood_list = self.get_normalised_cumulative_symptom_likelihood_for_infected(infection_status)

        random_number_for_symptom_selection = random.uniform(0,1)

        current_symptom_index = 0
        current_symptom =  symptom_likelihood_list[current_symptom_index]
        current_symptom[1] = current_symptom[1]
        while random_number_for_symptom_selection > current_symptom[1]:
            current_symptom_index +=1
            current_symptom =  symptom_likelihood_list[current_symptom_index]
            current_symptom[1] = current_symptom[1]

        return current_symptom[0]

    def get_normalised_cumulative_symptom_likelihood_for_infected(self, infection_status):
        if infection_status == 'infected':
            symptom_status = 'symptom_occurrence_rate_if_infected'
        else:
            symptom_status = 'symptom_occurrence_rate_if_not_infected'

        symptom_likelihood_list = []
        total_symptom_likelihood = 0
        for symptom in self.list_of_symptom_details:
            if symptom[symptom_status] != 0:
                total_symptom_likelihood += symptom[symptom_status]
                symptom_likelihood_list.append([symptom['symptom_name'], total_symptom_likelihood])
        symptom_likelihood_list_normalised = [[x[0], x[1]/total_symptom_likelihood] for x in symptom_likelihood_list]

        return symptom_likelihood_list_normalised

    def get_normalised_symptom_likelihood_for_infected(self, infection_status):
        if infection_status == 'infected':
            symptom_status = 'symptom_occurrence_rate_if_infected'
        else:
            symptom_status = 'symptom_occurrence_rate_if_not_infected'

        symptom_likelihood_list = []
        total_symptom_likelihood = 0
        for symptom in self.list_of_symptom_details:
            if symptom[symptom_status] != 0:
                total_symptom_likelihood += symptom[symptom_status]
                symptom_likelihood_list.append([symptom['symptom_name'], symptom[symptom_status]])
        symptom_likelihood_list_normalised = [[x[0], x[1]/total_symptom_likelihood] for x in symptom_likelihood_list]

        return symptom_likelihood_list_normalised

    def get_list_of_symptoms_from_symptom_description(self, list_of_symptom_description):
        symptom_list = []
        for symptom_details in self.list_of_symptom_details:
            if symptom_details['symptom_description'] in list_of_symptom_description:
                symptom_list.append(symptom_details['symptom_name'])

        return symptom_list
