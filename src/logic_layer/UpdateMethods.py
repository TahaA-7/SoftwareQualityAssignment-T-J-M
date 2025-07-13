from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data
from access_layer.db.UserData import user_data

from DataModels.ScooterModel import Scooter

from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter

from presentation_layer.utils.Roles import Roles
from presentation_layer.utils.Session import Session

from datetime import datetime

import hashlib

class UpdateDataService:
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()
        self.user_data = user_data()

    def updateUser_profile(self, original_username, username, u_fname, u_lname):
        for user in self.user_.get_all_users():
            if user[1].lower() == original_username.lower() and int(user[3]) == Roles.SERVICE_ENGINEER.value:
                self.user_.update_user_profile(original_username, username, u_fname, u_lname)
                return True
            elif user[1].lower() == original_username.lower() and int(user[3]) == Roles.SYSTEM_ADMINISTRATOR.value:
                if Session.user.role == Roles.SUPER_ADMINISTRATOR:
                    self.user_.update_user_profile(original_username, username, u_fname, u_lname)
                    return True
                else:
                    print("Error: only super administrators can update system admin profile!")
                    return False

        print("No Service engineer with that username.")
        return False

    def update_SystemAdmin(self):
        username = input("Username or id from user to update: ").strip()

        for user in self.user_.get_all_users():
            if user[1].lower() == username.lower() and user[3] == Roles(int(user[3])) or user[3] == Roles.SYSTEM_ADMINISTRATOR:
                first_name = input("New first name: ").strip()
                last_name = input("New last name: ").strip()
                self.user_.update_user_profile(username, first_name, last_name)
                print("User profile updated.")
                return

        print("No System Administrator with that username.")


    def updateUser_password(self, username_or_id, password):
        hashed_salted = PasswordHasherSalter.hash_salt_password(password)
        updated_user = self.user_.update_user_password(username_or_id, hashed_salted)
        return updated_user != None

    def updateTraveller(self, customer_id, fname, lname, bday, gender, street, house_num, zip, city, email, phone, license_num):
        # customer_id = input("Traveller ID: ").strip()
        # field = input("Which field to update (first_name, email, city, etc.): ").strip()
        # new_value = input("New value: ").strip()
        # allowed_fields = [
        #     'first_name', 'last_name', 'birthday', 'gender',
        #     'street_name', 'house_number', 'zip_code', 'city',
        #     'email', 'mobile_phone', 'driving_license_number'
        # ]
        # if field not in allowed_fields:
        #     print("Invalid field.")
        #     return
        # self.traveller_.update_traveller(customer_id, field, new_value)
        # print("Traveller updated.")
        for traveller in self.traveller_.get_travellers():
            if traveller[0] == customer_id:
                res = self.traveller_.update_traveller(customer_id, fname, lname, bday, gender, street, house_num, zip, city, email, phone, license_num)
                return res
        return False
 
    def updateScooterAttributes(self, scooter_obj: Scooter, SoC, target_SoC, location, out_of_service_status, mileage, last_maintenance):
        SoC = SoC if SoC != "" else None
        target_SoC_min, target_SoC_max = target_SoC.split("---") if target_SoC.count("---") == 1 else None
        lat, long = location.split('---') if location.count("---") == 1 else None
        out_of_service_status = out_of_service_status if out_of_service_status != "" else None
        mileage = mileage if mileage != "" else None
        last_maintenance = last_maintenance if datetime.strptime(last_maintenance, "%Y-%m-%d").date() else None

        updated_scooter = self.scooter_.update_scooter_attributes(scooter_obj, SoC, 
            target_SoC_min, target_SoC_max, lat, long, out_of_service_status, mileage, last_maintenance)
        return updated_scooter

    def updateScooter(self, original_serial, serial, brand, model, top_speed, battery, soc, soc_range, soc_min, soc_max, lat, lon, 
            out_of_service_status, mileage, last_maint_date):
        for scooter in self.scooter_.get_scooter_single(original_serial):
            if scooter[0] == original_serial:
                res = self.scooter_.update_scooter(original_serial, serial, brand, model, top_speed, battery, soc, soc_range, soc_min, soc_max,
                    lat, lon, out_of_service_status, mileage, last_maint_date)
                return res
        return False


    def update_service_engineer(self):
        pass


    def handle_input_length(self, inp: str):
        user_inp = inp[-1].upper() if len(inp) > 0 else " "
        return user_inp
