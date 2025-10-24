from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data

from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter
from logic_layer.utils.AuthenticationAttemptsTracker import AuthenticationAttemptsTracker, AttemptsState

from DataModels.ScooterModel import Scooter

import json
import os

user_keys_tuple = ('id', 'username', 'password', 'role', 'first_name', 'last_name', 'registration_date', 'is_active')

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
        for id, username, p, role, first_name, last_name, r, is_active in users:
            print(f"- {username} ({role}): {first_name} {last_name}")

    def get_user_by_username_or_id(self, username_or_id: str):
        return self.user_.fetch_user(username_or_id)

    def get_user(self, username: str, password: str):
        # print(type(self.super_admin_))
        # print(self.super_admin_)
        username = username.lower() # because must be case insensitive
        for u in self.super_admin_:
            # if u["username"] == username and u["password"] == password:
            if u["username"] == username:
                password_attempt = AuthenticationAttemptsTracker.check_password(password, u["password"])
                if password_attempt == AttemptsState.Correct:
                    return u
        for u_tuple in self.user_.get_all_users():
            u_obj = dict(zip(user_keys_tuple, u_tuple))
            # print(username + " " + u_obj['username'])
            if u_obj['username'].lower() == username and PasswordHasherSalter.verify_password(password, u_obj['password']):
                return u_obj
        return None

    def get_scooter(self, serial):
        try:
            result = self.scooter_.get_scooter_single(serial)[0]
            return result
        except Exception:
            return None

    def search_scooters(self, search_string):
        results = self.scooter_.search_scooter(search_string)
        # print(results) # [('SC-0001', 'Xia...)]
        results_list = []

        if not results:
            print("No scooters found.")
        else:
            print("Scooters Found:")
            for row in results:
                results_list.append(f"- Serial: {row[0]}, Brand: {row[1]}, Model: {row[2]}, Speed: {row[3]} km/h, Charge: {row[4]}%, Mileage: {row[5]} km")
        return results_list

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
