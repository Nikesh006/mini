from app import app, db
from sqlalchemy import text

def update_db():
    with app.app_context():
        print("Synchronizing database schema...")
        try:
            # 1. Add trainer_id to attendance
            print("Adding trainer_id to attendance table...")
            db.session.execute(text("ALTER TABLE attendance ADD COLUMN trainer_id INT NULL"))
            db.session.execute(text("ALTER TABLE attendance MODIFY COLUMN member_id INT NULL"))
            db.session.commit()
            print("Success: trainer_id added.")
        except Exception as e:
            print(f"trainer_id may already exist or error: {e}")

        try:
            # Re-run create_all for any missing tables
            db.create_all()
            print("All tables synchronized.")
        except Exception as e:
            print(f"Error updating tables: {e}")

if __name__ == "__main__":
    update_db()
