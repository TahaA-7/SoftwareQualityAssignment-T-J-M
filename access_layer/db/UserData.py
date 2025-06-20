from access_layer.db.db_context import DBContext
from presentation_layer.utils.Roles import Roles

class user_data:
    def __init__(self):
        self.db = DBContext()

    def get_all_users(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, hashed_salted_password, role, first_name, last_name, is_active FROM users")
            return cursor.fetchall()
        
    def add_user(self, username, hashed_salted_password, first_name, last_name):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (username, hashed_salted_password, role, first_name, last_name, registration_date, is_active)
                    VALUES (?, ?, ?, ?, ?, datetime('now'), ?)
                ''', (username.lower(), hashed_salted_password, Roles.SERVICE_ENGINEER.value, first_name, last_name, False))
                return True
            except Exception:
                return False

    def delete_user(self, username):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username.lower(),))

    def update_user_profile(self, username, first_name, last_name):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET first_name = ?, last_name = ?
                WHERE username = ?
            ''', (first_name, last_name, username.lower()))

    def update_user_password(self, username, hashed_salted_password):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users
                    SET hashed_salted_password = ?
                    WHERE username = ?
                ''', (hashed_salted_password, username.lower()))
            return True
        except Exception:
            return False
