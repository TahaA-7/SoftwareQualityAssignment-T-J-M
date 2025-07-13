from datetime import datetime


class Scooter:
    def __init__(self, serial_number, brand, model, top_speed,
                 battery_capacity, state_of_charge, target_soc_min,
                 target_soc_max, latitude, longitude, out_of_service,
                 mileage, last_maintenance_date, in_service_date):
        
        self.serial_number = serial_number
        if in_service_date == None:
            self.in_service_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.in_service_date = in_service_date

        self.brand = brand
        self.model = model
        self.top_speed = top_speed
        self.battery_capacity = battery_capacity
        self.state_of_charge = state_of_charge
        self.target_soc_min = target_soc_min
        self.target_soc_max = target_soc_max
        self.latitude = latitude
        self.longitude = longitude
        self.out_of_service = out_of_service  # Boolean
        self.mileage = mileage
        self.last_maintenance_date = last_maintenance_date
