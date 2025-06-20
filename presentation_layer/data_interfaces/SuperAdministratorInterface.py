from .SystemAdministratorInterface import SystemAdministratorInterface
from .ServiceEngineerInterface import ServiceEngineerInterface

from logic_layer.GetDataMethods import GetDataService
from logic_layer.AddMethods import AddDataService
from logic_layer.DeleteMethods import DeleteDataService
from logic_layer.UpdateMethods import UpdateDataService
from logic_layer.BackupMethods import BackupMethods

from logic_layer.utils.StringValidations import StringValidations

from getpass import getpass

class SuperAdministratorInterface():
    '''
    omitted methods:
        update_cls_password
        ALL OWN ACCOUNT METHODS because hardcoded
    '''
    def __init__(cls):
        cls.get_data_methods = GetDataService()
        cls.add_data_methods = AddDataService()
        cls.delete_data_methods = DeleteDataService()
        cls.update_data_methods = UpdateDataService()
        cls.backup_methods = BackupMethods()

    def menu(cls):
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
                    cls.add_system_administrator()
                case '2':
                    cls.update_system_administrator()
                case '3':
                    cls.delete_system_administrator()
                case '4':
                    cls.reset_system_administrator_password()
                case '5':
                    cls.share_backup_key()
                case '6':
                    cls.revoke_backup_key()
                case '7':
                    cls.generate_backup_key()
                case '8':
                    cls.view_log_single_or_multiple()
                case '0':
                    print("Exiting Super Administrator menu.")
                    break
                case _:
                    print("Invalid choice. Please enter a valid number.")

    @classmethod
    def start(cls):
        print("""Welcome to service engineer interface'
-   -   -   -   -   -   -""")
        while True:
            user_choice = StringValidations.handle_input_length(getpass(
f"""What do you want to do?:
[1] update own password
[2] update a scooter's attributes
[3] search a scooter

[L] logout\n"""))
            match user_choice:
                case '1':
                    ServiceEngineerInterface.update_own_password()
                case '2':
                    cls.update_scooter_attributes()
                case '3':
                    cls.view_scooter()

                case 'L':
                    Session.set_loggedin_false()
                    break
                case _:
                    print("Invalid input!")
                    continue

    # CHECK ALL USERS
    def check_users_and_roles(cls):
        SystemAdministratorInterface.check_users_and_roles(cls)
    # SERVICE ENGINEER
    def add_service_engineer(cls):
        SystemAdministratorInterface.add_service_engineer(cls)
    def update_service_engineer(cls):
        # account and profile
        SystemAdministratorInterface.update_service_engineer(cls)
    def delete_service_engineer(cls):
        SystemAdministratorInterface.delete_service_engineer(cls)
    def reset_service_engineer_password(cls):
        SystemAdministratorInterface.reset_service_engineer_password(cls)
    # LOG
    def view_log_single_or_multiple(cls):
        SystemAdministratorInterface.view_log_single_or_multiple(cls)
    # TRAVELLER
    def view_traveller(cls):
        SystemAdministratorInterface.view_traveller(cls)
    def add_traveller(cls):
        SystemAdministratorInterface.add_traveller(cls)
    def update_traveller(cls):
        SystemAdministratorInterface.update_traveller(cls)
    def delete_traveller(cls):
        SystemAdministratorInterface.delete_traveller(cls)

    # SCOOTER
    @classmethod
    def add_scooter(cls):
        SystemAdministratorInterface.add_scooter(cls)
    @classmethod
    def update_scooter(cls):
        SystemAdministratorInterface.update_scooter(cls)
    @classmethod
    def delete_scooter(cls):
        SystemAdministratorInterface.delete_scooter(cls)

    @classmethod
    def add_system_administrator(cls):
        cls.add_data_methods.addUser()

    @classmethod
    def update_system_administrator(cls):
        # account and profile
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
    def generate_backup_key(cls):
        cls.backup_methods.create_backup()

    @classmethod
    def revoke_backup_key(cls):
        cls.backup_methods.revoke_backup_code()
