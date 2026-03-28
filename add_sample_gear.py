from app import app, db
from models import Equipment

def add_sample_equipment():
    with app.app_context():
        samples = [
            {
                'name': 'Treadmill X-500',
                'description': 'High-end treadmill with heart rate monitoring and incline control.',
                'status': 'Working'
            },
            {
                'name': 'Olympic Barbell',
                'description': 'Standard 20kg barbell for heavy lifting.',
                'status': 'Working'
            },
            {
                'name': 'Dumbbell Set (5kg-50kg)',
                'description': 'Complete set of rubber-coated dumbbells.',
                'status': 'Working'
            },
            {
                'name': 'Leg Press Machine',
                'description': 'Heavy-duty leg press machine. Currently awaiting cable replacement.',
                'status': 'Maintenance'
            },
            {
                'name': 'Power Rack',
                'description': 'Versatile power rack for squats, bench press, and pull-ups.',
                'status': 'Working'
            }
        ]

        for s in samples:
            # Check if already exists to avoid duplicates
            existing = Equipment.query.filter_by(name=s['name']).first()
            if not existing:
                new_item = Equipment(
                    name=s['name'],
                    description=s['description'],
                    status=s['status'],
                    image_file='equipment_default.png'
                )
                db.session.add(new_item)
        
        db.session.commit()
        print("Sample equipment added successfully!")

if __name__ == "__main__":
    add_sample_equipment()
