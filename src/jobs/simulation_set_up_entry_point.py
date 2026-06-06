import math
import random
from src.models.doctor import Doctor
from src.services.surgeries import Surgeries
from src.dbs.doctor_db_connection import DoctorDBConnection
from src.dbs.surgery_db_connection import SurgeryDBConnection

class SimulationSetUp():
    def __init__(self):
        self.surgeries = Surgeries()
        self.set_up_underlying_infection_model()

    def set_up_underlying_infection_model(self,
        infection_center_latitude = 52.5,
        infection_center_longitude = -1,
        infection_center_radius = 3):

        # Connect to relevant DBs
        surgery_db = SurgeryDBConnection()
        doctor_db = DoctorDBConnection()

        for surgery in self.surgeries.get_city_locations():

            # Calculate distance from epicenter of infection zone
            surgery_distance_to_infection_epicenter = math.sqrt((infection_center_latitude - surgery[1])**2 + (infection_center_longitude - surgery[2])**2)
            # Calculate the strength of the infection based on the distance to epicenter with a cut of infection defined by infection radius.
            surgery_infection_status = max((infection_center_radius - surgery_distance_to_infection_epicenter)/infection_center_radius, 0)

            surgery_db.check_if_surgery_exists_create_one_if_it_does_not(surgery, surgery_infection_status)
            for doctor_count_in_surgery in range(random.randint(5, 10)):
                surgery_db.add_to_doctor_count(surgery[0])
                new_doctor = Doctor(doctor_db)
                new_doctor.create_doctor_record(surgery[0])

        return surgery_db.get_list_of_surgery_locations()

if __name__ == '__main__':
    
    sim = SimulationSetUp()

    # Set up the underlying infection model defining the epicentre of the infection
    sim.set_up_underlying_infection_model(
        infection_center_latitude=52.5,
        infection_center_longitude=-1,
        infection_center_radius=3
    )


