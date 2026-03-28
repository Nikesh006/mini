from app import app, db
from models import ExportLog

with app.app_context():
    try:
        logs = ExportLog.query.all()
        print(f"Total Export Logs found: {len(logs)}")
        for log in logs:
            print(f"ID: {log.id}, Type: {log.report_type}, Performed: {log.performed_at}, By: {log.performed_by}")
    except Exception as e:
        print(f"Error querying ExportLog: {e}")
