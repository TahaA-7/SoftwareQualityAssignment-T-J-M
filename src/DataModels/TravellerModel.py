import uuid
from datetime import datetime


class Traveller:
    def __init__(self, customer_id, registration_date, first_name, last_name, birthday, gender,
                 street_name, house_number, zip_code, city,
                 email, mobile_phone, driving_license_number):
        if customer_id in (None, "", " "): 
            self.customer_id = str(uuid.uuid4())
        else:
            self.customer_id = customer_id
        if registration_date in (None, "", " "):
            self.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.registration_date = registration_date
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.street_name = street_name
        self.house_number = house_number
        self.zip_code = zip_code
        self.city = city
        self.email = email
        self.mobile_phone = f"+31-6-{mobile_phone}"
        self.driving_license_number = driving_license_number
