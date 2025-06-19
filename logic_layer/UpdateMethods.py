from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data

import hashlib

class UpdateDataService:
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()

    def hash_password(self, plain_password):
        return hashlib.sha256(plain_password.encode()).hexdigest()

    def updateUser_profile(self):
        username = input("Username to update: ").strip()
        first_name = input("New first name: ").strip()
        last_name = input("New last name: ").strip()
        self.user_.update_user_profile(username, first_name, last_name)
        print("User profile updated.")

    def updateUser_password(self):
        username = input("Username to update password for: ").strip()
        new_password = input("New password: ").strip()
        if len(new_password) < 12:
            print("Password too short.")
            return
        hashed = self.hash_password(new_password)
        self.user_.update_user_password(username, hashed)
        print("Password updated.")

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
 
    def updateScooter(self):
        serial = input("Scooter serial number: ").strip()
        field = input("Which field to update (e.g., state_of_charge, mileage): ").strip()
        value = input("New value: ").strip()

        allowed_fields = [
            'brand', 'model', 'top_speed', 'battery_capacity',
            'state_of_charge', 'target_soc_min', 'target_soc_max',
            'latitude', 'longitude', 'out_of_service', 'mileage',
            'last_maintenance_date'
        ]
        if field not in allowed_fields:
            print("Invalid field.")
            return

        self.scooter_.update_scooter(serial, field, value)
        print("Scooter updated.")
