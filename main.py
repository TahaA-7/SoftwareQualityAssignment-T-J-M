# main.py

from db.db_context import DBContext

def main():
    db = DBContext()  # Creates DB and tables if they don't exist

    # Example usage: print all users
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Users in system:")
        for user in users:
            print(user)

if __name__ == '__main__':
    main()
