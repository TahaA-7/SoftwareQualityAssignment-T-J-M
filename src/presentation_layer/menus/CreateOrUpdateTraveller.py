from access_layer.db.TravellerData import traveller_data

from logic_layer.utils.TerminalClearner import TerminalCleaner
from logic_layer.utils.StringValidations import StringValidations
from logic_layer.utils.Logger import Logger

from logic_layer.AddMethods import AddDataService

from presentation_layer.menus.CreateOrUpdateMenu import CreateOrUpdateMenu

import random, uuid
import re, string
import time, datetime
import maskpass
from getpass import getpass


class CreateOrUpdateTraveller(CreateOrUpdateMenu):
    def menu(self):
        print("""Welcome
-   -   -   -   -   -   -""")
        while True:
            self.traveller_data_obj = traveller_data()
            print([f for f in self._get_traveller_fields_dict().items()])
            user_choice = self._handle_input_length(getpass(
f"""Please select a field and set it to a (new) value

[E] traveller first name {"✓" if self._get_traveller_fields_dict()["first_name"] not in [None, ""] else ""}
[F] traveller last name {"✓" if self._get_traveller_fields_dict()["last_name"] not in [None, ""] else ""}
[G] traveller birthday {"✓" if self._get_traveller_fields_dict()["birthday"] not in [None, ""] else ""}
[H] traveller gender {"✓" if self._get_traveller_fields_dict()["gender"] not in [None, ""] else ""}
[I] traveller street {"✓" if self._get_traveller_fields_dict()["street"] not in [None, ""] else ""}
[J] traveller house number {"✓" if self._get_traveller_fields_dict()["house_number"] not in [None, ""] else ""}
[K] traveller zip code {"✓" if self._get_traveller_fields_dict()["zip_code"] not in [None, ""] else ""}
[L] traveller city {"✓" if self._get_traveller_fields_dict()["city"] not in [None, ""] else ""}
[M] traveller email {"✓" if self._get_traveller_fields_dict()["email"] not in [None, ""] else ""}
[N] traveller phone {"✓" if self._get_traveller_fields_dict()["phone"] not in [None, ""] else ""}
[O] traveller license number {"✓" if self._get_traveller_fields_dict()["license_number"] not in [None, ""] else ""}

[1] submit register
[2] submit update to existing account/profile
[3] cancel
"""))
            
            match user_choice:
                case "E":
                    self._handle_first_name_submit("trav")
                case "F":
                    self._handle_last_name_submit("trav")
                case "G": 
                    self._handle_trav_birthday()
                case "H":
                    self._handle_trav_gender()
                case "I":
                    self._handle_trav_street()
                case "J":
                    self._handle_trav_house_number()
                case "K":
                    self._handle_trav_zip_code()
                case "L":
                    self._handle_trav_city()
                case "M":
                    self._handle_trav_email()
                case "N":
                    self._handle_trav_phone()
                case "O":
                    self._handle_license_number()
                    
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
        self.customer_id = str(uuid.uuid4())
        self.registration_date = datetime.date.today()
        self.license_number = self._generate_license_number()
        if "" not in self._get_traveller_fields_dict().items():
            add_data_service_obj = AddDataService()
            added_traveller = add_data_service_obj.addTraveller(self.customer_id, self.registration_date, 
                self.c_fname, self.c_lname, self.bday, self.gender, self.street, self.house_number,
                self.zip, self.city, self.c_email, self.phone, self.license_number)
            if added_traveller:
                Logger.log(self.customer_id, "Registered new traveller")
                print("Traveller registered succesfully.")
            else:
                Logger.log(self.username, "Registration failed", "Traveller already exists", suspicious=True)
                print("Error: traveller already exists")
        else:
            print("Error: cannot submit because one or more fields remained blank " + 
"either because left unhandled or couldn't be updated due to an invalid input.")

    # def _generate_license_number(self):
    #     # unique license number in `XXDDDDDDD` or `XDDDDDDDD` format
    #     existing_licenses = {trav['license_number'] for trav in self.traveller_data_obj.get_travellers()}
    #     while True:
    #         # Randomly choose format
    #         if random.choice([True, False]):
    #             # XXDDDDDDD
    #             lic = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=7))
    #         else:
    #             # XDDDDDDDD
    #             lic = random.choice(string.ascii_uppercase) + ''.join(random.choices(string.digits, k=8))
    #         if lic not in existing_licenses:
    #             break
    #     return lic

    def _handle_update(self):
        return super()._handle_update("traveller")
