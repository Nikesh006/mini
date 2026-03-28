import mysql.connector

def migrate():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nikesh@2006",
            database="gym_management"
        )
        cursor = conn.cursor()

        # Check for column
        cursor.execute("DESCRIBE equipment")
        columns = [column[0] for column in cursor.fetchall()]
        
        if 'broken_quantity' not in columns:
            print("Adding broken_quantity column to MySQL...")
            cursor.execute("ALTER TABLE equipment ADD COLUMN broken_quantity INT DEFAULT 0")
            
            # Migrate data from status if it exists
            if 'status' in columns:
                print("Migrating Maintenance status to broken_quantity...")
                cursor.execute("UPDATE equipment SET broken_quantity = quantity WHERE status = 'Maintenance'")
                # Optional: Drop status column
                # cursor.execute("ALTER TABLE equipment DROP COLUMN status")
        else:
            print("Column 'broken_quantity' already exists.")

        conn.commit()
        print("Migration complete!")
    except Exception as e:
        print(f"MySQL Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    migrate()
