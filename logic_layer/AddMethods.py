from db.UserData import user_data
from db.TravellerData import traveller_data
from db.ScooterData import scooter_data
from db.LogData import log_data

from DataModels.ScooterModel import Scooter
from DataModels.TravellerModel import Traveller

import re
import hashlib

class AddDataService:
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()

    def hash_password(self, plain_password):
        return hashlib.sha256(plain_password.encode()).hexdigest()

    def addUser(self):
        username = input("Username (8-10 chars): ").strip()
        password = input("Password (min 12 chars): ").strip()
        role = input("Role (service_engineer/system_admin): ").strip()
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()

        # Simple validation
        if len(username) < 8 or len(username) > 10:
            print("Invalid username length.")
            return
        if len(password) < 12:
            print("Password too short.")
            return

        hashed = self.hash_password(password)
        self.user_.add_user(username, hashed, role, first_name, last_name)
        print("User added successfully.")

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

        scooter = Scooter(brand, model, serial, top_speed, battery, soc, soc_min, soc_max, lat, lon, out_of_service, mileage, last_maint)
        self.scooter_.add_scooter(scooter)
        print("Scooter added successfully.")

    def addTraveller(self):
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

        traveller = Traveller(first_name, last_name, birthday, gender,
                            street, number, zip_code, city, email,
                            phone, license_number)

        self.traveller_.add_traveller(traveller)
        print("Traveller added successfully.")
