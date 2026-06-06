import pgeocode
import pathlib
import csv
import os

class Surgeries():

    def __init__(self):
        self.cities = self.get_city_locations()

    def get_city_locations(self):

        nomi = pgeocode.Nominatim('gb')

        with open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'uk-cities.csv'), newline='') as f:
            reader = csv.reader(f)
            raw = list(reader)
            data = [x[0] for x in raw]
        return [[x, *nomi.query_location(x).values[0][9:11].tolist()] for x in data]


