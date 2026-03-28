import mysql.connector

def add_status_column():
    config = {
        'user': 'root',
        'password': 'Nikesh@2006',
        'host': 'localhost',
        'database': 'gym_management'
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE equipment ADD COLUMN status VARCHAR(20) DEFAULT 'Working'")
        conn.commit()
        print("Successfully added status column to equipment table.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    add_status_column()
