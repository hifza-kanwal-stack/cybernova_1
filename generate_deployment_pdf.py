import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(40, 755, 572, 755)
            self.drawString(40, 760, "CYBERNOVA SOLUTIONS | PRODUCTION DEPLOYMENT MANUAL")
            self.setFont("Helvetica", 8)
            self.drawRightString(572, 760, "DEVOPS & CLOUD ARCHITECTURE")

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(40, 40, 572, 40)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(40, 28, "CYBERNOVA SOLUTIONS v4.0 — PRODUCTION VERIFIED DEPLOYMENT GUIDE")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 28, page_str)
        self.restoreState()

def build_deployment_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=10
    )
    section_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=5
    )
    body_text = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor("#334155")
    )
    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white
    )
    td_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )
    td_code = ParagraphStyle(
        'TDCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0369a1")
    )
    td_text = ParagraphStyle(
        'TDText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10,
        textColor=colors.HexColor("#334155")
    )

    def make_table(headers, rows, col_widths, header_color="#0f172a"):
        table_content = [[Paragraph(h, th_style) for h in headers]]
        for r in rows:
            formatted_row = []
            for cell in r:
                if isinstance(cell, str):
                    formatted_row.append(Paragraph(cell, td_text))
                else:
                    formatted_row.append(cell)
            table_content.append(formatted_row)
        
        t = Table(table_content, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_color)),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ]))
        return t

    story = []

    # Title & Subtitle
    story.append(Paragraph("CYBERNOVA SOLUTIONS", subtitle_style))
    story.append(Paragraph("Complete Production Deployment Guide", title_style))
    story.append(Paragraph("Comprehensive Cloud, Container & On-Premises Architecture Manual", ParagraphStyle(
        'SubSub', fontName='Helvetica', fontSize=8.8, leading=12, textColor=colors.HexColor("#475569"), spaceAfter=8
    )))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Target Environments:</b> Vercel Serverless, Docker, On-Prem", td_text),
            Paragraph("<b>Live URL:</b> <font color='#0284c7'><u>https://cybernova-solutions-v4.vercel.app</u></font>", td_text)
        ],
        [
            Paragraph("<b>Health Probe Endpoint:</b> <font color='#0369a1'>GET /healthz</font>", td_text),
            Paragraph("<b>GitHub:</b> <font color='#0284c7'><u>https://github.com/hifza-kanwal-stack/cybernova_1</u></font>", td_text)
        ],
        [
            Paragraph("<b>Runtime / Base:</b> Python 3.11-slim / FastAPI ASGI", td_text),
            Paragraph("<b>Published:</b> " + datetime.now().strftime("%B %d, %Y"), td_text)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[240, 292])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # 1. Executive Deployment Overview
    story.append(Paragraph("1. Executive Deployment Overview", section_title))
    overview_text = (
        "CyberNova Solutions is designed for <b>zero-dependency portability</b> across diverse infrastructure targets. "
        "The application utilizes an asynchronous Python ASGI core (FastAPI + Uvicorn) coupled with pure vanilla JavaScript "
        "and modern CSS3 frontend workstations, eliminating heavy node_modules build matrices and frontend asset compilations. "
        "This guide provides step-by-step procedures to deploy, configure, verify, and harden CyberNova in serverless, containerized, "
        "and bare-metal environments."
    )
    story.append(Paragraph(overview_text, body_text))
    story.append(Spacer(1, 6))

    target_rows = [
        [Paragraph("Vercel Serverless Platform", td_bold), Paragraph("@vercel/python /tmp SQLite", td_code), Paragraph("Zero-maintenance cloud runtime distributed globally across Vercel edge networks. Bundles HTML templates.", td_text)],
        [Paragraph("Docker Containerization", td_bold), Paragraph("python:3.11-slim + Compose", td_code), Paragraph("Lightweight production container with automated container health probes on /healthz and non-root execution.", td_text)],
        [Paragraph("Local Bare-Metal Setup", td_bold), Paragraph("Python 3.11+ Venv", td_code), Paragraph("Direct execution via python main.py or uvicorn for local development, security testing, and offline air-gapped nodes.", td_text)]
    ]
    story.append(make_table(["Deployment Target", "Underlying Technology", "Operational Profile & Use Case"], target_rows, [130, 135, 267]))
    story.append(Spacer(1, 6))

    # 2. Environment Variables & Secret Configuration
    story.append(Paragraph("2. Environment Variables & Cryptographic Secrets", section_title))
    env_rows = [
        [Paragraph("CYBERNOVA_ROOT_CA_SECRET", td_bold), Paragraph("Required", td_code), Paragraph("High-entropy secret key used to mint and cryptographically verify 64-char HMAC-SHA256 digital software licenses.", td_text)],
        [Paragraph("ALLOWED_ORIGINS", td_bold), Paragraph("Optional (CORS)", td_code), Paragraph("Comma-separated list of allowed domains (e.g. https://cybernova-solutions-v4.vercel.app). Defaults to [*] in dev.", td_text)],
        [Paragraph("SMTP_USER & SMTP_PASS", td_bold), Paragraph("Optional (Email 2FA)", td_code), Paragraph("Gmail address and 16-character Google App Password for live inbox 2FA OTP delivery. Fallback to in-app viewer if omitted.", td_text)],
        [Paragraph("SMTP_HOST & SMTP_PORT", td_bold), Paragraph("Default: smtp.gmail.com:587", td_code), Paragraph("SMTP relay endpoint supporting TLS/STARTTLS encryption protocols.", td_text)],
        [Paragraph("PORT", td_bold), Paragraph("Default: 8000", td_code), Paragraph("Binding port for Uvicorn ASGI server and Docker container port forwarding.", td_text)]
    ]
    story.append(make_table(["Environment Variable", "Requirement", "Security Function & Behavior"], env_rows, [140, 110, 282], header_color="#0369a1"))
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # 3. Target 1: Vercel Serverless Deployment
    story.append(Paragraph("3. Target 1: Vercel Serverless Cloud Deployment", section_title))
    vercel_text = (
        "The project includes a production <b>vercel.json</b> configuration tailored for Python serverless functions. "
        "Vercel utilizes a read-only filesystem except for the ephemeral <b>/tmp</b> directory."
    )
    story.append(Paragraph(vercel_text, body_text))
    story.append(Spacer(1, 4))

    vercel_steps = [
        [Paragraph("Step 1: Template Bundling", td_bold), Paragraph("vercel.json config", td_code), Paragraph("Explicitly packages HTML dashboards via includeFiles: ['templates/**'] to ensure serverless lambdas locate UI files.", td_text)],
        [Paragraph("Step 2: Ephemeral DB Adapter", td_bold), Paragraph("Dynamic DB_PATH", td_code), Paragraph("Detects os.environ.get('VERCEL') and binds SQLite to /tmp/cybernova_v4.db with automated top-level self-initialization.", td_text)],
        [Paragraph("Step 3: Continuous Deployment", td_bold), Paragraph("Git Push Trigger", td_code), Paragraph("Commits pushed to origin main at hifza-kanwal-stack/cybernova_1 automatically trigger live builds and edge deployments.", td_text)],
        [Paragraph("Step 4: Manual Vercel CLI", td_bold), Paragraph("vercel --prod", td_code), Paragraph("Deploys directly from the terminal without git webhooks; alias assigned to https://cybernova-solutions-v4.vercel.app.", td_text)]
    ]
    story.append(make_table(["Deployment Step", "Mechanism", "Technical Implementation Details"], vercel_steps, [125, 120, 287]))
    story.append(Spacer(1, 6))

    # 4. Target 2: Docker Containerization
    story.append(Paragraph("4. Target 2: Docker & Docker Compose Containerization", section_title))
    docker_text = (
        "For self-hosted, private cloud, or air-gapped deployments, CyberNova provides a hardened multi-stage Docker build."
    )
    story.append(Paragraph(docker_text, body_text))
    story.append(Spacer(1, 4))

    docker_rows = [
        [Paragraph("Base Image", td_bold), Paragraph("python:3.11-slim", td_code), Paragraph("Minimal footprint Debian Linux base minimizing image size and eliminating extraneous system binaries.", td_text)],
        [Paragraph("Bytecode Optimization", td_bold), Paragraph("PYTHONDONTWRITEBYTECODE=1", td_code), Paragraph("Prevents compiling .pyc files inside the container; unbuffered logging (PYTHONUNBUFFERED=1) for real-time stdout streams.", td_text)],
        [Paragraph("Healthcheck Probe", td_bold), Paragraph("curl -f http://.../healthz", td_code), Paragraph("Probes every 30s with a 5s timeout and 3 retries; guarantees container orchestrators detect service status.", td_text)],
        [Paragraph("Docker Compose", td_bold), Paragraph("docker-compose.yml", td_code), Paragraph("Binds port 8000:8000, loads environment variables, and enables restart: unless-stopped reliability.", td_text)]
    ]
    story.append(make_table(["Container Specification", "Configuration", "Operational Purpose"], docker_rows, [125, 130, 277]))
    story.append(Spacer(1, 6))

    # 5. Target 3: Local Bare-Metal Execution
    story.append(Paragraph("5. Target 3: Local Bare-Metal Setup & Execution", section_title))
    local_steps = [
        [Paragraph("1. Python Environment", td_bold), Paragraph("python -m venv venv", td_code), Paragraph("Establish isolated virtual environment running Python 3.11+.", td_text)],
        [Paragraph("2. Dependency Installation", td_bold), Paragraph("pip install -r requirements.txt", td_code), Paragraph("Installs FastAPI, Uvicorn, Pydantic, ReportLab, and cryptographic utilities.", td_text)],
        [Paragraph("3. Direct Script Launch", td_bold), Paragraph("python main.py", td_code), Paragraph("Executes built-in __main__ entrypoint; automatically starts server at http://127.0.0.1:8000.", td_text)],
        [Paragraph("4. Uvicorn Alternative", td_bold), Paragraph("uvicorn main:app --port 8000", td_code), Paragraph("Direct ASGI invocation (omit --reload on Windows to prevent socket spawn collisions).", td_text)]
    ]
    story.append(make_table(["Execution Step", "Command String", "Operational Details"], local_steps, [125, 145, 262]))
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # 6. Pre-Flight Health Check Checklist
    story.append(Paragraph("6. Pre-Flight Health Check & Verification Suite", section_title))
    check_rows = [
        [Paragraph("Service Healthcheck", td_bold), Paragraph("GET /healthz", td_code), Paragraph("Expected: {\"status\":\"healthy\",\"service\":\"cybernova-solutions-v4\",\"agents_active\":4}", td_text)],
        [Paragraph("System Bootstrap", td_bold), Paragraph("GET /api/bootstrap", td_code), Paragraph("Verifies database seeding, catalog availability, and system status flags.", td_text)],
        [Paragraph("Zero-Trust 2FA Check", td_bold), Paragraph("POST /api/auth/login", td_code), Paragraph("Returns challenge_id with 2FA_REQUIRED; strictly strips OTP from response body.", td_text)],
        [Paragraph("AI Prompt Guardrails", td_bold), Paragraph("Adversarial payload", td_code), Paragraph("OWASP prompt injections blocked with HTTP 403 Forbidden and session quarantined.", td_text)],
        [Paragraph("PDF Dossier Engine", td_bold), Paragraph("GET /api/audit/report/pdf", td_code), Paragraph("Generates binary application/pdf Letter stream with full threat tables and risk scoring.", td_text)]
    ]
    story.append(make_table(["Verification Step", "Endpoint / Action", "Expected Production Response"], check_rows, [125, 120, 287], header_color="#0f766e"))
    story.append(Spacer(1, 6))

    # 7. Pre-Seeded Demonstration Credentials
    story.append(Paragraph("7. Pre-Seeded Demonstration Credentials", section_title))
    cred_rows = [
        [Paragraph("System Administrator", td_bold), Paragraph("admin@cybernova.io", td_code), Paragraph("Admin@123", td_code), Paragraph("/dashboard/admin (Full SOC Command Center)", td_text)],
        [Paragraph("SOC Consultant", td_bold), Paragraph("consultant@cybernova.io", td_code), Paragraph("Consult@123", td_code), Paragraph("/dashboard/consultant (Telemetry & Reporting)", td_text)],
        [Paragraph("Enterprise User", td_bold), Paragraph("hifza@cybernova.io", td_code), Paragraph("Cyber@123", td_code), Paragraph("/dashboard/user (Posture & License Vault)", td_text)]
    ]
    story.append(make_table(["Role Name", "Login Email", "Password", "Target Workstation Route"], cred_rows, [115, 115, 80, 222]))
    story.append(Spacer(1, 6))

    # 8. Troubleshooting & Operational Runbook
    story.append(Paragraph("8. Troubleshooting & Operational Runbook", section_title))
    runbook_rows = [
        [Paragraph("Port 8000 Conflict [WinError 10048]", td_bold), Paragraph("An existing background Python instance is holding the port.", td_text), Paragraph("Run Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force, then rerun python main.py.", td_text)],
        [Paragraph("Vercel Missing Templates Error", td_bold), Paragraph("Serverless lambda cannot locate templates/ folder.", td_text), Paragraph("Ensure vercel.json includes 'config': {'includeFiles': ['templates/**']}.", td_text)],
        [Paragraph("SMTP Auth Failure (Error 535)", td_bold), Paragraph("Standard Gmail password entered instead of App Password.", td_text), Paragraph("Generate a 16-character Google App Password in Google Account > Security > 2-Step Verification.", td_text)],
        [Paragraph("Root-CA Secret Missing", td_bold), Paragraph("CYBERNOVA_ROOT_CA_SECRET not found in environment.", td_text), Paragraph("Set CYBERNOVA_ROOT_CA_SECRET in .env or Vercel Environment Variables dashboard.", td_text)]
    ]
    story.append(make_table(["Failure Scenario", "Root Cause Analysis", "Resolution Procedure"], runbook_rows, [130, 150, 252]))
    story.append(Spacer(1, 8))

    # Sign-off box
    sign_data = [
        [
            Paragraph("<b>Verified By:</b> Hifza Kanwal<br/>Engineering Lead, CyberNova Solutions", td_text),
            Paragraph("<b>Deployment Status:</b> PRODUCTION ACTIVE<br/>Endpoint: https://cybernova-solutions-v4.vercel.app", td_text)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[266, 266])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Deployment PDF successfully built: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "CyberNova_Deployment_Guide.pdf"
    build_deployment_pdf(out_file)
