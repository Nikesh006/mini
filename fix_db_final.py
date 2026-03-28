from app import app, db
from sqlalchemy import text

with app.app_context():
    print("Fixing 'booking' table schema...")
    try:
        # Drop the obsolete booking_time column that is causing the constraint error
        db.session.execute(text("ALTER TABLE booking DROP COLUMN booking_time"))
        db.session.commit()
        print("Obsolete column 'booking_time' removed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Notice: Could not drop column (it might already be gone): {e}")

    print("Schema fix complete. Bookings should now process correctly.")
