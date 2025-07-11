from access_layer.db.db_context import DBContext

class traveller_data:
    def __init__(self):
        self.db = DBContext()

    def get_travellers(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM travellers""")
            return cursor.fetchall()

    def search_traveller(self, keyword):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            keyword = f"%{keyword.lower()}%"
            cursor.execute('''
                SELECT customer_id, first_name, last_name, email, mobile_phone
                FROM travellers
                WHERE LOWER(customer_id) LIKE ?
                OR LOWER(first_name) LIKE ?
                OR LOWER(last_name) LIKE ?
                OR LOWER(email) LIKE ?
                OR LOWER(mobile_phone) LIKE ?
            ''', (keyword, keyword, keyword, keyword, keyword))
            return cursor.fetchall()
        
    def add_traveller(self, traveller):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO travellers (
                    customer_id, registration_date, first_name, last_name,
                    birthday, gender, street_name, house_number,
                    zip_code, city, email, mobile_phone, driving_license_number
                ) VALUES (?, datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                traveller.customer_id, traveller.first_name, traveller.last_name,
                traveller.birthday, traveller.gender, traveller.street_name,
                traveller.house_number, traveller.zip_code, traveller.city,
                traveller.email, traveller.mobile_phone, traveller.driving_license_number
            ))

    def delete_traveller(self, customer_id):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM travellers WHERE customer_id = ?", (customer_id,))

    def update_traveller(self, customer_id, field, new_value):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            query = f"UPDATE travellers SET {field} = ? WHERE customer_id = ?"
            cursor.execute(query, (new_value, customer_id))
