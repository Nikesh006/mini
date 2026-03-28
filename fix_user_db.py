from app import app, db
from sqlalchemy import text

with app.app_context():
    print("Fixing 'user' table schema...")
    try:
        # Add login_count column
        db.session.execute(text("ALTER TABLE user ADD COLUMN login_count INTEGER DEFAULT 0"))
        db.session.commit()
        print("login_count column added successfully.")
        
        # Initialize it to 1 for all existing users (since they have logged in at least once)
        # or 0 if you prefer. Setting to 1 so they get 'Welcome back' immediately.
        db.session.execute(text("UPDATE user SET login_count = 1 WHERE login_count IS NULL"))
        db.session.commit()
        print("Existing users initialized to login_count = 1.")
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        db.session.rollback()
