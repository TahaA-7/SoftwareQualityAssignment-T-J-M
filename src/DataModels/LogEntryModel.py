from datetime import datetime


class LogEntry:
    def __init__(self, username, description, additional_info='', suspicious=False):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.username = username
        self.description = description
        self.additional_info = additional_info
        self.suspicious = suspicious  # Boolean
