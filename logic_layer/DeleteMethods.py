from access_layer.db.UserData import user_data
from access_layer.db.TravellerData import traveller_data
from access_layer.db.ScooterData import scooter_data
from access_layer.db.LogData import log_data


class AddDataService:
    def __init__(self):
        self.user_ = user_data()
        self.traveller_ = traveller_data()
        self.scooter_ = scooter_data()
        self.log_ = log_data()

    def deleteUser(self):
        username = input("Enter the username to delete: ").strip()
        confirm = input(f"Are you sure you want to delete user '{username}'? (y/n): ").lower()
        if confirm == 'y':
            self.user_.delete_user(username)
            print(f"User '{username}' deleted.")
        else:
            print("Deletion cancelled.")

    def deleteTraveller(self):
        customer_id = input("Enter the customer ID to delete: ").strip()
        confirm = input(f"Delete traveller with ID '{customer_id}'? (y/n): ").lower()
        if confirm == 'y':
            self.traveller_.delete_traveller(customer_id)
            print("Traveller deleted.")
        else:
            print("Deletion cancelled.")

    def deleteScooter(self):
        serial = input("Enter the scooter serial number to delete: ").strip()
        confirm = input(f"Delete scooter with serial '{serial}'? (y/n): ").lower()
        if confirm == 'y':
            self.scooter_.delete_scooter(serial)
            print("Scooter deleted.")
        else:
            print("Deletion cancelled.")
