from logic_layer.BackupService import BackupService
from access_layer.db.UserData import user_data

class BackupMethods:
    def __init__(self):
        self.backup_service = BackupService()
        self.user_data = user_data()

    def create_backup(self):
        self.backup_service.create_backup()

    def assign_backup(self):
        username = input("Enter System Admin username: ").strip()
        
        for user in self.user_data.get_all_users():
            if user[0].lower() == username.lower() and user[1].lower() == "system_admin":
                backup_filename = self.backup_service.create_backup()
                self.backup_service.generate_restore_code(backup_filename, username)
                return

        print("No System Administrator with that username.")

    def restore_backup(self):
        code = input("Enter restore code: ").strip()
        username = input("Enter your username: ").strip()
        self.backup_service.restore_backup(code, username)

    def revoke_backup_code(self):
        code = input("Enter restore code to revoke: ").strip()
        username = input("Enter the username it was assigned to: ").strip()
        self.backup_service.revoke_restore_code(code, username)
