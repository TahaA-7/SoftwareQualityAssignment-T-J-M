'''
Backup
The System Administrator and Super Administrator should be able to create a backup of the backend
system. The Super Administrator can restore the backend system from any backup, the System
Administrator only from a specific backup.
'''

import hashlib
import os

class PasswordHasherSalter():
    @classmethod
    def hash_salt_password(cls, plain_password, salt=None):
        # return hashlib.sha256(plain_password.encode()).hexdigest()
        if salt is None:
            # Generate a new 16-byte salt
            salt = os.urandom(16)
        elif isinstance(salt, str):
            salt = salt.encode()
        # Combine salt and password, then hash
        hash_obj = hashlib.sha256(salt + plain_password.encode())
        return salt.hex() + ':' + hash_obj.hexdigest()

    @classmethod
    def verify_password(cls, plain_password, hashed):
        salt_hex, hash_val = hashed.split(':')
        salt = bytes.fromhex(salt_hex)
        return cls.hash_salt_password(plain_password, salt) == hashed
