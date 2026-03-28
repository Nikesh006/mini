
import os
import sys

# Add the current directory to sys.path so we can import app and models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, text

def update_database():
    with app.app_context():
        try:
            # Add age column if it doesn't exist
            try:
                db.session.execute(text("ALTER TABLE user ADD COLUMN age INTEGER"))
                db.session.commit()
                print("Added age column to user table.")
            except Exception as e:
                db.session.rollback()
                print(f"Notice: Age column not added (it might already exist).")
            
            # Add gender column if it doesn't exist
            try:
                db.session.execute(text("ALTER TABLE user ADD COLUMN gender VARCHAR(20)"))
                db.session.commit()
                print("Added gender column to user table.")
            except Exception as e:
                db.session.rollback()
                print(f"Notice: Gender column not added (it might already exist).")
            
            # Update existing members with defaults
            db.session.execute(text("UPDATE user SET age = 20 WHERE age IS NULL"))
            db.session.execute(text("UPDATE user SET gender = 'male' WHERE gender IS NULL"))
            db.session.commit()
            print("Successfully updated existing members with default age=20 and gender=male.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error during database update: {e}")

if __name__ == "__main__":
    update_database()
