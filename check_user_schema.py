from app import app, db
from sqlalchemy import text

with app.app_context():
    print("Checking 'user' table columns...")
    try:
        # For MySQL/MariaDB
        result = db.session.execute(text("DESCRIBE user"))
        columns = [row[0] for row in result]
        print(f"Columns in 'user': {columns}")
        
        if 'login_count' in columns:
            print("login_count column is present.")
        else:
            print("MISSING COLUMN: login_count")
            
    except Exception as e:
        print(f"Error describing table: {e}")
