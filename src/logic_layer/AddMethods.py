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

    def addUser(self, username, password, first_name, last_name, user_type="service_engineer"):
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

    def addScooter(self, serial, brand, model, top_speed, battery, soc, soc_min, soc_max, lat, lon,
                   out_of_service, mileage, last_maint, in_service_date=datetime.time()):
    
        is_valid_flag = True

        if not str(top_speed).isdigit():
            print("Invalid input: top_speed (km/h) must be a whole number")
            is_valid_flag = False
        if not str(battery).isdigit():
            print("Invalid input: battery capacity (Wh) must be a whole number")
            is_valid_flag = False
        if not str(soc).isdigit():
            print("Invalid input: (Soc) State of Charge (%) must be a whole number")
            is_valid_flag = False
        if not str(soc_min).isdigit():
            print("Invalid input: minimum SoC must be a whole number")
            is_valid_flag = False
        if not str(soc_max).isdigit():
            print("Invalid input: maximum SoC must be a whole number")
            is_valid_flag = False
        if not str(lat).isdecimal():
            print("Invalid input: maximum SoC must be a decimal number")
            is_valid_flag = False
        if not str(lon).isdecimal():
            print("Invalid input: longitude must be a decimal number")
            is_valid_flag = False
        if not str(out_of_service).upper() in ("Y", "N"):
            print("Invalid input: out_of_service boolean must be either `Y` or `N`")
            is_valid_flag = False
        if not str(mileage).isdigit():
            print("Invalid input: mileage (km/h) must be a whole number")
            is_valid_flag = False
        
        if is_valid_flag:
            soc_range = ";".join(soc_min, soc_max)
            location = ";".join(lat, lon)

            scooter = Scooter(brand, model, serial, top_speed, battery, soc, soc_min, soc_max, lat, lon, out_of_service, mileage, last_maint, in_service_date)
            self.scooter_.add_scooter(scooter)
            print("Scooter added successfully.")
            return scooter
        return None

    def addTraveller(self, customer_id, fname, lname, bday, gender, street, house_num, zip, city, email, phone, license_num, registration_date):
        if customer_id == None: customer_id = str(uuid.uuid4())
        if registration_date == None: registration_date = datetime.datetime()

        traveller = Traveller(customer_id, fname, lname, bday, gender,
                            street, house_num, zip, city, email,
                            phone, license_num, registration_date)

        self.traveller_.add_traveller(traveller)
