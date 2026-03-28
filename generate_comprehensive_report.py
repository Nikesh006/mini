
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def draw_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(colors.HexColor("#FF7A00"))
    canvas.drawString(inch, 10.5*inch, "NAMMUDE GYM - ULTIMATE TECHNICAL DOSSIER (CODE DEEP-DIVE)")
    canvas.line(inch, 10.4*inch, 7.5*inch, 10.4*inch)
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(4.25*inch, 0.5*inch, f"Page {doc.page} - Ultimate System Documentation")
    canvas.restoreState()

def generate_report():
    doc = SimpleDocTemplate("Nammude_Gym_Ultimate_Technical_Dossier.pdf", 
                            pagesize=letter,
                            rightMargin=50, leftMargin=50, 
                            topMargin=72, bottomMargin=72)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=28, textColor=colors.HexColor("#1e293b"), spaceAfter=20, fontName='Helvetica-Bold')
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=20, textColor=colors.HexColor("#FF7A00"), spaceBefore=25, spaceAfter=12, fontName='Helvetica-Bold')
    h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=15, textColor=colors.HexColor("#0f172a"), spaceBefore=15, spaceAfter=8, fontName='Helvetica-Bold')
    body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=10, alignment=0)
    code_title = ParagraphStyle('CodeTitle', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor("#1e293b"), spaceBefore=10)
    code_box = ParagraphStyle('CodeBox', parent=styles['Normal'], fontName='Courier', fontSize=8.5, leftIndent=15, textColor=colors.HexColor("#334155"), spaceBefore=5, spaceAfter=5, backColor=colors.HexColor("#f1f5f9"), borderPadding=5)

    # 1. TITLE PAGE
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("NAMMUDE GYM", ParagraphStyle('Title', fontSize=52, alignment=1, textColor=colors.HexColor("#FF7A00"), fontName='Helvetica-Bold')))
    elements.append(Paragraph("ULTIMATE TECHNICAL DOSSIER", ParagraphStyle('SubTitle', fontSize=26, alignment=1, textColor=colors.HexColor("#1e293b"), fontName='Helvetica-Bold')))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("COMPLETE CODEBASE ANALYSIS, ARCHITECTURE & LOGIC FLOW", ParagraphStyle('Desc', fontSize=14, alignment=1, textColor=colors.grey)))
    elements.append(Spacer(1, 3.5*inch))
    elements.append(Paragraph("VERSION: 3.0 (ULTIMATE EDITION)", ParagraphStyle('Ver', fontSize=12, alignment=1, fontName='Helvetica-Bold')))
    elements.append(PageBreak())

    # 2. CODEBASE ARCHITECTURE
    elements.append(Paragraph("1. CODEBASE ARCHITECTURE & FILE STRUCTURE", h1))
    elements.append(Paragraph("The Nammude Gym system follows a modular Monolithic Architecture. Below is the granular breakdown of every file and its technical purpose:", body))
    
    file_struct = [
        ["FILE NAME", "TECHNICAL PURPOSE", "KEY COMPONENT"],
        ["app.py", "Main Controller & Route Engine", "Flask App, 80+ Routes"],
        ["models.py", "Data Entity Definitions", "SQLAlchemy Models (15 Classes)"],
        ["config.py", "Environment Configuration", "MySQL URI, Secret Keys, Mail Server"],
        ["utils.py", "Service Layer / Helper Functions", "Email Engine, IST Time, File Validations"],
        ["check_schema.py", "DB Migration & Health Check", "Schema verification & initialization"],
        ["/templates", "Presentation Layer", "Jinja2 HTML with Glassmorphism UI"],
        ["/static/css", "Aesthetic Definition", "Modern CSS variables & layout logic"],
        ["/static/uploads", "Media Storage", "Profile pictures & Biometric archives"]
    ]
    st = Table(file_struct, colWidths=[1.3*inch, 2.7*inch, 3.0*inch])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    elements.append(st)
    elements.append(PageBreak())

    # 3. CORE ENGINE DEEP DIVE (app.py)
    elements.append(Paragraph("2. CORE ENGINE IMPLEMENTATION (app.py)", h1))
    
    elements.append(Paragraph("2.1 Authentication & RBAC Logic", h2))
    elements.append(Paragraph("The system uses Flask-Login to manage user sessions. Access control is enforced via custom decorators.", body))
    elements.append(Paragraph("Key Decorators:", code_title))
    elements.append(Paragraph("@login_required: Ensures user is authenticated.\n@role_required(['admin', 'trainer']): Restricts route to specific permission levels.\n@trainer_shift_required: Ensures a trainer has checked in before they can manage athletes.", code_box))

    elements.append(Paragraph("2.2 Strategic Route Mapping", h2))
    elements.append(Paragraph("Below are the primary logic controllers driving the application functionality:", body))
    
    routes = [
        ["MODULE", "ROUTE", "LOGIC DESCRIPTION"],
        ["Auth", "/register & /login", "Bcrypt validation, Session creation, OTP trigger."],
        ["Dashboard", "/dashboard", "Role-based branching to Admin, Trainer, or User views."],
        ["Progress", "/view_progress", "Chart.js data retrieval and weight logging logic."],
        ["Protocols", "/assign_workout", "Exercise list management and database linkage."],
        ["Finance", "/view_payments", "Revenue Hub filtering and invoice generation."],
        ["Reports", "/reports", "The Report Hub: Dynamic PDF generation for audits."]
    ]
    rt = Table(routes, colWidths=[1.2*inch, 1.8*inch, 4.0*inch])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FF7A00")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    elements.append(rt)
    elements.append(PageBreak())

    # 4. DATA INTEGRITY (models.py)
    elements.append(Paragraph("3. DATA INTEGRITY LAYER (models.py)", h1))
    elements.append(Paragraph("Our database uses SQLAlchemy ORM for object-relational mapping. The schema is designed for high relational integrity.", body))
    
    elements.append(Paragraph("Example: Member & User Relationship", h2))
    elements.append(Paragraph("class Member(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)\n    # ... profile data ...\n    user = db.relationship('User', backref='member_profile', uselist=False)", code_box))
    elements.append(Paragraph("The uselist=False parameter creates a strict One-to-One relationship, ensuring that one User account can only represent one Athlete profile, maintaining data purity.", body))

    elements.append(Paragraph("Example: Attendance Tracking", h2))
    elements.append(Paragraph("class Attendance(db.Model):\n    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))\n    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))\n    check_in = db.Column(db.DateTime, default=get_ist_time)", code_box))
    elements.append(Paragraph("The Attendance model is polymorphic; it can record both Member sessions and Trainer shifts, allowing for unified reporting in the Report Hub.", body))
    elements.append(PageBreak())

    # 5. SERVICE LAYER (utils.py & config.py)
    elements.append(Paragraph("4. SERVICE & UTILITY LAYER", h1))
    
    elements.append(Paragraph("4.1 Global Timing Protocol (utils.py)", h2))
    elements.append(Paragraph("Because the server might be hosted in a different timezone (UTC), we enforce Indian Standard Time (IST) globally across all entities to ensure accurate shift and payment logs.", body))
    elements.append(Paragraph("def get_ist_time():\n    return datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)", code_box))

    elements.append(Paragraph("4.2 Communication Engine (SMTP)", h2))
    elements.append(Paragraph("The send_email helper function utilizes Flask-Mail principles but is optimized for raw SMTP to reduce overhead. It supports two distinct templates: The RED ELITE (for warnings/deletions) and the BLUE PROTOCOL (for onboarding and updates).", body))
    elements.append(PageBreak())

    # 6. FEATURE IMPLEMENTATION DETAILS
    elements.append(Paragraph("5. CORE FEATURE IMPLEMENTATION LOGIC", h1))
    
    elements.append(Paragraph("5.1 Transformation Charting", h2))
    elements.append(Paragraph("The system extracts weight logs as a JSON list, which is then parsed by the client-side JavaScript to render an interactive line graph. This reduces server load as the actual rendering happens on the user's browser.", body))

    elements.append(Paragraph("5.2 Report Hub (PDF Generation)", h2))
    elements.append(Paragraph("Revenue and Attendance reports are generated on-the-fly using ReportLab. The system queries the filtered database results, builds a coordinate-based PDF layout, and streams the result directly to the user as a download attachment using Flask's send_file.", body))

    elements.append(Paragraph("5.3 Custom UI: confirmProtocol()", h2))
    elements.append(Paragraph("To eliminate standard browser dialogs, we implemented a custom JavaScript overlay in base.html. It traps the form submission, displays a high-impact security warning, and only re-triggers the submission if the user clicks 'AUTHORIZE'.", body))
    elements.append(PageBreak())

    # 7. SECURITY & ERROR HANDLING
    elements.append(Paragraph("6. SECURITY, STABILITY & ERROR HANDLING", h1))
    
    elements.append(Paragraph("6.1 Security Handshake (OTP)", h2))
    elements.append(Paragraph("When a user requests a membership upgrade, the verify_otp route is triggered. A random 6-digit code is generated via Python's 'random' library, hashed (optional), and stored. The user must submit this via a form to finalize the database update.", body))

    elements.append(Paragraph("6.2 Error Resilience", h2))
    elements.append(Paragraph("We implemented try-except blocks around all I/O operations (Database writes, Email dispatches, File uploads). For instance, if the SMTP server is down, the system will flash a 'WARNING' message but will NOT crash, allowing the database update to persist while notifying the admin of the email failure.", body))

    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("THE NAMMUDE GYM MANAGEMENT SYSTEM IS NOW A FULLY DOCUMENTED, PRODUCTION-READY ELITE ECOSYSTEM.", ParagraphStyle('Final', alignment=1, fontSize=14, fontName='Helvetica-Bold', textColor=colors.HexColor("#FF7A00"))))

    # Build PDF
    doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
    print("Ultimate Technical Dossier Generated: Nammude_Gym_Ultimate_Technical_Dossier.pdf")

if __name__ == "__main__":
    generate_report()
