# python -m pip install maskpass
import maskpass

from getpass import getpass
import time

from presentation_layer.utils.Session import Session
from logic_layer.utils.StringValidations import StringValidations
from logic_layer.GetDataMethods import GetDataService
from logic_layer.utils.Logger import Logger

from logic_layer.utils.TerminalClearner import TerminalCleaner

# from data_interfaces.SystemAdministratorInterface import SystemAdministratorInterface # temp

class LoginMenu:
    username = password = ""
    user = None
    @classmethod
    def get_fields_dict(cls):
        return {"username": cls.username, "password": "" if "" else len(cls.password) * "*"}
    
    @classmethod
    def login(cls):
        TerminalCleaner.clear_terminal()
        # from home import Home # Place here instead of atop the file to avoid circular import
        print("""Welcome to login page'
-   -   -   -   -   -   -""")
        while True:
            print([f for f in cls.get_fields_dict().items()])
            user_choice = cls.__handle_input_length(getpass(
f"""Please select a field and update it:
[U] username {"✓" if cls.get_fields_dict()["username"] not in [None, ""] else ""}
[P] password {"✓" if cls.get_fields_dict()["password"] not in [None, ""] else ""}

[L] login
[C] cancel\n"""))
            match user_choice:
                case _ if user_choice not in ["U", "P", "F", "L", "S", "C"]:
                    print("Invalid choice")
                case "U":
                    cls.__handle_username()
                # case "E":
                #     cls.handle_email()
                case "P":
                    cls.__handle_password()
                case "L":
                    if cls.__handle_submit():
                        Session.set_loggedin_true(cls.user)
                        break
                    else:
                        continue
                case "C":
                    cls.username = cls.password = cls.first_name = cls.last_name = ""
                    break

    @classmethod
    def __handle_username(cls):
        inp = input("Please enter username: ")
        cls.username = inp if StringValidations.is_valid_username(inp) else ""

    @classmethod
    def __handle_password(cls):
        inp = maskpass.askpass(prompt="Please enter password: ", mask="*")
        cls.password = inp if StringValidations.is_valid_password(inp) else ""

    @classmethod
    def __handle_submit(cls):
        if "" not in [cls.username, cls.password]:
            obj = GetDataService()
            fetched_user = obj.get_user(cls.username, cls.password)
            if fetched_user != None:
                if fetched_user['role'] == 3:
                    cls.user = fetched_user
                    print("Login succesfull")
                    time.sleep(0.5)
                    return True
                elif fetched_user['is_active']:
                    Logger.log(fetched_user['username'], "Logged in", additional_info=fetched_user['role'], suspicious=False)
                    cls.user = fetched_user
                    print("Login succesfull")
                    time.sleep(0.5)
                    return True
                else:
                    print("User is awaiting registration approval or is blacklisted")
                    time.sleep(0.5)
                    return False
            else:
                Logger.log(cls.username, "Unsuccesfull login", additional_info="Invalid credentials", suspicious=True)
                print("Error: no user found with current credentials")
                time.sleep(0.75)
                return False
        else:
            print("Error: please fill in all fields!")
            time.sleep(0.75)
            return False

    @classmethod
    def __handle_input_length(cls, inp):
        user_inp = inp[-1].upper() if len(inp) > 0 else " "
        return user_inp
