import os
import io
import random
import string
from datetime import datetime, timedelta, timezone
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from sqlalchemy import text, or_, and_
from sqlalchemy.orm import joinedload
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from config import Config
from models import db, User, Member, Trainer, WorkoutPlan, Payment, MembershipPlan, Attendance, Equipment, EquipmentUsage, WeightLog, Booking, Amenity, CustomPlan, ExportLog, DietPlan
from utils import IST, get_ist_time, send_email, allowed_file
import json
from functools import wraps

USE_FONT = 'Helvetica'

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background-color: #1e1e1e; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #333; }}
        .header {{ background: linear-gradient(135deg, #ff4b2b, #ff416c); padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; color: #fff; }}
        .content {{ padding: 30px; line-height: 1.6; }}
        .details-box {{ background-color: #2a2a2a; border-left: 4px solid #ff4b2b; padding: 20px; margin: 20px 0; border-radius: 4px; }}
        .detail-item {{ margin-bottom: 10px; font-size: 16px; }}
        .detail-label {{ font-weight: bold; color: #ff4b2b; text-transform: uppercase; font-size: 12px; display: block; }}
        .detail-value {{ color: #fff; font-size: 18px; }}
        .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #777; border-top: 1px solid #333; }}
        .btn {{ display: inline-block; padding: 12px 25px; background-color: #ff4b2b; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
        </div>
        <div class="content">
            <p>Hello {name},</p>
            <p>{message}</p>
            <div class="details-box">
                {details}
            </div>
            <p>Keep pushing your limits!</p>
            <a href="https://gymmasterelite.com/dashboard" class="btn">View Dashboard</a>
        </div>
        <div class="footer">
            &copy; 2024 Gym Master Elite. All rights reserved.
        </div>
    </div>
</body>
</html>
"""

BLUE_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background-color: #1e1e1e; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #333; }}
        .header {{ background: linear-gradient(135deg, #00c6ff, #0072ff); padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; color: #fff; }}
        .content {{ padding: 30px; line-height: 1.6; }}
        .details-box {{ background-color: #2a2a2a; border-left: 4px solid #00c6ff; padding: 20px; margin: 20px 0; border-radius: 4px; }}
        .detail-item {{ margin-bottom: 10px; font-size: 16px; }}
        .detail-label {{ font-weight: bold; color: #00c6ff; text-transform: uppercase; font-size: 12px; display: block; }}
        .detail-value {{ color: #fff; font-size: 18px; }}
        .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #777; border-top: 1px solid #333; }}
        .btn {{ display: inline-block; padding: 12px 25px; background-color: #0072ff; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
        </div>
        <div class="content">
            <p>Hello {name},</p>
            <p>{message}</p>
            <div class="details-box">
                {details}
            </div>
            <p>Keep pushing your limits!</p>
            <a href="https://gymmasterelite.com/dashboard" class="btn">View Dashboard</a>
        </div>
        <div class="footer">
            &copy; 2024 Gym Master Elite. All rights reserved.
        </div>
    </div>
</body>
</html>
"""

RED_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background-color: #1e1e1e; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #333; }}
        .header {{ background: linear-gradient(135deg, #cb2d3e, #ef473a); padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; color: #fff; }}
        .content {{ padding: 30px; line-height: 1.6; }}
        .details-box {{ background-color: #2a2a2a; border-left: 4px solid #ef473a; padding: 20px; margin: 20px 0; border-radius: 4px; }}
        .detail-item {{ margin-bottom: 10px; font-size: 16px; }}
        .detail-label {{ font-weight: bold; color: #ef473a; text-transform: uppercase; font-size: 12px; display: block; }}
        .detail-value {{ color: #fff; font-size: 18px; }}
        .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #777; border-top: 1px solid #333; }}
        .btn {{ display: inline-block; padding: 12px 25px; background-color: #ef473a; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
        </div>
        <div class="content">
            <p>Hello {name},</p>
            <p>{message}</p>
            <div class="details-box">
                {details}
            </div>
            <p>Keep pushing your limits!</p>
            <a href="https://gymmasterelite.com/dashboard" class="btn">View Dashboard</a>
        </div>
        <div class="footer">
            &copy; 2024 Gym Master Elite. All rights reserved.
        </div>
    </div>
</body>
</html>
"""

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
_runtime_schema_checked = False

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash('ACCESS DENIED: YOU DO NOT HAVE THE REQUIRED AUTHORIZATION LEVEL.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def trainer_shift_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'trainer':
            trainer = Trainer.query.filter_by(user_id=current_user.id).first()
            if trainer:
                # Logic: A shift is active if there is any record without a check_out time
                active_shift = Attendance.query.filter_by(trainer_id=trainer.id, check_out=None).first()
                if not active_shift:
                    flash('SHIFT PROTOCOL: YOU MUST CHECK-IN FOR YOUR SHIFT TO ACCESS COMPLETE GYM DATA.', 'warning')
                    return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def normalize_gym_id(raw_gym_id):
    if not raw_gym_id:
        return None
    return raw_gym_id.strip().upper()

def get_current_gym_id():
    if not current_user.is_authenticated:
        return None
    return normalize_gym_id(getattr(current_user, 'gym_id', None))

def get_admins_for_gym(gym_id):
    normalized_gym_id = normalize_gym_id(gym_id)
    query = User.query.filter_by(role='admin')
    if normalized_gym_id:
        query = query.filter_by(gym_id=normalized_gym_id)
    return query.all()

def apply_payment_gym_scope(query, gym_id=None):
    scoped_gym_id = normalize_gym_id(gym_id) if gym_id is not None else get_current_gym_id()
    if not scoped_gym_id:
        return query
    return query.outerjoin(Member, Payment.member_id == Member.id).filter(
        or_(
            Payment.gym_id == scoped_gym_id,
            and_(Payment.gym_id.is_(None), Member.gym_id == scoped_gym_id)
        )
    )

def ensure_runtime_schema():
    global _runtime_schema_checked
    if _runtime_schema_checked:
        return

    db.create_all()

    try:
        db.session.execute(text("ALTER TABLE equipment ADD COLUMN gym_id VARCHAR(50)"))
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        db.session.execute(text("ALTER TABLE payment ADD COLUMN gym_id VARCHAR(50)"))
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        db.session.execute(text("""
            UPDATE payment p
            JOIN member m ON p.member_id = m.id
            SET p.gym_id = m.gym_id
            WHERE p.gym_id IS NULL
        """))
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        db.session.execute(text("ALTER TABLE booking MODIFY trainer_id INTEGER NULL"))
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        unscoped_equipment = Equipment.query.filter(Equipment.gym_id.is_(None)).all()
        if unscoped_equipment:
            known_gym_ids = [
                gym_id for (gym_id,) in db.session.query(User.gym_id).filter(User.gym_id.isnot(None)).distinct().all()
                if gym_id
            ]
            default_gym_id = known_gym_ids[0] if len(known_gym_ids) == 1 else None

            for gear in unscoped_equipment:
                booking_gym_ids = [
                    gym_id for (gym_id,) in (
                        db.session.query(Member.gym_id)
                        .join(Booking, Booking.member_id == Member.id)
                        .filter(Booking.equipment_id == gear.id, Member.gym_id.isnot(None))
                        .distinct()
                        .all()
                    )
                    if gym_id
                ]

                if len(booking_gym_ids) == 1:
                    gear.gym_id = booking_gym_ids[0]
                elif default_gym_id:
                    gear.gym_id = default_gym_id

            db.session.commit()
    except Exception:
        db.session.rollback()

    _runtime_schema_checked = True

@app.before_request
def ensure_runtime_schema_before_request():
    ensure_runtime_schema()

def get_equipment_query_for_current_gym():
    ensure_runtime_schema()
    gym_id = get_current_gym_id()
    return Equipment.query.filter_by(gym_id=gym_id) if gym_id else Equipment.query

def delete_user_archive(user):
    member = Member.query.filter_by(user_id=user.id).first()
    trainer = Trainer.query.filter_by(user_id=user.id).first()

    try:
        if member:
            WorkoutPlan.query.filter_by(member_id=member.id).delete()
            Payment.query.filter_by(member_id=member.id).delete()
            Attendance.query.filter_by(member_id=member.id).delete()
            Booking.query.filter_by(member_id=member.id).delete()
            WeightLog.query.filter_by(member_id=member.id).delete()
            CustomPlan.query.filter_by(member_id=member.id).delete()
            DietPlan.query.filter_by(member_id=member.id).delete()
            EquipmentUsage.query.filter_by(member_id=member.id).delete()
            db.session.delete(member)

        if trainer:
            WorkoutPlan.query.filter_by(trainer_id=trainer.id).delete()
            Attendance.query.filter_by(trainer_id=trainer.id).delete()
            Booking.query.filter_by(trainer_id=trainer.id).delete()
            DietPlan.query.filter_by(trainer_id=trainer.id).delete()
            db.session.delete(trainer)

        db.session.delete(user)
        db.session.commit()

        try:
            db.session.execute(db.text("ALTER TABLE user AUTO_INCREMENT = 1"))
            db.session.execute(db.text("ALTER TABLE member AUTO_INCREMENT = 1"))
            db.session.execute(db.text("ALTER TABLE trainer AUTO_INCREMENT = 1"))
            db.session.commit()
        except Exception:
            db.session.rollback()
    except Exception:
        db.session.rollback()
        raise

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/resend_otp')
def resend_otp():
    user_id = session.get('pending_user_id')
    if not user_id:
        flash('Session expired. Please register again.', 'danger')
        return redirect(url_for('register'))
    
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for('register'))
    
    # Generate new OTP
    otp = ''.join(random.choices(string.digits, k=6))
    user.otp = otp
    user.otp_expiry = get_ist_time() + timedelta(minutes=5)
    db.session.commit()
    
    # Send OTP Email
    subject = "Nammude Gym: New Email Verification OTP"
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
            .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #007bff; }}
            h1 {{ color: #007bff; font-size: 28px; margin-bottom: 20px; }}
            p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
            .otp {{ font-size: 36px; font-weight: bold; letter-spacing: 4px; color: #ffffff; background: #333; padding: 15px; display: inline-block; margin: 20px 0; border: 1px dashed #007bff; }}
            .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SECURITY VERIFICATION</h1>
            <p>Hello {user.username},</p>
            <p>Your security verification code for Nammude Gym is:</p>
            <div class="otp">{otp}</div>
            <p>This code is valid for <strong>5 minutes</strong>. Please enter it on the verification page to authorize your account.</p>
            <div class="footer">
                Best Regards,<br>
                <strong>Team Nammude Gym</strong>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(subject, html_body, user.email)
    
    flash('SECURITY ALERT: A new verification code has been dispatched to your email.', 'info')
    return redirect(url_for('verify_otp'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            if user.deletion_requested:
                flash('ALERT: ACCOUNT DELETION PENDING. ACCESS RESTRICTED.', 'danger')
                return redirect(url_for('login'))
                
            if user.role == 'trainer':
                trainer = Trainer.query.filter_by(user_id=user.id).first()
                if trainer and not trainer.is_approved:
                    flash('WAITING FOR ADMIN APPROVAL: COACH REGISTRATION.', 'warning')
                    return redirect(url_for('login'))
            elif user.role == 'user':
                member = Member.query.filter_by(user_id=user.id).first()
                if member and not member.is_approved:
                    flash('WAITING FOR ADMIN APPROVAL: ATHLETE REGISTRATION.', 'warning')
                    return redirect(url_for('login'))
            
            login_user(user)
            
            # Update login count and show appropriate message
            if user.login_count == 0:
                flash(f'Welcome to Nammude Gym, {user.username}!', 'success')
            else:
                flash(f'Welcome back, {user.username}!', 'success')
            
            user.login_count += 1
            db.session.commit()
            
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
            
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        user = User.query.filter_by(username=username, email=email).first()
        
        if user:
            otp = ''.join(random.choices(string.digits, k=6))
            user.otp = otp
            user.otp_expiry = get_ist_time() + timedelta(minutes=5)
            db.session.commit()
            
            # Send OTP Email
            subject = "Nammude Gym: Password Reset OTP"
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                    .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #ff4b2b; }}
                    h1 {{ color: #ff4b2b; font-size: 28px; margin-bottom: 20px; }}
                    p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                    .otp {{ font-size: 36px; font-weight: bold; letter-spacing: 4px; color: #ffffff; background: #333; padding: 15px; display: inline-block; margin: 20px 0; border: 1px dashed #ff4b2b; }}
                    .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>PASSWORD RECOVERY PROTOCOL</h1>
                    <p>Hello {user.username.upper()},</p>
                    <p>We received a request to reset your secure passcode. Your verification code is:</p>
                    <div class="otp">{otp}</div>
                    <p>This code is valid for <strong>5 minutes</strong>. If you did not request this, please ignore this email.</p>
                    <div class="footer">
                        Best Regards,<br>
                        <strong>Team Nammude Gym</strong>
                    </div>
                </div>
            </body>
            </html>
            """
            send_email(subject, html_body, user.email)
            flash('RECOVERY DISPATCHED: A secure verification code has been sent to your email.', 'info')
            return redirect(url_for('reset_password', email=email))
        else:
            flash('ACCESS DENIED: No account associated with this email address.', 'danger')
            
    return render_template('forgot_password.html')

@app.route('/reset-password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    user = User.query.filter_by(email=email).first_or_404()
    
    if request.method == 'POST':
        otp = request.form.get('otp')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash('PROTOCOL VIOLATION: Passcodes do not match.', 'danger')
            return render_template('reset_password.html', email=email)
            
        if user.otp == otp and user.otp_expiry > get_ist_time():
            user.password = new_password
            user.otp = None
            user.otp_expiry = None
            db.session.commit()
            
            # Send Success Notification Email
            subject = "Nammude Gym: Passcode Reset Successful"
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                    .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #4CAF50; }}
                    h1 {{ color: #4CAF50; font-size: 28px; margin-bottom: 20px; }}
                    p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                    .status-box {{ background: #333; padding: 20px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #4CAF50; }}
                    .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>SECURITY UPDATED</h1>
                    <p>Hello {user.username.upper()},</p>
                    <div class="status-box">
                        <p><strong>SUCCESS:</strong> Your secure passcode has been successfully updated.</p>
                    </div>
                    <p>If you did not perform this action, please contact Nammude Gym administration immediately to secure your account.</p>
                    <div class="footer">
                        Best Regards,<br>
                        <strong>Team Nammude Gym</strong>
                    </div>
                </div>
            </body>
            </html>
            """
            send_email(subject, html_body, user.email)
            
            flash('SUCCESS: Secure passcode has been updated. Access granted.', 'success')
            return redirect(url_for('login'))
        else:
            flash('VERIFICATION FAILED: Invalid or expired code.', 'danger')
            
    return render_template('reset_password.html', email=email)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    def build_registration_form_data(form):
        return {
            'username': form.get('username', ''),
            'email': form.get('email', ''),
            'phone': form.get('phone', ''),
            'gym_id': form.get('gym_id', ''),
            'dob': form.get('dob', ''),
            'age': form.get('age', ''),
            'gender': form.get('gender', 'male'),
            'password': form.get('password', ''),
            'role': form.get('role', 'user'),
            'specialization': form.get('specialization', ''),
            'experience': form.get('experience', ''),
            'height': form.get('height', ''),
            'weight': form.get('weight', ''),
            'plan_id': form.get('plan_id', ''),
            'workout_days': form.getlist('workout_days')
        }
    
    if request.method == 'POST':
        form_data = build_registration_form_data(request.form)
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age_raw = request.form.get('age')
        age = int(age_raw) if age_raw and age_raw.strip() else 20
        password = request.form.get('password')
        role = request.form.get('role', 'user') # default is user
        gym_id = normalize_gym_id(request.form.get('gym_id'))
        gender = request.form.get('gender', 'male') if role != 'admin' else None
        dob_raw = request.form.get('dob') if role != 'admin' else None
        dob = datetime.strptime(dob_raw, '%Y-%m-%d').date() if dob_raw else None

        if not gym_id:
            flash('Gym ID is required for registration.', 'danger')
            return render_template('register.html', plans=MembershipPlan.query.all(), form_data=form_data)

        existing_admin = User.query.filter_by(role='admin', gym_id=gym_id).first()
        if role == 'admin':
            if existing_admin:
                flash('This Gym ID already exists. Admin registration must use a new Gym ID.', 'danger')
                return render_template('register.html', plans=MembershipPlan.query.all(), form_data=form_data)
        elif not existing_admin:
            flash('Gym ID not found. Members and trainers can only register under an existing admin Gym ID.', 'danger')
            return render_template('register.html', plans=MembershipPlan.query.all(), form_data=form_data)

        # Profile Picture Handling
        profile_pic_filename = 'default.png'
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add username prefix to make it unique
                filename = f"{username}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic_filename = filename

        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            if user_exists.username == username and user_exists.email == email:
                flash('This username and email are already used.', 'danger')
            elif user_exists.username == username:
                flash('This user ID is already used.', 'danger')
            else:
                flash('This email is already used.', 'danger')
            return render_template('register.html', plans=MembershipPlan.query.all(), form_data=form_data)

        new_user = User(username=username, email=email, phone=phone, age=age, dob=dob, gender=gender, password=password, role=role, profile_pic=profile_pic_filename, gym_id=gym_id)
        # Generate and Store OTP
        otp = ''.join(random.choices(string.digits, k=6))
        new_user.otp = otp
        new_user.otp_expiry = get_ist_time() + timedelta(minutes=5)
        
        db.session.add(new_user)
        db.session.commit()

        # Temporary storage for registration details to complete after OTP
        member_data = None
        if role == 'user':
            workout_days = request.form.getlist('workout_days')
            workout_days_str = ", ".join(workout_days)
            height_raw = request.form.get('height')
            weight_raw = request.form.get('weight')
            height = float(height_raw) if height_raw and height_raw.strip() else None
            weight = float(weight_raw) if weight_raw and weight_raw.strip() else None
            plan_id_raw = request.form.get('plan_id')
            plan_id = int(plan_id_raw) if plan_id_raw and plan_id_raw.strip() else None
            
            member_data = {
                'full_name': username,
                'phone': phone,
                'gym_id': gym_id,
                'workout_days': workout_days_str,
                'height': height,
                'weight': weight,
                'plan_id': plan_id
            }
        elif role == 'trainer':
            experience = request.form.get('experience', 0)
            specialization = request.form.get('specialization', 'Strength Training')
            member_data = {
                'full_name': username,
                'gym_id': gym_id,
                'specialization': specialization,
                'experience': experience,
                'phone': phone
            }

        # Store in session for finalization after OTP
        from flask import session
        session['pending_user_id'] = new_user.id
        session['pending_member_data'] = member_data

        # Send OTP Email
        subject = "Nammude Gym: Email Verification OTP"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #007bff; }}
                h1 {{ color: #007bff; font-size: 28px; margin-bottom: 20px; }}
                p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                .otp {{ font-size: 36px; font-weight: bold; letter-spacing: 4px; color: #ffffff; background: #333; padding: 15px; display: inline-block; margin: 20px 0; border: 1px dashed #007bff; }}
                .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SECURITY VERIFICATION</h1>
                <p>Hello {username},</p>
                <p>Your security verification code for Nammude Gym registration is:</p>
                <div class="otp">{otp}</div>
                <p>This code is valid for <strong>5 minutes</strong>. Please enter it on the verification page to authorize your account creation.</p>
                <div class="footer">
                    Best Regards,<br>
                    <strong>Team Nammude Gym</strong>
                </div>
            </div>
        </body>
        </html>
        """
        send_email(subject, html_body, email)
        
        flash('SECURITY PROTOCOL: A 6-digit verification code has been dispatched to your email.', 'info')
        return redirect(url_for('verify_otp'))
        
    plans = MembershipPlan.query.all()
    return render_template('register.html', plans=plans, form_data=build_registration_form_data(request.form))

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    from flask import session
    user_id = session.get('pending_user_id')
    if not user_id:
        flash('Session expired. Please register again.', 'danger')
        return redirect(url_for('register'))
        
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for('register'))

    if request.method == 'POST':
        entered_otp_raw = request.form.get('otp', '')
        entered_otp = ''.join(ch for ch in entered_otp_raw.strip() if ch.isdigit())
        stored_otp = ''.join(ch for ch in (user.otp or '').strip() if ch.isdigit())
        otp_not_expired = bool(user.otp_expiry) and user.otp_expiry >= get_ist_time()

        if stored_otp and stored_otp == entered_otp and otp_not_expired:
            # OTP Verified - Finalize Registration
            member_data = session.get('pending_member_data')
            
            if user.role == 'user' and member_data:
                member = Member(user_id=user.id, **member_data, is_approved=False)
                db.session.add(member)
            elif user.role == 'trainer' and member_data:
                trainer = Trainer(user_id=user.id, **member_data, is_approved=False)
                db.session.add(trainer)
            
            user.otp = None # Clear OTP after success
            db.session.commit()
            
            # Notify Admins of New Registration
            try:
                admin_users = get_admins_for_gym(user.gym_id)
                admin_emails = [u.email for u in admin_users]
                
                admin_details = f"""
                    <div class="detail-item">
                        <span class="detail-label">Username</span>
                        <span class="detail-value">{user.username}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Role</span>
                        <span class="detail-value">{'ATHLETE' if user.role == 'user' else 'COACH'}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Contact</span>
                        <span class="detail-value">{user.email} / {user.phone or 'N/A'}</span>
                    </div>
                """
                
                admin_html = BLUE_EMAIL_TEMPLATE.format(
                    title="NEW REGISTRATION RECEIVED",
                    name="Admin",
                    message="A new user has verified their email and is awaiting your authorization.",
                    details=admin_details
                )
                
                for admin_email in admin_emails:
                    send_email("NEW REGISTRATION RECEIVED - Nammude Gym", admin_html, admin_email)
            except Exception as e:
                print(f"Error notifying admins of new registration: {e}")
            
            # Send Success Email
            subject = "Nammude Gym: Email Verified & Registration Received"
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                    .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #007bff; }}
                    h1 {{ color: #007bff; font-size: 28px; margin-bottom: 20px; }}
                    p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                    .status {{ color: #007bff; font-weight: bold; }}
                    .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>REGISTRATION RECEIVED</h1>
                    <p>Hello {user.username},</p>
                    <p>Your email has been <span class="status">successfully verified!</span></p>
                    <p>Your registration as a <strong>{user.role.upper()}</strong> is now <strong>PENDING</strong> admin approval. You will receive another notification once your access has been authorized.</p>
                    <div class="footer">
                        Best Regards,<br>
                        <strong>Team Nammude Gym</strong>
                    </div>
                </div>
            </body>
            </html>
            """
            send_email(subject, html_body, user.email)
            
            session.pop('pending_user_id', None)
            session.pop('pending_member_data', None)
            
            flash('Email verified! Your registration is now pending admin approval.', 'success')
            return redirect(url_for('login'))
        else:
            flash('INVALID SECURITY CODE: The code provided is incorrect or has expired.', 'danger')
            
    return render_template('verify_otp.html')

@app.context_processor
def inject_now():
    active_session = None
    pending_bookings_count = 0
    pending_custom_plans_count = 0
    pending_plan_changes_count = 0
    if current_user.is_authenticated:
        if current_user.role == 'trainer':
            trainer = Trainer.query.filter_by(user_id=current_user.id).first()
            if trainer:
                active_session = Attendance.query.filter_by(trainer_id=trainer.id, check_out=None).first()
                pending_bookings_count = Booking.query.filter_by(trainer_id=trainer.id, status='Pending').count()
        elif current_user.role == 'admin':
            gym_id = get_current_gym_id()
            active_session = True # Admins are always on duty
            if gym_id:
                pending_bookings_count = Booking.query.join(Member, Booking.member_id == Member.id).filter(
                    Booking.status == 'Pending',
                    Member.gym_id == gym_id
                ).count()
                pending_custom_plans_count = CustomPlan.query.join(Member, CustomPlan.member_id == Member.id).filter(
                    CustomPlan.status == 'Pending',
                    Member.gym_id == gym_id
                ).count()
                pending_plan_changes_count = Member.query.filter(
                    Member.pending_plan_id.isnot(None),
                    Member.gym_id == gym_id
                ).count()
            else:
                pending_bookings_count = Booking.query.filter_by(status='Pending').count()
                pending_custom_plans_count = CustomPlan.query.filter_by(status='Pending').count()
                pending_plan_changes_count = Member.query.filter(Member.pending_plan_id.isnot(None)).count()
            
    return {
        'now': get_ist_time(), 
        'active_session': active_session, 
        'pending_bookings_count': pending_bookings_count, 
        'pending_custom_plans_count': pending_custom_plans_count,
        'pending_plan_changes_count': pending_plan_changes_count
    }

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        gym_id = get_current_gym_id()
        member_query = Member.query.filter_by(gym_id=gym_id) if gym_id else Member.query
        trainer_query = Trainer.query.filter_by(gym_id=gym_id) if gym_id else Trainer.query
        user_query = User.query.filter_by(gym_id=gym_id) if gym_id else User.query
        custom_plan_query = CustomPlan.query.join(Member, CustomPlan.member_id == Member.id).filter(Member.gym_id == gym_id) if gym_id else CustomPlan.query

        members_count = member_query.filter_by(is_approved=True).count()
        pending_members_count = member_query.filter_by(is_approved=False).count()
        trainers_count = trainer_query.filter_by(is_approved=True).count()
        pending_trainers_count = trainer_query.filter_by(is_approved=False).count()
        deletion_requests_count = user_query.filter_by(deletion_requested=True).count()
        pending_custom_plans_count = custom_plan_query.filter_by(status='Pending').count()
        pending_plan_changes = member_query.filter(Member.pending_plan_id.isnot(None)).all()
        
        # Calculate daily gross revenue (TODAY only)
        today = get_ist_time().date()
        total_revenue = apply_payment_gym_scope(
            db.session.query(db.func.sum(Payment.amount)).select_from(Payment).filter(db.func.date(Payment.payment_date) == today),
            gym_id
        ).scalar()
        if total_revenue is None:
            total_revenue = 0
            
        # Get activity logs for TODAY only (IST)
        today = get_ist_time().date()
        recent_check_ins_query = Attendance.query.options(joinedload(Attendance.member), joinedload(Attendance.trainer)).filter_by(date=today)
        recent_payments_query = apply_payment_gym_scope(
            Payment.query.options(joinedload(Payment.member)).filter(db.func.date(Payment.payment_date) == today),
            gym_id
        )
        if gym_id:
            recent_check_ins_query = recent_check_ins_query.outerjoin(Member, Attendance.member_id == Member.id).outerjoin(Trainer, Attendance.trainer_id == Trainer.id).filter(
                or_(Member.gym_id == gym_id, Trainer.gym_id == gym_id)
            )
        recent_check_ins = recent_check_ins_query.order_by(Attendance.check_in.desc()).all()
        recent_payments = recent_payments_query.order_by(Payment.payment_date.desc()).all()
        
        recent_logs = []
        for a in recent_check_ins:
            user_name = 'Unknown'
            if a.member:
                user_name = a.member.full_name
            elif a.trainer:
                user_name = f"{a.trainer.full_name} (Coach)"
            
            recent_logs.append({
                'type': 'Attendance', 
                'user': user_name, 
                'time': a.check_in, 
                'out_time': a.check_out,
                'msg': 'Check-in session'
            })
        for p in recent_payments:
            recent_logs.append({
                'type': 'Payment', 
                'user': p.member.full_name if p.member else 'Unknown', 
                'time': p.payment_date, 
                'out_time': None,
                'msg': f'Paid ₹{p.amount}'
            })
        
        recent_logs.sort(key=lambda x: x['time'], reverse=True)
        # We can still limit it to the most recent 10 of today if desired
        recent_logs = recent_logs[:10]

        all_members = member_query.filter_by(is_approved=True).order_by(Member.full_name).all()

        return render_template('admin_dashboard.html', 
                               members_count=members_count, 
                               pending_members_count=pending_members_count,
                               trainers_count=trainers_count, 
                               pending_trainers_count=pending_trainers_count, 
                               deletion_requests_count=deletion_requests_count,
                               pending_custom_plans_count=pending_custom_plans_count,
                               pending_plan_changes=pending_plan_changes,
                               total_revenue=total_revenue,
                               recent_logs=recent_logs,
                               all_members=all_members,
                               gym_id=gym_id)

    elif current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        active_session = Attendance.query.filter_by(trainer_id=trainer.id, date=get_ist_time().date(), check_out=None).first() if trainer else None
        admins = get_admins_for_gym(trainer.gym_id if trainer else None)
        members = Member.query.filter_by(gym_id=trainer.gym_id).all() if trainer and trainer.gym_id else Member.query.all()
        # Fetch today's records for the session count metric
        records = Attendance.query.join(Member, Attendance.member_id == Member.id).filter(
            Attendance.date == get_ist_time().date(),
            Member.gym_id == trainer.gym_id
        ).all() if trainer and trainer.gym_id else Attendance.query.filter_by(date=get_ist_time().date()).all()
        return render_template('trainer_dashboard.html', 
                               trainer=trainer, 
                               admins=admins, 
                               members=members, 
                               active_session=active_session,
                               records=records)
    else:
        member = Member.query.filter_by(user_id=current_user.id).first()
        
        # Check if membership has expired
        if member and member.expiry_date and member.expiry_date < get_ist_time():
            member.status = 'Expired'
            db.session.commit()
            
        # Calculate actual sessions logged
        sessions_count = Attendance.query.filter_by(member_id=member.id).count() if member else 0
        
        # Get latest workout protocol
        latest_workout = WorkoutPlan.query.filter_by(member_id=member.id).order_by(WorkoutPlan.created_at.desc()).first() if member else None
        
        # Get latest diet protocol
        latest_diet = DietPlan.query.filter_by(member_id=member.id).order_by(DietPlan.created_at.desc()).first() if member else None
        
        admins = get_admins_for_gym(member.gym_id if member else None)
        trainers = Trainer.query.filter_by(is_approved=True, gym_id=member.gym_id).all() if member and member.gym_id else Trainer.query.filter_by(is_approved=True).all()
        return render_template('user_dashboard.html', 
                               member=member, 
                               admins=admins, 
                               trainers=trainers, 
                               sessions_count=sessions_count,
                               latest_workout=latest_workout,
                               latest_diet=latest_diet)

@app.route('/book_session', methods=['GET', 'POST'])
@login_required
@role_required(['user', 'admin'])
def book_session():
    if request.method == 'POST':
        trainer_id = request.form.get('trainer_id')
        equipment_id = request.form.get('equipment_id')
        booking_date_str = request.form.get('booking_date')
        booking_time_from_str = request.form.get('booking_time_from')
        booking_time_to_str = request.form.get('booking_time_to')
        
        # PROTOCOL CHECK: Mandatory Date and Time Range
        if not booking_date_str or not booking_time_from_str or not booking_time_to_str:
            flash('ERROR: TARGET DATE, FROM TIME, AND TO TIME ARE COMPULSORY FOR ALL SESSIONS.', 'danger')
            return redirect(url_for('book_session'))
        
        # Admin can select member, User books for themselves
        if current_user.role == 'admin':
            member_id = request.form.get('member_id')
        else:
            member = Member.query.filter_by(user_id=current_user.id).first()
            member_id = member.id if member else None
            
        if not member_id:
            flash('Error: No valid athlete profile found for booking.', 'danger')
            return redirect(url_for('dashboard'))
        
        try:
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
            booking_time_from = datetime.strptime(booking_time_from_str, '%H:%M').time()
            booking_time_to = datetime.strptime(booking_time_to_str, '%H:%M').time()
            
            # Convert to integers for safety
            t_id = int(trainer_id) if trainer_id else None
            e_id = int(equipment_id) if (equipment_id and equipment_id.strip() != "") else None
            m_id = int(member_id) if member_id else None
            current_gym_id = get_current_gym_id()

            if current_gym_id:
                selected_member = db.session.get(Member, m_id) if m_id else None
                selected_trainer = db.session.get(Trainer, t_id) if t_id else None
                if selected_member and selected_member.gym_id != current_gym_id:
                    flash('Selected member does not belong to your Gym ID.', 'danger')
                    return redirect(url_for('book_session'))
                if selected_trainer and selected_trainer.gym_id != current_gym_id:
                    flash('Selected trainer does not belong to your Gym ID.', 'danger')
                    return redirect(url_for('book_session'))

            # Equipment Availability Check (Checking against BOTH Confirmed and Pending for safety)
            if e_id:
                equip = db.session.get(Equipment, e_id)
                if current_gym_id and equip and equip.gym_id != current_gym_id:
                    flash('Selected equipment does not belong to your Gym ID.', 'danger')
                    return redirect(url_for('book_session'))
                if equip:
                    working_quantity = max(0, equip.quantity - equip.broken_quantity)
                    overlapping_count = Booking.query.filter(
                        Booking.equipment_id == e_id,
                        Booking.booking_date == booking_date,
                        Booking.status.in_(['Confirmed', 'Pending']),
                        Booking.booking_time_from < booking_time_to,
                        Booking.booking_time_to > booking_time_from
                    ).count()
                    
                    if overlapping_count >= working_quantity:
                        flash(f'BOOKING ERROR: {equip.name.upper()} IS FULLY RESERVED OR IN MAINTENANCE FOR THIS TIME SLOT. PLEASE SELECT ANOTHER GEAR OR WINDOW.', 'danger')
                        return redirect(url_for('book_session'))

            # Admins automatically confirm the booking
            status = 'Confirmed' if current_user.role == 'admin' else 'Pending'
            
            new_booking = Booking(
                member_id=m_id, 
                trainer_id=t_id, 
                equipment_id=e_id,
                booking_date=booking_date, 
                booking_time_from=booking_time_from, 
                booking_time_to=booking_time_to,
                status=status,
                created_by_role=current_user.role
            )
            db.session.add(new_booking)
            db.session.commit()
            
            # Send Email Notification
            try:
                member = db.session.get(Member, m_id)
                user = db.session.get(User, member.user_id)
                trainer = Trainer.query.get(t_id) if t_id else None
                equipment = Equipment.query.get(e_id) if e_id else None
                
                details = f"""
                    <div class="detail-item">
                        <span class="detail-label">Date</span>
                        <span class="detail-value">{booking_date.strftime('%B %d, %Y')}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Time</span>
                        <span class="detail-value">{booking_time_from.strftime('%I:%M %p')} - {booking_time_to.strftime('%I:%M %p')}</span>
                    </div>
                """
                if trainer:
                    details += f"""
                        <div class="detail-item">
                            <span class="detail-label">Trainer</span>
                            <span class="detail-value">{trainer.full_name}</span>
                        </div>
                    """
                if equipment:
                    details += f"""
                        <div class="detail-item">
                            <span class="detail-label">Equipment</span>
                            <span class="detail-value">{equipment.name}</span>
                        </div>
                    """

                status_msg = "Your session request has been successfully submitted and is pending coach confirmation."
                if current_user.role == 'admin':
                    status_msg = "Your training session has been confirmed and reserved."

                html_body = EMAIL_TEMPLATE.format(
                    title="Booking Request Received",
                    name=member.full_name,
                    message=status_msg,
                    details=details
                )
                send_email("Booking Request Received - Nammude Gym", html_body, user.email)

                # NOTIFY TRAINER AND ADMINS
                details_notify = f"""
                    <div class="detail-item">
                        <span class="detail-label">Member Name</span>
                        <span class="detail-value">{member.full_name}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Date</span>
                        <span class="detail-value">{booking_date.strftime('%B %d, %Y')}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Time</span>
                        <span class="detail-value">{booking_time_from.strftime('%I:%M %p')} - {booking_time_to.strftime('%I:%M %p')}</span>
                    </div>
                """
                if equipment:
                    details_notify += f"""
                        <div class="detail-item">
                            <span class="detail-label">Equipment</span>
                            <span class="detail-value">{equipment.name}</span>
                        </div>
                    """

                admin_users = get_admins_for_gym(member.gym_id)
                admin_emails = [u.email for u in admin_users]
                
                # Admin Notification
                admin_html = BLUE_EMAIL_TEMPLATE.format(
                    title="NEW BOOKING REQUEST",
                    name="Admin",
                    message=f"A new booking request has been submitted by {member.full_name}.",
                    details=details_notify
                )
                for admin_email in admin_emails:
                    send_email("NEW BOOKING REQUEST - Nammude Gym", admin_html, admin_email)
                
                # Trainer Notification
                if trainer:
                    trainer_user = db.session.get(User, trainer.user_id)
                    if trainer_user:
                        trainer_html = BLUE_EMAIL_TEMPLATE.format(
                            title="NEW BOOKING REQUEST",
                            name=trainer.full_name,
                            message=f"A new booking request has been assigned to you by {member.full_name}.",
                            details=details_notify
                        )
                        send_email("NEW BOOKING REQUEST - Nammude Gym", trainer_html, trainer_user.email)

            except Exception as email_err:
                print(f"Error sending booking emails: {email_err}")

            if current_user.role == 'admin':
                flash('Training session and equipment have been successfully booked.', 'success')
                return redirect(url_for('my_bookings'))
            else:
                flash('Your session has been booked. Equipment availability will be locked upon coach confirmation.', 'success')
                return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc() # This will show the real error in your terminal
            flash(f'ERROR: Session archive failed. {e}', 'danger')
            return redirect(url_for('book_session'))
            
    gym_id = get_current_gym_id()
    trainers = Trainer.query.filter_by(is_approved=True, gym_id=gym_id).all() if gym_id else Trainer.query.filter_by(is_approved=True).all()
    members = Member.query.filter_by(is_approved=True, gym_id=gym_id).all() if current_user.role == 'admin' and gym_id else (Member.query.filter_by(is_approved=True).all() if current_user.role == 'admin' else [])
    
    # Calculate real-time availability for the booking form
    equipment_list = get_equipment_query_for_current_gym().filter_by(status='Working').all()
    now = get_ist_time()
    current_time = now.time()
    
    for gear in equipment_list:
        today_bookings = Booking.query.filter(
            Booking.equipment_id == gear.id,
            Booking.status.in_(['Confirmed', 'Pending']),
            Booking.booking_date == now.date()
        ).all()
        
        occupied = 0
        for b in today_bookings:
            if b.booking_time_from < b.booking_time_to:
                if b.booking_time_from <= current_time <= b.booking_time_to:
                    occupied += 1
            else:
                if current_time >= b.booking_time_from or current_time <= b.booking_time_to:
                    occupied += 1
                    
        gear.available_now = max(0, gear.quantity - occupied)
    
    return render_template('book_session.html', 
                           trainers=trainers, 
                           members=members, 
                           equipment=equipment_list)

@app.route('/api/check_equipment_availability')
@login_required
def check_equipment_availability():
    date_str = request.args.get('date')
    time_from_str = request.args.get('from')
    time_to_str = request.args.get('to')
    
    if not all([date_str, time_from_str, time_to_str]):
        return json.dumps({'error': 'Missing parameters'}), 400
        
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_from = datetime.strptime(time_from_str, '%H:%M').time()
        time_to = datetime.strptime(time_to_str, '%H:%M').time()
    except ValueError:
        return json.dumps({'error': 'Invalid format'}), 400
        
    all_gear = get_equipment_query_for_current_gym().all()
    availability = []
    
    for gear in all_gear:
        # Working units are total quantity minus broken units
        working_quantity = max(0, gear.quantity - gear.broken_quantity)
        
        overlapping_count = Booking.query.filter(
            Booking.equipment_id == gear.id,
            Booking.booking_date == selected_date,
            Booking.status.in_(['Confirmed', 'Pending']),
            Booking.booking_time_from < time_to,
            Booking.booking_time_to > time_from
        ).count()
        
        available_count = max(0, working_quantity - overlapping_count)
        availability.append({
            'id': gear.id,
            'name': gear.name.upper(),
            'available': available_count,
            'total': working_quantity
        })
        
    return json.dumps(availability)

@app.route('/my_bookings')
@login_required
@trainer_shift_required
def my_bookings():
    selected_date_str = request.args.get('date')
    today = get_ist_time().date()
    
    query = Booking.query
    
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            query = query.filter(Booking.booking_date == selected_date)
        except ValueError:
            query = query.filter(Booking.booking_date >= today)
    else:
        # Default: Show only today and future bookings
        query = query.filter(Booking.booking_date >= today)

    if current_user.role == 'user':
        member = Member.query.filter_by(user_id=current_user.id).first()
        bookings = query.options(joinedload(Booking.member), joinedload(Booking.trainer), joinedload(Booking.equipment)).filter_by(member_id=member.id).order_by(Booking.booking_date.asc()).all() if member else []
    elif current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        bookings = query.options(joinedload(Booking.member), joinedload(Booking.trainer), joinedload(Booking.equipment)).filter_by(trainer_id=trainer.id).order_by(Booking.booking_date.asc()).all() if trainer else []
    else:
        gym_id = get_current_gym_id()
        if gym_id:
            query = query.join(Member, Booking.member_id == Member.id).filter(Member.gym_id == gym_id)
        bookings = query.options(joinedload(Booking.member), joinedload(Booking.trainer), joinedload(Booking.equipment)).order_by(Booking.booking_date.asc()).all()
        
    return render_template('bookings.html', bookings=bookings, selected_date=selected_date_str)

@app.route('/update_booking_status/<int:booking_id>', methods=['POST'])
@login_required
@role_required(['trainer', 'admin'])
@trainer_shift_required
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    gym_id = get_current_gym_id()
    member = Member.query.get(booking.member_id)
    if gym_id and member and member.gym_id != gym_id:
        flash('Access denied for this booking.', 'danger')
        return redirect(url_for('my_bookings'))

    status = request.form.get('status')
    if status in ['Confirmed', 'Cancelled']:
        booking.status = status
        db.session.commit()
        
        # Send Email Notification
        try:
            user = db.session.get(User, member.user_id)
            trainer = Trainer.query.get(booking.trainer_id) if booking.trainer_id else None
            equipment = Equipment.query.get(booking.equipment_id) if booking.equipment_id else None
            
            title = "Booking Confirmed" if status == 'Confirmed' else "Booking Cancelled"
            message = "Get ready! Your training session has been confirmed by our team." if status == 'Confirmed' else "We regret to inform you that your session has been cancelled."
            
            details = f"""
                <div class="detail-item">
                    <span class="detail-label">Date</span>
                    <span class="detail-value">{booking.booking_date.strftime('%B %d, %Y')}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Time</span>
                    <span class="detail-value">{booking.booking_time_from.strftime('%I:%M %p')} - {booking.booking_time_to.strftime('%I:%M %p')}</span>
                </div>
            """
            if trainer:
                details += f"""
                    <div class="detail-item">
                        <span class="detail-label">Trainer</span>
                        <span class="detail-value">{trainer.full_name}</span>
                    </div>
                """
            if equipment:
                details += f"""
                    <div class="detail-item">
                        <span class="detail-label">Equipment</span>
                        <span class="detail-value">{equipment.name}</span>
                    </div>
                """

            html_body = EMAIL_TEMPLATE.format(
                title=title,
                name=member.full_name,
                message=message,
                details=details
            )
            send_email(f"{title} - Nammude Gym", html_body, user.email)

            if status == 'Cancelled':
                # NOTIFY TRAINER AND ADMINS
                details_notify = f"""
                    <div class="detail-item">
                        <span class="detail-label">Member Name</span>
                        <span class="detail-value">{member.full_name}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Date</span>
                        <span class="detail-value">{booking.booking_date.strftime('%B %d, %Y')}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Time</span>
                        <span class="detail-value">{booking.booking_time_from.strftime('%I:%M %p')} - {booking.booking_time_to.strftime('%I:%M %p')}</span>
                    </div>
                """
                if equipment:
                    details_notify += f"""
                        <div class="detail-item">
                            <span class="detail-label">Equipment</span>
                            <span class="detail-value">{equipment.name}</span>
                        </div>
                    """

                admin_users = get_admins_for_gym(member.gym_id)
                admin_emails = [u.email for u in admin_users]
                
                # Admin Notification
                admin_html = RED_EMAIL_TEMPLATE.format(
                    title="SESSION CANCELLED",
                    name="Admin",
                    message=f"The session for {member.full_name} has been cancelled.",
                    details=details_notify
                )
                for admin_email in admin_emails:
                    send_email("SESSION CANCELLED - Nammude Gym", admin_html, admin_email)
                
                # Trainer Notification
                if trainer:
                    trainer_user = db.session.get(User, trainer.user_id)
                    if trainer_user:
                        trainer_html = RED_EMAIL_TEMPLATE.format(
                            title="SESSION CANCELLED",
                            name=trainer.full_name,
                            message=f"Your session with {member.full_name} has been cancelled.",
                            details=details_notify
                        )
                        send_email("SESSION CANCELLED - Nammude Gym", trainer_html, trainer_user.email)

        except Exception as email_err:
            print(f"Error sending booking update emails: {email_err}")

        flash(f'Booking status updated to {status}.', 'success')
    return redirect(url_for('my_bookings'))

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
@trainer_shift_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Check authorization: Only the member who booked it or an admin can cancel
    if current_user.role == 'user':
        member = Member.query.filter_by(user_id=current_user.id).first()
        if not member or booking.member_id != member.id:
            flash('Unauthorized: You can only cancel your own bookings.', 'danger')
            return redirect(url_for('my_bookings'))
    
    # Check if already cancelled
    if booking.status == 'Cancelled':
        flash('This booking is already cancelled.', 'info')
        return redirect(url_for('my_bookings'))

    booking.status = 'Cancelled'
    db.session.commit()
    
    # Send Email Notification
    try:
        member = Member.query.get(booking.member_id)
        user = db.session.get(User, member.user_id)
        trainer = Trainer.query.get(booking.trainer_id) if booking.trainer_id else None
        equipment = Equipment.query.get(booking.equipment_id) if booking.equipment_id else None
        
        details = f"""
            <div class="detail-item">
                <span class="detail-label">Date</span>
                <span class="detail-value">{booking.booking_date.strftime('%B %d, %Y')}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Time</span>
                <span class="detail-value">{booking.booking_time_from.strftime('%I:%M %p')} - {booking.booking_time_to.strftime('%I:%M %p')}</span>
            </div>
        """
        if trainer:
            details += f"""
                <div class="detail-item">
                    <span class="detail-label">Trainer</span>
                    <span class="detail-value">{trainer.full_name}</span>
                </div>
            """
        if equipment:
            details += f"""
                <div class="detail-item">
                    <span class="detail-label">Equipment</span>
                    <span class="detail-value">{equipment.name}</span>
                </div>
            """

        html_body = EMAIL_TEMPLATE.format(
            title="Booking Cancelled",
            name=member.full_name,
            message="Your session has been cancelled as per request.",
            details=details
        )
        send_email("Booking Cancelled - Nammude Gym", html_body, user.email)

        # NOTIFY TRAINER AND ADMINS
        details_notify = f"""
            <div class="detail-item">
                <span class="detail-label">Member Name</span>
                <span class="detail-value">{member.full_name}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Date</span>
                <span class="detail-value">{booking.booking_date.strftime('%B %d, %Y')}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Time</span>
                <span class="detail-value">{booking.booking_time_from.strftime('%I:%M %p')} - {booking.booking_time_to.strftime('%I:%M %p')}</span>
            </div>
        """
        if equipment:
            details_notify += f"""
                <div class="detail-item">
                    <span class="detail-label">Equipment</span>
                    <span class="detail-value">{equipment.name}</span>
                </div>
            """

        admin_users = get_admins_for_gym(member.gym_id)
        admin_emails = [u.email for u in admin_users]
        
        # Admin Notification
        admin_html = RED_EMAIL_TEMPLATE.format(
            title="SESSION CANCELLED",
            name="Admin",
            message=f"The session for {member.full_name} has been cancelled.",
            details=details_notify
        )
        for admin_email in admin_emails:
            send_email("SESSION CANCELLED - Nammude Gym", admin_html, admin_email)
        
        # Trainer Notification
        if trainer:
            trainer_user = db.session.get(User, trainer.user_id)
            if trainer_user:
                trainer_html = RED_EMAIL_TEMPLATE.format(
                    title="SESSION CANCELLED",
                    name=trainer.full_name,
                    message=f"Your session with {member.full_name} has been cancelled.",
                    details=details_notify
                )
                send_email("SESSION CANCELLED - Nammude Gym", trainer_html, trainer_user.email)

    except Exception as email_err:
        print(f"Error sending cancellation emails: {email_err}")

    flash('Your session has been cancelled. Reserved equipment is now back in stock for this slot.', 'warning')
    return redirect(url_for('my_bookings'))

@app.route('/update_weight', methods=['POST'])
@login_required
@role_required(['trainer', 'admin'])
@trainer_shift_required
def update_weight():
    member_id = request.form.get('member_id')
    new_weight = request.form.get('weight')
    
    member = Member.query.get_or_404(member_id)
    if new_weight:
        weight_val = float(new_weight)
        member.weight = weight_val
        # Log it
        log = WeightLog(member_id=member.id, weight=weight_val)
        db.session.add(log)
        db.session.commit()
        flash(f'Transformation data for {member.full_name} has been recorded.', 'success')
    
    return redirect(url_for('view_progress', user_id=member.user_id))

@app.route('/download_progress/<int:member_id>')
@login_required
@trainer_shift_required
def download_progress(member_id):
    member = Member.query.get_or_404(member_id)
    
    # Permission Check
    if current_user.role == 'user':
        current_member = Member.query.filter_by(user_id=current_user.id).first()
        if not current_member or current_member.id != member.id:
            flash('Unauthorized access to private transformation archive.', 'danger')
            return redirect(url_for('dashboard'))
            
    weight_logs = WeightLog.query.filter_by(member_id=member.id).order_by(WeightLog.date.desc()).all()
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width/2, height - 1*inch, "NAMMUDE GYM - TRANSFORMATION REPORT")
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, height - 1.3*inch, f"Athlete Identity: {member.full_name.upper()}")
    p.drawCentredString(width/2, height - 1.5*inch, f"Generated on: {get_ist_time().strftime('%Y-%m-%d %I:%M %p')}")

    # Summary Stats
    p.rect(0.5*inch, height - 3*inch, 7.5*inch, 1.2*inch)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(1*inch, height - 2.2*inch, "BIOMETRIC SUMMARY")
    p.setFont("Helvetica", 11)
    p.drawString(1*inch, height - 2.5*inch, f"Height: {member.height or 'N/A'} CM")
    p.drawString(1*inch, height - 2.7*inch, f"Latest Weight: {member.weight or 'N/A'} KG")
    
    # BMI Logic
    if member.height and member.weight:
        bmi = member.weight / ((member.height/100)**2)
        status = 'NORMAL' if 18.5 <= bmi <= 24.9 else 'UNDERWEIGHT' if bmi < 18.5 else 'OVERWEIGHT' if 25 <= bmi <= 29.9 else 'OBESE'
        p.drawString(4*inch, height - 2.5*inch, f"Calculated BMI: {bmi:.1f}")
        p.drawString(4*inch, height - 2.7*inch, f"Status Category: {status}")

    # History Table Header
    p.setFont("Helvetica-Bold", 12)
    p.drawString(0.5*inch, height - 3.5*inch, "TRANSFORMATION LOG HISTORY")
    p.line(0.5*inch, height - 3.7*inch, 7.5*inch, height - 3.7*inch)
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(1*inch, height - 3.9*inch, "DATE RECORDED")
    p.drawString(4*inch, height - 3.9*inch, "WEIGHT (KG)")
    p.drawString(6*inch, height - 3.9*inch, "CHANGE")
    p.line(0.5*inch, height - 4.0*inch, 7.5*inch, height - 4.0*inch)

    # Rows
    y = height - 4.3*inch
    p.setFont("Helvetica", 10)
    
    for i in range(len(weight_logs)):
        log = weight_logs[i]
        if y < 1*inch:
            p.showPage()
            y = height - 1*inch
            p.setFont("Helvetica", 10)
            
        p.drawString(1*inch, y, log.date.strftime('%B %d, %Y').upper())
        p.drawString(4*inch, y, f"{log.weight} KG")
        
        # Change calculation
        if i < len(weight_logs) - 1:
            prev_weight = weight_logs[i+1].weight
            diff = log.weight - prev_weight
            change_str = f"{'+' if diff > 0 else ''}{diff:.1f} KG"
            p.drawString(6*inch, y, change_str)
        else:
            p.drawString(6*inch, y, "INITIAL")
            
        y -= 0.3*inch

    # Footer
    p.setFont("Helvetica-Oblique", 9)
    p.drawCentredString(width/2, 0.8*inch, "The path to elite performance is built through consistency. Keep pushing. Team Nammude.")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Transformation_{member.full_name.replace(' ', '_')}.pdf", mimetype='application/pdf')

@app.route('/progress')
@app.route('/progress/<int:user_id>')
@login_required
@trainer_shift_required
def view_progress(user_id=None):
    if user_id and current_user.role in ['admin', 'trainer']:
        target_user_id = user_id
    else:
        target_user_id = current_user.id
        
    member = Member.query.filter_by(user_id=target_user_id).first()
    if not member:
        flash('Athlete profile not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    weight_logs = WeightLog.query.filter_by(member_id=member.id).order_by(WeightLog.date.asc()).all()
    return render_template('progress.html', member=member, weight_logs=weight_logs)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/build_custom_plan', methods=['GET', 'POST'])
@login_required
@role_required(['user'])
def build_custom_plan():
    member = Member.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        selected_days = request.form.getlist('days')
        selected_amenities_ids = request.form.getlist('amenities')
        
        amenities = Amenity.query.filter(Amenity.id.in_(selected_amenities_ids)).all()
        amenity_names = [a.name for a in amenities]
        
        # Calculate price: Sum of amenity daily prices (No Base Gym Access Fee anymore as per request)
        base_daily_price = 0.0 
        daily_amenity_total = sum(a.price_per_day for a in amenities)
        
        total_daily = base_daily_price + daily_amenity_total
        num_days_per_week = len(selected_days)
        
        # Monthly estimate (4 weeks)
        total_price = total_daily * num_days_per_week * 4
        
        new_custom_plan = CustomPlan(
            member_id=member.id,
            selected_days=", ".join(selected_days),
            amenities=json.dumps(amenity_names),
            total_price=total_price,
            status='Pending'
        )
        db.session.add(new_custom_plan)
        db.session.commit()
        flash(f'Custom plan request submitted! Estimated Monthly Total: ₹{total_price:.2f}', 'success')
        return redirect(url_for('dashboard'))
        
    amenities = Amenity.query.all()
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return render_template('build_custom_plan.html', amenities=amenities, days_of_week=days_of_week)

@app.route('/admin/custom_plans')
@login_required
@role_required(['admin'])
def manage_custom_plans():
    gym_id = get_current_gym_id()
    plans_query = CustomPlan.query.join(Member, CustomPlan.member_id == Member.id)
    if gym_id:
        plans_query = plans_query.filter(Member.gym_id == gym_id)
    plans = plans_query.order_by(CustomPlan.created_at.desc()).all()
    return render_template('admin_custom_plans.html', plans=plans, json=json)

@app.route('/admin/approve_custom_plan/<int:plan_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def approve_custom_plan(plan_id):
    plan = CustomPlan.query.get_or_404(plan_id)
    gym_id = get_current_gym_id()
    member = Member.query.get(plan.member_id)
    if gym_id and member and member.gym_id != gym_id:
        flash('Access denied for this custom plan.', 'danger')
        return redirect(url_for('manage_custom_plans'))

    plan.status = 'Approved'
    
    # Record payment
    new_payment = Payment(member_id=plan.member_id, gym_id=member.gym_id, amount=plan.total_price, status='Paid')
    db.session.add(new_payment)
    
    # Update member status and expiry (30 days for custom plan)
    member.status = 'Active'
    member.expiry_date = get_ist_time() + timedelta(days=30)
    member.workout_days = plan.selected_days
    # CLEAR Regular plan to indicate they are now on Custom Plan ONLY
    member.plan_id = None
    
    db.session.commit()
    
    # Send Email Notification
    try:
        user = db.session.get(User, member.user_id)
        details = f"""
            <div class="detail-item">
                <span class="detail-label">Selected Days</span>
                <span class="detail-value">{plan.selected_days}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Amenities</span>
                <span class="detail-value">{", ".join(json.loads(plan.amenities))}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Total Price</span>
                <span class="detail-value">₹{plan.total_price:.2f}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Expiry Date</span>
                <span class="detail-value">{member.expiry_date.strftime('%B %d, %Y')}</span>
            </div>
        """
        
        html_body = EMAIL_TEMPLATE.format(
            title="Custom Plan Approved",
            name=member.full_name,
            message="Congratulations! Your custom workout plan has been approved and activated. Your payment has been recorded successfully.",
            details=details
        )
        send_email("Custom Plan Approved - Nammude Gym", html_body, user.email)
    except Exception as email_err:
        print(f"Error sending custom plan approval email: {email_err}")

    flash(f'Custom plan for {member.full_name} approved and payment of ₹{plan.total_price} recorded.', 'success')
    return redirect(url_for('manage_custom_plans'))

@app.cli.command("init-db")
def init_db():
    db.create_all()
    
    # Manual schema update for existing tables
    try:
        # User updates
        try:
            db.session.execute(text("ALTER TABLE user ADD COLUMN dob DATE"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE user ADD COLUMN age INTEGER"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE user ADD COLUMN gender VARCHAR(20)"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE user ADD COLUMN gym_id VARCHAR(50)"))
            db.session.commit()
        except Exception:
            db.session.rollback()

        # Member updates
        try:
            db.session.execute(text("ALTER TABLE member ADD COLUMN gym_id VARCHAR(50)"))
            db.session.commit()
        except Exception:
            db.session.rollback()

        # Trainer updates
        try:
            db.session.execute(text("ALTER TABLE trainer ADD COLUMN gym_id VARCHAR(50)"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE payment ADD COLUMN gym_id VARCHAR(50)"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("""
                UPDATE member m
                JOIN user u ON m.user_id = u.id
                SET m.gym_id = u.gym_id
                WHERE m.gym_id IS NULL
            """))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("""
                UPDATE trainer t
                JOIN user u ON t.user_id = u.id
                SET t.gym_id = u.gym_id
                WHERE t.gym_id IS NULL
            """))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("""
                UPDATE payment p
                JOIN member m ON p.member_id = m.id
                SET p.gym_id = m.gym_id
                WHERE p.gym_id IS NULL
            """))
            db.session.commit()
        except Exception:
            db.session.rollback()

        # MembershipPlan updates
        try:
            db.session.execute(text("ALTER TABLE membership_plan ADD COLUMN duration_days INTEGER DEFAULT 30"))
            db.session.commit()
        except Exception:
            db.session.rollback()

        # Equipment updates
        try:
            db.session.execute(text("ALTER TABLE equipment ADD COLUMN quantity INTEGER DEFAULT 1"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE equipment ADD COLUMN gym_id VARCHAR(50)"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            unscoped_equipment = Equipment.query.filter(Equipment.gym_id.is_(None)).all()
            if unscoped_equipment:
                known_gym_ids = [
                    gym_id for (gym_id,) in db.session.query(User.gym_id).filter(User.gym_id.isnot(None)).distinct().all()
                    if gym_id
                ]
                default_gym_id = known_gym_ids[0] if len(known_gym_ids) == 1 else None

                for gear in unscoped_equipment:
                    booking_gym_ids = [
                        gym_id for (gym_id,) in (
                            db.session.query(Member.gym_id)
                            .join(Booking, Booking.member_id == Member.id)
                            .filter(Booking.equipment_id == gear.id, Member.gym_id.isnot(None))
                            .distinct()
                            .all()
                        )
                        if gym_id
                    ]

                    if len(booking_gym_ids) == 1:
                        gear.gym_id = booking_gym_ids[0]
                    elif default_gym_id:
                        gear.gym_id = default_gym_id

                db.session.commit()
        except Exception:
            db.session.rollback()

        # Booking updates - ADDED INDIVIDUALLY TO PREVENT SILENT FAILURES
        for col_def in [
            "ALTER TABLE booking ADD COLUMN booking_time_from TIME",
            "ALTER TABLE booking ADD COLUMN booking_time_to TIME",
            "ALTER TABLE booking ADD COLUMN equipment_id INTEGER REFERENCES equipment(id)",
            "ALTER TABLE booking ADD COLUMN created_by_role VARCHAR(20) DEFAULT 'user'"
        ]:
            try:
                db.session.execute(text(col_def))
                db.session.commit()
            except Exception:
                db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE booking MODIFY trainer_id INTEGER NULL"))
            db.session.commit()
        except Exception:
            db.session.rollback()

    except Exception as e:
        print(f"Migration Notice: {e}")
    
    # Create an admin if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@gym.com', password='admin123', role='admin')
        db.session.add(admin)
        
    # Create default plans if not exists
    if not MembershipPlan.query.first():
        plans = [
            MembershipPlan(name='Monthly', price=1500, duration_days=30, features='Standard Gym Access, Locker Room'),
            MembershipPlan(name='Quarterly', price=4000, duration_days=90, features='Standard Gym Access, Locker Room, 2 Guest Passes'),
            MembershipPlan(name='Yearly', price=12000, duration_days=365, features='All Access, Personal Trainer Intro, Unlimited Guest Passes')
        ]
        db.session.add_all(plans)

    # Create default amenities if not exists
    if not Amenity.query.first():
        amenities = [
            Amenity(name='Elite Locker Access', price_per_day=10),
            Amenity(name='Steam & Sauna Protocol', price_per_day=25),
            Amenity(name='Personal Trainer Assistance', price_per_day=100),
            Amenity(name='Supplement Bar Credits', price_per_day=40),
            Amenity(name='VIP Shower Lounge', price_per_day=15)
        ]
        db.session.add_all(amenities)
    
    db.session.commit()
    print("Database initialized with updated schema, default plans and amenities!")

@app.route('/payments')
@login_required
@role_required(['admin', 'user'])
def view_payments():
    # Get selected date range from query params
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    today = get_ist_time().date()
    
    # Default values for template display
    display_start = start_date_str or today.strftime('%Y-%m-%d')
    display_end = end_date_str or today.strftime('%Y-%m-%d')

    if current_user.role == 'admin':
        gym_id = get_current_gym_id()
        query = apply_payment_gym_scope(Payment.query, gym_id)
        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                query = query.filter(db.func.date(Payment.payment_date) >= start_date, 
                                     db.func.date(Payment.payment_date) <= end_date)
            except ValueError:
                pass
        else:
            query = query.filter(db.func.date(Payment.payment_date) == today)
            
        payments = query.all()
    else:
        member = Member.query.filter_by(user_id=current_user.id).first()
        payments = Payment.query.filter_by(member_id=member.id).all() if member else []

    plans = MembershipPlan.query.all()
    return render_template('payments.html', 
                           payments=payments, 
                           start_date=display_start, 
                           end_date=display_end,
                           plans=plans)

@app.route('/update_membership', methods=['POST'])
@login_required
@role_required(['user'])
def update_membership():
    plan_id = request.form.get('plan_id')
    member = Member.query.filter_by(user_id=current_user.id).first()
    
    if not member:
        flash('MEMBER PROFILE NOT FOUND.', 'danger')
        return redirect(url_for('dashboard'))
    
    plan = MembershipPlan.query.get(plan_id)
    if not plan:
        flash('INVALID MEMBERSHIP PLAN SELECTED.', 'danger')
        return redirect(url_for('view_payments'))
    
    # Store as pending instead of updating immediately
    member.pending_plan_id = plan.id
    db.session.commit()
    
    # Notify Admin via Email
    try:
        admin_users = get_admins_for_gym(member.gym_id)
        admin_emails = [u.email for u in admin_users]
        
        details = f"""
            <div class="detail-item">
                <span class="detail-label">Athlete Name</span>
                <span class="detail-value">{member.full_name}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Current Tier</span>
                <span class="detail-value">{member.plan.name if member.plan else 'None'}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Requested Tier</span>
                <span class="detail-value">{plan.name}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Protocol Cost</span>
                <span class="detail-value">₹{plan.price:.2f}</span>
            </div>
        """
        
        admin_html = BLUE_EMAIL_TEMPLATE.format(
            title="MEMBERSHIP CHANGE REQUESTED",
            name="Admin",
            message=f"{member.full_name} has requested to switch their membership tier. Please authorize this in the command center.",
            details=details
        )
        
        for admin_email in admin_emails:
            send_email("MEMBERSHIP CHANGE REQUESTED - Nammude Gym", admin_html, admin_email)
    except Exception as e:
        print(f"Error notifying admins of plan change: {e}")
    
    flash(f'REQUEST SUBMITTED: THE {plan.name.upper()} PROTOCOL IS PENDING ADMIN AUTHORIZATION.', 'info')
    return redirect(url_for('view_payments'))

@app.route('/admin/approve_plan_change/<int:member_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def approve_plan_change(member_id):
    member = Member.query.get_or_404(member_id)
    if not member.pending_plan_id:
        flash('NO PENDING PLAN REQUEST FOUND.', 'warning')
        return redirect(url_for('dashboard'))
        
    new_plan = MembershipPlan.query.get(member.pending_plan_id)
    if not new_plan:
        member.pending_plan_id = None
        db.session.commit()
        flash('INVALID PENDING PLAN REFERENCE. REQUEST CLEARED.', 'danger')
        return redirect(url_for('dashboard'))

    # Update member tier and expiry
    member.plan_id = new_plan.id
    member.pending_plan_id = None
    member.status = 'Active'
    member.expiry_date = get_ist_time() + timedelta(days=new_plan.duration_days)
    
    # Record payment for revenue tracking
    new_payment = Payment(member_id=member.id, gym_id=member.gym_id, amount=new_plan.price, status='Paid')
    db.session.add(new_payment)
    db.session.commit()
    
    # Notify Member via Email
    try:
        member_user = db.session.get(User, member.user_id)
        if member_user and member_user.email:
            details = f"""
                <div class="detail-item">
                    <span class="detail-label">New Tier</span>
                    <span class="detail-value">{new_plan.name}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Protocol Cost</span>
                    <span class="detail-value">₹{new_plan.price:.2f}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Expiry Date</span>
                    <span class="detail-value">{member.expiry_date.strftime('%B %d, %Y')}</span>
                </div>
            """
            
            html_body = BLUE_EMAIL_TEMPLATE.format(
                title="MEMBERSHIP PROTOCOL AUTHORIZED",
                name=member.full_name,
                message=f"Your request to switch to the {new_plan.name.upper()} tier has been authorized. Your new expiry date and payment have been recorded.",
                details=details
            )
            send_email("Membership Protocol Authorized - Nammude Gym", html_body, member_user.email)
    except Exception as e:
        print(f"Error sending plan approval email: {e}")

    flash(f'PROTOCOL AUTHORIZED: {member.full_name} is now on the {new_plan.name.upper()} plan. Payment of ₹{new_plan.price} recorded.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/reject_plan_change/<int:member_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def reject_plan_change(member_id):
    member = Member.query.get_or_404(member_id)
    rejected_plan = MembershipPlan.query.get(member.pending_plan_id) if member.pending_plan_id else None
    member.pending_plan_id = None
    db.session.commit()
    
    # Notify Member via Email
    try:
        member_user = db.session.get(User, member.user_id)
        if member_user and member_user.email:
            details = f"""
                <div class="detail-item">
                    <span class="detail-label">Requested Tier</span>
                    <span class="detail-value">{rejected_plan.name if rejected_plan else 'Unknown'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Status</span>
                    <span class="detail-value">REJECTED</span>
                </div>
            """
            
            html_body = RED_EMAIL_TEMPLATE.format(
                title="MEMBERSHIP CHANGE REJECTED",
                name=member.full_name,
                message="Your request to switch your membership tier has been rejected by the board. Please contact administration for further details.",
                details=details
            )
            send_email("Membership Change Rejected - Nammude Gym", html_body, member_user.email)
    except Exception as e:
        print(f"Error sending plan rejection email: {e}")

    flash(f'PROTOCOL REJECTED: Plan change request for {member.full_name} has been dismissed.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/add_payment', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def add_payment():
    gym_id = get_current_gym_id()
    if request.method == 'POST':
        member_id = request.form.get('member_id', type=int)
        amount_raw = request.form.get('amount')
        amount = float(amount_raw) if amount_raw else 0
        member = Member.query.get_or_404(member_id)
        if gym_id and member.gym_id != gym_id:
            flash('Access denied for this gym member.', 'danger')
            return redirect(url_for('view_payments'))

        new_payment = Payment(member_id=member_id, gym_id=member.gym_id, amount=amount)
        db.session.add(new_payment)
        
        # Update member expiry date
        # Set validity from today based on plan duration (default to 30 if not set)
        duration = member.plan.duration_days if member.plan else 30
        member.expiry_date = get_ist_time() + timedelta(days=duration)
        member.status = 'Active'
            
        db.session.commit()
        flash(f'Payment recorded successfully! Membership valid for {duration} days.', 'success')
        return redirect(url_for('view_payments'))
    members = Member.query.filter_by(is_approved=True, gym_id=gym_id).all() if gym_id else Member.query.filter_by(is_approved=True).all()
    return render_template('add_payment.html', members=members)

@app.route('/workouts')
@login_required
@trainer_shift_required
def view_workouts():
    if current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        workouts = WorkoutPlan.query.filter_by(trainer_id=trainer.id).all() if trainer else []
    elif current_user.role == 'user':
        member = Member.query.filter_by(user_id=current_user.id).first()
        workouts = WorkoutPlan.query.filter_by(member_id=member.id).all() if member else []
    else:
        workouts = WorkoutPlan.query.all()
    return render_template('workouts.html', workouts=workouts)

@app.route('/assign_workout', methods=['GET', 'POST'])
@login_required
@role_required(['trainer', 'admin'])
@trainer_shift_required
def assign_workout():
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        plan_name = request.form.get('plan_name')
        exercises = request.form.get('exercises')
        day = request.form.get('day')
        
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        if trainer:
            trainer_id = trainer.id
        else:
            first_trainer = Trainer.query.first()
            if not first_trainer:
                flash('Error: No trainers exist in the system to assign this workout.', 'danger')
                return redirect(url_for('assign_workout'))
            trainer_id = first_trainer.id

        new_plan = WorkoutPlan(member_id=member_id, trainer_id=trainer_id, plan_name=plan_name, exercises=exercises, day=day)
        db.session.add(new_plan)
        db.session.commit()
        flash('Workout plan assigned!', 'success')
        return redirect(url_for('view_workouts'))
    members = Member.query.filter_by(is_approved=True).all()
    return render_template('assign_workout.html', members=members)

@app.route('/delete_workout/<int:workout_id>', methods=['POST'])
@login_required
@role_required(['trainer', 'admin'])
@trainer_shift_required
def delete_workout(workout_id):
    workout = WorkoutPlan.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('Workout protocol deleted successfully.', 'success')
    return redirect(url_for('view_workouts'))

@app.route('/edit_trainer_profile', methods=['GET', 'POST'])
@login_required
@role_required(['trainer'])
@trainer_shift_required
def edit_trainer_profile():
    trainer = Trainer.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age_raw = request.form.get('age')
        specialization = request.form.get('specialization')
        experience = request.form.get('experience')
        
        # Profile Picture Update
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{current_user.username}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.profile_pic = filename

        # Update User data
        current_user.email = email
        current_user.phone = phone
        if age_raw:
            current_user.age = int(age_raw)
        
        # Update Trainer data
        if trainer:
            trainer.full_name = full_name
            trainer.phone = phone
            trainer.specialization = specialization
            trainer.experience = int(experience) if experience and experience.strip() else 0
        
        db.session.commit()
        flash('Your coach profile has been successfully updated.', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('edit_trainer_profile.html', trainer=trainer)

@app.route('/edit_admin_profile', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def edit_admin_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age_raw = request.form.get('age')
        
        # Profile Picture Update
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"admin_{current_user.username}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.profile_pic = filename

        # Update User data
        current_user.username = username
        current_user.email = email
        current_user.phone = phone
        if age_raw:
            current_user.age = int(age_raw)
        
        db.session.commit()
        flash('Admin profile updated successfully.', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('edit_admin_profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
@role_required(['user'])
def edit_profile():
    member = Member.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob_raw = request.form.get('dob')
        age_raw = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')
        workout_days = request.form.getlist('workout_days')
        
        # Profile Picture Update
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{current_user.username}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.profile_pic = filename

        # Update User data
        current_user.email = email
        current_user.phone = phone
        if dob_raw:
            current_user.dob = datetime.strptime(dob_raw, '%Y-%m-%d').date()
        if age_raw:
            current_user.age = int(age_raw)
        
        # Update Member data
        if member:
            member.full_name = full_name
            member.phone = phone
            member.height = float(height) if height and height.strip() else None
            member.weight = float(weight) if weight and weight.strip() else None
            member.workout_days = ", ".join(workout_days)
        
        db.session.commit()
        flash('Your profile has been successfully updated.', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('edit_profile.html', member=member)

@app.route('/profile/<int:user_id>')
@login_required
@trainer_shift_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    
    # Check permissions: Admins/Trainers can see anyone, users can only see their own
    if current_user.role == 'user' and current_user.id != user_id:
        flash('Unauthorized access to private profile archive.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get associated profile data
    member = Member.query.filter_by(user_id=user_id).first()
    trainer = Trainer.query.filter_by(user_id=user_id).first()
    
    # Get associated workouts and payments
    workouts = []
    payments = []
    if member:
        workouts = WorkoutPlan.query.filter_by(member_id=member.id).all()
        payments = Payment.query.filter_by(member_id=member.id).all()
    elif trainer:
        workouts = WorkoutPlan.query.filter_by(trainer_id=trainer.id).all()

    return render_template('profile_view.html', user=user, member=member, trainer=trainer, workouts=workouts, payments=payments)

@app.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    user = db.session.get(User, member.user_id)
    
    try:
        # Clean up all related archives to satisfy database constraints
        WorkoutPlan.query.filter_by(member_id=member.id).delete()
        Payment.query.filter_by(member_id=member.id).delete()
        Attendance.query.filter_by(member_id=member.id).delete()
        Booking.query.filter_by(member_id=member.id).delete()
        WeightLog.query.filter_by(member_id=member.id).delete()
        CustomPlan.query.filter_by(member_id=member.id).delete()
        DietPlan.query.filter_by(member_id=member.id).delete()
        EquipmentUsage.query.filter_by(member_id=member.id).delete()
        
        db.session.delete(member)
        if user:
            db.session.delete(user)
        
        db.session.commit()
        
        # Reset auto-increment for clean records (optional, MySQL specific)
        try:
            db.session.execute(db.text("ALTER TABLE user AUTO_INCREMENT = 1"))
            db.session.execute(db.text("ALTER TABLE member AUTO_INCREMENT = 1"))
            db.session.execute(db.text("ALTER TABLE workout_plan AUTO_INCREMENT = 1"))
            db.session.execute(db.text("ALTER TABLE payment AUTO_INCREMENT = 1"))
            db.session.commit()
        except:
            db.session.rollback()
            
        flash('ATHLETE DELETED SUCCESSFULLY.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'ERROR DURING DELETION PROTOCOL: {str(e)}', 'danger')
        
    return redirect(url_for('member_list'))

@app.route('/delete_trainer/<int:trainer_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    user = db.session.get(User, trainer.user_id)
    
    try:
        # Clean up all related archives to satisfy database constraints
        WorkoutPlan.query.filter_by(trainer_id=trainer.id).delete()
        Attendance.query.filter_by(trainer_id=trainer.id).delete()
        Booking.query.filter_by(trainer_id=trainer.id).delete()
        DietPlan.query.filter_by(trainer_id=trainer.id).delete()
        
        db.session.delete(trainer)
        if user:
            db.session.delete(user)
            
        db.session.commit()
        
        # Reset auto-increment for clean records
        try:
            db.session.execute(db.text("ALTER TABLE user AUTO_INCREMENT = 1"))
            db.session.execute(db.text("ALTER TABLE trainer AUTO_INCREMENT = 1"))
            db.session.execute(db.text("ALTER TABLE workout_plan AUTO_INCREMENT = 1"))
            db.session.commit()
        except:
            db.session.rollback()
            
        flash('COACH DELETED SUCCESSFULLY.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'ERROR DURING DELETION PROTOCOL: {str(e)}', 'danger')
        
    return redirect(url_for('trainer_list'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('ERROR: USER NOT FOUND IN ARCHIVE.', 'danger')
        return redirect(url_for('deletion_requests'))

    try:
        delete_user_archive(user)
        flash(f'USER {user.username.upper()} AND ALL ASSOCIATED DATA REMOVED PERMANENTLY.', 'danger')
    except Exception as e:
        flash(f'CRITICAL DELETION ERROR: {str(e)}', 'danger')

    return redirect(url_for('deletion_requests'))

@app.route('/approve_member/<int:member_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def approve_member(member_id):
    member = Member.query.get_or_404(member_id)
    admin_gym_id = get_current_gym_id()
    if admin_gym_id and member.gym_id != admin_gym_id:
        flash('Access denied for this gym member.', 'danger')
        return redirect(url_for('member_list'))
    
    if member.is_approved:
        flash(f'Athlete {member.full_name} is already authorized.', 'info')
        return redirect(url_for('member_list'))

    member.is_approved = True
    member.date_approved = get_ist_time()
    
    # Automatically record payment if a plan was chosen
    amount_recorded = 0
    duration_days = 0
    
    # NEW PROTOCOL: Check if athlete has a pending custom plan. 
    # If yes, we skip the base plan payment to prevent double-charging.
    pending_custom = CustomPlan.query.filter_by(member_id=member.id, status='Pending').first()
    
    if member.plan_id and not pending_custom:
        plan = MembershipPlan.query.get(member.plan_id)
        if plan:
            new_payment = Payment(member_id=member.id, gym_id=member.gym_id, amount=plan.price, status='Paid')
            db.session.add(new_payment)
            amount_recorded = plan.price
            duration_days = plan.duration_days
            
            # Set validity from approval day based on plan duration
            member.expiry_date = member.date_approved + timedelta(days=plan.duration_days)
            member.status = 'Active'
    elif not pending_custom:
        member.expiry_date = member.date_approved
        member.status = 'Expired'
            
    db.session.commit()
    
    # Send Approval Success Email to Member
    member_user = db.session.get(User, member.user_id)
    if member_user and member_user.email:
        subject = "Nammude Gym: Athlete Profile Approved!"
        approval_message = (
            f"Your <strong>{duration_days}-day membership</strong> is now active and your training protocols are ready."
            if duration_days > 0 else
            "Your profile is approved with <strong>0-day validity</strong>. Please choose a membership plan from payments to activate gym access."
        )
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #007bff; }}
                h1 {{ color: #007bff; font-size: 28px; margin-bottom: 20px; }}
                p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                .cta {{ display: inline-block; background: #007bff; color: #ffffff; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-transform: uppercase; }}
                .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>PROFILE ACTIVATED</h1>
                <p>Hello {member.full_name},</p>
                <p>Great news! Your athlete registration at <strong>Nammude Gym</strong> has been <strong>APPROVED</strong> by the executive board.</p>
                <p>{approval_message}</p>
                <a href="#" class="cta">Start Your Journey</a>
                <div class="footer">
                    Best Regards,<br>
                    <strong>Team Nammude Gym</strong>
                </div>
            </div>
        </body>
        </html>
        """
        send_email(subject, html_body, member_user.email)
        
    if duration_days > 0:
        flash(f'Athlete {member.full_name} has been approved. The {duration_days}-day membership validity starts from today. Payment of ₹{amount_recorded} has been recorded.', 'success')
    else:
        flash(f'Athlete {member.full_name} has been approved with 0-day validity. No plan was selected during registration.', 'success')
    return redirect(url_for('member_list'))

@app.route('/members')
@login_required
@role_required(['admin', 'trainer'])
@trainer_shift_required
def member_list():
    gym_id = get_current_gym_id()
    athletes_query = Member.query.options(joinedload(Member.user))
    if gym_id:
        athletes_query = athletes_query.filter_by(gym_id=gym_id)
    athletes = athletes_query.all()
    return render_template('athletes_pool.html', athletes=athletes)

@app.route('/approve_trainer/<int:trainer_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def approve_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    admin_gym_id = get_current_gym_id()
    if admin_gym_id and trainer.gym_id != admin_gym_id:
        flash('Access denied for this gym trainer.', 'danger')
        return redirect(url_for('trainer_list'))
    trainer.is_approved = True
    db.session.commit()
    
    # Send Approval Success Email to Trainer
    trainer_user = db.session.get(User, trainer.user_id)
    if trainer_user and trainer_user.email:
        subject = "Nammude Gym: Coach Profile Activated!"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #007bff; }}
                h1 {{ color: #007bff; font-size: 28px; margin-bottom: 20px; }}
                p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                .cta {{ display: inline-block; background: #007bff; color: #ffffff; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-transform: uppercase; }}
                .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>COACH ACTIVATED</h1>
                <p>Hello {trainer.full_name},</p>
                <p>Your coaching registration at <strong>Nammude Gym</strong> has been <strong>APPROVED</strong> by the executive board.</p>
                <p>Your profile is now active and you can begin managing athlete sessions and workout protocols.</p>
                <p>Welcome to the team!</p>
                <a href="#" class="cta">Access Dashboard</a>
                <div class="footer">
                    Best Regards,<br>
                    <strong>Team Nammude Gym</strong>
                </div>
            </div>
        </body>
        </html>
        """
        send_email(subject, html_body, trainer_user.email)
        
    flash(f'Coach {trainer.full_name} has been approved and activated.', 'success')
    return redirect(url_for('trainer_list'))

@app.route('/reject_deletion/<int:user_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def reject_deletion(user_id):
    user = User.query.get_or_404(user_id)
    admin_gym_id = get_current_gym_id()
    if admin_gym_id and user.gym_id != admin_gym_id:
        flash('Access denied for this gym user.', 'danger')
        return redirect(url_for('dashboard'))
    user.deletion_requested = False
    db.session.commit()
    flash(f'Account removal request for {user.username} has been rejected.', 'info')
    if user.role == 'trainer':
        return redirect(url_for('trainer_list'))
    return redirect(url_for('member_list'))

@app.route('/admin/deletion_requests')
@login_required
@role_required(['admin'])
def deletion_requests():
    gym_id = get_current_gym_id()
    requests = User.query.filter_by(deletion_requested=True, gym_id=gym_id).all() if gym_id else User.query.filter_by(deletion_requested=True).all()
    return render_template('deletion_requests.html', requests=requests)

@app.route('/trainers')
@login_required
@role_required(['admin'])
def trainer_list():
    gym_id = get_current_gym_id()
    coaches_query = Trainer.query.options(joinedload(Trainer.user))
    if gym_id:
        coaches_query = coaches_query.filter_by(gym_id=gym_id)
    coaches = coaches_query.all()
    return render_template('elite_coaches.html', coaches=coaches)

@app.route('/admin/plans')
@login_required
@role_required(['admin'])
def manage_plans():
    plans = MembershipPlan.query.all()
    return render_template('admin_plans.html', plans=plans)

@app.route('/admin/plans/edit/<int:plan_id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def edit_plan(plan_id):
    plan = MembershipPlan.query.get_or_404(plan_id)
    if request.method == 'POST':
        plan.name = request.form.get('name')
        plan.price = request.form.get('price')
        plan.duration_days = int(request.form.get('duration_days', 30))
        plan.features = request.form.get('features')
        db.session.commit()
        flash('Membership plan updated successfully.', 'success')
        return redirect(url_for('manage_plans'))
    return render_template('edit_plan.html', plan=plan)

@app.route('/trainer/send_email', methods=['GET', 'POST'])
@login_required
@role_required(['trainer', 'admin'])
@trainer_shift_required
def trainer_send_email():
    if request.method == 'POST':
        recipient_email = request.form.get('recipient_email')
        subject = request.form.get('subject')
        message_content = request.form.get('message')
        
        # Determine recipient name for the email template
        recipient_user = User.query.filter_by(email=recipient_email).first()
        recipient_name = recipient_user.username if recipient_user else "Athlete"
        
        # Use BLUE_EMAIL_TEMPLATE for a professional look
        html_body = BLUE_EMAIL_TEMPLATE.format(
            title="COACH COMMUNICATION",
            name=recipient_name,
            message=f"You have received a direct message from Coach {current_user.username.upper()}:",
            details=f"<div style='color: #ffffff; font-size: 16px; line-height: 1.6;'>{message_content}</div>"
        )
        
        if send_email(f"Message from Nammude Gym: {subject}", html_body, recipient_email):
            flash(f'PROTOCOL SUCCESS: COMMUNICATION DISPATCHED TO {recipient_email.upper()}.', 'success')
        else:
            flash('ERROR: COMMUNICATION PROTOCOL FAILED. CHECK SMTP UPLINK.', 'danger')
            
        return redirect(url_for('dashboard'))
    
    # Pre-populate recipient if coming from a profile or directory link
    target_email = request.args.get('email', '')
    gym_id = get_current_gym_id()
    members = Member.query.filter_by(gym_id=gym_id).all() if gym_id else Member.query.all()
    admins = get_admins_for_gym(gym_id) if gym_id else User.query.filter_by(role='admin').all()
    
    return render_template('trainer_send_email.html', target_email=target_email, members=members, admins=admins)

@app.route('/settings')
@login_required
@trainer_shift_required
def settings():
    return render_template('settings.html')

@app.route('/download_invoice/<int:payment_id>')
@login_required
@role_required(['admin', 'user'])
def download_invoice(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    # Check permission
    if current_user.role == 'user':
        member = Member.query.filter_by(user_id=current_user.id).first()
        if not member or payment.member_id != member.id:
            flash('Unauthorized access to invoice.', 'danger')
            return redirect(url_for('view_payments'))
    else:
        gym_id = get_current_gym_id()
        payment_member = Member.query.get(payment.member_id)
        if gym_id and payment_member and payment_member.gym_id != gym_id:
            flash('Unauthorized access to invoice.', 'danger')
            return redirect(url_for('view_payments'))
            
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height - 1*inch, "NAMMUDE GYM")
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height - 1.3*inch, "Official Payment Invoice")
    
    # Invoice Box
    p.rect(0.5*inch, height - 4.5*inch, 7.5*inch, 3*inch)
    
    # Details
    p.setFont(f"{USE_FONT}-Bold" if USE_FONT != 'Arial' else USE_FONT, 14)
    p.drawString(1*inch, height - 2*inch, f"Invoice ID: #INV-{payment.id:04d}")
    p.setFont(USE_FONT, 12)
    p.drawString(1*inch, height - 2.3*inch, f"Date: {payment.payment_date.strftime('%B %d, %Y')}")
    
    p.line(1*inch, height - 2.5*inch, 7*inch, height - 2.5*inch)
    
    p.drawString(1*inch, height - 3*inch, f"Athlete Name: {payment.member.full_name.upper()}")
    p.drawString(1*inch, height - 3.3*inch, f"Membership Tier: {payment.member.plan.name.upper() if payment.member.plan else 'STANDARD'}")
    p.drawString(1*inch, height - 3.6*inch, f"Contact: {payment.member.phone or 'N/A'}")
    
    p.setFont(f"{USE_FONT}-Bold" if USE_FONT != 'Arial' else USE_FONT, 14)
    p.drawString(1*inch, height - 4.1*inch, f"Total Amount Paid: ₹ {payment.amount:.2f}")
    p.setFont(USE_FONT, 10)
    p.drawString(1*inch, height - 4.3*inch, f"Status: {payment.status.upper()}")
    
    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width/2, 1*inch, "Thank you for being part of NAMMUDE GYM. This is a computer-generated document.")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Invoice_NAMMUDE_{payment.id}.pdf", mimetype='application/pdf')

@app.route('/admin/export_revenue')
@login_required
@role_required(['admin'])
def export_revenue():
    # Supports both range (from reports hub) and single date (from ledger)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    single_date_str = request.args.get('date')
    
    gym_id = get_current_gym_id()
    query = apply_payment_gym_scope(Payment.query, gym_id)
    range_label = "ALL TIME"
    
    if single_date_str:
        try:
            selected_date = datetime.strptime(single_date_str, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Payment.payment_date) == selected_date)
            range_label = single_date_str
        except ValueError:
            pass
    elif start_date_str and end_date_str:
        try:
            start_dt = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Payment.payment_date >= start_dt, Payment.payment_date < end_dt)
            range_label = f"{start_date_str} TO {end_date_str}"
        except ValueError:
            pass

    payments = query.all()
    total_revenue = sum(p.amount for p in payments)
    
    # Log the export
    try:
        start_date_log = None
        end_date_log = None
        
        # Use the strings that WERE actually used for filtering
        if single_date_str:
            try:
                start_date_log = datetime.strptime(single_date_str, '%Y-%m-%d').date()
                end_date_log = start_date_log
            except: pass
        elif start_date_str and end_date_str:
            try:
                start_date_log = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date_log = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except: pass
            
        # Fallback to TODAY if no dates provided (matches Ledger default)
        if not start_date_log:
            start_date_log = get_ist_time().date()
            end_date_log = start_date_log

        log = ExportLog(
            report_type='Revenue',
            start_date=start_date_log,
            end_date=end_date_log,
            total_amount=total_revenue,
            performed_by=current_user.username if current_user.is_authenticated else 'System'
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Logging System Failure: {e}")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width/2, height - 1*inch, "NAMMUDE GYM - REVENUE REPORT")
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, height - 1.2*inch, f"PERIOD: {range_label}")
    p.drawCentredString(width/2, height - 1.4*inch, f"Generated on: {get_ist_time().strftime('%Y-%m-%d %I:%M %p')}")

    # Summary
    p.setFont(f"{USE_FONT}-Bold" if USE_FONT != 'Arial' else USE_FONT, 12)
    p.drawString(0.5*inch, height - 1.8*inch, f"Total Transactions: {len(payments)}")
    p.drawString(0.5*inch, height - 2.0*inch, f"Gross Revenue: ₹ {total_revenue:.2f}")
    
    # Table Header
    p.line(0.5*inch, height - 2.2*inch, 7.5*inch, height - 2.2*inch)
    p.setFont(f"{USE_FONT}-Bold" if USE_FONT != 'Arial' else USE_FONT, 10)
    p.drawString(0.5*inch, height - 2.4*inch, "ID")
    p.drawString(1.2*inch, height - 2.4*inch, "ATHLETE")
    p.drawString(3.5*inch, height - 2.4*inch, "DATE")
    p.drawString(5.5*inch, height - 2.4*inch, "AMOUNT")
    p.line(0.5*inch, height - 2.5*inch, 7.5*inch, height - 2.5*inch)
    
    # Rows
    y = height - 2.7*inch
    p.setFont(USE_FONT, 9)
    for pay in payments:
        if y < 1*inch:
            p.showPage()
            y = height - 1*inch
            p.setFont(f"{USE_FONT}-Bold" if USE_FONT != 'Arial' else USE_FONT, 10)
            p.drawString(0.5*inch, y, "ID")
            p.drawString(1.2*inch, y, "ATHLETE")
            p.drawString(3.5*inch, y, "DATE")
            p.drawString(5.5*inch, y, "AMOUNT")
            y -= 0.3*inch
            p.setFont(USE_FONT, 9)
            
        p.drawString(0.5*inch, y, f"#{pay.id:04d}")
        p.drawString(1.2*inch, y, pay.member.full_name[:30].upper())
        p.drawString(3.5*inch, y, pay.payment_date.strftime('%Y-%m-%d'))
        p.drawString(5.5*inch, y, f"₹ {pay.amount:.2f}")
        y -= 0.2*inch
        
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Revenue_Report_{get_ist_time().strftime('%Y%m%d')}.pdf", mimetype='application/pdf')

@app.route('/admin/export_history')
@login_required
@role_required(['admin'])
def export_history():
    logs = ExportLog.query.filter_by(performed_by=current_user.username).order_by(ExportLog.performed_at.desc()).all()
    return render_template('export_history.html', logs=logs)

@app.route('/admin/delete_export_log/<int:log_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_export_log(log_id):
    log = ExportLog.query.get_or_404(log_id)
    if log.performed_by != current_user.username:
        flash('Access denied for this export record.', 'danger')
        return redirect(url_for('export_history'))
    db.session.delete(log)
    db.session.commit()
    flash('Export record deleted.', 'danger')
    return redirect(url_for('export_history'))

@app.route('/attendance')
@login_required
@trainer_shift_required
def attendance():
    # Get selected date from query params, default to today IST
    selected_date_str = request.args.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = get_ist_time().date()
    else:
        selected_date = get_ist_time().date()

    if current_user.role == 'user':
        member = Member.query.filter_by(user_id=current_user.id).first()
        records = Attendance.query.options(joinedload(Attendance.member), joinedload(Attendance.trainer)).filter_by(member_id=member.id, date=selected_date).order_by(Attendance.check_in.desc()).all() if member else []
        active_session = Attendance.query.filter_by(member_id=member.id, check_out=None).first() if member else None
    elif current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        # Trainers see member logs for today + their own shifts
        records = Attendance.query.options(joinedload(Attendance.member), joinedload(Attendance.trainer)).join(Member, Attendance.member_id == Member.id).filter(
            Attendance.date == selected_date,
            Member.gym_id == trainer.gym_id
        ).order_by(Attendance.check_in.desc()).all() if trainer and trainer.gym_id else Attendance.query.options(joinedload(Attendance.member), joinedload(Attendance.trainer)).filter_by(date=selected_date).order_by(Attendance.check_in.desc()).all()
        active_session = Attendance.query.filter_by(trainer_id=trainer.id, check_out=None).first() if trainer else None
    else:
        gym_id = get_current_gym_id()
        records_query = Attendance.query.options(joinedload(Attendance.member), joinedload(Attendance.trainer)).filter_by(date=selected_date)
        if gym_id:
            records_query = records_query.join(Member, Attendance.member_id == Member.id).filter(Member.gym_id == gym_id)
        records = records_query.order_by(Attendance.check_in.desc()).all()
        active_session = None

    if current_user.role in ['admin', 'trainer']:
        gym_id = get_current_gym_id() if current_user.role == 'admin' else (trainer.gym_id if trainer else None)
        members = Member.query.filter_by(is_approved=True, gym_id=gym_id).all() if gym_id else Member.query.filter_by(is_approved=True).all()
    else:
        members = []
    return render_template('attendance.html', 
                           records=records, 
                           members=members, 
                           active_session=active_session, 
                           selected_date=selected_date.strftime('%Y-%m-%d'))

@app.route('/mark_check_in', methods=['POST'])
@login_required
@role_required(['admin', 'trainer'])
def mark_check_in():
    member_id = request.form.get('member_id')
    today = get_ist_time().date()
    
    # Check if a trainer is checking themselves in (Starting Shift)
    if not member_id and current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        if trainer:
            # AUTO-CLEANUP: Check for ANY unclosed shifts from previous sessions
            stuck_shifts = Attendance.query.filter_by(trainer_id=trainer.id, check_out=None).all()
            for shift in stuck_shifts:
                if shift.date < today:
                    shift.check_out = datetime.combine(shift.date, datetime.max.time())
                else:
                    flash('You already have an active shift for today.', 'warning')
                    return redirect(url_for('dashboard'))
            
            db.session.commit()
            
            new_attendance = Attendance(trainer_id=trainer.id)
            db.session.add(new_attendance)
            db.session.commit()
            flash('Your coaching shift has officially commenced. Access to athlete data is now authorized.', 'success')
            return redirect(url_for('dashboard'))

    # Shift check for Trainers managing members
    if current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        active_shift = Attendance.query.filter_by(trainer_id=trainer.id, date=today, check_out=None).first()
        
        if member_id and not active_shift:
            flash('SHIFT PROTOCOL: YOU MUST COMMENCE YOUR SHIFT BEFORE MANAGING ATHLETE ATTENDANCE.', 'danger')
            return redirect(url_for('dashboard'))

    # Rest of mark_check_in logic for members...
    if member_id:
        member = Member.query.get(member_id)
        now_dt = get_ist_time()
        current_time = now_dt.time()
        
        buffer_time = (now_dt + timedelta(minutes=15)).time()
        
        valid_booking = Booking.query.filter(
            Booking.member_id == member_id,
            Booking.booking_date == today,
            Booking.status == 'Confirmed',
            Booking.booking_time_from <= buffer_time,
            Booking.booking_time_to >= current_time
        ).first()
        
        if not valid_booking:
            if current_user.role != 'admin':
                flash(f' ERROR: NO ACTIVE BOOKING DETECTED FOR {member.full_name.upper()} AT THIS TIME.', 'danger')
                return redirect(url_for('attendance'))

    already_in = Attendance.query.filter_by(member_id=member_id, check_out=None).first()
    if already_in:
        flash('Athlete is already checked in.', 'warning')
        return redirect(url_for('attendance'))
        
    new_attendance = Attendance(member_id=member_id)
    db.session.add(new_attendance)
    db.session.commit()
    flash('Check-in recorded successfully for scheduled session!', 'success')
    return redirect(url_for('attendance'))

@app.route('/mark_check_out/<int:attendance_id>', methods=['POST'])
@login_required
@role_required(['admin', 'trainer'])
def mark_check_out(attendance_id):
    record = Attendance.query.get_or_404(attendance_id)
    
    # Authorization & Shift check for Trainers
    if current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        active_shift = Attendance.query.filter_by(trainer_id=trainer.id, date=get_ist_time().date(), check_out=None).first()
        
        # Trainers can check out themselves ANYTIME
        if record.trainer_id and record.trainer_id == trainer.id:
            pass 
        # But checking out members requires an active shift
        elif not active_shift:
            flash(' ERROR: YOU MUST HAVE AN ACTIVE SHIFT TO MANAGE ATHLETE LOGS.', 'danger')
            return redirect(url_for('attendance'))
        
        if record.trainer_id and record.trainer_id != trainer.id:
            flash('You cannot check-out another coach.', 'danger')
            return redirect(url_for('attendance'))

    if not record.check_out:
        record.check_out = get_ist_time()
        db.session.commit()
        
        # Send Daily Attendance Report to Member via Email
        if record.member:
            member_user = User.query.get(record.member.user_id)
            if member_user and member_user.email:
                duration = "--"
                diff = record.check_out - record.check_in
                h, rem = divmod(diff.total_seconds(), 3600)
                m, s = divmod(rem, 60)
                duration = f"{int(h)}h {int(m)}m {int(s)}s"
                
                subject = f"Nammude Gym: Daily Attendance Report - {record.date}"
                html_body = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                        .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #007bff; }}
                        h1 {{ color: #007bff; font-size: 28px; margin-bottom: 20px; }}
                        .stats {{ background: #333; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                        .stat-item {{ margin-bottom: 10px; font-size: 16px; }}
                        .label {{ color: #007bff; font-weight: bold; }}
                        .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>WORKOUT COMPLETE</h1>
                        <p>Hello {record.member.full_name},</p>
                        <p>Here is your attendance summary for today's session:</p>
                        <div class="stats">
                            <div class="stat-item"><span class="label">DATE:</span> {record.date}</div>
                            <div class="stat-item"><span class="label">CHECK-IN:</span> {record.check_in.strftime('%I:%M:%S %p')}</div>
                            <div class="stat-item"><span class="label">CHECK-OUT:</span> {record.check_out.strftime('%I:%M:%S %p')}</div>
                            <div class="stat-item"><span class="label">DURATION:</span> {duration}</div>
                        </div>
                        <p>Keep pushing your limits! Consistency is the key to transformation.</p>
                        <div class="footer">
                            Best Regards,<br>
                            <strong>Team Nammude Gym</strong>
                        </div>
                    </div>
                </body>
                </html>
                """
                send_email(subject, html_body, member_user.email)
        
        flash('Shift/Session recorded successfully! Report sent to email.', 'success')
    return redirect(url_for('attendance'))

@app.route('/admin/expiry_alerts')
@login_required
@role_required(['admin'])
def expiry_alerts():
    today = get_ist_time().date()
    # Find members expiring within 7 days or already expired
    # We include 'Active' and 'Expired' status
    upcoming_expiry = Member.query.filter(
        Member.expiry_date.isnot(None),
        Member.is_approved == True
    ).all()
    
    alert_list = []
    for member in upcoming_expiry:
        expiry_date = member.expiry_date.date()
        days_left = (expiry_date - today).days
        
        # Include if expired or expiring in next 7 days
        if days_left <= 7:
            alert_list.append({
                'member': member,
                'days_left': days_left,
                'status_label': 'EXPIRED' if days_left < 0 else 'EXPIRES TODAY' if days_left == 0 else f'EXPIRES IN {days_left} DAYS'
            })
            
    # Sort by days_left (most urgent first)
    alert_list.sort(key=lambda x: x['days_left'])
    
    return render_template('admin_expiry_alerts.html', alert_list=alert_list)

@app.route('/admin/send_expiry_alert/<int:member_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def send_expiry_alert(member_id):
    member = Member.query.get_or_404(member_id)
    today = get_ist_time().date()
    expiry_date = member.expiry_date.date()
    days_left = (expiry_date - today).days
    
    member_user = db.session.get(User, member.user_id)
    if not member_user or not member_user.email:
        flash(f'ERROR: NO EMAIL ARCHIVE FOUND FOR {member.full_name.upper()}.', 'danger')
        return redirect(url_for('expiry_alerts'))

    subject = "Nammude Gym: Membership Status Alert"
    if days_left < 0:
        msg = f"Your membership EXPIRED on {expiry_date.strftime('%B %d, %Y')}."
        title = "MEMBERSHIP EXPIRED"
    elif days_left == 0:
        msg = "Your membership expires TODAY."
        title = "EXPIRY ALERT: TODAY"
    else:
        msg = f"Your membership will expire in {days_left} days ({expiry_date.strftime('%B %d, %Y')})."
        title = f"EXPIRY ALERT: {days_left} DAYS"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
            .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: #ff4d4d 4px solid; }}
            h1 {{ color: #ff4d4d; font-size: 28px; margin-bottom: 20px; }}
            p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
            .cta {{ display: inline-block; background: #007bff; color: #ffffff; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-transform: uppercase; }}
            .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <p>Hello {member.full_name},</p>
            <p>This is a status update from <strong>Nammude Gym</strong> regarding your membership protocol.</p>
            <p style="font-size: 18px; color: #ff4d4d; font-weight: bold;">{msg}</p>
            <p>Please renew your membership to maintain uninterrupted access to elite training sessions and facility amenities.</p>
            <a href="#" class="cta">RENEW PROTOCOL</a>
            <div class="footer">
                Best Regards,<br>
                <strong>Team Nammude Gym</strong>
            </div>
        </div>
    </body>
    </html>
    """
    
    if send_email(subject, html_body, member_user.email):
        flash(f'PROTOCOL SUCCESS: Expiry alert dispatched to {member.full_name.upper()}.', 'success')
    else:
        flash(f'ERROR: COMMUNICATION FAILURE WITH {member_user.email}.', 'danger')
        
    return redirect(url_for('expiry_alerts'))

@app.route('/admin/send_all_expiry_alerts', methods=['POST'])
@login_required
@role_required(['admin'])
def send_all_expiry_alerts():
    today = get_ist_time().date()
    members = Member.query.filter(Member.expiry_date.isnot(None), Member.is_approved == True).all()
    
    count = 0
    for member in members:
        expiry_date = member.expiry_date.date()
        days_left = (expiry_date - today).days
        
        if days_left <= 7:
            member_user = db.session.get(User, member.user_id)
            if member_user and member_user.email:
                # Reusing the email logic for mass send
                if days_left < 0:
                    msg = f"Your membership EXPIRED on {expiry_date.strftime('%B %d, %Y')}."
                    title = "MEMBERSHIP EXPIRED"
                elif days_left == 0:
                    msg = "Your membership expires TODAY."
                    title = "EXPIRY ALERT: TODAY"
                else:
                    msg = f"Your membership will expire in {days_left} days ({expiry_date.strftime('%B %d, %Y')})."
                    title = f"EXPIRY ALERT: {days_left} DAYS"

                html_body = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                        .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: #ff4d4d 4px solid; }}
                        h1 {{ color: #ff4d4d; font-size: 28px; margin-bottom: 20px; }}
                        p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                        .cta {{ display: inline-block; background: #007bff; color: #ffffff; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-transform: uppercase; }}
                        .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>{title}</h1>
                        <p>Hello {member.full_name},</p>
                        <p>This is a status update from <strong>Nammude Gym</strong> regarding your membership protocol.</p>
                        <p style="font-size: 18px; color: #ff4d4d; font-weight: bold;">{msg}</p>
                        <p>Please renew your membership to maintain uninterrupted access to elite training sessions and facility amenities.</p>
                        <a href="#" class="cta">RENEW PROTOCOL</a>
                        <div class="footer">
                            Best Regards,<br>
                            <strong>Team Nammude Gym</strong>
                        </div>
                    </div>
                </body>
                </html>
                """
                if send_email("Nammude Gym: Membership Status Alert", html_body, member_user.email):
                    count += 1
                    
    flash(f'NOTIFICATION PROTOCOL: {count} expiry alerts dispatched to athlete emails.', 'success')
    return redirect(url_for('expiry_alerts'))

@app.route('/download_attendance')
@login_required
@trainer_shift_required
def download_attendance():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    query = Attendance.query
    range_label = "ALL TIME"
    
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Attendance.date >= start_date, Attendance.date <= end_date)
            range_label = f"{start_date_str} TO {end_date_str}"
        except ValueError:
            pass

    if current_user.role == 'user':
        member = Member.query.filter_by(user_id=current_user.id).first()
        records = query.filter_by(member_id=member.id).all() if member else []
        title = f"Attendance Report: {member.full_name.upper() if member else 'N/A'}"
    else:
        records = query.all()
        title = "NAMMUDE GYM - MASTER ATTENDANCE LOG"
        
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.setFont(f"{USE_FONT}-Bold" if USE_FONT != 'Arial' else USE_FONT, 20)
    p.drawCentredString(width/2, height - 0.8*inch, title)
    p.setFont(USE_FONT, 10)
    p.drawCentredString(width/2, height - 1.1*inch, f"PERIOD: {range_label}")
    p.drawCentredString(width/2, height - 1.3*inch, f"Generated on: {get_ist_time().strftime('%Y-%m-%d %I:%M:%S %p')}")
    p.line(0.5*inch, height - 1.8*inch, 7.5*inch, height - 1.8*inch)
    p.setFont(f"{USE_FONT}-Bold" if USE_FONT != 'Arial' else USE_FONT, 10)
    p.drawString(0.5*inch, height - 2*inch, "DATE")
    p.drawString(1.5*inch, height - 2*inch, "ATHLETE")
    p.drawString(4*inch, height - 2*inch, "CHECK IN")
    p.drawString(5.5*inch, height - 2*inch, "CHECK OUT")
    p.drawString(7*inch, height - 2*inch, "DUR.")
    p.line(0.5*inch, height - 2.1*inch, 7.5*inch, height - 2.1*inch)
    y = height - 2.3*inch
    p.setFont(USE_FONT, 9)
    for rec in records:
        if y < 1*inch:
            p.showPage()
            y = height - 1*inch
            p.setFont(USE_FONT, 9)
        duration = "--"
        if rec.check_out:
            diff = rec.check_out - rec.check_in
            h, rem = divmod(diff.total_seconds(), 3600)
            m, s = divmod(rem, 60)
            duration = f"{int(h)}h {int(m)}m {int(s)}s"
        p.drawString(0.5*inch, y, rec.date.strftime('%Y-%m-%d'))
        name = "Unknown"
        if rec.member:
            name = rec.member.full_name
        elif rec.trainer:
            name = f"{rec.trainer.full_name} (Coach)"
        p.drawString(1.5*inch, y, name[:30].upper())
        p.drawString(4*inch, y, rec.check_in.strftime('%I:%M:%S %p'))
        p.drawString(5.5*inch, y, rec.check_out.strftime('%I:%M:%S %p') if rec.check_out else "Active")
        p.drawString(7*inch, y, duration)
        y -= 0.2*inch
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Attendance_Report.pdf", mimetype='application/pdf')

@app.route('/update_db')
def update_db_schema():
    try:
        # Check if status column exists
        from sqlalchemy import text
        db.session.execute(text("ALTER TABLE equipment ADD COLUMN status VARCHAR(20) DEFAULT 'Working'"))
        db.session.commit()
        return "Database updated successfully!"
    except Exception as e:
        db.session.rollback()
        return f"Error updating database: {e}"

@app.route('/equipment')
@login_required
@trainer_shift_required
def view_equipment():
    all_gear = get_equipment_query_for_current_gym().all()
    now = get_ist_time()
    
    # Enrich gear objects with real-time availability
    for gear in all_gear:
        working_quantity = max(0, gear.quantity - gear.broken_quantity)
        
        # Fetch all overlapping confirmed/pending bookings for this gear today
        today_bookings = Booking.query.filter(
            Booking.equipment_id == gear.id,
            Booking.status.in_(['Confirmed', 'Pending']),
            Booking.booking_date == now.date()
        ).all()
        
        occupied_count = 0
        current_time = now.time()
        
        for b in today_bookings:
            # Handle normal slots (e.g. 10 AM to 1 PM) and overnight slots (e.g. 10 PM to 1 AM)
            if b.booking_time_from < b.booking_time_to:
                if b.booking_time_from <= current_time <= b.booking_time_to:
                    occupied_count += 1
            else:
                # Slot spans across midnight (e.g. 10 PM to 1 AM)
                if current_time >= b.booking_time_from or current_time <= b.booking_time_to:
                    occupied_count += 1
        
        gear.available_now = max(0, working_quantity - occupied_count)
        gear.working_quantity = working_quantity
        
    return render_template('equipment.html', gear=all_gear)

@app.route('/add_equipment', methods=['POST'])
@login_required
@role_required(['admin', 'trainer'])
@trainer_shift_required
def add_equipment():
    gym_id = get_current_gym_id()
    if not gym_id:
        flash('Gym ID is required to manage equipment.', 'danger')
        return redirect(url_for('view_equipment'))

    name = request.form.get('name')
    description = request.form.get('description')
    quantity = int(request.form.get('quantity', 1))
    broken_quantity = int(request.form.get('broken_quantity', 0))
    
    img_filename = 'equipment_default.png'
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"equip_{get_ist_time().timestamp()}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_filename = filename

    new_equip = Equipment(gym_id=gym_id, name=name, description=description, quantity=quantity, broken_quantity=broken_quantity, image_file=img_filename)
    db.session.add(new_equip)
    db.session.commit()
    flash(f'Equipment {name} added to the inventory with total quantity {quantity}.', 'success')
    return redirect(url_for('view_equipment'))

@app.route('/edit_equipment/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def edit_equipment(equipment_id):
    equip = Equipment.query.get_or_404(equipment_id)
    gym_id = get_current_gym_id()
    if gym_id and equip.gym_id != gym_id:
        flash('Access denied for this gym equipment.', 'danger')
        return redirect(url_for('view_equipment'))

    if request.method == 'POST':
        equip.gym_id = gym_id or equip.gym_id
        equip.name = request.form.get('name')
        equip.description = request.form.get('description')
        equip.quantity = int(request.form.get('quantity', 1))
        equip.broken_quantity = int(request.form.get('broken_quantity', 0))
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"equip_{get_ist_time().timestamp()}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                equip.image_file = filename
                
        db.session.commit()
        flash(f'Inventory protocol for {equip.name} has been updated.', 'success')
        return redirect(url_for('view_equipment'))
    return render_template('edit_equipment.html', gear=equip)

@app.route('/delete_equipment/<int:equipment_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_equipment(equipment_id):
    equip = Equipment.query.get_or_404(equipment_id)
    gym_id = get_current_gym_id()
    if gym_id and equip.gym_id != gym_id:
        flash('Access denied for this gym equipment.', 'danger')
        return redirect(url_for('view_equipment'))

    db.session.delete(equip)
    db.session.commit()
    flash('Equipment removed from inventory.', 'success')
    return redirect(url_for('view_equipment'))

@app.route('/reports')
@login_required
@role_required(['admin', 'trainer'])
@trainer_shift_required
def reports_hub():
    # Date filtering for reports
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    today = get_ist_time().date()
    
    display_start = start_date_str or today.strftime('%Y-%m-%d')
    display_end = end_date_str or today.strftime('%Y-%m-%d')
    
    # Calculate filtered revenue
    gym_id = get_current_gym_id()
    query = apply_payment_gym_scope(Payment.query, gym_id)
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            # Include the entire end day by checking date only
            query = query.filter(db.func.date(Payment.payment_date) >= start_date, 
                                 db.func.date(Payment.payment_date) <= end_date)
        except ValueError:
            query = query.filter(db.func.date(Payment.payment_date) == today)
    else:
        query = query.filter(db.func.date(Payment.payment_date) == today)
    
    filtered_payments = query.all()
    period_revenue = sum(p.amount for p in filtered_payments)
    
    # Quick overall stats
    total_members = Member.query.filter_by(gym_id=gym_id).count() if gym_id else Member.query.count()
    today_sessions = Attendance.query.join(Member, Attendance.member_id == Member.id).filter(
        Attendance.date == today,
        Member.gym_id == gym_id
    ).count() if gym_id else Attendance.query.filter_by(date=today).count()
    
    # Fetch latest export logs for admin
    export_logs = ExportLog.query.filter_by(performed_by=current_user.username).order_by(ExportLog.performed_at.desc()).limit(10).all() if current_user.role == 'admin' else []

    all_members = Member.query.filter_by(is_approved=True, gym_id=gym_id).order_by(Member.full_name).all() if gym_id else Member.query.filter_by(is_approved=True).order_by(Member.full_name).all()

    return render_template('reports_hub.html',
                           total_members=total_members,
                           total_revenue=period_revenue,
                           today_sessions=today_sessions,
                           export_logs=export_logs,
                           start_date=display_start,
                           end_date=display_end,
                           num_transactions=len(filtered_payments),
                           payments=filtered_payments,
                           all_members=all_members)
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    if current_user.role == 'admin':
        otp = ''.join(random.choices(string.digits, k=6))
        current_user.otp = otp
        current_user.otp_expiry = get_ist_time() + timedelta(minutes=5)
        db.session.commit()
        session['pending_delete_user_id'] = current_user.id

        try:
            subject = "Nammude Gym: Admin Account Deletion OTP"
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                    .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #FF5E5E; }}
                    h1 {{ color: #FF5E5E; font-size: 28px; margin-bottom: 20px; }}
                    p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                    .otp {{ font-size: 36px; font-weight: bold; letter-spacing: 4px; color: #ffffff; background: #333; padding: 15px; display: inline-block; margin: 20px 0; border: 1px dashed #FF5E5E; }}
                    .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>ADMIN DELETE VERIFICATION</h1>
                    <p>Hello {current_user.username},</p>
                    <p>Your OTP for permanent admin account deletion is:</p>
                    <div class="otp">{otp}</div>
                    <p>This code is valid for <strong>5 minutes</strong>. Enter it to permanently remove your admin account.</p>
                    <div class="footer">
                        Best Regards,<br>
                        <strong>Team Nammude Gym</strong>
                    </div>
                </div>
            </body>
            </html>
            """
            send_email(subject, html_body, current_user.email)
        except Exception as e:
            print(f"Error sending admin deletion OTP: {e}")

        flash('ADMIN ACCOUNT DELETE OTP SENT TO YOUR EMAIL.', 'warning')
        return redirect(url_for('verify_delete_account_otp'))

    current_user.deletion_requested = True
    db.session.commit()

    # Notify Admins of Deletion Request
    try:
        admin_users = get_admins_for_gym(get_current_gym_id())
        admin_emails = [u.email for u in admin_users]
        
        admin_details = f"""
            <div class="detail-item">
                <span class="detail-label">Username</span>
                <span class="detail-value">{current_user.username}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Role</span>
                <span class="detail-value">{'ATHLETE' if current_user.role == 'user' else 'COACH' if current_user.role == 'trainer' else current_user.role.upper()}</span>
            </div>
        """
        
        admin_html = RED_EMAIL_TEMPLATE.format(
            title="DELETION REQUEST SUBMITTED",
            name="Admin",
            message="A user has requested to permanently remove their account. Please authorize or reject this in the Deletion Requests center.",
            details=admin_details
        )
        
        for admin_email in admin_emails:
            send_email("DELETION REQUEST SUBMITTED - Nammude Gym", admin_html, admin_email)
    except Exception as e:
        print(f"Error notifying admins of deletion request: {e}")

    flash('ACCOUNT DELETION REQUESTED. WAITING FOR ADMIN APPROVAL.', 'danger')
    logout_user()
    return redirect(url_for('register'))

@app.route('/verify_delete_account_otp', methods=['GET', 'POST'])
@login_required
def verify_delete_account_otp():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('settings'))

    pending_delete_user_id = session.get('pending_delete_user_id')
    if pending_delete_user_id != current_user.id:
        flash('Delete session expired. Please try again.', 'danger')
        return redirect(url_for('settings'))

    if request.method == 'POST':
        entered_otp = ''.join(ch for ch in request.form.get('otp', '').strip() if ch.isdigit())
        stored_otp = ''.join(ch for ch in (current_user.otp or '').strip() if ch.isdigit())
        otp_not_expired = bool(current_user.otp_expiry) and current_user.otp_expiry >= get_ist_time()

        if stored_otp and stored_otp == entered_otp and otp_not_expired:
            username = current_user.username
            current_user.otp = None
            current_user.otp_expiry = None
            db.session.commit()
            user_to_delete = db.session.get(User, current_user.id)
            logout_user()
            session.pop('pending_delete_user_id', None)
            try:
                delete_user_archive(user_to_delete)
                flash(f'ADMIN ACCOUNT {username.upper()} REMOVED PERMANENTLY.', 'danger')
                return redirect(url_for('register'))
            except Exception as e:
                flash(f'CRITICAL DELETION ERROR: {str(e)}', 'danger')
                return redirect(url_for('settings'))

        flash('INVALID SECURITY CODE: The code provided is incorrect or has expired.', 'danger')

    return render_template('delete_account_otp.html')

@app.route('/resend_delete_account_otp')
@login_required
def resend_delete_account_otp():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('settings'))

    session['pending_delete_user_id'] = current_user.id
    otp = ''.join(random.choices(string.digits, k=6))
    current_user.otp = otp
    current_user.otp_expiry = get_ist_time() + timedelta(minutes=5)
    db.session.commit()

    try:
        subject = "Nammude Gym: Admin Account Deletion OTP"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ background-color: #1a1a1a; color: #ffffff; font-family: sans-serif; padding: 20px; }}
                .container {{ max-width: 600px; margin: auto; background: #262626; padding: 30px; border-radius: 8px; border-top: 4px solid #FF5E5E; }}
                h1 {{ color: #FF5E5E; font-size: 28px; margin-bottom: 20px; }}
                p {{ font-size: 16px; line-height: 1.5; color: #dddddd; }}
                .otp {{ font-size: 36px; font-weight: bold; letter-spacing: 4px; color: #ffffff; background: #333; padding: 15px; display: inline-block; margin: 20px 0; border: 1px dashed #FF5E5E; }}
                .footer {{ margin-top: 30px; border-top: 1px solid #444; padding-top: 20px; font-size: 14px; color: #888; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>ADMIN DELETE VERIFICATION</h1>
                <p>Hello {current_user.username},</p>
                <p>Your new OTP for permanent admin account deletion is:</p>
                <div class="otp">{otp}</div>
                <p>This code is valid for <strong>5 minutes</strong>.</p>
                <div class="footer">
                    Best Regards,<br>
                    <strong>Team Nammude Gym</strong>
                </div>
            </div>
        </body>
        </html>
        """
        send_email(subject, html_body, current_user.email)
    except Exception as e:
        print(f"Error resending admin deletion OTP: {e}")

    flash('A NEW ADMIN DELETE OTP HAS BEEN SENT TO YOUR EMAIL.', 'info')
    return redirect(url_for('verify_delete_account_otp'))
@app.route('/diet_plans')
@login_required
@trainer_shift_required
def view_diet_plans():
    if current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        diet_plans = DietPlan.query.filter_by(trainer_id=trainer.id).all() if trainer else []
    elif current_user.role == 'user':
        member = Member.query.filter_by(user_id=current_user.id).first()
        diet_plans = DietPlan.query.filter_by(member_id=member.id).all() if member else []
    else:
        diet_plans = DietPlan.query.all()
    return render_template('diet_plans.html', diet_plans=diet_plans)

@app.route('/assign_diet', methods=['GET', 'POST'])
@login_required
@role_required(['trainer', 'admin'])
@trainer_shift_required
def assign_diet():
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        plan_name = request.form.get('plan_name')
        description = request.form.get('description')
        breakfast = request.form.get('breakfast')
        lunch = request.form.get('lunch')
        dinner = request.form.get('dinner')
        snacks = request.form.get('snacks')
        
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        if trainer:
            trainer_id = trainer.id
        else:
            first_trainer = Trainer.query.first()
            if not first_trainer:
                flash('Error: No trainers exist in the system to assign this diet protocol.', 'danger')
                return redirect(url_for('assign_diet'))
            trainer_id = first_trainer.id

        new_diet = DietPlan(
            member_id=member_id, 
            trainer_id=trainer_id, 
            plan_name=plan_name, 
            description=description,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snacks=snacks
        )
        db.session.add(new_diet)
        db.session.commit()
        
        # Notify Member via Email
        member = Member.query.get(member_id)
        if member:
            user = db.session.get(User, member.user_id)
            if user and user.email:
                subject = f"Nammude Gym: New Diet Protocol - {plan_name}"
                details = f"""
                    <div class="detail-item">
                        <span class="detail-label">Protocol Name</span>
                        <span class="detail-value">{plan_name}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Breakfast</span>
                        <span class="detail-value">{breakfast}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Lunch</span>
                        <span class="detail-value">{lunch}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Dinner</span>
                        <span class="detail-value">{dinner}</span>
                    </div>
                """
                
                html_body = BLUE_EMAIL_TEMPLATE.format(
                    title="DIET PROTOCOL ASSIGNED",
                    name=member.full_name,
                    message=f"Coach {current_user.username.upper()} has assigned a new nutritional protocol to your profile.",
                    details=details
                )
                send_email(subject, html_body, user.email)
        
        flash('Diet protocol assigned and athlete notified via email.', 'success')
        return redirect(url_for('view_diet_plans'))
        
    members = Member.query.filter_by(is_approved=True).all()
    return render_template('assign_diet.html', members=members)

@app.route('/delete_diet/<int:diet_id>', methods=['POST'])
@login_required
@role_required(['trainer', 'admin'])
@trainer_shift_required
def delete_diet(diet_id):
    diet = DietPlan.query.get_or_404(diet_id)
    db.session.delete(diet)
    db.session.commit()
    flash('Diet protocol removed successfully.', 'success')
    return redirect(url_for('view_diet_plans'))

if __name__ == '__main__':
    app.run(debug=True)

