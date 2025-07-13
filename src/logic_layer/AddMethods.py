from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data

from DataModels.ScooterModel import Scooter
from DataModels.TravellerModel import Traveller

from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter

from presentation_layer.utils.Roles import Roles
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

    def addUser(self, username, password, first_name, last_name, user_type=Roles.SERVICE_ENGINEER.value):
        if any(not field.strip() for field in [username, password, first_name, last_name]):
            return None
        id = str(uuid.uuid4())
        hashed_salted = PasswordHasherSalter.hash_salt_password(password)
        added_user = self.user_.add_user(id, username, hashed_salted, first_name, last_name, user_type)
        # print("User added successfully.") if added_user else "Oops, user couldn't be registered"
        return added_user
    
    def addSystemAdmin(self):
        # username = self.registerMenu_.handle_username()
        # password = self.registerMenu_.handle_password()
        # first_name = self.registerMenu_.handle_first_name_submit()
        # last_name = self.registerMenu_.handle_last_name_submit()

        # hashed_salted = PasswordHasherSalter.hash_salt_password(password)

        # self.user_.add_systemAdmin(username, hashed_salted, first_name, last_name)
        # print("User added successfully.")
        pass

    def addServiceEngineer(self):
        # username = self.registerMenu_.handle_username()
        # password = self.registerMenu_.handle_password()
        # first_name = self.registerMenu_.handle_first_name_submit()
        # last_name = self.registerMenu_.handle_last_name_submit()

        # hashed_salted = PasswordHasherSalter.hash_salt_password(password)

        # self.user_.add_serviceEngineer(username, hashed_salted, first_name, last_name)
        # print("User added successfully.")
        pass

    def addScooter(self, serial, brand, model, top_speed, battery, soc, soc_min, soc_max, lat, lon,
                   out_of_service, mileage, last_maint, in_service_date=None):
    
        if out_of_service in (None, "", " "):
            out_of_service = False

        # Validate all required string fields
        string_fields = [serial, brand, model]
        if any(not isinstance(field, str) or not field.strip() for field in string_fields):
            print("Invalid string field")
            return None

        # Validate required numeric/boolean fields
        numeric_fields = [top_speed, battery, soc, soc_min, soc_max, lat, lon, out_of_service, mileage]
        if any(field is None for field in numeric_fields):
            print("Invalid numeric field")
            return None

        if in_service_date is None:
            in_service_date = datetime.date.today()

        is_valid_flag = True

        # if not str(top_speed).isdigit():
        #     print("Invalid input: top_speed (km/h) must be a whole number")
        #     is_valid_flag = False
        # if not str(battery).isdigit():
        #     print("Invalid input: battery capacity (Wh) must be a whole number")
        #     is_valid_flag = False
        # if not str(soc).isdigit():
        #     print("Invalid input: (Soc) State of Charge (%) must be a whole number")
        #     is_valid_flag = False
        # if not str(soc_min).isdigit():
        #     print("Invalid input: minimum SoC must be a whole number")
        #     is_valid_flag = False
        # if not str(soc_max).isdigit():
        #     print("Invalid input: maximum SoC must be a whole number")
        #     is_valid_flag = False
        # if not str(lat).isdecimal():
        #     print("Invalid input: maximum SoC must be a decimal number")
        #     is_valid_flag = False
        # if not str(lon).isdecimal():
        #     print("Invalid input: longitude must be a decimal number")
        #     is_valid_flag = False
        # if not str(out_of_service).upper() in ("Y", "N"):
        #     print("Invalid input: out_of_service boolean must be either `Y` or `N`")
        #     is_valid_flag = False
        # if not str(mileage).isdigit():
        #     print("Invalid input: mileage (km/h) must be a whole number")
        #     is_valid_flag = False
        
        if is_valid_flag:
            soc_range = ";".join((soc_min, soc_max))
            # location = ";".join((str(lat), str(lon)))

            scooter = Scooter(serial, model, brand, top_speed, battery, soc, soc_min, soc_max, lat, lon, out_of_service, mileage, last_maint, in_service_date)
            return self.scooter_.add_scooter(scooter)
        return None

    def addTraveller(self, customer_id, registration_date, fname, lname, bday, gender, street, house_num, zip, city, email, phone, license_num):
        if any(not str(field).strip() for field in [fname, lname, gender, street, house_num, zip, city, email, phone, license_num]):
            return None
        # if not isinstance(bday, datetime.date):
        #     return None
        if customer_id == None: customer_id = str(uuid.uuid4())
        if registration_date == None: registration_date = datetime.date.today()

        traveller = Traveller(customer_id, registration_date, fname, lname, bday, gender,
                            street, house_num, zip, city, email,
                            phone, license_num)

        return self.traveller_.add_traveller(traveller)
