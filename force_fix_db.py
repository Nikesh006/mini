import mysql.connector

def force_fix():
    print("Connecting to MySQL...")
    try:
        conn = mysql.connector.connect(
            user='root',
            password='Nikesh@2006',
            host='localhost',
            database='gym_management'
        )
        cursor = conn.cursor()
        print("Adding 'status' column to 'equipment' table...")
        cursor.execute("ALTER TABLE equipment ADD COLUMN status VARCHAR(20) DEFAULT 'Working'")
        conn.commit()
        print("SUCCESS: Database column added.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        if err.errno == 1060:
            print("INFO: Column 'status' already exists. You are good to go!")
        else:
            print(f"ERROR: {err}")

if __name__ == "__main__":
    force_fix()
