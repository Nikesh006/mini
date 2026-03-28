import mysql.connector
from app import app, db
from models import Equipment
import mysql.connector

def fix_everything():
    # 1. Manually add the status column via raw MySQL if it's missing
    print("Step 1: Checking/Adding 'status' column to MySQL...")
    config = {
        'user': 'root',
        'password': 'Nikesh@2006',
        'host': 'localhost',
        'database': 'gym_management'
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # Check if column exists
        cursor.execute("SHOW COLUMNS FROM equipment LIKE 'status'")
        result = cursor.fetchone()
        if not result:
            print("Status column missing. Adding it now...")
            cursor.execute("ALTER TABLE equipment ADD COLUMN status VARCHAR(20) DEFAULT 'Working'")
            conn.commit()
            print("Status column added successfully.")
        else:
            print("Status column already exists.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database sync warning/error: {err}")

    # 2. Add sample equipment using the Flask App Context
    print("\nStep 2: Adding sample equipment...")
    with app.app_context():
        samples = [
            {
                'name': 'Treadmill X-500',
                'description': 'High-end treadmill with heart rate monitoring and incline control.',
                'status': 'Working'
            },
            {
                'name': 'Olympic Barbell',
                'description': 'Standard 20kg barbell for heavy lifting.',
                'status': 'Working'
            },
            {
                'name': 'Dumbbell Set (5kg-50kg)',
                'description': 'Complete set of rubber-coated dumbbells.',
                'status': 'Working'
            },
            {
                'name': 'Leg Press Machine',
                'description': 'Heavy-duty leg press machine. Currently awaiting cable replacement.',
                'status': 'Maintenance'
            },
            {
                'name': 'Power Rack',
                'description': 'Versatile power rack for squats, bench press, and pull-ups.',
                'status': 'Working'
            }
        ]

        for s in samples:
            existing = Equipment.query.filter_by(name=s['name']).first()
            if not existing:
                new_item = Equipment(
                    name=s['name'],
                    description=s['description'],
                    status=s['status'],
                    image_file='equipment_default.png'
                )
                db.session.add(new_item)
                print(f"Added: {s['name']}")
        
        db.session.commit()
        print("Done!")

if __name__ == "__main__":
    fix_everything()
