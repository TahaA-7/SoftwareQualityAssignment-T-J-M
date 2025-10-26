from logic_layer.utils.TerminalClearner import TerminalCleaner
from logic_layer.utils.StringValidations import StringValidations
from logic_layer.utils.Logger import Logger

from logic_layer.AddMethods import AddDataService

from presentation_layer.menus.CreateOrUpdateMenu import CreateOrUpdateMenu

import re
import time
import datetime
import maskpass
from getpass import getpass

from DataModels.ScooterModel import Scooter
from access_layer.db.ScooterData import scooter_data

class CreateOrUpdateScooter(CreateOrUpdateMenu):

    def __init__(self):
        self.scooter_ = scooter_data()
        
    def menu(self):
        print("""Welcome
-   -   -   -   -   -   -""")
        while True:
            print([f for f in self._get_scooter_fields_dict().items()])
            user_choice = self._handle_input_length(getpass(
f"""Please select a field and set it to a (new) value

[P] scooter serial {"✓" if self._get_scooter_fields_dict()["serial"] not in [None, ""] else ""}
[Q] scooter brand {"✓" if self._get_scooter_fields_dict()["brand"] not in [None, ""] else ""}
[R] scooter model {"✓" if self._get_scooter_fields_dict()["model"] not in [None, ""] else ""}
[S] scooter top speed {"✓" if self._get_scooter_fields_dict()["top_speed"] not in [None, ""] else ""}
[T] scooter battery {"✓" if self._get_scooter_fields_dict()["battery"] not in [None, ""] else ""}
[U] scooter State of Charge (SoC) {"✓" if self._get_scooter_fields_dict()["soc"] not in [None, ""] else ""}
[V] SoC range {"✓" if self._get_scooter_fields_dict()["soc_min"] not in [None, ""] 
                and self._get_scooter_fields_dict()["soc_max"] not in [None, ""] else ""}
[W] location {"✓" if self._get_scooter_fields_dict()["lat"] not in [None, ""] 
               and self._get_scooter_fields_dict()["lon"] not in [None, ""] else ""}
[X] mileage {"✓" if self._get_scooter_fields_dict()["mileage"] not in [None, ""] else ""}
[Y] out of service status {"✓" if self._get_scooter_fields_dict()["out_of_service_status"] not in [None, ""] else ""}

[1] submit register
[2] submit update to existing scooter
[3] cancel
"""))
            
            match user_choice:
                case "P":
                    self._handle_scooter_serial()
                case "Q":
                    self._handle_scooter_brand()
                case "R":
                    self._handle_scooter_model()
                case "S":
                    self._handle_scooter_top_speed()
                case "T":
                    self._handle_scooter_battery()
                case "U":
                    self._handle_scooter_state_of_charge()
                case "V":
                    self._handle_scooter_soc_target_range()
                case "W":
                    self._handle_scooter_location()
                case "X":
                    self._handle_scooter_mileage()
                case "Y":
                    self._handle_scooter_out_of_service_status()
                    
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
        if not hasattr(self, 'last_maint_date') or not self.last_maint_date:
            self.last_maint_date = datetime.date.today().strftime("%Y-%m-%d")
        if "" not in self._get_scooter_fields_dict().items():
            add_data_service_obj = AddDataService()
            added_scooter = add_data_service_obj.addScooter(self.serial, self.brand, self.model, 
                self.top_speed, self.battery, self.soc, self.soc_min, self.soc_max,
                self.lat, self.lon, self.out_of_service_status, self.mileage, self.last_maint_date)
            if added_scooter:
                Logger.log(self.customer_id, "Registered new scooter")
                print("Scooter registered succesfully.")
            else:
                Logger.log(self.username, "Registration failed", "Scooter already exists", suspicious=True)
                print("Error: scooter already exists")
        else:
            print("Error: cannot submit because one or more fields remained blank " + 
"either because left unhandled or couldn't be updated due to an invalid input.")

    def _handle_update(self):
        return super()._handle_update("scooter")


    def get_int(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a whole number.")

    def get_float(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a number.")

    def addScooter_(self):
        serial = input("Serial Number: ").strip()
        brand = input("Brand: ").strip()
        model = input("Model: ").strip()
        top_speed = self.get_int("Top speed (km/h): ")
        battery = self.get_int("Battery capacity (Wh): ")
        soc = self.get_int("State of charge (%): ")
        soc_min = self.get_int("Min SoC: ")
        soc_max = self.get_int("Max SoC: ")
        lat = self.get_float("Latitude: ")
        lon = self.get_float("Longitude: ")

        while True:
            out_of_service_input = input("Is out of service (y/n): ").strip().lower()
            if out_of_service_input in ['y', 'n']:
                out_of_service = out_of_service_input == 'y'
                break
            print("Please enter 'y' or 'n'.")

        mileage = self.get_float("Mileage (km): ")
        
        while True:
            last_maint = input("Last maintenance date (YYYY-MM-DD): ").strip()
            try:
                datetime.datetime.strptime(last_maint, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        scooter = Scooter(serial, brand, model, top_speed, battery, soc, soc_min, soc_max, lat, lon, out_of_service, mileage, last_maint)
        self.scooter_.add_scooter(scooter)
        print("Scooter added successfully.")