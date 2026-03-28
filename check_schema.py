from app import app, db
from sqlalchemy import text

with app.app_context():
    print("Checking 'booking' table columns...")
    try:
        # For MySQL/MariaDB
        result = db.session.execute(text("DESCRIBE booking"))
        columns = [row[0] for row in result]
        print(f"Columns in 'booking': {columns}")
        
        required_cols = ['booking_time_from', 'booking_time_to', 'equipment_id', 'created_by_role']
        missing = [c for d in required_cols if d not in columns]
        
        if not missing:
            print("All required columns are present.")
        else:
            print(f"MISSING COLUMNS: {missing}")
            
    except Exception as e:
        print(f"Error describing table: {e}")
