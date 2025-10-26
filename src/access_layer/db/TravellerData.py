from access_layer.db.db_context import DBContext
from presentation_layer.utils.Session import Session
from logic_layer.utils.AuthenticationAttemptsTracker import AuthenticationAttemptsTracker
from logic_layer.utils.SensitiveDataEncryptor import SensitiveDataEncryptor

class traveller_data:
    def __init__(self):
        self.db = DBContext()

    def get_travellers(self):
        # Function not accessible for service engineers
        if Session.user.role.value not in (2, 3):
            return None

        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM travellers""")
            rows = cursor.fetchall()
            
            # Decrypt all traveller data
            decrypted_travellers = []
            for row in rows:
                decrypted_travellers.append(SensitiveDataEncryptor.decrypt_traveller_row(row))
            
            return decrypted_travellers

    def search_traveller(self, keyword):
        # Function not accessible for service engineers
        if Session.user.role.value not in (2, 3):
            return None

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
            rows = cursor.fetchall()
            
            # Decrypt search results
            decrypted_results = []
            for row in rows:
                decrypted_row = list(row)
                decrypted_row[1] = SensitiveDataEncryptor.decrypt_field(row[1])  # first_name
                decrypted_row[2] = SensitiveDataEncryptor.decrypt_field(row[2])  # last_name
                decrypted_row[3] = SensitiveDataEncryptor.decrypt_field(row[3])  # email
                decrypted_row[4] = SensitiveDataEncryptor.decrypt_field(row[4])  # mobile_phone
                decrypted_results.append(tuple(decrypted_row))
            
            return decrypted_results
        
    def add_traveller(self, traveller):
        # Function not accessible for service engineers
        if Session.user.role.value not in (2, 3):
            return False

        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO travellers (
                    customer_id, registration_date, first_name, last_name,
                    birthday, gender, street_name, house_number,
                    zip_code, city, email, mobile_phone, driving_license_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                traveller.customer_id, 
                traveller.registration_date, 
                SensitiveDataEncryptor.encrypt_field(traveller.first_name), 
                SensitiveDataEncryptor.encrypt_field(traveller.last_name),
                SensitiveDataEncryptor.encrypt_field(traveller.birthday), 
                traveller.gender, 
                SensitiveDataEncryptor.encrypt_field(traveller.street_name),
                SensitiveDataEncryptor.encrypt_field(traveller.house_number), 
                SensitiveDataEncryptor.encrypt_field(traveller.zip_code), 
                SensitiveDataEncryptor.encrypt_field(traveller.city),
                SensitiveDataEncryptor.encrypt_field(traveller.email), 
                SensitiveDataEncryptor.encrypt_field(traveller.mobile_phone), 
                SensitiveDataEncryptor.encrypt_field(traveller.driving_license_number)
            ))
            return cursor.rowcount > 0

    def delete_traveller(self, customer_id):
        # Function not accessible for service engineers
        if Session.user.role.value not in (2, 3):
            return None

        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM travellers WHERE customer_id = ?", (customer_id,))

    def update_traveller(self, customer_id, fname, lname, bday, gender, street, house_num, zip, city, email, phone, license_num):
        # Function not accessible for service engineers
        if Session.user.role.value not in (2, 3):
            return None

        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM travellers WHERE customer_id = ?", (customer_id,))
                row = cursor.fetchone()
                if not row:
                    print("Traveller not found")
                    return False
                
                # Decrypt current values using SensitiveDataEncryptor
                decrypted_row = SensitiveDataEncryptor.decrypt_traveller_row(row)
                (curr_id, curr_registration_date, curr_fname, curr_lname, curr_bday, curr_gender,
                curr_street, curr_house_num, curr_zip, curr_city,
                curr_email, curr_phone, curr_license_num) = decrypted_row
                
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
                license_num = license_num if license_num != "" else curr_license_num

                cursor.execute("""UPDATE travellers
                                SET first_name = ?, last_name = ?, birthday = ?, gender = ?, street_name = ?, house_number = ?, zip_code = ?,
                                    city = ?, email = ?, mobile_phone = ?, driving_license_number = ?
                                WHERE customer_id = ?
                """, (
                    SensitiveDataEncryptor.encrypt_field(fname), 
                    SensitiveDataEncryptor.encrypt_field(lname), 
                    SensitiveDataEncryptor.encrypt_field(bday), 
                    gender, 
                    SensitiveDataEncryptor.encrypt_field(street), 
                    SensitiveDataEncryptor.encrypt_field(house_num), 
                    SensitiveDataEncryptor.encrypt_field(zip), 
                    SensitiveDataEncryptor.encrypt_field(city), 
                    SensitiveDataEncryptor.encrypt_field(email), 
                    SensitiveDataEncryptor.encrypt_field(phone), 
                    SensitiveDataEncryptor.encrypt_field(license_num), 
                    customer_id
                ))

                return cursor.rowcount > 0
        except Exception:
            return False
        

