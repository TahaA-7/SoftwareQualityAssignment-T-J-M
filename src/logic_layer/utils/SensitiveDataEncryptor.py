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
