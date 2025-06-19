from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data

import json
import os

class GetDataService:

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, "access_layer", "superadministrators.json")
        with open(json_path, "r", encoding="utf-8") as f:
            self.super_admin_ = json.load(f)
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()

    def list_users(self):
        users = self.user_.get_all_users()
        print("List of Users and their Roles:")
        for username, role, first_name, last_name in users:
            print(f"- {username} ({role}): {first_name} {last_name}")

    def get_user(self, username: str, password: str):
        # print(type(self.super_admin_))
        # print(self.super_admin_)
        for u in self.super_admin_:
            if u["username"] == username and u["password"] == password:
                return u
        for u in self.user_:
            if u.username == username and u.password == password and u.is_active == True:
                return u
        return None

    def search_scooters(self):
        search_term = input("Enter keyword to search for scooters: ").strip()
        results = self.scooter_.search_scooter(search_term)

        if not results:
            print("No scooters found.")
        else:
            print("Scooters Found:")
            for row in results:
                print(f"- Serial: {row[0]}, Brand: {row[1]}, Model: {row[2]}, Speed: {row[3]} km/h, Charge: {row[4]}%, Mileage: {row[5]} km")

    def search_travellers(self):
        keyword = input("Enter name, email, phone or ID: ").strip()
        results = self.traveller_.search_traveller(keyword)

        if not results:
            print("No travellers found.")
        else:
            print("Travellers found:")
            for row in results:
                print(f"- ID: {row[0]} | Name: {row[1]} {row[2]} | Email: {row[3]} | Phone: {row[4]}")

    def view_logs(self):
        logs = self.log_.get_logs()
        print("System Logs:\n")
        for log in logs:
            suspicious_mark = "⚠️  Suspicious" if log[4] else ""
            print(f"{log[0]} | {log[1]} | {log[2]} | {log[3]} {suspicious_mark}")
