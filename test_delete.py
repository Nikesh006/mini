import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.dyxrxcfavrfffmepqacl:Nikesh%40%23%232006@aws-1-ap-south-1.pooler.supabase.com:6543/postgres'

from app import app, db, User, delete_user_archive

print("Testing delete_user_archive on Supabase...")
with app.app_context():
    user = User.query.filter_by(role='user').first()
    if user:
        print(f"Attempting to delete user ID {user.id} ({user.username})...")
        try:
            delete_user_archive(user)
            print("Deletion completed successfully without errors!")
        except Exception as e:
            print("CRASH DETECTED!")
            import traceback
            traceback.print_exc()
    else:
        print("No standard user found in the database. Cannot test.")
