# main.py

from access_layer.db.db_context import DBContext

class DB_Startup():

    @classmethod
    def startup(cls):
        db = DBContext()  # Creates DB and tables if they don't exist

        # Example usage: print all users
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            # print("Users in system:")
            # for user in users:
            #     print(user)
