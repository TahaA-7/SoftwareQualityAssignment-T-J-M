from logic_layer.utils.StringValidations import StringValidations
from getpass import getpass

class ServiceEngineerInterface():
    # service engineer is standard user
    def __init__(cls, ):
        pass

    @classmethod
    def start(cls):
        print("""Welcome to service engineer interface'
-   -   -   -   -   -   -""")
        while True:
            user_choice = cls.__handle_input_length(getpass(
f"""What do you want to do?:
[1] update own password
[2] update a scooter's attributes
[3] search a scooter

[L] logout\n"""))

    @classmethod
    def update_own_password(cls):
        new_password = input("Please enter new password")
        if StringValidations.is_valid_password(new_password):
            return False
        else:
            # update_password
            pass

    @classmethod
    def update_scooter_attributes(cls):
        # print scooters
        # if user is service engineer, rights are limited
        pass

    @classmethod
    def view_scooter(cls):
        # search scooter info
        '''
        Note 2: The search function must accept reasonable data fields as a search key. It must also accept
        partial keys. For example, a user can search for a Traveller with a name “Mike Thomson” and customer
        ID “2123287421” by entering any of these keys: “mik”, “omso”, or “2328”, etc.
        '''
        pass

    @classmethod
    def __handle_input_length(cls, inp):
        user_inp = inp[-1].upper() if len(inp) > 0 else " "
        return user_inp
