from access_layer.db.db_context import DBContext
from presentation_layer.utils.Roles import Roles
from presentation_layer.utils.Session import Session
from logic_layer.utils.Logger import Logger
from cryptography.fernet import Fernet

from logic_layer.utils.AuthenticationAttemptsTracker import AuthenticationAttemptsTracker

import uuid

class user_data:
    def __init__(self):
        self.db = DBContext()

    # NEW
    def _get_encryption_key(self):
        return Logger._get_key()
    
    # NEW
    def _encrypt_name(self, name):
        if not name:
            return name
        key = self._get_encryption_key()
        fernet = Fernet(key)
        return fernet.encrypt(name.encode()).decode()
    
    # NEW
    def _decrypt_name(self, encrypted_name):
        if not encrypted_name:
            return encrypted_name
        try:
            key = self._get_encryption_key()
            fernet = Fernet(key)
            return fernet.decrypt(encrypted_name.encode()).decode()
        except Exception:
            return encrypted_name  
        
        # ------- verder gaan vanaf onder , dus bij fetch user ------------------------
        # -----------------------------------------------------------------------------

    def fetch_user(self, username_or_id):
        # Should be accessible by all since this function is used to log in
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT id, username, hashed_salted_password, role, first_name, last_name, 
                    is_active FROM users WHERE id = ?""", (username_or_id,))
                fetched = cursor.fetchone()
                if fetched:
                    decrypted = list(fetched)
                    decrypted[1] = self._decerypt_name(fetched[1]) # username
                    decrypted[4] = self._decrypt_name(fetched[4])
                    decrypted[5] = self._decrypt_name(fetched[5])
                    return tuple(decrypted)
                
                cursor.execute("""SELECT id, username, hashed_salted_password, role, first_name, last_name, 
                    is_active FROM users""")
                all_users = cursor.fetchall()
                
                for user in all_users:
                    decrypted_username = self._decrypt_name(user[1])
                    if decrypted_username.lower() == username_or_id.lower():
                        decrypted = list(user)
                        decrypted[1] = decrypted_username  # username
                        decrypted[4] = self._decrypt_name(user[4])  # first_name
                        decrypted[5] = self._decrypt_name(user[5])  # last_name
                        return tuple(decrypted)
                
                return None
        except Exception:
            return None
            

    def get_all_users(self):
        # function not allowed for system admins to view the users data
        # if Session.user.role.value not in (2, 3):
        #     return None
        # with self.db.connect() as conn:
        #     cursor = conn.cursor()
        #     cursor.execute("SELECT * FROM users")
        #     rows =  cursor.fetchall()
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            
            decrypted_users = []
            for row in rows:
                decrypted_row = list(row)
                decrypted_row[1] = self._decrypt_name(row[1]) # username
                decrypted_row[4] = self._decrypt_name(row[4])
                decrypted_row[5] = self._decrypt_name(row[5])
                decrypted_users.append(tuple(decrypted_row))

            return decrypted_users
        
    def add_user(self, id, username, hashed_salted_password, first_name, last_name, user_to_add_type=Roles.SERVICE_ENGINEER.value):
        # system and/or system admin
        if id in ["", None]: id = str(uuid.uuid4())
        # can't add super admins, and system admins can't add other system admins
        if user_to_add_type >= Session.user.role.value:
            return None
        
        encrypted_username = self._encrypt_name(username.lower())
        encrypted_first_name = self._encrypt_name(first_name)
        encrypted_last_name = self._encrypt_name(last_name)
        

        # ^ not necessary since the add system admin method is only accessible by a super admin through the presentation layer anyway
        with self.db.connect() as conn:
            cursor = conn.cursor()
            try:
                if self.fetch_user(username) == None:
                    cursor.execute('''
                        INSERT INTO users (id, username, hashed_salted_password, role, first_name, last_name, registration_date, is_active)
                        VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
                    ''', (id, encrypted_username, hashed_salted_password, user_to_add_type, encrypted_first_name, encrypted_last_name, True))
                    return True
                return False
            except Exception:
                return False
            
    # def add_serviceEngineer(self, id, username, hashed_salted_password, first_name, last_name):
    #     if id in ["", None]: id = str(uuid.uuid4())
    #     if Session.user.role.value not in (2, 3):
    #         return None
    #     with self.db.connect() as conn:
    #         cursor = conn.cursor()
    #         try:
    #             cursor.execute('''
    #                 INSERT INTO users (id, username, hashed_salted_password, role, first_name, last_name, registration_date, is_active)
    #                 VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
    #             ''', (id, username.lower(), hashed_salted_password, Roles.SERVICE_ENGINEER.value, first_name, last_name, False))
    #             return True
    #         except Exception:
    #             return False
            
    # def add_systemAdmin(self, id, username, hashed_salted_password, first_name, last_name):
    #     if id in ["", None]: id = str(uuid.uuid4())
    #     with self.db.connect() as conn:
    #         cursor = conn.cursor()
    #         try:
    #             cursor.execute('''
    #                 INSERT INTO users (id, username, hashed_salted_password, role, first_name, last_name, registration_date, is_active)
    #                 VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
    #             ''', (id, username.lower(), hashed_salted_password, Roles.SYSTEM_ADMINISTRATOR.value, first_name, last_name, False))
    #             return True
    #         except Exception:
    #             return False

    def delete_user(self, username_or_id, user_to_delete_type):
        if Session.user.role.value == 1: 
            return None
        elif Session.user.role.value == 2:
            # system admins can delete own account, but no other admins
            if username_or_id != Session.user.user_id:
                return None
            if user_to_delete_type > 2:
                return None
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                
                # First try by ID
                cursor.execute("DELETE FROM users WHERE id = ?", (username_or_id,))
                if cursor.rowcount > 0:
                    return True
                
                # Then try by finding encrypted username
                user = self.fetch_user(username_or_id)
                if user:
                    cursor.execute("DELETE FROM users WHERE id = ?", (user[0],))
                    return cursor.rowcount > 0
                
                return False
        except Exception:
            return False

    def update_user_profile(self, original_username, username, first_name, last_name):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                
                # First get the user
                user = self.fetch_user(original_username)
                if not user:
                    print("User not found.")
                    return False
                
                user_id = user[0]
                user_role = user[3]
                
                # Cannot update a user with a higher rank
                if int(user_role) > int(Session.user.role.value):
                    return False
                
                # Get current decrypted values
                current_username = user[1]
                current_first_name = user[4]
                current_last_name = user[5]

                # Use current value if input is blank
                username = username if username and username.strip() != "" else current_username
                first_name = first_name if first_name and first_name.strip() != "" else current_first_name
                last_name = last_name if last_name and last_name.strip() != "" else current_last_name

                # Encrypt the new values
                encrypted_username = self._encrypt_name(username.lower())
                encrypted_first_name = self._encrypt_name(first_name)
                encrypted_last_name = self._encrypt_name(last_name)
 
                cursor.execute('''
                    UPDATE users
                    SET username = ?, first_name = ?, last_name = ?
                    WHERE id = ?
                ''', (encrypted_username, encrypted_first_name, encrypted_last_name, user_id))
                return cursor.rowcount > 0
        except Exception as ex:
            print(ex)
            return False

    def update_user_password(self, username_or_id, hashed_salted_password):
        try:
            # Get the user first
            user = self.fetch_user(username_or_id)
            if not user:
                print("User not found.")
                return False
            
            user_id = user[0]
            user_role = user[3]
            
            if int(user_role) > int(Session.user.role.value):
                return False

            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users
                    SET hashed_salted_password = ?
                    WHERE id = ?
                ''', (hashed_salted_password, user_id))
                return cursor.rowcount > 0
        except Exception as ex:
            print(ex)
            return False
        