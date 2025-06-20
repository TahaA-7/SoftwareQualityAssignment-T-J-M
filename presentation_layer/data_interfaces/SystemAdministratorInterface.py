from .ServiceEngineerInterface import ServiceEngineerInterface

from logic_layer.GetDataMethods import GetDataService
from logic_layer.AddMethods import AddDataService
from logic_layer.DeleteMethods import DeleteDataService
from logic_layer.UpdateMethods import UpdateDataService
from logic_layer.BackupMethods import BackupMethods

class SystemAdministratorInterface(ServiceEngineerInterface):
    def __init__(self):
        super().__init__()
        self.get_data_methods = GetDataService()
        self.add_data_methods = AddDataService()
        self.delete_data_methods = DeleteDataService()
        self.update_data_methods = UpdateDataService()
        self.backup_methods = BackupMethods()

    def menu(self):
            while True:
                print("\n--- System Administrator Menu ---")
                print("[1] Check the list of users and their roles")
                print("[2] Add a new Service Engineer")
                print("[3] Update an existing Service Engineer account and profile")
                print("[4] Delete a Service Engineer account")
                print("[5] Reset Service Engineer password (temporary password)")
                print("[6] Update own account and profile")
                print("[7] Delete own account")
                print("[8] Make a backend system backup")
                print("[9] Restore a specific backup (with one-use code)")
                print("[10] View logs file(s)")
                print("[11] Add a new Traveller")
                print("[12] Update a Traveller")
                print("[13] Delete a Traveller")
                print("[14] Search for Traveller info")
                print("[15] Add a new Scooter")
                print("[16] Update a Scooter")
                print("[17] Delete a Scooter")
                print("[0] Exit")

                choice = input("Enter your choice: ")

                match choice:
                    case '1':
                        self.check_users_and_roles()
                    case '2':
                        self.add_service_engineer()
                    case '3':
                        self.update_service_engineer()
                    case '4':
                        self.delete_service_engineer()
                    case '5':
                        self.reset_service_engineer_password()
                    case '6':
                        self.update_self_account_profile()
                    case '7':
                        self.delete_self_account()
                    case '8':
                        self.make_backend_backup()
                    case '9':
                        self.restore_backend_backup()
                    case '10':
                        self.view_log_single_or_multiple()
                    case '11':
                        self.add_traveller()
                    case '12':
                        self.update_traveller()
                    case '13':
                        self.delete_traveller()
                    case '14':
                        self.view_traveller()
                    case '15':
                        self.add_scooter()
                    case '16':
                        self.update_scooter()
                    case '17':
                        self.delete_scooter()
                    case '0':
                        print("Exiting System Administrator menu.")
                        break
                    case _:
                        print("Invalid choice. Please enter a valid number.")

    # CHECK ALL USERS
    def check_users_and_roles(self):
        self.get_data_methods.list_users()

    # SERVICE ENGINEER
    def add_service_engineer(self):
        self.add_data_methods.addUser()

    def update_service_engineer(self):
        # account and profile
        self.update_data_methods.update_ServiceEngineer()

    def delete_service_engineer(self):
        self.delete_data_methods.deleteServiceEngineer()

    def reset_service_engineer_password(self):
        # replaces current with a temporary password
        pass

    # OWN ACCOUNT
    def update_self_account_profile(self):
        self.update_data_methods.update_SystemAdmin()

    def delete_self_account(self):
        self.delete_data_methods.deleteSystemAdmin()

    # BACKUP
    def make_backend_backup(self):
        self.backup_methods.create_backup()

    def restore_backend_backup(self):
        # uses super-administrator generated `one-use-only` key linked to specific backup
        self.backup_methods.restore_backup()

    # LOG
    def view_log_single_or_multiple(self):
        self.get_data_methods.view_logs()

    # TRAVELLER
    def view_traveller(self):
        '''
        Note 2: The search function must accept reasonable data fields as a search key. It must also accept
        partial keys. For example, a user can search for a Traveller with a name “Mike Thomson” and customer
        ID “2123287421” by entering any of these keys: “mik”, “omso”, or “2328”, etc.
        '''
        self.get_data_methods.search_travellers()

    def add_traveller(self):
        # traveller is not a user
        self.add_data_methods.addTraveller()

    def update_traveller(self):
        self.update_data_methods.updateTraveller()

    def delete_traveller(self):
        self.delete_data_methods.deleteTraveller()

    # SCOOTER
    def add_scooter(self):
        self.add_data_methods.addScooter()

    def update_scooter(self):
        self.update_data_methods.updateScooter()

    def delete_scooter(self):
        self.delete_data_methods.deleteScooter()
