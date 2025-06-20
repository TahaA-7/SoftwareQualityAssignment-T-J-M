from .SystemAdministratorInterface import SystemAdministratorInterface
from .ServiceEngineerInterface import ServiceEngineerInterface

from logic_layer.GetDataMethods import GetDataService
from logic_layer.AddMethods import AddDataService
from logic_layer.DeleteMethods import DeleteDataService
from logic_layer.UpdateMethods import UpdateDataService
from logic_layer.BackupMethods import BackupMethods

class SuperAdministratorInterface(SystemAdministratorInterface):
    '''
    omitted methods:
        update_self_password
        ALL OWN ACCOUNT METHODS because hardcoded
    '''
    def __init__(self):
        self.get_data_methods = GetDataService()
        self.add_data_methods = AddDataService()
        self.delete_data_methods = DeleteDataService()
        self.update_data_methods = UpdateDataService()
        self.backup_methods = BackupMethods()

    def menu(self):
        while True:
            print("\n--- Super Administrator Menu ---")
            print("[1] Add a new System Administrator")
            print("[2] Update a System Administrator")
            print("[3] Delete a System Administrator")
            print("[4] Reset System Administrator password (temporary password)")
            print("[5] Assign a restore code to a System Administrator")
            print("[6] Revoke a restore code")
            print("[7] Create a backup of the backend system")
            print("[8] View logs")
            print("[0] Exit")

            choice = input("Enter your choice: ")

            match choice:
                case '1':
                    self.add_system_administrator()
                case '2':
                    self.update_system_administrator()
                case '3':
                    self.delete_system_administrator()
                case '4':
                    self.reset_system_administrator_password()
                case '5':
                    self.share_backup_key()
                case '6':
                    self.revoke_backup_key()
                case '7':
                    self.generate_backup_key()
                case '8':
                    self.view_log_single_or_multiple()
                case '0':
                    print("Exiting Super Administrator menu.")
                    break
                case _:
                    print("Invalid choice. Please enter a valid number.")

    # CHECK ALL USERS
    def check_users_and_roles(self):
        SystemAdministratorInterface.check_users_and_roles(self)
    # SERVICE ENGINEER
    def add_service_engineer(self):
        SystemAdministratorInterface.add_service_engineer(self)
    def update_service_engineer(self):
        # account and profile
        SystemAdministratorInterface.update_service_engineer(self)
    def delete_service_engineer(self):
        SystemAdministratorInterface.delete_service_engineer(self)
    def reset_service_engineer_password(self):
        SystemAdministratorInterface.reset_service_engineer_password(self)
    # LOG
    def view_log_single_or_multiple(self):
        SystemAdministratorInterface.view_log_single_or_multiple(self)
    # TRAVELLER
    def view_traveller(self):
        SystemAdministratorInterface.view_traveller(self)
    def add_traveller(self):
        SystemAdministratorInterface.add_traveller(self)
    def update_traveller(self):
        SystemAdministratorInterface.update_traveller(self)
    def delete_traveller(self):
        SystemAdministratorInterface.delete_traveller(self)

    # SCOOTER
    def add_scooter(self):
        SystemAdministratorInterface.add_scooter(self)
    def update_scooter(self):
        SystemAdministratorInterface.update_scooter(self)
    def delete_scooter(self):
        SystemAdministratorInterface.delete_scooter(self)

    def add_system_administrator(self):
        self.add_data_methods.addUser()

    def update_system_administrator(self):
        # account and profile
        self.update_data_methods.update_SystemAdmin()

    def delete_system_administrator(self):
        self.delete_data_methods.deleteSystemAdmin()

    def reset_system_administrator_password(self):
        pass

    def share_backup_key(self):
        self.backup_methods.assign_backup()

    def generate_backup_key(self):
        self.backup_methods.create_backup()

    def revoke_backup_key(self):
        self.backup_methods.revoke_backup_code()
