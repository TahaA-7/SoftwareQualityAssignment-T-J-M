'''
Log
The system should log all activities. All suspicious activities must be flagged, and the system needs to
produce an alert/notification for unread suspicious activities once a System Administrator or Super
Administrator is logged in to the system. The content of the log file(s) must be encrypted and should be
only readable through the system interface, by the System Administrator or Super Administrator. It
means that it should not be readable by any other tool, such as file explorer, browser or text editor.
'''
import os
import datetime
from cryptography.fernet import Fernet
from access_layer.db.LogData import log_data

class Logger:
    LOG_FILE = os.path.join(os.path.dirname(__file__), "../../system.log.enc")
    KEY_FILE = os.path.join(os.path.dirname(__file__), "../../logkey.key")
    ALERT_FILE = os.path.join(os.path.dirname(__file__), "../../alerts.flag")
    LOG_HEADER = "No.;Date;Time;Username;Description;Additional Information;Suspicious\n"

    @staticmethod
    def _get_key():
        if not os.path.exists(Logger.KEY_FILE):
            key = Fernet.generate_key()
            with open(Logger.KEY_FILE, "wb") as f:
                f.write(key)
        else:
            with open(Logger.KEY_FILE, "rb") as f:
                key = f.read()
        return key

    @staticmethod
    def _get_next_log_number():
        key = Logger._get_key()
        fernet = Fernet(key)
        if not os.path.exists(Logger.LOG_FILE):
            return 1
        count = 0
        with open(Logger.LOG_FILE, "rb") as f:
            for line in f:
                try:
                    decrypted = fernet.decrypt(line.strip()).decode()
                    if decrypted and decrypted[0].isdigit():
                        count += 1
                except Exception:
                    continue
        return count + 1
    
    @staticmethod
    def log(username, description, additional_info="", suspicious=False):
        key = Logger._get_key()
        fernet = Fernet(key)
        now = datetime.datetime.now()
        log_no = Logger._get_next_log_number()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")
        suspicious_str = "Yes" if suspicious else "No"
        log_entry = f"{log_no};{date};{time};{username};{description};{additional_info};{suspicious_str}\n"
        encrypted_entry = fernet.encrypt(log_entry.encode())

        with open(Logger.LOG_FILE, "ab") as f:
            f.write(encrypted_entry + b"\n")

        # encrypty voor database
        enc_username = fernet.encrypt(username.encode()).decode()
        enc_description = fernet.encrypt(description.encode()).decode()
        enc_additional_info = fernet.encrypt(additional_info.encode()).decode()

        # database
        log_db = log_data()
        log_db.add_log(
            f"{date} {time}",
            enc_username,
            enc_description,
            enc_additional_info,
            suspicious_str
        )

        if suspicious:
            with open(Logger.ALERT_FILE, "a") as f:
                f.write(f"{log_no};{date};{time};{username};{description}\n")


    @staticmethod
    def read_logs(user_role):
        # Only System Administrator (2) or Super Administrator (3) can read logs
        if user_role not in [2, 3]:
            raise PermissionError("Insufficient rights to read logs.")
        key = Logger._get_key()
        fernet = Fernet(key)
        logs = []
        if not os.path.exists(Logger.LOG_FILE):
            return logs
        with open(Logger.LOG_FILE, "rb") as f:
            for line in f:
                try:
                    decrypted = fernet.decrypt(line.strip()).decode()
                    logs.append(decrypted)
                except Exception:
                    continue
        return [Logger.LOG_HEADER] + logs if logs else [Logger.LOG_HEADER]
    
    @staticmethod
    def check_alerts(user_role):
        # Only System Administrator (2) or Super Administrator (3) can see alerts
        if user_role not in [2, 3]:
            return []
        if not os.path.exists(Logger.ALERT_FILE):
            return []
        with open(Logger.ALERT_FILE, "r") as f:
            alerts = f.readlines()
        # Clear alerts after reading
        open(Logger.ALERT_FILE, "w").close()
        return [alert.strip() for alert in alerts]