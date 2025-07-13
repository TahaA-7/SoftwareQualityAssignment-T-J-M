from logic_layer.utils.TerminalClearner import TerminalCleaner
from logic_layer.utils.StringValidations import StringValidations
from logic_layer.utils.Logger import Logger

from logic_layer.AddMethods import AddDataService

from presentation_layer.menus.CreateOrUpdateMenu import CreateOrUpdateMenu


import re
import time
import datetime
import uuid
import maskpass
from getpass import getpass


class CreateOrUpdateEmployee(CreateOrUpdateMenu):
    user_type = "employee"
    def menu(self):
        print("""Welcome
-   -   -   -   -   -   -""")
        while True:
            print([f for f in self._get_employee_fields_dict().items()])
            user_choice = self._handle_input_length(getpass(
f"""Please select a field and set it to a (new) value or leave blank to keep old value (in case of update)

[A] employee username {"✓" if self._get_employee_fields_dict()["username"] not in [None, ""] else ""}
[B] employee password {"✓" if self._get_employee_fields_dict()["password"] not in [None, ""] else ""}
[C] first name {"✓" if self._get_employee_fields_dict()["first_name"] not in [None, ""] else ""}
[D] last name {"✓" if self._get_employee_fields_dict()["last_name"] not in [None, ""] else ""}

[1] submit register
[2] submit update to existing account/profile
[3] cancel
"""))
            
            match user_choice:
                case "A":
                    self._handle_username()
                case "B":
                    self._handle_password()
                case "C":
                    self._handle_first_name_submit("emp")
                case "D":
                    self._handle_last_name_submit("emp")

                case "1":
                    self._handle_register()
                    break
                case "2":
                    self._handle_update()
                    break
                case "3":
                    break
                case _:
                    print("Invalid choice")

    def _handle_register(self):
        self.user_id = str(uuid.uuid4())
        if "" not in self._get_employee_fields_dict().items():
            add_data_service_obj = AddDataService()
            added_user = add_data_service_obj.addUser(
                self.username, self.password, self.u_fname, self.u_lname, self.user_type)
            if added_user != None:
                Logger.log(self.username, "Registered new account")
                print("User registered succesfully.")
            else:
                Logger.log(self.username, "Registration failed", "User already exists", suspicious=True)
                print("Error: user already exists")
        else:
            print("""Error: cannot submit because username and/or email and/or password has remained blank,'
either because left unhandled or couldn't be updated due to an invalid input.""")

    def _handle_update(self):
        return super()._handle_update(self.user_type)
