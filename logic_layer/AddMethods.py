from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data

from DataModels.ScooterModel import Scooter
from DataModels.TravellerModel import Traveller

from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter

import re, datetime, uuid

class AddDataService():
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()

    def addUser(self, username, password, first_name, last_name):
        hashed_salted = PasswordHasherSalter.hash_salt_password(password)
        added_user = self.user_.add_user(username, hashed_salted, first_name, last_name)
        print("User added successfully.") if added_user else "Oops, user couldn't be registered"
        return added_user

    def addScooter(self):
        serial = input("Serial Number: ").strip()
        brand = input("Brand: ").strip()
        model = input("Model: ").strip()
        top_speed = int(input("Top speed (km/h): "))
        battery = int(input("Battery capacity (Wh): "))
        soc = int(input("State of charge (%): "))
        soc_min = int(input("Min SoC: "))
        soc_max = int(input("Max SoC: "))
        lat = float(input("Latitude: "))
        lon = float(input("Longitude: "))
        out_of_service = input("Is out of service (y/n): ").lower() == 'y'
        mileage = float(input("Mileage (km): "))
        last_maint = input("Last maintenance date (YYYY-MM-DD): ")
        in_service_date = datetime.datetime()

        scooter = Scooter(brand, model, serial, top_speed, battery, soc, soc_min, soc_max, lat, lon, out_of_service, mileage, last_maint, in_service_date)
        self.scooter_.add_scooter(scooter)
        print("Scooter added successfully.")

    def addTraveller(self):
        customer_id = str(uuid.uuid4())
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        birthday = input("Birthday (YYYY-MM-DD): ")
        gender = input("Gender (male/female): ")
        street = input("Street name: ")
        number = int(input("House number: "))
        zip_code = input("Zip code (DDDDXX): ")
        city = input("City (must be in list): ")
        email = input("Email: ")
        phone = input("Phone (8 digits): ")
        license_number = input("Driving license (X/DDDDDDD): ")
        registration_date = datetime.datetime()

        traveller = Traveller(customer_id, first_name, last_name, birthday, gender,
                            street, number, zip_code, city, email,
                            phone, license_number, registration_date)

        self.traveller_.add_traveller(traveller)
        print("Traveller added successfully.")
