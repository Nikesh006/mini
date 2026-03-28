from app import app, db
from models import User, Trainer, Attendance
from utils import get_ist_time

with app.app_context():
    admin = User.query.filter_by(role='admin').first()
    if admin:
        print(f"Admin found: {admin.username} (ID: {admin.id})")
        trainer_profile = Trainer.query.filter_by(user_id=admin.id).first()
        if trainer_profile:
            print(f"Admin HAS a trainer profile: ID {trainer_profile.id}")
            active = Attendance.query.filter_by(trainer_id=trainer_profile.id, check_out=None).first()
            if active:
                print(f"Active shift found for admin-as-trainer: ID {active.id}, Started: {active.check_in}")
            else:
                print("No active shift for admin-as-trainer.")
        else:
            print("Admin does NOT have a trainer profile.")
    else:
        print("No admin user found.")
