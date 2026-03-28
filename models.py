from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
from utils import get_ist_time

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gym_id = db.Column(db.String(50), index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user') # 'admin', 'user', 'trainer'
    profile_pic = db.Column(db.String(255), default='default.png')
    phone = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    dob = db.Column(db.Date)
    date_created = db.Column(db.DateTime, default=get_ist_time)
    deletion_requested = db.Column(db.Boolean, default=False)
    login_count = db.Column(db.Integer, default=0)
    otp = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)

    # Relationships
    member_profile = db.relationship('Member', backref='user', uselist=False, cascade="all, delete-orphan")
    trainer_profile = db.relationship('Trainer', backref='user', uselist=False, cascade="all, delete-orphan")

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gym_id = db.Column(db.String(50), index=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    membership_type = db.Column(db.String(50))
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plan.id'))
    pending_plan_id = db.Column(db.Integer, db.ForeignKey('membership_plan.id'))
    status = db.Column(db.String(20), default='Active') # 'Active', 'Expired'
    is_approved = db.Column(db.Boolean, default=False)
    workout_days = db.Column(db.String(255)) # Store as comma-separated days
    expiry_date = db.Column(db.DateTime)
    date_approved = db.Column(db.DateTime)

    # Relationship
    plan = db.relationship('MembershipPlan', foreign_keys=[plan_id], backref='members')
    pending_plan = db.relationship('MembershipPlan', foreign_keys=[pending_plan_id], backref='pending_members')

class MembershipPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, default=30) # New field: 30, 90, 365
    features = db.Column(db.Text) # Comma separated or JSON
    created_at = db.Column(db.DateTime, default=get_ist_time)

class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gym_id = db.Column(db.String(50), index=True)
    full_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    experience = db.Column(db.Integer) # in years
    phone = db.Column(db.String(20))
    is_approved = db.Column(db.Boolean, default=False)

class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=False)
    plan_name = db.Column(db.String(100))
    exercises = db.Column(db.Text)
    day = db.Column(db.String(20)) # e.g., 'Monday', 'Tuesday', etc.
    created_at = db.Column(db.DateTime, default=get_ist_time)

    # Relationships
    member = db.relationship('Member', backref='workout_plans')
    trainer = db.relationship('Trainer', backref='workout_plans')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    gym_id = db.Column(db.String(50), index=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=get_ist_time)
    status = db.Column(db.String(20), default='Paid') # 'Paid', 'Pending'

    # Relationship
    member = db.relationship('Member', backref='payments')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=True)
    check_in = db.Column(db.DateTime, default=get_ist_time)
    check_out = db.Column(db.DateTime)
    date = db.Column(db.Date, default=lambda: get_ist_time().date())

    # Relationships
    member = db.relationship('Member', backref='attendance_records')
    trainer = db.relationship('Trainer', backref='attendance_records')

class WeightLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=get_ist_time)

    member = db.relationship('Member', backref='weight_logs')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True) # Optional link to equipment
    booking_date = db.Column(db.Date, nullable=False)
    booking_time_from = db.Column(db.Time, nullable=False)
    booking_time_to = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Pending') # 'Pending', 'Confirmed', 'Cancelled'
    created_by_role = db.Column(db.String(20), default='user') # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=get_ist_time)

    member = db.relationship('Member', backref='bookings')
    trainer = db.relationship('Trainer', backref='bookings')
    equipment = db.relationship('Equipment', backref='bookings')

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_per_day = db.Column(db.Float, default=0.0)

class CustomPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    selected_days = db.Column(db.String(200)) # e.g., "Monday, Wednesday, Friday"
    amenities = db.Column(db.Text) # JSON string of selected amenity names
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Approved, Paid
    created_at = db.Column(db.DateTime, default=get_ist_time)

    member = db.relationship('Member', backref='custom_plans')

class ExportLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False) # 'Revenue', 'Attendance'
    performed_at = db.Column(db.DateTime, default=get_ist_time)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    total_amount = db.Column(db.Float, default=0.0)
    performed_by = db.Column(db.String(100))

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gym_id = db.Column(db.String(50), index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1) # Total number of units
    broken_quantity = db.Column(db.Integer, default=0) # Number of units not working
    status = db.Column(db.String(20), default='Working') # 'Working', 'Maintenance'
    image_file = db.Column(db.String(255), default='equipment_default.png')
    created_at = db.Column(db.DateTime, default=get_ist_time)

class EquipmentUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=get_ist_time)
    end_time = db.Column(db.DateTime)

    equipment = db.relationship('Equipment', backref='usage_records')
    member = db.relationship('Member', backref='equipment_usages')

class DietPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    breakfast = db.Column(db.Text)
    lunch = db.Column(db.Text)
    dinner = db.Column(db.Text)
    snacks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=get_ist_time)

    # Relationships
    member = db.relationship('Member', backref='diet_plans')
    trainer = db.relationship('Trainer', backref='diet_plans')

