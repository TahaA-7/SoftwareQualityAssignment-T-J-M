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


class CreateOrUpdateScooter(CreateOrUpdateMenu):
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
[2] submit update to existing account/profile
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
        self.last_maint_date = datetime.time()
        if "" not in self._get_scooter_fields_dict().items():
            add_data_service_obj = AddDataService()
            added_scooter = add_data_service_obj.addScooter(self.serial, self.brand, self.model, 
                self.top_speed, self.battery, self.soc, self.soc_range, self.soc_min, self.soc_max,
                self.lat, self.lon, self.out_of_service_status, self.mileage, self.last_maint_date)
            if added_scooter != None:
                Logger.log(self.customer_id, "Registered new scooter")
                print("Scooter registered succesfully.")
            else:
                Logger.log(self.username, "Registration failed", "Scooter already exists", suspicious=True)
                print("Error: traveller already exists")
        else:
            print("Error: cannot submit because one or more fields remained blank " + 
"either because left unhandled or couldn't be updated due to an invalid input.")

    def _handle_update(self):
        return super()._handle_update("scooter")
