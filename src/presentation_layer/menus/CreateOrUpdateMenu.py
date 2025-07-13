from logic_layer.utils.TerminalClearner import TerminalCleaner
from logic_layer.utils.StringValidations import StringValidations
from logic_layer.AddMethods import AddDataService
from logic_layer.UpdateMethods import UpdateDataService
from logic_layer.GetDataMethods import GetDataService

from access_layer.db.TravellerData import traveller_data

import random, uuid
import string, re
import time, datetime
import maskpass
from getpass import getpass



class CreateOrUpdateMenu:
    alnum_dash = set(string.ascii_letters + string.digits + "-")
    object_type = ""
    user_type = 1  # service_engineer
    # for service_engineer or system_admin account/profile
    user_id = ""
    username = password = u_fname = u_lname = ""
    original_username_or_id = ""
    # for traveller
    customer_id = registration_date = ""
    c_fname = c_lname = bday = gender = street = house_number = zip = city = c_email = phone = ""
    license_number = ""
    traveller_data_obj = traveller_data()
    # for scooter
    original_serial = ""
    serial = brand = model = top_speed = battery = soc = soc_range = soc_min = soc_max = lat = lon = out_of_service_status = mileage = last_maint_date = ""

    city_names_dict = {"A": "Amsterdam", "R": "Rotterdam", "D": "Den Haag", "U": "Utrecht", "M": "Maastricht",
                "G": "Groningen", "E": "Eindhoven", "H": "Haarlem", "L": "Leiden", "S": "'s-Hertogenbosch"}

    def _init_(self):
        pass

    def _get_employee_fields_dict(self):
        return {
            "username": self.username,
            "password": "" if self.password == "" else len(self.password) * "*",
            "first_name": self.u_fname,
            "last_name": self.u_lname
        }

    def _get_traveller_fields_dict(self):
        return {
            # "customer_id": self.customer_id,
            # "registration_date": self.registration_date,
            "first_name": self.c_fname,
            "last_name": self.c_lname,
            "birthday": self.bday,
            "gender": self.gender,
            "street": self.street,
            "house_number": self.house_number,
            "zip_code": self.zip,
            "city": self.city,
            "email": self.c_email,
            "phone": self.phone,
            "license_number": self.license_number
        }

    def _get_scooter_fields_dict(self):
        return {
            "serial": self.serial,
            "brand": self.brand,
            "model": self.model,
            "top_speed": self.top_speed,
            "battery": self.battery,
            "soc": self.soc,
            #"soc_range": self.soc_range
            "soc_min": self.soc_min,
            "soc_max": self.soc_max,
            #"location": self.location
            "lat": self.lat,
            "lon": self.lon,
            #"last_maintenance_date: self.last_maintenance_date"
            "mileage": self.mileage,
            "out_of_service_status": "ACTIVE" if self.out_of_service_status == "" else self.out_of_service_status
        }

    # MENUS
#     def _menu(self):
#         TerminalCleaner.clear_terminal()
#         print("""Welcome
# -   -   -   -   -   -   -""")
#         while True:
#             # print([f for f in self._get_employee_fields_dict().items()])
#             user_choice = self._handle_input_length(getpass(
# f"""Please select a field and set it to a (new) value

# [A] employee username {"✓" if self._get_employee_fields_dict()["username"] not in [None, ""] else ""}
# [B] employee password {"✓" if self._get_employee_fields_dict()["password"] not in [None, ""] else ""}
# [C] first name {"✓" if self._get_employee_fields_dict()["first_name"] not in [None, ""] else ""}
# [D] last name {"✓" if self._get_employee_fields_dict()["last_name"] not in [None, ""] else ""}

# [E] traveller first name {"✓" if self._get_traveller_fields_dict()["first_name"] not in [None, ""] else ""}
# [F] traveller last name {"✓" if self._get_traveller_fields_dict()["last_name"] not in [None, ""] else ""}
# [G] traveller birthday {"✓" if self._get_traveller_fields_dict()["birthday"] not in [None, ""] else ""}
# [H] traveller gender {"✓" if self._get_traveller_fields_dict()["gender"] not in [None, ""] else ""}
# [I] traveller street {"✓" if self._get_traveller_fields_dict()["street"] not in [None, ""] else ""}
# [J] traveller house number {"✓" if self._get_traveller_fields_dict()["house_number"] not in [None, ""] else ""}
# [K] traveller zip code {"✓" if self._get_traveller_fields_dict()["zip_code"] not in [None, ""] else ""}
# [L] traveller city {"✓" if self._get_traveller_fields_dict()["city"] not in [None, ""] else ""}
# [M] traveller email {"✓" if self._get_traveller_fields_dict()["email"] not in [None, ""] else ""}
# [N] traveller phone {"✓" if self._get_traveller_fields_dict()["phone"] not in [None, ""] else ""}
# [O] traveller license number {"✓" if self._get_traveller_fields_dict()["license_number"] not in [None, ""] else ""}

# [P] scooter serial {"✓" if self._get_scooter_fields_dict()["serial"] not in [None, ""] else ""}
# [Q] scooter brand {"✓" if self._get_scooter_fields_dict()["brand"] not in [None, ""] else ""}
# [R] scooter model {"✓" if self._get_scooter_fields_dict()["model"] not in [None, ""] else ""}
# [S] scooter top speed {"✓" if self._get_scooter_fields_dict()["top_speed"] not in [None, ""] else ""}
# [T] scooter battery {"✓" if self._get_scooter_fields_dict()["battery"] not in [None, ""] else ""}
# [U] scooter State of Charge (SoC) {"✓" if self._get_scooter_fields_dict()["soc"] not in [None, ""] else ""}
# [V] SoC range {"✓" if self._get_scooter_fields_dict()["soc_min"] not in [None, ""] 
#                and self._get_scooter_fields_dict()["soc_max"] not in [None, ""] else ""}
# [W] location {"✓" if self._get_scooter_fields_dict()["lat"] not in [None, ""] 
#               and self._get_scooter_fields_dict()["lon"] not in [None, ""] else ""}
# [X] mileage {"✓" if self._get_scooter_fields_dict()["mileage"] not in [None, ""] else ""}
# [Y] out of service status {"✓" if self._get_scooter_fields_dict()["out_of_service_status"] not in [None, ""] else ""}

# [1] submit register
# [2] submit update to existing account/profile
# [3] cancel
# """))
            
            # match user_choice:
            #     case "A":
            #         self._handle_username()
            #     case "B":
            #         self._handle_password()
            #     case "C":
            #         self._handle_first_name_submit("emp")
            #     case "D":
            #         self._handle_last_name_submit("emp")

            #     case "E":
            #         self._handle_first_name_submit("trav")
            #     case "F":
            #         self._handle_last_name_submit("trav")
            #     case "G": 
            #         self._handle_trav_birthday()
            #     case "H":
            #         self._handle_trav_gender()
            #     case "I":
            #         self._handle_trav_street()
            #     case "J":
            #         self._handle_trav_house_number()
            #     case "K":
            #         self._handle_trav_zip_code()
            #     case "L":
            #         self._handle_trav_city()
            #     case "M":
            #         self._handle_trav_email()
            #     case "N":
            #         self._handle_trav_phone()
            #     case "O":
            #         self._handle_license_number()

            #     case "P":
            #         self._handle_scooter_serial()
            #     case "Q":
            #         self._handle_scooter_brand()
            #     case "R":
            #         self._handle_scooter_model()
            #     case "S":
            #         self._handle_scooter_top_speed()
            #     case "T":
            #         self._handle_scooter_battery()
            #     case "U":
            #         self._handle_scooter_state_of_charge()
            #     case "V":
            #         self._handle_scooter_soc_target_range()
            #     case "W":
            #         self._handle_scooter_location()
            #     case "X":
            #         self._handle_scooter_mileage()
            #     case "Y":
            #         self._handle_scooter_out_of_service_status()

            #     case "1":
            #         self._handle_register()
            #     case "2":
            #         self._handle_update()
            #     case "3":
            #         break
            #     case _:
            #         print("Invalid choice")


    # SUBMIT
    def _handle_register(self):
        pass

    def _handle_update(self, type):
        get_data_service_obj = GetDataService()
        update_data_service_obj = UpdateDataService()
        result = False
        if type == "employee":
            self.original_username_or_id = input(
                "Please enter the original username or ID of the user to be updated: ")
            fetched_user = get_data_service_obj.get_user_by_username_or_id(self.original_username_or_id)
            if fetched_user:
                # fetched_user[1] refers to the original username
                result = update_data_service_obj.updateUser_profile(fetched_user[1], self.username, self.u_fname, self.u_lname)
            else:
                print("Error: no user found with that ID or username!")
        elif type == "traveller":
            self.customer_id = input("Please enter the ID of the traveller to be updated: ")
            result = update_data_service_obj.updateTraveller(self.customer_id, self.c_fname, self.c_lname, self.bday, self.gender,
                self.street, self.house_number, self.zip, self.city, self.c_email, self.phone, 
                self.license_number)
        elif type == "scooter":
            self.original_serial = input("Please enter the original serial number of the scooter to be updated: ")
            result = update_data_service_obj.updateScooter(self.original_serial, self.serial, self.brand, self.model, self.top_speed,
                self.battery, self.soc, self.soc_range, self.soc_min, self.soc_max, self.lat, self.lon, self.out_of_service_status,
                self.mileage, last_maint_date=datetime.date.today())

        if result:
            print('added sucessfully')
        else:
            print('error: update failed')
        return result


    # USERS MAINLY
    def _handle_username(self):
        username_input = input("""Please enter your username:
    ○ must be unique and have a length of at least 8 characters
    ○ must be no longer than 10 characters
    ○ must be started with a letter or underscores (_)
    ○ can contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (,)
    ○ no distinction between lowercase and uppercase letters (case-insensitive):\n""")
        if username_input in ("", " "): return
        if StringValidations.is_valid_username(username_input) == False:
            print("Invalid username")
            time.sleep(0.75)
        else:
            print("Username set succesfully")
            time.sleep(0.75)
            self.username = username_input
        return self.username


    def _handle_password(self):
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
            self.password = password_input
        return self.password


    def _handle_first_name_submit(self, emp_or_cust):
        name_input = input("Please enter a first name: ")
        if name_input in ("", " "):
            return
        if StringValidations.is_valid_first_or_last_name(name_input) == False:
            print("Invalid first name")
            time.sleep(0.75)
        else:
            print("First name set succesfully")
            time.sleep(0.75)
            if emp_or_cust == "emp":
                self.u_fname = name_input
            else:
                self.c_fname = name_input
        return self.u_fname if emp_or_cust == "emp" else self.c_fname


    def _handle_last_name_submit(self, emp_or_cust):
        name_input = input("Please enter a last name: ")
        if name_input in ("", " "):
            return
        if StringValidations.is_valid_first_or_last_name(name_input) == False:
            print("Invalid last name")
            time.sleep(0.75)
        else:
            print("Last name set succesfully")
            time.sleep(0.75)
            if emp_or_cust == "emp":
                self.u_lname = name_input
            else:
                self.c_lname = name_input
        return self.u_lname if emp_or_cust == "emp" else self.c_lname


    # TRAVELLERS
    # def handle_trav_first_name(self):
    #     pass
    # def handle_trav_last_name(self):
    #     pass
    def _handle_trav_birthday(self):
        birthday = input("Please enter a birthday (YYYY-MM-DD): ").strip()
        self.bday = birthday if datetime.datetime.strptime(birthday, "%Y-%m-%d") else ""
    def _handle_trav_gender(self):
        gender = input("Please enter a gender (M/F/O): ").strip()
        self.gender = gender if gender.upper() in ("M", "F", "O", "MALE", "FEMALE", "OTHER") else ""
    def _handle_trav_street(self):
        street = input("Please enter a street name: ").strip()
        self.street = street
    def _handle_trav_house_number(self):
        house_numer = input("Please enter a house number: ").strip()
        self.house_number = house_numer if house_numer.isdigit() else ""
    def _handle_trav_zip_code(self):
        zip_code = input("Please enter a zip code (DDDDXX): ").strip().upper()
        if len(zip_code) == 6:
            self.zip = zip_code if zip_code[0:3].isdigit() and zip_code[4:5].isalpha() else ""
        else:
            self.zip = ""
        # self.zip = zip_code if len(zip_code) < 12 else ""
    def _handle_trav_city(self):
        city_char = self._select_city()
        if city_char == 'O':
            city_input = input("Please enter a city name: ")
            self.city = city_input if city_input.isalpha() else ""
        else:
            self.city = self.city_names_dict[city_char] if city_char in self.city_names_dict.keys() else ""
    def _handle_trav_email(self):
        email = input("Please enter an email: ").strip()
        self.c_email = email if StringValidations.is_valid_email(email) else ""
    def _handle_trav_phone(self):
        phone = input("Please enter a phone number (+31-6-DDDDDDDD): ").strip()
        phone = phone.split("-")[-1] if "-" in phone else phone  # On a separate line for readability
        self.phone = phone if phone.isdigit() and len(phone) == 8 else ""
    def _handle_license_number(self):
        self.license_number = self._generate_license_number()


    # SCOOTERS
    def _handle_scooter_serial(self):
        serial = input("Serial Number: ").strip()
        self.serial = serial if all(c in self.alnum_dash for c in serial) else ""
    def _handle_scooter_brand(self):
        brand = input("Brand: ").strip()
        self.brand = brand if brand.isalpha() else ""
    def _handle_scooter_model(self):
        model = input("Model: ").strip()
        self.model = model if model.isalpha() else ""
    def _handle_scooter_top_speed(self):
        top_speed = input("Top speed (km/h): ").strip()
        self.top_speed = top_speed if top_speed.isdigit() else ""
    def _handle_scooter_battery(self):
        battery = input("Battery capacity (Wh): ").strip()
        self.battery = battery if battery.isdigit() else ""
    def _handle_scooter_state_of_charge(self):
        soc = input("(SoC) State of charge (%): ").strip()
        self.soc = soc.replace("%", "") if soc.replace("%", "").isdigit() else ""
    def _handle_scooter_soc_target_range(self):
        try:
            soc_range = input("Min SoC - Max SoC, split with `-` (10-20): ").strip()
            # self.soc_range = soc_range.replace(";", "") if soc_range.count(";") == 1 and soc_range.replace(";", "").isdigit()
            if soc_range.count("-") == 1:
                soc_min, soc_max = soc_range.split("-")
                if soc_min.isnumeric() and soc_max.isnumeric():
                    self.soc_min = soc_min
                    self.soc_max = soc_max
        except Exception:
            print("Invalid input. Format should be: `10-20`")
    def _handle_scooter_location(self):
        try:
            location = input("Min SoC - Max SoC, split with `;` (52.3676;4.9041): ").strip().replace(",", ".")
            # self.location = location.replace(";", "") if location.count(";") == 1 and re.fullmatch(r'\d+(\.\d+)?', location.replace(";", ""))
            if location.count(";") == 1:
                lat_str, lon_str = location.split(";")
                lat = float(lat_str.strip())
                lon = float(lon_str.strip())
                self.lat = lat
                self.lon = lon
        except Exception:
            print("Invalid input. Format should be: `52.3676;4.9041`")
    def _handle_scooter_out_of_service_status(self):
        out_of_service = input("Is out of service enter details or `n/N` to leave empty ").strip()
        self.out_of_service_status = out_of_service if out_of_service not in ('n', 'N', '') else ""
    def _handle_scooter_mileage(self):
        mileage = input("Mileage (km): ").strip()
        self.mileage = mileage if mileage.replace(".", "").isnumeric() else ""


    def _select_city(self):
        city_choice = self._handle_input_length(input("""Please choose a city below or enter a different one:
[A]msterdam
[R]otterdam
[D]en Haag (The Hague)
[U]trecht
[M]aastricht
[G]roningen
[E]indhoven
[H]aarlem
[L]eiden
[S]-Hertogenbosch ('s-Hertogenbosch)

[O]ther
""")).strip().upper()
        return city_choice

    def _generate_license_number(self):
        # unique license number in `XXDDDDDDD` or `XDDDDDDDD` format
        # trav[12] is the license number
        existing_licenses = {trav[12] for trav in self.traveller_data_obj.get_travellers()}
        while True:
            # Randomly choose format
            if random.choice([True, False]):
                # XXDDDDDDD
                lic = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=7))
            else:
                # XDDDDDDDD
                lic = random.choice(string.ascii_uppercase) + ''.join(random.choices(string.digits, k=8))
            if lic not in existing_licenses:
                break
        return lic

    def _handle_input_length(self, inp):
        user_inp = inp[-1].upper() if len(inp) > 0 else " "
        return user_inp
