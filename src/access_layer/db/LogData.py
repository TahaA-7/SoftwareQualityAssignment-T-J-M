from access_layer.db.db_context import DBContext
from presentation_layer.utils.Session import Session
from logic_layer.utils.AuthenticationAttemptsTracker import AuthenticationAttemptsTracker

class log_data:
    def __init__(self):
        self.db = DBContext()

    def get_logs(self):
        # Function accessible for system admin and super admin
        if Session.user.role.value not in (2, 3):
            return None
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, username, description, additional_info, suspicious
                FROM logs
                ORDER BY timestamp DESC
            ''')
            return cursor.fetchall()
        
        from logic_layer.utils.Logger import Logger
        from cryptography.fernet import Fernet
        key = Logger._get_key()
        fernet = Fernet(key)
        for row in rows:
            timestamp = row[0]
            username = fernet.decrypt(row[1].encode()).decode()
            description = fernet.decrypt(row[3].encode()).decode()
            suspicious = row[4]
            decrypted_rows.append((timestamp, username, description, additional_info, suspicious))
        return decrypted_rows
        
        
    def add_log(self, timestamp, username, description, additional_info="", suspicious=False):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (timestamp, username, description, additional_info, suspicious)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, username, description, additional_info, suspicious))
            conn.commit()
