from app import app, db
from models import User, Member, Trainer, WorkoutPlan, Payment, MembershipPlan, Attendance, Equipment, EquipmentUsage, WeightLog, Booking, Amenity, CustomPlan, ExportLog, DietPlan

def fix_db():
    with app.app_context():
        print("Synchronizing database schema and creating missing tables...")
        try:
            # db.create_all() creates any tables that are missing from the database
            db.create_all()
            print("--- SUCCESS ---")
            print("The 'diet_plan' table (and any other missing tables) should now be present in 'gym_management'.")
        except Exception as e:
            print(f"--- ERROR ---")
            print(f"Could not update database: {e}")

if __name__ == "__main__":
    fix_db()
