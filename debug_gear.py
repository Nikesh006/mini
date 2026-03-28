from app import app, db, get_ist_time
from models import Equipment, Booking
from datetime import datetime

with app.app_context():
    now = get_ist_time()
    print(f"Current System Time (IST): {now}")
    print(f"Current Date: {now.date()}")
    print(f"Current Time: {now.time()}")
    
    all_gear = Equipment.query.all()
    print(f"\nEquipment Inventory ({len(all_gear)} items):")
    for gear in all_gear:
        # Debug the query logic
        bookings = Booking.query.filter(
            Booking.equipment_id == gear.id,
            Booking.status.in_(['Confirmed', 'Pending']),
            Booking.booking_date == now.date()
        ).all()
        
        print(f"\n- {gear.name} (ID: {gear.id}, Total Qty: {gear.quantity})")
        print(f"  Active/Pending Bookings for today: {len(bookings)}")
        
        occupied_count = 0
        for b in bookings:
            print(f"    Booking ID {b.id}: {b.booking_time_from} to {b.booking_time_to} (Status: {b.status})")
            if b.booking_time_from <= now.time() <= b.booking_time_to:
                occupied_count += 1
                print(f"    => OCCUPYING NOW")
        
        available = max(0, gear.quantity - occupied_count)
        print(f"  CALCULATED AVAILABLE NOW: {available}")
