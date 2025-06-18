from getpass import getpass
import os, sys, platform

# Treat as an import: 
#   add the parent directory to the Python path so logic_layer, access_layer, etc. are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from enum import Enum
from menus.RegisterMenu import RegisterMenu
from logic_layer.utils.TerminalClearner import TerminalCleaner
from presentation_layer.data_interfaces.ServiceEngineerInterface import ServiceEngineerInterface
from presentation_layer.data_interfaces.SystemAdministratorInterface import SystemAdministratorInterface
from presentation_layer.data_interfaces.SuperAdministratorInterface import SuperAdministratorInterface

# class Roles(Enum):
#     SERVICE_ENGINEER = 1
#     SYSTEM_ADMINISTRATOR = 2
#     SUPER_ADMINISTRATOR = 3

class Home:
    logged_in = False
    user = None

    @classmethod
    def start(cls):
        cls.home_screen()

    @classmethod
    def home_screen(cls):
        # getpass hides the input
        getpass(f" -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -\nPress enter to continue ")
        while True:
            if not cls.logged_in:
                TerminalCleaner.clear_terminal()
                print("""What do you want to do?
[R] register
[L] login
[E] exit program""")
                user_inp = cls.__handle_input_length(getpass(""))
                print(user_inp)
                if user_inp == 'R':
                    RegisterMenu.register()
                elif user_inp == 'L':
                    pass
                    #LoginMenu.login()
                elif user_inp == 'E':
                    break
                else:
                    print("Invalid input!")
            else:
                match cls.user:
                    case 1:
                        ServiceEngineerInterface.start(cls.user)
                    case 2:
                        SystemAdministratorInterface.start(cls.user)
                    case 3:
                        SuperAdministratorInterface.start(cls.user)
                        


    @classmethod
    def __handle_input_length(cls, inp):
        user_inp = inp[-1].upper() if len(inp) > 0 else " "
        return user_inp

    @classmethod
    def set_loggedin_true(cls, fetched_user=None):
        cls.logged_in = True
        cls.user = fetched_user


if __name__ == '__main__':
    # pip install maskpass
    Home.start()
