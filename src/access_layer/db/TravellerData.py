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

    def update_traveller(self, customer_id, fname, lname, bday, gender, street, house_num, zip, city, email, phone):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM travellers WHERE customer_id = ?", (customer_id,))
                row = cursor.fetchone()
                if not row:
                    print("Traveller not found")
                    return False
                # curr as in current
                curr_fname = curr_fname = curr_lname = curr_bday = curr_gender = curr_street = curr_house_num = curr_zip = curr_city = row
                curr_email = curr_phone = row
                # Use current value if input is blank
                fname = fname if fname != "" else curr_fname
                lname = lname if lname != "" else curr_lname
                bday = bday if bday != "" else curr_bday
                gender = gender if gender != "" else curr_gender
                street = street if street != "" else curr_street
                house_num = house_num if house_num != "" else curr_house_num
                zip = zip if zip != "" else curr_zip
                city = city if city != "" else curr_city
                email = email if email != "" else curr_email
                phone = phone if phone != "" else curr_phone

                cursor.execute("""UPDATE travellers
                                SET first_name = ?, last_name = ?, birthday = ?, gender = ?, street = ?, house_number = ?, zip_code = ?,
                                    city = ?, email = ?, mobile_phone = ?
                                WHERE customer_id = ?
                """, (fname, lname, bday, gender, street, house_num, zip, city, email, phone, customer_id))

                return cursor.rowcount > 0
        except Exception:
            return False
