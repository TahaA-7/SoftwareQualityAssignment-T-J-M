from access_layer.db.db_context import DBContext

from DataModels.ScooterModel import Scooter

from presentation_layer.utils.Session import Session

from logic_layer.utils.AuthenticationAttemptsTracker import AuthenticationAttemptsTracker

class scooter_data:
    def __init__(self):
        self.db = DBContext()


    # def get_scooters()

    def get_scooter_single(self, original_serial):
        # Function accessible for service engineers, system admin and super admin
        if Session.user.role.value not in (1, 2, 3):
            AuthenticationAttemptsTracker.handle_tresspass()
            return None
        
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT *
                FROM scooters
                WHERE serial_number = ?
            ''', (original_serial,))
            return cursor.fetchall()

    def search_scooter(self, keyword):
        # Function accessible for service engineers, system admin and super admin
        if Session.user.role.value not in (1, 2, 3):
            AuthenticationAttemptsTracker.handle_tresspass()
            return None
        
        with self.db.connect() as conn:
            cursor = conn.cursor()
            keyword = f"%{keyword.lower()}%"
            cursor.execute('''
                SELECT serial_number, brand, model, top_speed, state_of_charge, mileage
                FROM scooters
                WHERE LOWER(serial_number) LIKE ?
                OR LOWER(brand) LIKE ?
                OR LOWER(model) LIKE ?
            ''', (keyword, keyword, keyword))
            return cursor.fetchall()

    def add_scooter(self, scooter):
        # Function not accessible for service engineers
        if Session.user.role.value not in (2, 3):
            return None

        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO scooters (
                        serial_number, in_service_date, brand, model, top_speed, battery_capacity,
                        state_of_charge, target_soc_min, target_soc_max, latitude, longitude,
                        out_of_service, mileage, last_maintenance_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    scooter.serial_number, scooter.in_service_date, scooter.brand, scooter.model,
                    scooter.top_speed, scooter.battery_capacity,
                    scooter.state_of_charge, scooter.target_soc_min,
                    scooter.target_soc_max, scooter.latitude, scooter.longitude,
                    int(scooter.out_of_service), scooter.mileage,
                    scooter.last_maintenance_date
                ))
                return cursor.rowcount > 0
        except Exception:
            return None

    def delete_scooter(self, serial_number):
        # Function not accessible for service engineers
        if Session.user.role.value not in (2, 3):
            return None

        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM scooters WHERE serial_number = ?", (serial_number,))
                return True
        except Exception:
            return None

    def update_scooter(self, original_serial, serial, brand, model, top_speed, battery, soc, soc_range, soc_min, soc_max,
                    lat, lon, out_of_service_status, mileage, last_maint_date):
        # For the service engineer there exists a seperate update function
        if Session.user.role.value not in (2, 3):
            return None
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT serial_number, in_service_date, brand, model, top_speed, battery_capacity, state_of_charge,
                                    target_soc_min, target_soc_max, latitude, longitude, out_of_service, mileage, last_maintenance_date
                                FROM scooters WHERE serial_number = ?""", (original_serial,))
                row = cursor.fetchone()
                if not row:
                    print("Scooter not found")
                    return False
                # curr as in current
                (curr_serial, curr_in_service_date, curr_brand, curr_model, curr_top_speed, curr_battery, curr_soc, curr_soc_min, 
                 curr_soc_max, curr_lat, curr_lon, curr_out_of_service_status, curr_mileage, curr_last_maint_date) = row
                # Use current value if input is blank
                serial = serial if serial != "" else curr_serial
                brand = brand if brand != "" else curr_brand
                model = model if model != "" else curr_model
                top_speed = top_speed if top_speed != "" else curr_top_speed
                battery = battery if battery != "" else curr_battery
                soc = soc if soc != "" else curr_soc
                # soc_range = soc_range if soc_range != "" else curr_soc_range
                soc_min = soc_min if soc_min != "" else curr_soc_min
                soc_max = soc_max if soc_max != "" else curr_soc_max
                lat = lat if lat != "" else curr_lat
                lon = lon if lon != "" else curr_lon
                out_of_service_status = out_of_service_status if out_of_service_status not in (False, "", "ACTIVE", "active") else " "
                mileage = mileage if mileage != "" else curr_mileage
                last_maint_date = last_maint_date if last_maint_date != "" else curr_last_maint_date
                cursor.execute("""UPDATE scooters
                    SET serial_number = ?, brand = ?, model = ?, top_speed = ?, battery_capacity = ?, state_of_charge = ?, target_soc_min = ?, 
                        target_soc_max = ?, latitude = ?, longitude = ?, out_of_service = ?, mileage = ?, last_maintenance_date = ?
                    WHERE serial_number = ?
                """, (serial, brand, model, top_speed, battery, soc, soc_min, soc_max,
                    lat, lon, out_of_service_status, mileage, last_maint_date, original_serial))

                return cursor.rowcount > 0
        except Exception as ex:
            print(ex)
            return False
    
    def update_scooter_attributes(
            self, scooter_obj: tuple, SoC=None, target_SoC_min=None, target_SoC_max=None, lat=None, lon=None, 
            out_of_service_status=None, mileage=None, last_maintenance=None):
        # Function accessible for service engineers, system admin and super admin
        if Session.user.role.value not in (1, 2, 3):
            AuthenticationAttemptsTracker.handle_tresspass()
            return None
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                updates = []
                params = []

                if SoC is not None:
                    updates.append("state_of_charge = ?")
                    params.append(SoC)
                if target_SoC_min is not None:
                    updates.append("target_soc_min = ?")
                    params.append(target_SoC_min)
                if target_SoC_max is not None:
                    updates.append("target_soc_max = ?")
                    params.append(target_SoC_max)
                if lat is not None:
                    updates.append("latitude = ?")
                    params.append(lat)
                if lon is not None:
                    updates.append("longitude = ?")
                    params.append(lon)
                if out_of_service_status is not None:
                    updates.append("out_of_service = ?")
                    params.append(out_of_service_status)
                if mileage is not None:
                    updates.append("mileage = ?")
                    params.append(mileage)
                if last_maintenance is not None:
                    updates.append("last_maintenance_date = ?")
                    params.append(last_maintenance)

                if not updates:
                    return  # Nothing to update

                query = f"UPDATE scooters SET {', '.join(updates)} WHERE brand = ? AND model = ?"
                params.append(scooter_obj[2])
                params.append(scooter_obj[3])
                cursor.execute(query, params)
                conn.commit()

                return cursor.rowcount > 0
        except Exception:
            return False 
