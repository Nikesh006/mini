from app import app, db
from sqlalchemy import text

with app.app_context():
    print("Forcing database schema sync...")
    try:
        # Check and add created_by_role
        db.session.execute(text("ALTER TABLE booking ADD COLUMN created_by_role VARCHAR(20) DEFAULT 'user'"))
        db.session.commit()
        print("Column 'created_by_role' added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Notice: created_by_role might already exist or error: {e}")

    try:
        # Check and add booking_time_from/to just in case
        db.session.execute(text("ALTER TABLE booking ADD COLUMN booking_time_from TIME"))
        db.session.execute(text("ALTER TABLE booking ADD COLUMN booking_time_to TIME"))
        db.session.commit()
        print("Time columns verified.")
    except Exception as e:
        db.session.rollback()
        print("Notice: Time columns might already exist.")

    try:
        # Check and add equipment_id
        db.session.execute(text("ALTER TABLE booking ADD COLUMN equipment_id INTEGER REFERENCES equipment(id)"))
        db.session.commit()
        print("Equipment link verified.")
    except Exception as e:
        db.session.rollback()
        print("Notice: equipment_id might already exist.")

    print("Schema sync complete.")
