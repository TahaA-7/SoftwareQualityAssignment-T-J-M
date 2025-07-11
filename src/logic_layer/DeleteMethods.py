from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data

from access_layer.db.UserData import user_data

class DeleteDataService:
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()
        self.user_data = user_data()

    def deleteServiceEngineer(self):
        username = input("Enter Service Engineer username to delete: ").strip()

        for user in self.user_.get_all_users():
            if user[0].lower() == username.lower() and user[1].lower() == "service_engineer":
                confirm = input(f"Are you sure you want to delete '{username}'? (y/n): ").lower()
                if confirm == 'y':
                    self.user_.delete_user(username)
                    print(f"Service Engineer '{username}' deleted.")
                else:
                    print("Deletion cancelled.")
                return

        print("No Service Engineer with that username.")

    def deleteSystemAdmin(self):
        username = input("Enter System admin username to delete: ").strip()

        for user in self.user_.get_all_users():
            if user[0].lower() == username.lower() and user[1].lower() == "system_admin":
                confirm = input(f"Are you sure you want to delete '{username}'? (y/n): ").lower()
                if confirm == 'y':
                    self.user_.delete_user(username)
                    print(f"System admin '{username}' deleted.")
                else:
                    print("Deletion cancelled.")
                return

        print("No System admin with that username.")

    def deleteTraveller(self, customer_id):
        for traveller in self.traveller_.get_travellers():
            if traveller[0].lower() == customer_id.lower():
                confirm = input(f"Are you sure you want to delete '{customer_id}'? (y/n): ").lower()
                if confirm == 'y':
                    if self.user_.delete_user(customer_id.upper()):
                        print(f"Traveller '{customer_id}' deleted.")
                    print("No Traveller with that ID.")
                else:
                    print("Deletion cancelled.")
                return

    def deleteScooter(self, serial, confirm):
        is_valid_flag = True
        if not str(serial).strip().isdigit():
            is_valid_flag = False
            print("Invalid input: serial must be a whole number")
        if not str(confirm).strip().upper() in ("Y", "N"):
            print("Invalid input: confirmation must be either `Y or `N`")
            is_valid_flag = False

        if is_valid_flag and confirm in ('y', 'Y'):
            self.scooter_.delete_scooter(serial)
            print("Scooter deleted.")
        else:
            print("Deletion cancelled.")
