from access_layer.db.db_context import DBContext
from presentation_layer.utils.Roles import Roles
# from presentation_layer.utils.Session import Session

import uuid

class user_data:
    def __init__(self):
        self.db = DBContext()

    def fetch_user(self, username_or_id):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT id, username, hashed_salted_password, role, first_name, last_name, 
                    is_active FROM users WHERE id = ?""", (username_or_id,))
                fetched = cursor.fetchone()
                if fetched is not None:
                    return fetched
                cursor.execute("""SELECT id, username, hashed_salted_password, role, first_name, last_name, 
                    is_active FROM users WHERE username = ?""", (username_or_id.lower(),))
                return cursor.fetchone()
        except Exception:
            return None

    def get_all_users(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
        
    def add_user(self, id, username, hashed_salted_password, first_name, last_name, user_type=Roles.SERVICE_ENGINEER.value):
        if id in ["", None]: id = str(uuid.uuid4())
        # if user_type > 1 and Session.user.role.value != 3:
        #     return None
        # ^ not necessary since the add system admin method is only accessible by a super admin through the presentation layer anyway
        with self.db.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (id, username, hashed_salted_password, role, first_name, last_name, registration_date, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
                ''', (id, username.lower(), hashed_salted_password, user_type, first_name, last_name, False))
                return True
            except Exception:
                return False
            
    def add_serviceEngineer(self, id, username, hashed_salted_password, first_name, last_name):
        if id in ["", None]: id = str(uuid.uuid4())
        with self.db.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (id, username, hashed_salted_password, role, first_name, last_name, registration_date, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
                ''', (id, username.lower(), hashed_salted_password, Roles.SERVICE_ENGINEER.value, first_name, last_name, False))
                return True
            except Exception:
                return False
            
    def add_systemAdmin(self, id, username, hashed_salted_password, first_name, last_name):
        if id in ["", None]: id = str(uuid.uuid4())
        with self.db.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (id, username, hashed_salted_password, role, first_name, last_name, registration_date, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
                ''', (id, username.lower(), hashed_salted_password, Roles.SYSTEM_ADMINISTRATOR.value, first_name, last_name, False))
                return True
            except Exception:
                return False

    def delete_user(self, username_or_id):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM users WHERE id = ? OR LOWER(username) = ?",
                    (username_or_id, username_or_id.lower())
                )
                return cursor.rowcount > 0
        except Exception:
            return False

    def update_user_profile(self, original_username, username, first_name, last_name):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                # Fetch current values
                cursor.execute('''
                    SELECT username, first_name, last_name FROM users WHERE username = ?
                ''', (original_username,))
                row = cursor.fetchone()
                if not row:
                    print("User not found.")
                    return False
                current_username, current_first_name, current_last_name = row
                # Use current value if input is blank
                username = username if username.strip() != "" else current_username
                first_name = first_name if first_name.strip() != "" else current_first_name
                last_name = last_name if last_name.strip() != "" else current_last_name
                cursor.execute('''
                    UPDATE users
                    SET username = ?, first_name = ?, last_name = ?
                    WHERE username = ?
                ''', (username.lower(), first_name, last_name, original_username))
                return cursor.rowcount > 0
        except Exception:
            return False

    def update_user_password(self, username_or_id, hashed_salted_password):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users
                    SET hashed_salted_password = ?
                    WHERE username = ?
                ''', (hashed_salted_password, username_or_id.lower()))

                if cursor.rowcount > 0:
                    return True
                cursor.execute('''
                    UPDATE users
                    SET hashed_salted_password = ?
                    WHERE id = ?
                ''', (hashed_salted_password, username_or_id))
                return cursor.rowcount > 0
        except Exception:
            return False
