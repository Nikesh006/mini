
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_pdf():
    doc = SimpleDocTemplate("Gym_Master_Database_Description.pdf", pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#FF7A00"),
        alignment=1,
        spaceAfter=30
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.white,
        backColor=colors.HexColor("#1e293b"),
        alignment=0,
        spaceBefore=20,
        spaceAfter=10,
        leftIndent=5
    )

    # Title Section
    elements.append(Paragraph("NAMMUDE GYM ARCHITECTURE", title_style))
    elements.append(Paragraph("System Database Schema & Entity Relationships", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))

    tables_data = [
        {
            "name": "USER (CORE AUTHENTICATION)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique system-wide identifier"],
                ["username", "VARCHAR(50)", "Unique credential for login"],
                ["email", "VARCHAR(100)", "Unique communication channel"],
                ["role", "VARCHAR(20)", "Access Level: admin, trainer, user"],
                ["status", "BOOLEAN", "Deletion request tracking"],
                ["otp", "VARCHAR(6)", "Security verification archive"]
            ]
        },
        {
            "name": "MEMBER (ATHLETE PROFILE)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique athlete identifier"],
                ["user_id", "INT (FK)", "Reference to core User account"],
                ["full_name", "VARCHAR(100)", "Official legal name"],
                ["plan_id", "INT (FK)", "Active membership protocol link"],
                ["status", "VARCHAR(20)", "Current state: Active/Expired"],
                ["is_approved", "BOOLEAN", "Admin authorization status"]
            ]
        },
        {
            "name": "TRAINER (COACHING STAFF)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique coach identifier"],
                ["user_id", "INT (FK)", "Reference to core User account"],
                ["specialization", "VARCHAR(100)", "Expert domain expertise"],
                ["is_approved", "BOOLEAN", "Facility authorization status"]
            ]
        },
        {
            "name": "MEMBERSHIP PLAN (PROTOCOLS)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique protocol ID"],
                ["name", "VARCHAR(100)", "Plan title (Elite, Basic, etc)"],
                ["price", "FLOAT", "Currency cost of the plan"],
                ["duration_days", "INT", "Validity window in days"]
            ]
        },
        {
            "name": "WORKOUT PLAN (ROUTINES)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique routine ID"],
                ["member_id", "INT (FK)", "Associated Athlete link"],
                ["trainer_id", "INT (FK)", "Assigned Elite Coach link"],
                ["exercises", "TEXT", "Detailed performance instructions"]
            ]
        },
        {
            "name": "DIET PLAN (NUTRITION)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique nutrition ID"],
                ["member_id", "INT (FK)", "Athlete assignment"],
                ["plan_name", "VARCHAR(100)", "Protocol title"],
                ["breakfast/lunch/dinner", "TEXT", "Scheduled meal archives"]
            ]
        },
        {
            "name": "ATTENDANCE (SHIFT LOGS)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique log identifier"],
                ["member_id", "INT (FK)", "Athlete check-in link (Optional)"],
                ["trainer_id", "INT (FK)", "Coach shift link (Optional)"],
                ["check_in/out", "DATETIME", "Entry/Exit timestamps"]
            ]
        },
        {
            "name": "PAYMENT (REVENUE HUB)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique invoice ID"],
                ["member_id", "INT (FK)", "Linked Athlete profile"],
                ["amount", "FLOAT", "Transaction value"],
                ["status", "VARCHAR(20)", "Payment state: Paid/Pending"]
            ]
        },
        {
            "name": "BOOKING (SESSION RESERVATIONS)",
            "rows": [
                ["COLUMN", "TYPE / KEY", "DESCRIPTION"],
                ["id", "INT (PK)", "Unique booking ID"],
                ["member_id", "INT (FK)", "Requesting Athlete"],
                ["trainer_id", "INT (FK)", "Assigned Coach"],
                ["booking_date", "DATE", "Scheduled session date"],
                ["status", "VARCHAR(20)", "Confirmed/Pending/Cancelled"]
            ]
        }
    ]

    for table_info in tables_data:
        # Table Header/Title
        elements.append(Paragraph(table_info['name'], table_header_style))
        
        # Create Table
        t = Table(table_info['rows'], colWidths=[1.5*inch, 1.5*inch, 4*inch])
        
        # Table Styling
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FF7A00")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 0.3*inch))

    # Build PDF
    doc.build(elements)
    print("PDF Re-Generated in Table Format: Gym_Master_Database_Description.pdf")

if __name__ == "__main__":
    generate_pdf()
