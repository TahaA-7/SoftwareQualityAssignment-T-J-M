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

            print(">>> SYSTEM ADMINISTRATOR MANAGEMENT")
            print("[1] Add a new System Administrator")
            print("[2] Update a System Administrator")
            print("[3] Delete a System Administrator")
            print("[4] Reset System Administrator password (temporary password)")

            print("\n>>> SERVICE ENGINEER MANAGEMENT")
            print("[5] Add a Service Engineer")
            print("[6] Update a Service Engineer")
            print("[7] Delete a Service Engineer")
            print("[8] Reset Service Engineer password")

            print("\n>>> BACKUP MANAGEMENT")
            print("[9] Assign a restore code to a System Administrator")
            print("[10] Revoke a restore code")
            print("[11] Create a system backup")

            print("\n>>> USERS & LOGS")
            print("[12] View list of users and their roles")
            print("[13] View system logs")

            print("\n>>> OWN ACCOUNT")
            print("[14] Update own profile")
            print("[15] Delete own account")

            print("\n>>> TRAVELLER MANAGEMENT")
            print("[16] Add a Traveller")
            print("[17] Update a Traveller")
            print("[18] Delete a Traveller")
            print("[19] Search for a Traveller")

            print("\n>>> SCOOTER MANAGEMENT")
            print("[20] Add a Scooter")
            print("[21] Update a Scooter")
            print("[22] Delete a Scooter")

            print("\n[0] Exit")

            choice = input("Enter your choice: ")

            match choice:
                case '1': cls.add_system_administrator()
                case '2': cls.update_system_administrator()
                case '3': cls.delete_system_administrator()
                case '4': cls.reset_system_administrator_password()

                case '5': cls.add_service_engineer()
                case '6': cls.update_service_engineer()
                case '7': cls.delete_service_engineer()
                case '8': cls.reset_service_engineer_password()

                case '9': cls.share_backup_key()
                case '10': cls.revoke_backup_key()
                case '11': cls.generate_backup_key()

                case '12': cls.check_users_and_roles()
                case '13': cls.view_log_single_or_multiple()

                case '14': cls.update_cls_account_profile()
                case '15': cls.delete_cls_account()

                case '16': cls.add_traveller()
                case '17': cls.update_traveller()
                case '18': cls.delete_traveller()
                case '19': cls.view_traveller()

                case '20': cls.add_scooter()
                case '21': cls.update_scooter()
                case '22': cls.delete_scooter()

                case '0':
                    print("Exiting Super Administrator menu.")
                    Session.set_loggedin_false()
                    break
                case _:
                    print("Invalid choice. Please enter a valid number.")

    # === SUPER ADMIN–ONLY METHODS ===
    @classmethod
    def add_system_administrator(cls):
        cls.add_data_methods.addUser()

    @classmethod
    def update_system_administrator(cls):
        cls.update_data_methods.update_SystemAdmin()

    @classmethod
    def delete_system_administrator(cls):
        cls.delete_data_methods.deleteSystemAdmin()

    @classmethod
    def reset_system_administrator_password(cls):
        print("⚠️ Not yet implemented. Coming soon.")

    @classmethod
    def share_backup_key(cls):
        cls.backup_methods.assign_backup()

    @classmethod
    def revoke_backup_key(cls):
        cls.backup_methods.revoke_backup_code()

    @classmethod
    def generate_backup_key(cls):
        cls.backup_methods.create_backup()
