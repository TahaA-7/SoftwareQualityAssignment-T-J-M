from .SystemAdministratorInterface import SystemAdministratorInterface
from .ServiceEngineerInterface import ServiceEngineerInterface

from logic_layer.utils.StringValidations import StringValidations

from getpass import getpass

class SuperAdministratorInterface():
    '''
    omitted methods:
        update_cls_password
        ALL OWN ACCOUNT METHODS because hardcoded
    '''
    def __init__(cls):
        pass

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
        SystemAdministratorInterface.delete_scooter(cls)
    # SCOOTER
    def add_scooter(cls):
        SystemAdministratorInterface.add_scooter(cls)
    def update_scooter(cls):
        SystemAdministratorInterface.update_scooter(cls)
    def delete_scooter(cls):
        SystemAdministratorInterface.delete_scooter(cls)

    def add_system_administrator(cls):
        pass

    def update_system_administrator(cls):
        # account and profile
        pass

    def delete_system_administrator(cls):
        pass

    def reset_system_administrator_password(cls):
        pass

    def make_or_restore_backup(cls):
        pass

    def handle_backup_key(cls):
        foo = None
        if foo == "make":
            SystemAdministratorInterface.make_backend_backup(cls)
        elif foo == "share":
            backup_key = cls.__share_backup_key(cls)
        elif foo == "generate":
            cls.__generate_backup_key(cls)
        elif foo == "revoke":
            cls.__revoke_backup_key(cls)
        pass

    def __share_backup_key(cls):
        pass

    def __generate_backup_key(cls):
        pass

    def __revoke_backup_key(cls):
        pass
