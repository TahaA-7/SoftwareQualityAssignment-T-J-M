from access_layer.db.db_context import DBContext

from DataModels.ScooterModel import Scooter

class scooter_data:
    def __init__(self):
        self.db = DBContext()

    def get_scooter_single(self, brand, model):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT serial_number, brand, model, top_speed, state_of_charge, mileage
                FROM scooters
                WHERE brand = ? AND model = ?
            ''', (brand, model))
            return cursor.fetchall()

    def search_scooter(self, keyword):
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
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO scooters (
                    serial_number, in_service_date, brand, model, top_speed, battery_capacity,
                    state_of_charge, target_soc_min, target_soc_max, latitude, longitude,
                    out_of_service, mileage, last_maintenance_date
                ) VALUES (?, datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                scooter.serial_number, scooter.brand, scooter.model,
                scooter.top_speed, scooter.battery_capacity,
                scooter.state_of_charge, scooter.target_soc_min,
                scooter.target_soc_max, scooter.latitude, scooter.longitude,
                int(scooter.out_of_service), scooter.mileage,
                scooter.last_maintenance_date
            ))

    def delete_scooter(self, serial_number):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM scooters WHERE serial_number = ?", (serial_number,))

    def update_scooter(self, serial_number, field, value):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            query = f"UPDATE scooters SET {field} = ? WHERE serial_number = ?"
            cursor.execute(query, (value, serial_number))
    
    def update_scooter_attributes(
            self, scooter_obj: tuple, SoC=None, target_SoC_min=None, target_SoC_max=None, lat=None, lon=None, 
            out_of_service_status=None, mileage=None, last_maintenance=None):
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
