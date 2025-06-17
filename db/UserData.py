from db.db_context import DBContext

class user_data:
    def __init__(self):
        self.db = DBContext()

    def get_all_users(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, role, first_name, last_name FROM users")
            return cursor.fetchall()
        
    def add_user(self, username, hashed_password, role, first_name, last_name):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, hashed_password, role, first_name, last_name, registration_date)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            ''', (username.lower(), hashed_password, role, first_name, last_name))

    def delete_user(self, username):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username.lower(),))
