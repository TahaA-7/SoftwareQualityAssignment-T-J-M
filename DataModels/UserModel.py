from datetime import datetime


class User:
    def __init__(self, username, hashed_password, role, first_name, last_name):
        self.username = username.lower()
        self.hashed_password = hashed_password  # Hashed, not plain text!
        self.role = role  # "super_admin", "system_admin", "service_engineer"
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')