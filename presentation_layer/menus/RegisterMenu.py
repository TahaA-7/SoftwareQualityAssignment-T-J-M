# python -m pip install maskpass
import maskpass

from getpass import getpass
import time
from logic_layer.utils.StringValidations import StringValidations
from logic_layer.AddMethods import AddDataService
from logic_layer.utils.Logger import Logger

class RegisterMenu:
    # initialise each as "", from then each are individually manipulable
    username = password = first_name = last_name = ""
    @classmethod
    def get_fields_dict(cls):
        return {
            "username": cls.username,
            "password": "" if "" else len(cls.password) * "*",
            "first_name": cls.first_name,
            "last_name": cls.last_name
        }

    @classmethod
    def register(cls):
        print("""Welcome to register page'
-   -   -   -   -   -   -""")
        while True:
            print([f for f in cls.get_fields_dict().items()])
            user_choice = cls.__handle_input_length(getpass(
f"""Please select a field and update it:
[U] username {"✓" if cls.get_fields_dict()["username"] not in [None, ""] else ""}
[P] password {"✓" if cls.get_fields_dict()["password"] not in [None, ""] else ""}
[F] first name {"✓" if cls.get_fields_dict()["first_name"] not in [None, ""] else ""}
[L] last name {"✓" if cls.get_fields_dict()["last_name"] not in [None, ""] else ""}

[S] submit
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
                case "F":
                    cls.__handle_first_name_submit()
                case "L":
                    cls.__handle_last_name_submit()
                case "S":
                    if cls.__handle_submit() == False:
                        continue
                    break
                case "C":
                    cls.username = cls.password = cls.first_name = cls.last_name = ""
                    break

    @classmethod
    def __handle_username(cls):
        username_input = input("""Please enter your username:
    ○ must be unique and have a length of at least 8 characters
    ○ must be no longer than 10 characters
    ○ must be started with a letter or underscores (_)
    ○ can contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (,)
    ○ no distinction between lowercase and uppercase letters (case-insensitive):\n""")
        if StringValidations.is_valid_username(username_input) == False:
            print("Invalid username")
            time.sleep(0.75)
        else:
            print("Username set succesfully")
            time.sleep(0.75)
            cls.username = username_input

    # def handle_email(cls):
    #     email_input = input("Please enter your email. It is used for password recovery, so please use your legitimate one:\n")
    #     if StringValidations.is_valid_username(email_input) == False:
    #         print("Invalid email")
    #     else:
    #         cls.email = email_input.lower()

    @classmethod
    def __handle_password(cls):
        print(r"""Password:
    ○ must have a length of at least 12 characters
    ○ must be no longer than 30 characters
    ○ can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%&_-
    +=`|\(){}[]:;'<>,.?/
    ○ must have a combination of at least one lowercase letter, one uppercase letter, one digit,
    and one special character:""")
        password_input = maskpass.askpass(prompt="", mask="*")
        confirm_password_input = maskpass.askpass(prompt="Please confirm your password: ", mask="*")
        if StringValidations.is_valid_password(password_input) == False or password_input != confirm_password_input:
            print("Invalid password")
            time.sleep(0.75)
        else:
            print("Password set succesfully")
            time.sleep(0.75)
            cls.password = password_input
    
    @classmethod
    def __handle_submit(cls):
        # if "" not in [cls.username, cls.email, cls.password]:
        if "" not in [cls.username, cls.password, cls.first_name, cls.last_name]:
            add_Data_Service_obj = AddDataService()
            added_user = add_Data_Service_obj.addUser(cls.username, cls.password, cls.first_name, cls.last_name)
            if added_user != None:
                Logger.log(cls.username, "Registered new account")
                print("User registered succesfully and is now awaiting approval by an admin.")
            else:
                Logger.log(cls.username, "Registration failed", "User already exists", suspicious=True)
                print("Error: user already exists")
        else:
            print("""Error: cannot submit because username and/or email and/or password has remained blank,'
either because left unhandled or couldn't be updated due to an invalid input.""")
        time.sleep(0.75)

    @classmethod
    def __handle_first_name_submit(cls):
        name_input = input("Please enter your first name: ")
        if StringValidations.is_valid_first_or_last_name(name_input) == False:
            print("Invalid first name")
            time.sleep(0.75)
        else:
            print("First name set succesfully")
            time.sleep(0.75)
            cls.first_name = name_input

    @classmethod
    def __handle_last_name_submit(cls):
        name_input = input("Please enter your last name: ")
        if StringValidations.is_valid_first_or_last_name(name_input) == False:
            print("Invalid last name")
            time.sleep(0.75)
        else:
            print("Last name set succesfully")
            time.sleep(0.75)
            cls.last_name = name_input

    @classmethod
    def __handle_input_length(cls, inp):
        user_inp = inp[-1].upper() if len(inp) > 0 else " "
        return user_inp
