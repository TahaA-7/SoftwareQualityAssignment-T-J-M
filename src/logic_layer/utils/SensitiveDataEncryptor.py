'''
Encryption of sensitive data
As mentioned before, all sensitive data in the database, including usernames, and traveller phones and
addresses, as well as log data must be encrypted. For this encryption, you must use a symmetric
algorithm.
'''

'''
Additional Clarification: At any point in time, whether the application is running or not running, any user
with any text editor (outside of the Urban Mobility application) must not be able to see any meaningful
data in the database or log file [unless they can decrypt the file(s)]. So, decryption and encryption of the
files on start and exit is not an acceptable solution.
'''

from logic_layer.utils.Logger import Logger
from cryptography.fernet import Fernet

class SensitiveDataEncryptor:
    
    @staticmethod
    def _get_encryption_key():
        """Get the encryption key from Logger for consistency"""
        return Logger._get_key()
    
    @staticmethod
    def encrypt_field(field):
        """Encrypt a single field"""
        if not field:
            return field
        key = SensitiveDataEncryptor._get_encryption_key()
        fernet = Fernet(key)
        return fernet.encrypt(str(field).encode()).decode()
    
    @staticmethod
    def decrypt_field(encrypted_field):
        """Decrypt a single field"""
        if not encrypted_field:
            return encrypted_field
        try:
            key = SensitiveDataEncryptor._get_encryption_key()
            fernet = Fernet(key)
            return fernet.decrypt(encrypted_field.encode()).decode()
        except Exception:
            return encrypted_field

    @staticmethod
    def encrypt_traveller_row(row):
        """Encrypt sensitive fields in a traveller row"""
        encrypted_row = list(row)
        # Indices: customer_id(0), registration_date(1), first_name(2), last_name(3), 
        # birthday(4), gender(5), street_name(6), house_number(7), zip_code(8), 
        # city(9), email(10), mobile_phone(11), driving_license_number(12)
        
        encrypted_row[2] = SensitiveDataEncryptor.encrypt_field(row[2])   # first_name
        encrypted_row[3] = SensitiveDataEncryptor.encrypt_field(row[3])   # last_name
        encrypted_row[4] = SensitiveDataEncryptor.encrypt_field(row[4])   # birthday
        encrypted_row[6] = SensitiveDataEncryptor.encrypt_field(row[6])   # street_name
        encrypted_row[7] = SensitiveDataEncryptor.encrypt_field(row[7])   # house_number
        encrypted_row[8] = SensitiveDataEncryptor.encrypt_field(row[8])   # zip_code
        encrypted_row[9] = SensitiveDataEncryptor.encrypt_field(row[9])   # city
        encrypted_row[10] = SensitiveDataEncryptor.encrypt_field(row[10]) # email
        encrypted_row[11] = SensitiveDataEncryptor.encrypt_field(row[11]) # mobile_phone
        encrypted_row[12] = SensitiveDataEncryptor.encrypt_field(row[12]) # driving_license_number
        
        return tuple(encrypted_row)

    @staticmethod
    def decrypt_traveller_row(row):
        """Decrypt sensitive fields in a traveller row"""
        decrypted_row = list(row)
        
        decrypted_row[2] = SensitiveDataEncryptor.decrypt_field(row[2])   # first_name
        decrypted_row[3] = SensitiveDataEncryptor.decrypt_field(row[3])   # last_name
        decrypted_row[4] = SensitiveDataEncryptor.decrypt_field(row[4])   # birthday
        decrypted_row[6] = SensitiveDataEncryptor.decrypt_field(row[6])   # street_name
        decrypted_row[7] = SensitiveDataEncryptor.decrypt_field(row[7])   # house_number
        decrypted_row[8] = SensitiveDataEncryptor.decrypt_field(row[8])   # zip_code
        decrypted_row[9] = SensitiveDataEncryptor.decrypt_field(row[9])   # city
        decrypted_row[10] = SensitiveDataEncryptor.decrypt_field(row[10]) # email
        decrypted_row[11] = SensitiveDataEncryptor.decrypt_field(row[11]) # mobile_phone
        decrypted_row[12] = SensitiveDataEncryptor.decrypt_field(row[12]) # driving_license_number
        
        return tuple(decrypted_row)

    @staticmethod
    def encrypt_user_names(first_name, last_name):
        """Encrypt user first and last names"""
        encrypted_first = SensitiveDataEncryptor.encrypt_field(first_name)
        encrypted_last = SensitiveDataEncryptor.encrypt_field(last_name)
        return encrypted_first, encrypted_last

    @staticmethod
    def decrypt_user_names(encrypted_first_name, encrypted_last_name):
        """Decrypt user first and last names"""
        decrypted_first = SensitiveDataEncryptor.decrypt_field(encrypted_first_name)
        decrypted_last = SensitiveDataEncryptor.decrypt_field(encrypted_last_name)
        return decrypted_first, decrypted_last
