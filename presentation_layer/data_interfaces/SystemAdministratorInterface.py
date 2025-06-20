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

from utils.Session import Session

class SystemAdministratorInterface(ServiceEngineerInterface):
    def __init__(cls):
        super().__init__()
        cls.get_data_methods = GetDataService()
        cls.add_data_methods = AddDataService()
        cls.delete_data_methods = DeleteDataService()
        cls.update_data_methods = UpdateDataService()
        cls.backup_methods = BackupMethods()

    @classmethod
    def system_start(cls):
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
                    cls.check_users_and_roles()
                case '2':
                    cls.add_service_engineer()
                case '3':
                    cls.update_service_engineer()
                case '4':
                    cls.delete_service_engineer()
                case '5':
                    cls.reset_service_engineer_password()
                case '6':
                    cls.update_cls_account_profile()
                case '7':
                    cls.delete_cls_account()
                case '8':
                    cls.make_backend_backup()
                case '9':
                    cls.restore_backend_backup()
                case '10':
                    cls.view_log_single_or_multiple()
                case '11':
                    cls.add_traveller()
                case '12':
                    cls.update_traveller()
                case '13':
                    cls.delete_traveller()
                case '14':
                    cls.view_traveller()
                case '15':
                    cls.add_scooter()
                case '16':
                    cls.update_scooter()
                case '17':
                    cls.delete_scooter()
                case '0':
                    print("Exiting System Administrator menu.")
                    Session.set_loggedin_false()
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
        cls.add_data_methods.addUser()

    # CHECK ALL USERS
    @classmethod
    def check_users_and_roles(cls):
        pass

    # SERVICE ENGINEER
    @classmethod
    def add_service_engineer(cls):
        pass

    @classmethod
    def update_service_engineer(cls):
        # account and profile
        cls.update_data_methods.update_ServiceEngineer()

    @classmethod
    def delete_service_engineer(cls):
        cls.delete_data_methods.deleteServiceEngineer()

    @classmethod
    def reset_service_engineer_password(cls, engineer: User):
        # replaces current with a temporary password
        """Password:
            ○ must have a length of at least 12 characters
            ○ must be no longer than 30 characters
            ○ can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%&_-
            +=`|\(){}[]:;'<>,.?/
            ○ must have a combination of at least one lowercase letter, one uppercase letter, one digit,
            and one special character:
        """
        # Generate a valid temporary password
        temp_password = cls.__generate_hashed_salted_password()

        hashed_salted_password = PasswordHasherSalter.hash_salt_password(temp_password)
        # salted_password = PasswordHasherSalter.salt_password(hashed_salted_password)
        engineer.hashed_salted_password = hashed_salted_password

        # return temp_password

    @classmethod
    def __generate_hashed_salted_password(cls):
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
    def update_cls_account_profile(cls):
        cls.update_data_methods.update_SystemAdmin()

    @classmethod
    def delete_cls_account(cls):
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
        # traveller is not a user
        cls.add_data_methods.addTraveller()

    @classmethod
    def update_traveller(cls):
        cls.update_data_methods.updateTraveller()

    @classmethod
    def delete_traveller(cls):
        cls.delete_data_methods.deleteTraveller()

    # SCOOTER
    @classmethod
    def add_scooter(cls):
        cls.add_data_methods.addScooter()

    @classmethod
    def update_scooter(cls):
        cls.update_data_methods.updateScooter()

    @classmethod
    def delete_scooter(cls):
        cls.delete_data_methods.deleteScooter()

    # SERVICE ENGINEER METHODS
    @classmethod
    def __view_scooter(cls):
        ServiceEngineerInterface.__view_scooter()
