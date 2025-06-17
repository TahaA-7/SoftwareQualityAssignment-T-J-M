from db.UserData import user_data
from db.TravellerData import traveller_data
from db.ScooterData import scooter_data
from db.LogData import log_data

class GetDataService:
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()

    def list_users(self):
        users = self.user_.get_all_users()
        print("List of Users and their Roles:")
        for username, role, first_name, last_name in users:
            print(f"- {username} ({role}): {first_name} {last_name}")

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
