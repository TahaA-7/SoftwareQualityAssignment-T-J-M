from datetime import datetime 

# ADDED `is_active` FLAG AND GAVE IT A DEFAULT VALUE ALONG WITH `role` TO ALLOW SELF-INITIALISATION BEFORE ADMIN-VALIDATION

class User:
    def __init__(self, username: str, hashed_password: str, first_name: str, last_name: str, role="service_engineer", is_active=False):
        self.username = username.lower()
        self.hashed_password = hashed_password  # Hashed, not plain text!
        self.role = role  # "super_admin", "system_admin", "service_engineer"
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.is_active = is_active
