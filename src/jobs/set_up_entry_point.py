from random import choice, randint
from src.endpoints.endpoint_for_services import EndpointForServices

class SimulationSetUp():
    def __init__(self):
        self.endpoints = EndpointForServices()

    def set_up_underlying_infection_model(self,
                                          infection_center_latitude=52.5,
                                          infection_center_longitude=-1,
                                          infection_center_radius=3):
        # set the epicentre of infection
        epicentre_details = {'infection_center_latitude':infection_center_latitude,
                             'infection_center_longitude':infection_center_longitude,
                             'infection_center_radius':infection_center_radius}

        # create list of names
        doctor_name_list = self.endpoints.create_list_british_names_for_doctors(200)

        # get list of all surgery locations
        surgery_locations = self.endpoints.get_list_of_surgery_locations()

        for surgery in surgery_locations:

            self.endpoints.check_if_surgery_exists_create_one_if_it_does_not(surgery, epicentre_details)

            for doctor_count_in_surgery in range(randint(5, 10)):
                self.endpoints.create_doctor_record(surgery[0], choice(doctor_name_list))

        return self.endpoints.get_list_of_surgery_locations()



if __name__ == '__main__':
    
    sim = SimulationSetUp()

    # Set up the underlying infection model defining the epicentre of the infection
    sim.set_up_underlying_infection_model(
        infection_center_latitude=52.5,
        infection_center_longitude=-1,
        infection_center_radius=3
    )


