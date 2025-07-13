from .SystemAdministratorInterface import SystemAdministratorInterface
from logic_layer.GetDataMethods import GetDataService
from logic_layer.AddMethods import AddDataService
from logic_layer.DeleteMethods import DeleteDataService
from logic_layer.UpdateMethods import UpdateDataService
from logic_layer.BackupMethods import BackupMethods
from presentation_layer.utils.Session import Session

from presentation_layer.menus.CreateOrUpdateEmployee import CreateOrUpdateEmployee
from presentation_layer.menus.LoginMenu import LoginMenu


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
            cls.get_data_methods = GetDataService()
            cls.add_data_methods = AddDataService()
            cls.delete_data_methods = DeleteDataService()
            cls.update_data_methods = UpdateDataService()
            cls.backup_methods = BackupMethods()
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
                    LoginMenu.username = ""
                    LoginMenu.password = ""
                    break
                case _:
                    print("Invalid choice. Please enter a valid number.")

    # === SUPER ADMIN–ONLY METHODS ===
    @classmethod
    def add_system_administrator(cls):
        employee_menu = CreateOrUpdateEmployee()
        employee_menu.user_type = 2  # system_administrator
        employee_menu.menu()

    @classmethod
    def update_system_administrator(cls):
        employee_menu = CreateOrUpdateEmployee()
        # employee_menu.object_type = "employee"  # system_administrator
        employee_menu.menu()

    @classmethod
    def delete_system_administrator(cls):
        username_or_id = input("Enter Service Engineer username or ID to delete: ").strip()
        cls.delete_data_methods.deleteSystemAdmin(username_or_id)

    @classmethod
    def reset_system_administrator_password(cls):
        temp_pw = cls._generate_temp_password()
        username_or_id = input("Please enter the name or ID of the system admin to reset their password: ")
        user = cls.get_data_methods.get_user_by_username_or_id(username_or_id)
        if user != None:
            updated_user = cls.update_data_methods.updateUser_password(username_or_id, temp_pw)
            if updated_user:
                print("System admin password sucessfully reset")
            else:
                print("Error: could not update system admin password")
        else:
            print("Error: no user found with that username or ID")

    @classmethod
    def share_backup_key(cls):
        cls.backup_methods.assign_backup()

    @classmethod
    def revoke_backup_key(cls):
        cls.backup_methods.revoke_backup_code()

    @classmethod
    def generate_backup_key(cls):
        cls.backup_methods.create_backup()
