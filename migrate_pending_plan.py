from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        print("Migrating database to add 'pending_plan_id' to 'member' table...")
        try:
            db.session.execute(text("ALTER TABLE member ADD COLUMN pending_plan_id INTEGER REFERENCES membership_plan(id)"))
            db.session.commit()
            print("--- SUCCESS ---")
            print("Column 'pending_plan_id' added successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"--- NOTICE ---")
            print(f"Column might already exist or error occurred: {e}")

if __name__ == "__main__":
    migrate()
