import os
import zipfile
from datetime import datetime
from access_layer.db.db_context import DBContext
import uuid

class BackupService:
    def __init__(self):
        # Go one folder up from this file (to the project root)
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Set paths in the root folder
        self.db_file = os.path.join(root_path, 'urban_mobility.db')
        self.backup_dir = os.path.join(root_path, 'backups')

        self.db = DBContext()

        # Create the backups folder if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)


    def create_backup(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{timestamp}.zip"
        backup_path = os.path.join(self.backup_dir, backup_filename)

        with zipfile.ZipFile(backup_path, 'w') as zipf:
            zipf.write(self.db_file, os.path.basename(self.db_file))

        print(f"Backup successfully created: {backup_filename}")
        return backup_filename

    def generate_restore_code(self, backup_filename, username):
        code = str(uuid.uuid4())
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO backup_codes (code, assigned_to_username, backup_filename, created_at, used)
                VALUES (?, ?, ?, ?, 0)
            ''', (code, username, backup_filename, created_at))

        print(f"Restore code generated for {username}: {code}")
        return code
    
    def restore_backup(self, code, username):
        # Use context manager properly
        with self.db.connect() as conn:
            cursor = conn.cursor()

            # Find the restore code entry
            cursor.execute("SELECT backup_filename, used FROM backup_codes WHERE code = ? AND assigned_to_username = ?", (code, username))
            result = cursor.fetchone()

            if result is None:
                print("Restore code not found or not for this user.")
                return False

            # Unpack the result
            backup_filename, is_used = result

            if is_used:
                print("This restore code has already been used.")
                return False

            # Check if the backup zip file exists
            backup_file_path = os.path.join(self.backup_dir, backup_filename)
            if not os.path.exists(backup_file_path):
                print("Backup file is missing.")
                return False

            # Extract (restore) the database file
            with zipfile.ZipFile(backup_file_path, 'r') as zip_file:
                zip_file.extractall()  # Replaces the current DB

            # Mark restore code as used
            cursor.execute("UPDATE backup_codes SET used = 1 WHERE code = ?", (code,))
            print("Backup restored successfully.")
            return True

    def revoke_restore_code(self, code, username):
        with self.db.connect() as conn:
            cursor = conn.cursor()

            # Check if the restore code exists for this user
            cursor.execute("SELECT * FROM backup_codes WHERE code = ? AND assigned_to_username = ?", (code, username))
            result = cursor.fetchone()

            if result is None:
                print("No such restore code for this user.")
                return False

            # Delete the restore code
            cursor.execute("DELETE FROM backup_codes WHERE code = ?", (code,))
            print("Restore code has been revoked (deleted).")
            return True
