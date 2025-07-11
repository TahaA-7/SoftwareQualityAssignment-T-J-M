from .SystemAdministratorInterface import SystemAdministratorInterface
from logic_layer.GetDataMethods import GetDataService
from logic_layer.AddMethods import AddDataService
from logic_layer.DeleteMethods import DeleteDataService
from logic_layer.UpdateMethods import UpdateDataService
from logic_layer.BackupMethods import BackupMethods
from presentation_layer.utils.Session import Session


class SuperAdministratorInterface(SystemAdministratorInterface):
    '''
    Super Administrator interface — inherits all System Admin functions,
    and includes additional Super Admin-only options.
    '''

    # Shared services
    get_data_methods = GetDataService()
    add_data_methods = AddDataService()
    delete_data_methods = DeleteDataService()
    update_data_methods = UpdateDataService()
    backup_methods = BackupMethods()

    @classmethod
    def super_start(cls):
        while True:
            print("\n--- Super Administrator Menu ---")

            print("[1] Update a Scooter")
            print("[2] Search and retrieve Scooter info")

            print("\n[3] View list of users and their roles")
            print("[4] Add a Service Engineer")
            print("[5] Update a Service Engineer")
            print("[6] Delete a Service Engineer")
            print("[7] Reset Service Engineer password")
            print("[8] View logs")
            print("[9] Add a Traveller")
            print("[10] Update a Traveller")
            print("[11] Delete a Traveller")
            print("[12] Add a Scooter")
            print("[13] Update Scooter information")
            print("[14] Delete a Scooter")
            print("[15] Search for a Traveller")

            print("\n[16] Add a System Administrator")
            print("[17] Update a System Administrator")
            print("[18] Delete a System Administrator")
            print("[19] Reset System Administrator password")
            print("[20] Create a system backup")
            print("[21] Assign a restore code")
            print("[22] Revoke a restore code")

            print("\n[0] Exit")

            choice = input("Enter your choice: ")

            match choice:
                # Service Engineer–level
                case '1': 
                    cls.update_scooter()
                case '2': 
                    cls.view_scooter()

                # System Admin–level
                case '3':
                    cls.check_users_and_roles()
                case '4': 
                    cls.add_service_engineer()
                case '5': 
                    cls.update_service_engineer()
                case '6': 
                    cls.delete_service_engineer()
                case '7': 
                    cls.reset_service_engineer_password()
                case '8': 
                    cls.view_log_single_or_multiple()
                case '9': 
                    cls.add_traveller()
                case '10': 
                    cls.update_traveller()
                case '11': 
                    cls.delete_traveller()
                case '12': 
                    cls.add_scooter()
                case '13': 
                    cls.update_scooter()
                case '14': 
                    cls.delete_scooter()
                case '15': 
                    cls.view_traveller()

                # Super Admin only
                case '16': 
                    cls.add_system_administrator()
                case '17': 
                    cls.update_system_administrator()
                case '18': 
                    cls.delete_system_administrator()
                case '19': 
                    cls.reset_system_administrator_password()
                case '20': 
                    cls.generate_backup_key()
                case '21': 
                    cls.share_backup_key()
                case '22': 
                    cls.revoke_backup_key()

                case '0':
                    print("Exiting Super Administrator menu.")
                    Session.set_loggedin_false()
                    break
                case _:
                    print("Invalid choice. Please enter a valid number.")

    # === SUPER ADMIN–ONLY METHODS ===
    @classmethod
    def add_system_administrator(cls):
        cls.add_data_methods.addSystemAdmin()

    @classmethod
    def update_system_administrator(cls):
        cls.update_data_methods.update_SystemAdmin()

    @classmethod
    def delete_system_administrator(cls):
        cls.delete_data_methods.deleteSystemAdmin()

    @classmethod
    def reset_system_administrator_password(cls):
        pass

    @classmethod
    def share_backup_key(cls):
        cls.backup_methods.assign_backup()

    @classmethod
    def revoke_backup_key(cls):
        cls.backup_methods.revoke_backup_code()

    @classmethod
    def generate_backup_key(cls):
        cls.backup_methods.create_backup()
