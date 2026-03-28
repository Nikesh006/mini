from app import app, db
# Explicitly import models to ensure SQLAlchemy detects them
from models import User, Member, Equipment, EquipmentUsage, Attendance, Payment

def update_db():
    with app.app_context():
        print("Synchronizing database schema...")
        try:
            # This will create any tables that are missing (Equipment and EquipmentUsage)
            db.create_all()
            print("--- SUCCESS ---")
            print("Tables 'equipment' and 'equipment_usage' have been created.")
        except Exception as e:
            print(f"--- ERROR ---")
            print(f"Could not update database: {e}")

if __name__ == "__main__":
    update_db()
