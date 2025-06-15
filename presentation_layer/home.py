from getpass import getpass
import sqlite3

def home_screen():
    getpass(f" -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -\nPress enter to continue ")
    print("""What do you want to do?
[R] register
[L] login
[E] exit program""")
    while True:
        user_inp = handle_input_length(getpass(""))
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
        email_inp = input("welcome to register page.\nEmail:")
        


def login():
    print("welcome to login page")


def handle_input_length(inp):
    user_inp = inp[-1].upper() if len(inp) > 0 else " "
    return user_inp


if __name__ == '__main__':
    home_screen()
