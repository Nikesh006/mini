from app import app, db
from models import User, Member, Trainer, Payment, Attendance

def check_tables():
    with app.app_context():
        try:
            u = User.query.count()
            m = Member.query.count()
            t = Trainer.query.count()
            p = Payment.query.count()
            a = Attendance.query.count()
            print(f"User: {u}, Member: {m}, Trainer: {t}, Payment: {p}, Attendance: {a}")
            print("All core tables are accessible.")
        except Exception as e:
            print(f"Error accessing tables: {e}")

if __name__ == "__main__":
    check_tables()
