from .ServiceEngineerInterface import ServiceEngineerInterface

from logic_layer.GetDataMethods import GetDataService
from logic_layer.AddMethods import AddDataService
from logic_layer.DeleteMethods import DeleteDataService
from logic_layer.UpdateMethods import UpdateDataService
from logic_layer.BackupMethods import BackupMethods

from logic_layer.utils.StringValidations import StringValidations
from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter

from DataModels.UserModel import User
import random, string

from getpass import getpass

from presentation_layer.utils.Session import Session
from presentation_layer.menus.LoginMenu import LoginMenu

from presentation_layer.menus.CreateOrUpdateEmployee import CreateOrUpdateEmployee
from presentation_layer.menus.CreateOrUpdateTraveller import CreateOrUpdateTraveller
from presentation_layer.menus.CreateOrUpdateScooter import CreateOrUpdateScooter


class SystemAdministratorInterface(ServiceEngineerInterface):
    get_data_methods = GetDataService()
    add_data_methods = AddDataService()
    delete_data_methods = DeleteDataService()
    update_data_methods = UpdateDataService()
    backup_methods = BackupMethods()

    @classmethod
    def system_start(cls):
        while True:
            cls.get_data_methods = GetDataService()
            cls.add_data_methods = AddDataService()
            cls.delete_data_methods = DeleteDataService()
            cls.update_data_methods = UpdateDataService()
            cls.backup_methods = BackupMethods()
            print("\n--- System Administrator Menu ---")

            print("[1] Update your own password")
            print("[2] Update a Scooter")
            print("[3] Search and retrieve Scooter info")

            print("\n[4] View users and their roles")
            print("[5] Add a Service Engineer")
            print("[6] Update a Service Engineer")
            print("[7] Delete a Service Engineer")
            print("[8] Reset Service Engineer password (temporary password)")
            print("[9] Update own account and profile")
            print("[10] Delete own account")
            print("[11] Create a system backup")
            print("[12] Restore a backup (with one-use code)")
            print("[13] View logs")
            print("[14] Add a Traveller")
            print("[15] Update a Traveller")
            print("[16] Delete a Traveller")
            print("[17] Add a Scooter")
            print("[18] Delete a Scooter")
            print("[19] Search and retrieve Traveller info")

            print("\n[0] Exit")

            choice = input("Enter your choice: ")
            
            if len(choice) > 5:
                continue

            match choice:
                # Service Engineer functionality
                case '1': 
                    cls.update_own_password()
                case '2': 
                    cls.update_scooter()
                case '3':
                    cls.view_scooter()

                # System Admin functionality
                case '4': 
                    cls.check_users_and_roles()
                case '5': 
                    cls.add_service_engineer()
                case '6': 
                    cls.update_service_engineer()
                case '7': 
                    cls.delete_service_engineer()
                case '8': 
                    cls.reset_service_engineer_password()
                case '9': 
                    cls.update_own_account_profile()
                case '10': 
                    cls.delete_own_account()
                case '11': 
                    cls.make_backend_backup()
                case '12': 
                    cls.restore_backend_backup()
                case '13': 
                    cls.view_log_single_or_multiple()
                case '14': 
                    cls.add_traveller()
                case '15': 
                    cls.update_traveller()
                case '16': 
                    cls.delete_traveller()
                case '17': 
                    cls.add_scooter()
                case '18': 
                    cls.delete_scooter()
                case '19': 
                    cls.view_traveller()

                case '0':
                    print("Exiting System Administrator menu.")
                    Session.set_loggedin_false()
                    LoginMenu.username = ""
                    LoginMenu.password = ""
                    break
                case _:
                    print("Invalid choice. Please enter a valid number.")

    # CHECK ALL USERS
    @classmethod
    def check_users_and_roles(cls):
        cls.get_data_methods.list_users()

    # SERVICE ENGINEER
    @classmethod
    def add_service_engineer(cls):
        employee_menu = CreateOrUpdateEmployee()
        employee_menu.menu()

    @classmethod
    def update_service_engineer(cls):
        employee_menu = CreateOrUpdateEmployee()
        employee_menu.menu()

    @classmethod
    def delete_service_engineer(cls):
        username_or_id = input("Enter Service Engineer username or ID to delete: ").strip()
        cls.delete_data_methods.deleteServiceEngineer(username_or_id)

    @classmethod
    def reset_service_engineer_password(cls):
        temp_pw = cls._generate_temp_password()
        username_or_id = input("Please enter the name or ID of the service engineer to reset their password: ")
        user = cls.get_data_methods.get_user_by_username_or_id(username_or_id)
        if user != None:
            updated_user = cls.update_data_methods.updateUser_password(username_or_id, temp_pw)
            if updated_user != None:
                print("Service engineer password sucessfully reset")
            else:
                print("Error: could not update service engineer password")
        else:
            print("Error: no user found with that username or ID")


    @classmethod
    def _generate_temp_password(cls):
        specials = "~!@#$%&_-+=`|\\(){}[]:;'<>,.?/"
        temp_password = ""
        while True:
            temp_password = (
                random.choice(string.ascii_lowercase) +
                random.choice(string.ascii_uppercase) +
                random.choice(string.digits) +
                random.choice(specials) +
                ''.join(random.choices(string.ascii_letters + string.digits + specials, k=8))
            )
            if 12 <= len(temp_password) <= 30:
                break

        return temp_password

    # OWN ACCOUNT
    @classmethod
    def update_own_account_profile(cls):
        cls.update_data_methods.update_SystemAdmin()

    @classmethod
    def delete_own_account(cls):
        cls.delete_data_methods.deleteSystemAdmin()

    # BACKUP
    @classmethod
    def make_backend_backup(cls):
        cls.backup_methods.create_backup()

    @classmethod
    def restore_backend_backup(cls):
        # uses super-administrator generated `one-use-only` key linked to specific backup
        cls.backup_methods.restore_backup()

    # LOG
    @classmethod
    def view_log_single_or_multiple(cls):
        cls.get_data_methods.view_logs()

    # TRAVELLER
    @classmethod
    def view_traveller(cls):
        '''
        Note 2: The search function must accept reasonable data fields as a search key. It must also accept
        partial keys. For example, a user can search for a Traveller with a name “Mike Thomson” and customer
        ID “2123287421” by entering any of these keys: “mik”, “omso”, or “2328”, etc.
        '''
        cls.get_data_methods.search_travellers()


    @classmethod
    def add_traveller(cls):
        travellermenu_obj = CreateOrUpdateTraveller()
        travellermenu_obj.menu()

    @classmethod
    def update_traveller(cls):
        travellermenu_obj = CreateOrUpdateTraveller()
        travellermenu_obj.menu()

    @classmethod
    def delete_traveller(cls):
        customer_id = input("Enter Traveller customer ID (format=CUST00) to delete: ").strip()
        cls.delete_data_methods.deleteTraveller(customer_id)

    # SCOOTER
    @classmethod
    def add_scooter(cls):              
        scootermenu_obj = CreateOrUpdateScooter()
        scootermenu_obj.menu()

    @classmethod
    def update_scooter(cls):
        scootermenu_obj = CreateOrUpdateScooter()
        scootermenu_obj.menu()

    @classmethod
    def delete_scooter(cls):
        serial = input("Enter the scooter serial number to delete: ")
        confirm = input(f"Delete scooter with serial '{serial}'? (y/n): ")
        cls.delete_data_methods.deleteScooter(serial, confirm)

    # SERVICE ENGINEER METHODS
    @classmethod
    def view_scooter(cls):
        # search scooter info
        '''
        Note 2: The search function must accept reasonable data fields as a search key. It must also accept
        partial keys. For example, a user can search for a Traveller with a name “Mike Thomson” and customer
        ID “2123287421” by entering any of these keys: “mik”, “omso”, or “2328”, etc.
        '''
        getdataservice_obj = GetDataService()
        user_input = input("Please enter a (part of a) brand or model name to search by: ")
        flag_brand_model = False
        if all(c in cls.alnum_space for c in user_input):
            flag_brand_model = True
        if not flag_brand_model:
            print("Error: only letters, digits and spaces allowed")
            return
        scooters = getdataservice_obj.search_scooters(user_input)
        for scooter in scooters:
            print(scooter)
