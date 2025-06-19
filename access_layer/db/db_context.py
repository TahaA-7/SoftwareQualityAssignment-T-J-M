import sqlite3
from contextlib import contextmanager


class DBContext:
    def __init__(self, db_name='urban_mobility.db'):
        self.db_name = db_name
        self._create_tables()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            # Traveller table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS travellers (
                    customer_id TEXT PRIMARY KEY,
                    registration_date TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    birthday TEXT,
                    gender TEXT,
                    street_name TEXT,
                    house_number INTEGER,
                    zip_code TEXT,
                    city TEXT,
                    email TEXT,
                    mobile_phone TEXT,
                    driving_license_number TEXT
                )
            ''')

            # User table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    hashed_password TEXT,
                    role TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    registration_date TEXT
                )
            ''')

            # Scooter table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scooters (
                    serial_number TEXT PRIMARY KEY,
                    in_service_date TEXT,
                    brand TEXT,
                    model TEXT,
                    top_speed INTEGER,
                    battery_capacity INTEGER,
                    state_of_charge INTEGER,
                    target_soc_min INTEGER,
                    target_soc_max INTEGER,
                    latitude REAL,
                    longitude REAL,
                    out_of_service INTEGER,
                    mileage REAL,
                    last_maintenance_date TEXT
                )
            ''')

            # Logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    username TEXT,
                    description TEXT,
                    additional_info TEXT,
                    suspicious INTEGER
                )
            ''')

            # Backup codes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backup_codes (
                    code TEXT PRIMARY KEY,
                    assigned_to_username TEXT,
                    backup_filename TEXT,
                    created_at TEXT,
                    used INTEGER
                )
            ''')
