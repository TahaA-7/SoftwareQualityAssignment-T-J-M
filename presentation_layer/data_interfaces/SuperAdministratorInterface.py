from .SystemAdministratorInterface import SystemAdministratorInterface
from .ServiceEngineerInterface import ServiceEngineerInterface

class SuperAdministratorInterface(SystemAdministratorInterface):
    '''
    omitted methods:
        update_self_password
        ALL OWN ACCOUNT METHODS because hardcoded
    '''
    def __init__(self):
        pass

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
        SystemAdministratorInterface.delete_scooter(self)
    # SCOOTER
    def add_scooter(self):
        SystemAdministratorInterface.add_scooter(self)
    def update_scooter(self):
        SystemAdministratorInterface.update_scooter(self)
    def delete_scooter(self):
        SystemAdministratorInterface.delete_scooter(self)

    def add_system_administrator(self):
        pass

    def update_system_administrator(self):
        # account and profile
        pass

    def delete_system_administrator(self):
        pass

    def reset_system_administrator_password(self):
        pass

    def make_or_restore_backup(self):
        pass

    def handle_backup_key(self):
        foo = None
        if foo == "make":
            SystemAdministratorInterface.make_backend_backup(self)
        elif foo == "share":
            backup_key = self.__share_backup_key(self)
        elif foo == "generate":
            self.__generate_backup_key(self)
        elif foo == "revoke":
            self.__revoke_backup_key(self)
        pass

    def __share_backup_key(self):
        pass

    def __generate_backup_key(self):
        pass

    def __revoke_backup_key(self):
        pass
