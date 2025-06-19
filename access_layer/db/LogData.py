from access_layer.db.db_context import DBContext

class log_data:
    def __init__(self):
        self.db = DBContext()

    def get_logs(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, username, description, additional_info, suspicious
                FROM logs
                ORDER BY timestamp DESC
            ''')
            return cursor.fetchall()
