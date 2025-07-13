import sqlite3
import os
import uuid
from contextlib import contextmanager
from datetime import datetime

from presentation_layer.utils.Roles import Roles
from logic_layer.utils.PasswordHasherSalter import PasswordHasherSalter


initial_dummy_pass = PasswordHasherSalter.hash_salt_password("sV5~8lgS|ri%")
class DBContext:
    def __init__(self, db_name='urban_mobility.db'):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.db_name = os.path.join(base_dir, db_name)

        self._replace_old_users_table()
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


    def _replace_old_users_table(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM old_users")
            old_data = cursor.fetchall()

            for row in old_data:
                cursor.execute('''
                    INSERT OR IGNORE INTO users (
                        id, username, hashed_salted_password, role,
                        first_name, last_name, registration_date, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),   # New UUID
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                ))

    def _create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            # Traveller table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS travellers (
                    customer_id TEXT PRIMARY KEY,
                    registration_date TEXT,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    birthday TEXT,
                    gender VARCHAR(10),
                    street_name VARCHAR(100),
                    house_number INTEGER,
                    zip_code VARCHAR(10),
                    city VARCHAR(50),
                    email VARCHAR(100),
                    mobile_phone VARCHAR(20),
                    driving_license_number VARCHAR(20)
                )
            ''')

            # Seed travellers
            cursor.execute("SELECT 1 FROM travellers WHERE customer_id = ?", ("CUST001",))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO travellers (
                        customer_id,
                        registration_date,
                        first_name,
                        last_name,
                        birthday,
                        gender,
                        street_name,
                        house_number,
                        zip_code,
                        city,
                        email,
                        mobile_phone,
                        driving_license_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    "CUST001",
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "Alice",
                    "Willems",
                    "1996-07-12",
                    "Female",
                    "Kanaalstraat",
                    145,
                    "1054XD",
                    "Amsterdam",
                    "alice.willems@example.com",
                    "+31612345678",
                    "DLN-A1234567"
                ))

            # 2
            cursor.execute("SELECT 1 FROM travellers WHERE customer_id = ?", ("CUST002",))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO travellers (
                        customer_id,
                        registration_date,
                        first_name,
                        last_name,
                        birthday,
                        gender,
                        street_name,
                        house_number,
                        zip_code,
                        city,
                        email,
                        mobile_phone,
                        driving_license_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    "CUST002",
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "Mehdi",
                    "El Hamdaoui",
                    "1988-11-23",
                    "Male",
                    "Laan van NOI",
                    78,
                    "2595AV",
                    "The Hague",
                    "mehdi.hamdaoui@example.com",
                    "+31687654321",
                    "DLN-B7654321"
                ))

            # User table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT PRIMARY KEY,
                    hashed_salted_password VARCHAR(128),
                    role VARCHAR(30),
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    registration_date TEXT,
                    is_active BOOL
                )
            ''')
            # Seed user with dummy service engineer and system engineer
            cursor.execute("SELECT 1 FROM users WHERE username = ?", ("DummyAcc1_",))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO users (
                        id,
                        username,
                        hashed_salted_password,
                        role,
                        first_name,
                        last_name,
                        registration_date,
                        is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    "2bf36451-ee7c-43f8-8573-c070dcbe18e5",
                    "DummyAcc1_",
                    initial_dummy_pass,
                    Roles.SERVICE_ENGINEER.value,
                    "Dummy",
                    "ServiceEngineer",
                    None,
                    True
                ))
            cursor.execute("SELECT 1 FROM users WHERE username = ?", ("DummyAcc2_",))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO users (
                        id,
                        username,
                        hashed_salted_password,
                        role,
                        first_name,
                        last_name,
                        registration_date,
                        is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    "caa2fc3b-7198-466b-b9d5-9b926da012c2",
                    "DummyAcc2_",
                    initial_dummy_pass,
                    Roles.SYSTEM_ADMINISTRATOR.value,
                    "Dummy",
                    "SystemAdmin",
                    None,
                    True
                ))
            cursor.execute("SELECT 1 FROM users WHERE username = ?", ("DummyAcc222_",))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO users (
                        id,
                        username,
                        hashed_salted_password,
                        role,
                        first_name,
                        last_name,
                        registration_date,
                        is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    "ead64393-6e8b-48df-be72-3fd1e2a7844e",
                    "DummyAcc222_",
                    initial_dummy_pass,
                    Roles.SYSTEM_ADMINISTRATOR.value,
                    "Dummy",
                    "SystemAdmin",
                    None,
                    True
                ))

            # Scooter table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scooters (
                    serial_number VARCHAR(20) PRIMARY KEY,
                    in_service_date DATE,
                    brand VARCHAR(50),
                    model VARCHAR(50),
                    top_speed INTEGER,
                    battery_capacity INTEGER,
                    state_of_charge INTEGER,
                    target_soc_min INTEGER,
                    target_soc_max INTEGER,
                    latitude VARCHAR(20),
                    longitude VARCHAR(20),
                    out_of_service VARCHAR(20),
                    mileage REAL,
                    last_maintenance_date DATE
                )
            ''')

            # Seed scooters
            cursor.execute("SELECT 1 FROM scooters WHERE serial_number = ?", ("SC-0001",))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO scooters (
                        serial_number,
                        in_service_date,
                        brand,
                        model,
                        top_speed,
                        battery_capacity,
                        state_of_charge,
                        target_soc_min,
                        target_soc_max,
                        latitude,
                        longitude,
                        out_of_service,
                        mileage,
                        last_maintenance_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    "SC-0001",
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "Xiaomi",
                    "M365 Pro",
                    25,
                    474,
                    85,
                    30,
                    90,
                    "52.3676",     # Amsterdam
                    "4.9041",
                    "False",
                    1543.7,
                    "2024-12-01"
                ))

            cursor.execute("SELECT 1 FROM scooters WHERE serial_number = ?", ("SC-0002",))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO scooters (
                        serial_number,
                        in_service_date,
                        brand,
                        model,
                        top_speed,
                        battery_capacity,
                        state_of_charge,
                        target_soc_min,
                        target_soc_max,
                        latitude,
                        longitude,
                        out_of_service,
                        mileage,
                        last_maintenance_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    "SC-0002",
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "Segway",
                    "Ninebot Max",
                    30,
                    551,
                    40,
                    25,
                    85,
                    "51.9244",     # Rotterdam
                    "4.4777",
                    "True",
                    2398.5,
                    "2025-02-15"
                ))

            # Logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    username VARCHAR(20),
                    description VARCHAR(225),
                    additional_info VARCHAR(225),
                    suspicious INTEGER
                )
            ''')

            # Backup codes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backup_codes (
                    code VARCHAR(64) PRIMARY KEY,
                    assigned_to_username VARCHAR(20),
                    backup_filename VARCHAR(100),
                    created_at TEXT,
                    used INTEGER
                )
            ''')
