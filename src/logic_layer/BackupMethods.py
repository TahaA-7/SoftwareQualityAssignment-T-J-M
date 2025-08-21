from logic_layer.BackupService import BackupService
from access_layer.db.UserData import user_data

from enum import Enum
from presentation_layer.utils.Roles import Roles
from presentation_layer.utils.Session import Session


class BackupMethods:
    def __init__(self):
        self.backup_service = BackupService()
        self.user_data = user_data()

    def create_backup(self):
        # Function only for super admins
        if Session.user.role.value != 3:
            return None
        self.backup_service.create_backup()
    #

    def assign_backup(self):
            # Function only for super admins
        if Session.user.role.value != 3:
            return None
        username = input("Enter System Admin username: ").strip()
        
        for user in self.user_data.get_all_users():
            if user[1].lower() == username.lower() and int(user[3]) == Roles.SYSTEM_ADMINISTRATOR.value:
                backup_filename = self.backup_service.create_backup()
                self.backup_service.generate_restore_code(backup_filename, username)
                return

        print("No System Administrator with that username.")

    def restore_backup(self):
        # Function not accessible for service engineers
        if Session.user.role.value not in (2, 3):
            return None
        
        code = input("Enter restore code: ").strip()
        username = input("Enter your username: ").strip()
        self.backup_service.restore_backup(code, username)

    def revoke_backup_code(self):
        # Function only for super admins
        if Session.user.role.value != 3:
            return None
        code = input("Enter restore code to revoke: ").strip()
        username = input("Enter the username it was assigned to: ").strip()
        self.backup_service.revoke_restore_code(code, username)
