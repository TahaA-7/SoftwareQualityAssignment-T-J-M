from db.db_context import DBContext

class scooter_data:
    def __init__(self):
        self.db = DBContext()

    def search_scooter(self, keyword):
        with self.connect() as conn:
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
