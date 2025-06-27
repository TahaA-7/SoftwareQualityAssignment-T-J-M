from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data

from DataModels.ScooterModel import Scooter
from DataModels.TravellerModel import Traveller

from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter

from presentation_layer.menus.RegisterMenu import RegisterMenu 

import re, datetime, uuid

class AddDataService():
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()
        self.registerMenu_ = RegisterMenu()

    def get_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a whole number.")

    def get_float(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a number.")

    def addUser(self, username, password, first_name, last_name):
        hashed_salted = PasswordHasherSalter.hash_salt_password(password)
        added_user = self.user_.add_user(username, hashed_salted, first_name, last_name)
        print("User added successfully.") if added_user else "Oops, user couldn't be registered"
        return added_user
    
    def addSystemAdmin(self):
        username = self.registerMenu_.handle_username()
        password = self.registerMenu_.handle_password()
        first_name = self.registerMenu_.handle_first_name_submit()
        last_name = self.registerMenu_.handle_last_name_submit()

        hashed_salted = PasswordHasherSalter.hash_salt_password(password)

        self.user_.add_systemAdmin(username, hashed_salted, first_name, last_name)
        print("User added successfully.")

    def addServiceEngineer(self):
        username = self.registerMenu_.handle_username()
        password = self.registerMenu_.handle_password()
        first_name = self.registerMenu_.handle_first_name_submit()
        last_name = self.registerMenu_.handle_last_name_submit()

        hashed_salted = PasswordHasherSalter.hash_salt_password(password)

        self.user_.add_serviceEngineer(username, hashed_salted, first_name, last_name)
        print("User added successfully.")

    def addScooter(self):
        serial = input("Serial Number: ").strip()
        brand = input("Brand: ").strip()
        model = input("Model: ").strip()
        top_speed = self.get_int("Top speed (km/h): ")
        battery = self.get_int("Battery capacity (Wh): ")
        soc = self.get_int("State of charge (%): ")
        soc_min = self.get_int("Min SoC: ")
        soc_max = self.get_int("Max SoC: ")
        lat = self.get_float("Latitude: ")
        lon = self.get_float("Longitude: ")
        out_of_service = input("Is out of service (y/n): ").lower() == 'y'
        mileage = self.get_float("Mileage (km): ")
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
        number = self.get_int("House number: ")
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
