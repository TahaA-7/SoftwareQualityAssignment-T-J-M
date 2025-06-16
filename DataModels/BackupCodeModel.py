from datetime import datetime
import uuid


class BackupCode:
    def __init__(self, assigned_to_username, backup_filename):
        self.code = str(uuid.uuid4())
        self.assigned_to_username = assigned_to_username
        self.backup_filename = backup_filename
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.used = False
