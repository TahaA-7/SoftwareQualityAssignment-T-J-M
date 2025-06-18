'''
Backup
The System Administrator and Super Administrator should be able to create a backup of the backend
system. The Super Administrator can restore the backend system from any backup, the System
Administrator only from a specific backup.
'''

import hashlib

class PasswordHasherSalter():
    @classmethod
    def hash_password(cls, plain_password):
        return hashlib.sha256(plain_password.encode()).hexdigest()

    def salt_password(cls, password):
        pass
