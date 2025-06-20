from getpass import getpass
import os, sys, platform

# Treat as an import: 
#   add the parent directory to the Python path so logic_layer, access_layer, etc. are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enum import Enum
from presentation_layer.utils.Roles import Roles
from presentation_layer.utils.Session import Session
from presentation_layer.menus.RegisterMenu import RegisterMenu
from presentation_layer.menus.LoginMenu import LoginMenu
from logic_layer.utils.TerminalClearner import TerminalCleaner
from presentation_layer.data_interfaces.ServiceEngineerInterface import ServiceEngineerInterface
from presentation_layer.data_interfaces.SystemAdministratorInterface import SystemAdministratorInterface
from presentation_layer.data_interfaces.SuperAdministratorInterface import SuperAdministratorInterface


class Home:
    @classmethod
    def start(cls):
        cls.home_screen()

    @classmethod
    def home_screen(cls):
        # getpass hides the input
        getpass(f" -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -\nPress enter to continue ")
        while True:
            TerminalCleaner.clear_terminal()
            if not Session.logged_in:
                print("""What do you want to do?
[R] register
[L] login
[E] exit program""")
                user_inp = cls.__handle_input_length(getpass(""))
                print(user_inp)
                if user_inp == 'R':
                    RegisterMenu.register()
                elif user_inp == 'L':
                    LoginMenu.login()
                    #LoginMenu.login()
                elif user_inp == 'E':
                    break
                else:
                    print("Invalid input!")
            else:
                match Session.user.role:
                    case Roles.SERVICE_ENGINEER:
                        ServiceEngineerInterface.start()  # start(Session.user)
                    case Roles.SYSTEM_ADMINISTRATOR:
                        SystemAdministratorInterface.system_start()
                    case Roles.SUPER_ADMINISTRATOR:
                        SuperAdministratorInterface.super_start()
                    case _:
                        print("INVALID ROLE")
                        print(Session.user)
                        print(Session.user.role)
                        print("DEBUG:", Session.user.role, type(Session.user.role))
                        Session.set_loggedin_false()


    @classmethod
    def __handle_input_length(cls, inp):
        user_inp = inp[-1].upper() if len(inp) > 0 else " "
        return user_inp


if __name__ == '__main__':
    # pip install maskpass
    Home.start()
