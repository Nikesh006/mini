
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def draw_slide_background(canvas, doc):
    canvas.saveState()
    # Dark theme background
    canvas.setFillColor(colors.HexColor("#020408"))
    canvas.rect(0, 0, doc.width + 2*doc.leftMargin, doc.height + 2*doc.topMargin, fill=1)
    
    # Header bar
    canvas.setFillColor(colors.HexColor("#0f172a"))
    canvas.rect(0, doc.height + doc.topMargin - 0.8*inch, doc.width + 2*doc.leftMargin, 0.8*inch, fill=1)
    
    # Decorative accents
    canvas.setStrokeColor(colors.HexColor("#FF7A00"))
    canvas.setLineWidth(3)
    canvas.line(0, doc.height + doc.topMargin - 0.8*inch, doc.width + 2*doc.leftMargin, doc.height + doc.topMargin - 0.8*inch)
    
    # Footer
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.drawCentredString((doc.width + 2*doc.leftMargin)/2, 0.4*inch, "NAMMUDE GYM MANAGEMENT SYSTEM - PROJECT ARCHITECTURE")
    canvas.restoreState()

def generate_presentation():
    # Use landscape letter
    pagesize = landscape(letter)
    doc = SimpleDocTemplate("Nammude_Gym_Elite_Project_Presentation.pdf", 
                            pagesize=pagesize,
                            leftMargin=0.75*inch,
                            rightMargin=0.75*inch,
                            topMargin=1*inch,
                            bottomMargin=0.75*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=48,
        textColor=colors.white,
        alignment=1,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        fontSize=24,
        textColor=colors.HexColor("#FF7A00"),
        alignment=1,
        spaceAfter=40,
        fontName='Helvetica-Bold'
    )
    
    slide_header_style = ParagraphStyle(
        'SlideHeader',
        fontSize=28,
        textColor=colors.white,
        alignment=0,
        spaceBefore=0,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        fontSize=18,
        textColor=colors.white,
        leading=24,
        spaceBefore=10,
        leftIndent=20,
        fontName='Helvetica'
    )
    
    green_sub_style = ParagraphStyle(
        'GreenSub',
        fontSize=14,
        textColor=colors.HexColor("#10B981"),
        fontName='Helvetica-BoldOblique',
        spaceAfter=20
    )

    # 1. Title Slide
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("NAMMUDE GYM", title_style))
    elements.append(Paragraph("ELITE GYM MANAGEMENT ECOSYSTEM", subtitle_style))
    elements.append(Paragraph("A Full-Stack Solution for Modern Fitness Centers", 
                              ParagraphStyle('Tag', fontSize=16, textColor=colors.HexColor("#94a3b8"), alignment=1)))
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("PRESENTED BY: TEAM NAMMUDE", 
                              ParagraphStyle('Presenter', fontSize=14, textColor=colors.white, alignment=1, fontName='Helvetica-Bold')))
    elements.append(PageBreak())

    # Slides Data
    slides = [
        {
            "title": "Introduction",
            "points": [
                "Nammude Gym is a high-performance management system designed to bridge the gap between facility owners, coaches, and athletes.",
                "The system replaces fragmented paper-based tracking with a unified digital command center.",
                "It focuses on elite transformation tracking, automated financial auditing, and security.",
                "Built with a 'User-First' philosophy using modern web technologies."
            ]
        },
        {
            "title": "Problem Statement",
            "sub": "THE CHALLENGES WE SOLVED",
            "points": [
                "Inconsistent tracking of athlete progress leading to poor transformation results.",
                "Manual revenue management often results in financial discrepancies and untracked billing.",
                "Fragmented communication between coaches and members regarding nutrition and routines.",
                "Lack of centralized equipment inventory management and maintenance records.",
                "Security risks associated with open access to sensitive membership data."
            ]
        },
        {
            "title": "Objectives",
            "points": [
                "To provide a robust, real-time dashboard for three distinct user roles: Admin, Trainer, and User.",
                "To automate the generation of individual transformation reports and financial invoices.",
                "To implement a secure, OTP-based verification system for sensitive operations.",
                "To centralize all gym protocols, including nutrition, performance plans, and gear inventory.",
                "To enable seamless performance monitoring through interactive data visualization."
            ]
        },
        {
            "title": "Feasibility Study",
            "sub": "IS THE SYSTEM VIABLE?",
            "points": [
                "TECHNICAL FEASIBILITY: The system uses stable technologies like Flask and MySQL, ensuring scalability and reliability.",
                "ECONOMIC FEASIBILITY: Reduces administrative overhead costs and eliminates paper-based record-keeping expenses.",
                "OPERATIONAL FEASIBILITY: Intuitive UI/UX design ensures that trainers and athletes can use the system with zero technical training.",
                "SECURITY FEASIBILITY: Implements Bcrypt hashing and role-based access control (RBAC) to protect organizational data."
            ]
        },
        {
            "title": "System Requirements",
            "points": [
                "SOFTWARE REQUIREMENTS: Python 3.x, Flask Framework, MySQL Database, ReportLab for PDF, Chart.js for Visualization.",
                "HARDWARE REQUIREMENTS: Any modern server/PC with 4GB+ RAM, 10GB Storage, and an active Internet connection.",
                "CLIENT REQUIREMENTS: Any modern web browser (Chrome, Safari, Edge) on Desktop or Mobile.",
                "COMMUNICATION: SMTP Server for automated email dispatches and OTP verification."
            ]
        },
        {
            "title": "System Architecture",
            "sub": "THE TECHNOLOGY ECOSYSTEM",
            "points": [
                "FRONTEND LAYER: Responsive HTML5/CSS3 with Glassmorphism aesthetic and JavaScript interactivity.",
                "BACKEND LAYER: Flask Micro-framework handling routing, authentication, and server-side logic.",
                "DATABASE LAYER: MySQL Relational Database for structured entity relationship management.",
                "STORAGE LAYER: Secure local/cloud storage for athlete biometric archives and profile media.",
                "EXTERNAL SERVICES: SMTP Protocol for transactional emails and PDF generation engine."
            ]
        },
        {
            "title": "Database Design",
            "sub": "ENTITY RELATIONSHIP OVERVIEW",
            "points": [
                "USER ENTITY: Handles authentication, security roles, and system access logs.",
                "ATHLETE ENTITY: Manages biometric data, membership expiry, and plan assignments.",
                "COACH ENTITY: Tracks trainer specializations, experience, and shift attendance.",
                "FINANCIAL ENTITY: Archives revenue, invoices, and transaction status.",
                "CORE MODULES: Attendance logs, Performance plans, Nutrition protocols, and Gear inventory."
            ]
        },
        {
            "title": "Core System Modules",
            "points": [
                "PERFORMANCE HUB: Individual workout routines assigned by elite coaches.",
                "NUTRITION CENTER: Bespoke diet protocols and meal archives for athletes.",
                "TRANSFORMATION ENGINE: Visual weight tracking and biometric evolution logs.",
                "REVENUE COMMAND: Centralized billing, invoice generation, and revenue auditing.",
                "SHIFT MANAGER: Real-time attendance tracking for both coaches and members."
            ]
        },
        {
            "title": "Conclusion & Future Scope",
            "points": [
                "CONCLUSION: Nammude Gym effectively centralizes facility management, providing a modern, secure, and data-driven experience.",
                "FUTURE SCOPE: Integration of IoT devices for automated weight tracking and smart entry.",
                "FUTURE SCOPE: Implementation of AI-driven workout recommendations based on biometric data.",
                "FUTURE SCOPE: Native mobile application for real-time notifications and session booking."
            ]
        }
    ]

    for slide in slides:
        # Move up to the header bar area
        elements.append(Spacer(1, -0.65*inch))
        elements.append(Paragraph(slide['title'].upper(), slide_header_style))
        elements.append(Spacer(1, 0.65*inch))
        
        if 'sub' in slide:
            elements.append(Paragraph(slide['sub'], green_sub_style))
        else:
            elements.append(Spacer(1, 0.2*inch))
            
        for point in slide['points']:
            elements.append(Paragraph(f"• {point}", bullet_style))
            
        elements.append(PageBreak())

    # Build PDF with background drawer
    doc.build(elements, onFirstPage=draw_slide_background, onLaterPages=draw_slide_background)
    print("Project Presentation PDF Re-Generated (Platypus Format): Nammude_Gym_Elite_Project_Presentation.pdf")

if __name__ == "__main__":
    generate_presentation()
