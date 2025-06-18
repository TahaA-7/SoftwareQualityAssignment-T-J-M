from getpass import getpass
import os, sys, platform
import sqlite3

def home_screen():
    # getpass hides the input
    getpass(f" -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -\nPress enter to continue ")
    while True:
        clear_terminal()
        print("""What do you want to do?
[R] register
[L] login
[E] exit program""")
        user_inp = handle_input_length(getpass(""))
        print(user_inp)
        if user_inp == 'R':
            register()
        elif user_inp == 'L':
            login()
        elif user_inp == 'E':
            break
        else:
            print("Invalid input!")


def register():
    while True:
        email_inp = input("welcome to register page.\nEmail: ")
        


def login():
    print("welcome to login page")


def handle_input_length(inp):
    user_inp = inp[-1].upper() if len(inp) > 0 else " "
    return user_inp


def clear_terminal():
    os.system(CLEAR)

if __name__ == '__main__':
    CLEAR = ""
    if sys.platform in ('linux', 'unix', 'macos', 'darwin'):
        CLEAR = 'clear'
    elif sys.platform in ('windows'):
        CLEAR = 'cls'
    home_screen()
