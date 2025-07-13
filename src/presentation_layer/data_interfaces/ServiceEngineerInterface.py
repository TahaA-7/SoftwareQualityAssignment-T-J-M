from logic_layer.utils.StringValidations import StringValidations

from logic_layer.UpdateMethods import UpdateDataService
from logic_layer.GetDataMethods import GetDataService

from DataModels.ScooterModel import Scooter

from getpass import getpass

from presentation_layer.utils.Session import Session

import maskpass


class ServiceEngineerInterface():
    get_data_methods = GetDataService()
    update_data_methods = UpdateDataService()
    # service engineer is standard user
    def __init__(cls, ):
        pass

    @classmethod
    def start(cls):
        print("""Welcome to service engineer interface'
-   -   -   -   -   -   -""")
        while True:
            cls.get_data_methods = GetDataService()
            cls.update_data_methods = UpdateDataService()
            user_choice = StringValidations.handle_input_length(getpass(
f"""What do you want to do?:
[1] update own password
[2] update a scooter's attributes
[3] search a scooter

[L] logout\n"""))
            match user_choice:
                case '1':
                    cls.update_own_password()
                case '2':
                    cls.update_scooter_attributes()
                case '3':
                    cls.view_scooter()

                case 'L':
                    Session.set_loggedin_false()
                    break
                case _:
                    print("Invalid input!")
                    continue

    @classmethod
    def update_own_password(cls):
        updatedataservice_obj = UpdateDataService()
        new_password = maskpass.askpass(prompt="Please enter new password: ", mask="*")
        confirm_new_password = maskpass.askpass(prompt="Please confirm new password: ", mask="*")
        if not StringValidations.is_valid_password(new_password) or new_password != confirm_new_password:
            return False
        else:
            if updatedataservice_obj.updateUser_password(Session.user.username, new_password):
                print("User profile updated.")
            else:
                print("Error: password couldn't be updated.")
            

    @classmethod
    def update_scooter_attributes(cls):
        updatedataservice_obj = UpdateDataService()
        getdataservice_obj = GetDataService()
        brand_model_input = input(
            "Please enter a brand and model name, separated by a triple hypen (---): ")
        if brand_model_input.count("---") == 1:
            brand_input, model_input = brand_model_input.split(
                "---")
        else:
            print("Invalid input")
            return None
        
        scooter_obj = getdataservice_obj.get_scooter(brand_input, model_input)
        if scooter_obj != None: # and type(scooter_obj, Scooter)
            state_of_charge_input = input("Please enter new State of Charge or leave empty: ")
            target_rage_SoC_input = input(
                "Please enter new targe-range State of Charge, split by a triple hyphen (---) or leave empty: ")
            location_input = input(
                "Please enter current GPS coordinates by latitude and longitude, split by triple hypen (---) or leave empty: "
                )
            out_of_service_status_input = input(
                "Is scooter still in service? If not, please enter details else leave empty: "
                )
            mileage_input = input("Please enter new total distance travelled in kilometers or leave empty: ")
            last_maintenance_date_input = input(
                "Please enter date of last maintenance in YYYY-MM-DD format or leave empty: "
                )

            scooter_updated = updatedataservice_obj.updateScooterAttributes(scooter_obj,
                state_of_charge_input, target_rage_SoC_input, location_input,
                  out_of_service_status_input, mileage_input, last_maintenance_date_input)
            return scooter_updated
        else:
            return None

    @classmethod
    def view_scooter(cls):
        # search scooter info
        '''
        Note 2: The search function must accept reasonable data fields as a search key. It must also accept
        partial keys. For example, a user can search for a Traveller with a name “Mike Thomson” and customer
        ID “2123287421” by entering any of these keys: “mik”, “omso”, or “2328”, etc.
        '''
        getdataservice_obj = GetDataService()
        user_input = input("Please enter a (part of a) brand or model name to search by: ")
        scooters = getdataservice_obj.search_scooters(user_input)
        for scooter in scooters:
            print(scooter)
