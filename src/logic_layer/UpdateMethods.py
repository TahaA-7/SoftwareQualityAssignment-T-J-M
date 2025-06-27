from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data
from access_layer.db.UserData import user_data

from DataModels.ScooterModel import Scooter

from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter

from datetime import datetime

import hashlib

class UpdateDataService:
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()
        self.user_data = user_data()

    def updateUser_profile(self):
        username = input("Username to update: ").strip()

        for user in self.user_.get_all_users():
            if user[0].lower() == username.lower() and user[1].lower() == "service_engineer":
                first_name = input("New first name: ").strip()
                last_name = input("New last name: ").strip()
                self.user_.update_user_profile(username, first_name, last_name)
                print("User profile updated.")
                return

        print("No Service engineer with that username.")

    def update_SystemAdmin(self):
        username = input("Username to update: ").strip()

        for user in self.user_.get_all_users():
            if user[0].lower() == username.lower() and user[1].lower() == "system_admin":
                first_name = input("New first name: ").strip()
                last_name = input("New last name: ").strip()
                self.user_.update_user_profile(username, first_name, last_name)
                print("User profile updated.")
                return

        print("No System Administrator with that username.")


    def updateUser_password(self, username, password):
        hashed_salted = PasswordHasherSalter.hash_salt_password(password)
        is_updated_bool = self.user_.update_user_password(username, hashed_salted)
        return is_updated_bool

    def updateTraveller(self):
        customer_id = input("Traveller ID: ").strip()
        field = input("Which field to update (first_name, email, city, etc.): ").strip()
        new_value = input("New value: ").strip()
        allowed_fields = [
            'first_name', 'last_name', 'birthday', 'gender',
            'street_name', 'house_number', 'zip_code', 'city',
            'email', 'mobile_phone', 'driving_license_number'
        ]
        if field not in allowed_fields:
            print("Invalid field.")
            return
        self.traveller_.update_traveller(customer_id, field, new_value)
        print("Traveller updated.")
 
    def updateScooterAttributes(self, scooter_obj: Scooter, SoC, target_SoC, location, out_of_service_status, mileage, last_maintenance):
        SoC = SoC if SoC != "" else None
        target_SoC_min, target_SoC_max = target_SoC.split("---") if target_SoC.count("---") == 1 else None
        lat, long = location.split('---') if location.count("---") == 1 else None
        out_of_service_status = out_of_service_status if out_of_service_status != "" else None
        mileage = mileage if mileage != "" else None
        last_maintenance = last_maintenance if datetime.strptime(last_maintenance, "%Y-%m-%d") else None

        updated_scooter = self.scooter_.update_scooter_attributes(scooter_obj, SoC, 
            target_SoC_min, target_SoC_max, lat, long, out_of_service_status, mileage, last_maintenance)
        return updated_scooter

    def updateScooter(self):
        pass

    def updateScooter_serviceEngineer(self, scooter_obj: Scooter, SoC, target_SoC, location, out_of_service_status, mileage, last_maintenance):
        SoC = SoC if SoC != "" else None

        if target_SoC != "" and target_SoC.count("---") == 1:
            target_SoC_min, target_SoC_max = target_SoC.split("---")
        else:
            target_SoC_min = target_SoC_max = None

        if location != "" and location.count("---") == 1:
            lat, long = location.split('---')
        else:
            lat = long = None

        out_of_service_status = out_of_service_status if out_of_service_status != "" else None
        mileage = mileage if mileage != "" else None

        try:
            last_maintenance = last_maintenance if last_maintenance != "" else None
            if last_maintenance:
                last_maintenance = datetime.strptime(last_maintenance, "%Y-%m-%d").date()
        except Exception:
            print("Invalid date format. Ignoring maintenance date.")
            last_maintenance = None

        updated_scooter = self.scooter_.update_scooter_attributes(
            scooter_obj, SoC,
            target_SoC_min, target_SoC_max,
            lat, long,
            out_of_service_status,
            mileage,
            last_maintenance
        )
        return updated_scooter


    def handle_input_length(self, inp: str):
        user_inp = inp[-1].upper() if len(inp) > 0 else " "
        return user_inp
