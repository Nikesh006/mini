from app import app, db
from models import ExportLog
from datetime import date

with app.app_context():
    try:
        log = ExportLog(
            report_type='Test',
            start_date=date.today(),
            end_date=date.today(),
            total_amount=100.0,
            performed_by='system_test'
        )
        db.session.add(log)
        db.session.commit()
        print("Manual Test Log added successfully.")
        
        logs = ExportLog.query.all()
        print(f"Total Export Logs now: {len(logs)}")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
