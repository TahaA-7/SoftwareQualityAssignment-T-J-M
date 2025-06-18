from .ServiceEngineerInterface import ServiceEngineerInterface

class SystemAdministratorInterface(ServiceEngineerInterface):
    def __init__(self):
        super().__init__()

    # CHECK ALL USERS
    def check_users_and_roles(self):
        pass

    # SERVICE ENGINEER
    def add_service_engineer(self):
        pass

    def update_service_engineer(self):
        # account and profile
        pass

    def delete_service_engineer(self):
        pass

    def reset_service_engineer_password(self):
        # replaces current with a temporary password
        pass

    # OWN ACCOUNT
    def update_self_account_profile(self):
        pass

    def delete_self_account(self):
        pass

    # BACKUP
    def make_backend_backup(self):
        pass

    def restore_backend_backup(self):
        # uses super-administrator generated `one-use-only` key linked to specific backup
        pass

    # LOG
    def view_log_single_or_multiple(self):
        pass

    # TRAVELLER
    def view_traveller(self):
        '''
        Note 2: The search function must accept reasonable data fields as a search key. It must also accept
        partial keys. For example, a user can search for a Traveller with a name “Mike Thomson” and customer
        ID “2123287421” by entering any of these keys: “mik”, “omso”, or “2328”, etc.
        '''
        pass
    def add_traveller(self):
        # traveller is not a user
        pass

    def update_traveller(self):
        pass

    def delete_traveller(self):
        pass

    # SCOOTER
    def add_scooter(self):
        pass

    def update_scooter(self):
        pass

    def delete_scooter(self):
        pass
