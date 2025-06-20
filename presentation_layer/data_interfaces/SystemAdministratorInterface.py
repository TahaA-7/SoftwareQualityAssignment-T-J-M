from .ServiceEngineerInterface import ServiceEngineerInterface

from logic_layer.utils.StringValidations import StringValidations
from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter

from DataModels.UserModel import User
import random, string

from getpass import getpass

from utils.Session import Session

class SystemAdministratorInterface():
    Parent = ServiceEngineerInterface()


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
                    ServiceEngineerInterface.update_scooter_attributes()
                case '3':
                    ServiceEngineerInterface.view_scooter()

                case 'L':
                    Session.set_loggedin_false()
                    break
                case _:
                    print("Invalid input!")
                    continue

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
        pass

    @classmethod
    def delete_service_engineer(cls):
        pass

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
        pass

    @classmethod
    def delete_cls_account(cls):
        pass

    # BACKUP
    @classmethod
    def make_backend_backup(cls):
        pass

    @classmethod
    def restore_backend_backup(cls):
        # uses super-administrator generated `one-use-only` key linked to specific backup
        pass

    # LOG
    @classmethod
    def view_log_single_or_multiple(cls):
        pass

    # TRAVELLER
    @classmethod
    def view_traveller(cls):
        '''
        Note 2: The search function must accept reasonable data fields as a search key. It must also accept
        partial keys. For example, a user can search for a Traveller with a name “Mike Thomson” and customer
        ID “2123287421” by entering any of these keys: “mik”, “omso”, or “2328”, etc.
        '''
        pass

    @classmethod
    def add_traveller(cls):
        # traveller is not a user
        pass

    @classmethod
    def update_traveller(cls):
        pass

    @classmethod
    def delete_traveller(cls):
        pass

    # SCOOTER
    @classmethod
    def add_scooter(cls):
        pass

    @classmethod
    def update_scooter(cls):
        pass

    @classmethod
    def delete_scooter(cls):
        pass


    # SERVICE ENGINEER METHODS
    def __view_scooter(cls):
        ServiceEngineerInterface.__view_scooter()
