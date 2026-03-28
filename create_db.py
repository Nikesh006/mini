import mysql.connector

def create_database():
    user = 'root'
    password = 'Nikesh@2006'
    host = 'localhost'
    db_name = 'gymcopy'

    try:
        print(f"Attempting to connect to MySQL as {user}...")
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Successfully created database '{db_name}' (or it already exists).")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database()
