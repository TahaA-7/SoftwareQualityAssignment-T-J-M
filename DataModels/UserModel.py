from datetime import datetime 
from presentation_layer.utils.Roles import Roles

# ADDED `is_active` FLAG AND GAVE IT A DEFAULT VALUE ALONG WITH `role` TO ALLOW SELF-INITIALISATION BEFORE ADMIN-VALIDATION

class User:
    def __init__(self, username: str, hashed_password: str, first_name: str, last_name: str, role=Roles.SERVICE_ENGINEER, is_active=False):
        self.username = username.lower()
        self.hashed_password = hashed_password  # Hashed, not plain text!
        self.role = role  # "super_admin=3", "system_admin=2", "service_engineer=1"
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.is_active = is_active
