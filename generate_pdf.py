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
            self.drawString(40, 760, "CYBERNOVA SOLUTIONS v4.0 | TECHNICAL ARCHITECTURE & STACK SPECIFICATION")
            self.setFont("Helvetica", 8)
            self.drawRightString(572, 760, "ENTERPRISE SPECIFICATION")

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(40, 40, 572, 40)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(40, 28, "CONFIDENTIAL & PROPRIETARY — CYBERNOVA SOLUTIONS ARCHITECTURE REVIEW")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 28, page_str)
        self.restoreState()

def build_pdf(filename):
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
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=12
    )
    section_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_text = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )
    td_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a")
    )
    td_code = ParagraphStyle(
        'TDCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0369a1")
    )
    td_text = ParagraphStyle(
        'TDText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.2,
        textColor=colors.HexColor("#334155")
    )

    story = []

    # Title & Header Banner
    story.append(Paragraph("CYBERNOVA SOLUTIONS", subtitle_style))
    story.append(Paragraph("Complete Project Tech Stack Specification", title_style))
    story.append(Paragraph("Autonomous Multi-Agent AI Mesh, Zero-Trust Architecture & Full-Stack Deployment", ParagraphStyle(
        'SubSub', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#475569"), spaceAfter=10
    )))

    # Metadata Grid Box
    meta_data = [
        [
            Paragraph("<b>Production Status:</b> Live on Vercel", td_text),
            Paragraph("<b>Live URL:</b> <font color='#0284c7'><u>https://cybernova-solutions-v4.vercel.app</u></font>", td_text)
        ],
        [
            Paragraph("<b>Version:</b> v4.0 / v5.0 Production Ready", td_text),
            Paragraph("<b>GitHub:</b> <font color='#0284c7'><u>https://github.com/hifza-kanwal-stack/cybernova_1</u></font>", td_text)
        ],
        [
            Paragraph("<b>Security Standard:</b> NIST CSF 2.0 & ISO/IEC 27001", td_text),
            Paragraph("<b>Generated:</b> " + datetime.now().strftime("%B %d, %Y"), td_text)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[240, 292])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # Executive Overview
    story.append(Paragraph("1. Executive Architecture Overview", section_title))
    overview_text = (
        "CyberNova Solutions is an enterprise-grade cybersecurity and governance platform built with an "
        "asynchronous Python ASGI core, an autonomous mesh of 4 specialized AI agents, cryptographic Root-CA "
        "digital license signing, and a role-based workstation model. It delivers autonomous risk assessment, "
        "real-time prompt-injection defense, automated incident response playbooks, and multi-rail payment verification."
    )
    story.append(Paragraph(overview_text, body_text))
    story.append(Spacer(1, 8))

    def make_table(headers, rows, col_widths):
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
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ]))
        return t

    # 2. Core Backend Architecture
    story.append(Paragraph("2. Core Backend & Web Framework", section_title))
    backend_rows = [
        [Paragraph("Python 3.11+", td_bold), Paragraph("Language Core", td_code), Paragraph("Primary backend language powering ASGI routing, cryptographic pipelines, and agent loops.", td_text)],
        [Paragraph("FastAPI (>=0.115.0)", td_bold), Paragraph("ASGI Framework", td_code), Paragraph("High-throughput REST API framework; utilizes dependency injection, automatic Pydantic validation, and OpenAPI documentation.", td_text)],
        [Paragraph("Uvicorn (>=0.32.0)", td_bold), Paragraph("ASGI Server", td_code), Paragraph("Production-grade asynchronous web server; supports reload hooks and direct Python script execution.", td_text)],
        [Paragraph("Pydantic (>=2.9.0)", td_bold), Paragraph("Data Validation", td_code), Paragraph("Strict typing and schema enforcement for API payloads (RegisterReq, LoginReq, CheckoutReq, etc.).", td_text)],
        [Paragraph("Async Lifespan & db_conn", td_bold), Paragraph("Resource Manager", td_code), Paragraph("Manages startup initialization and thread-safe SQLite connection contexts to prevent database locking.", td_text)]
    ]
    story.append(make_table(["Technology", "Category", "Role & Usage Details"], backend_rows, [120, 110, 302]))
    story.append(Spacer(1, 8))

    # 3. Autonomous Multi-Agent AI Mesh
    story.append(Paragraph("3. Autonomous Multi-Agent AI Mesh", section_title))
    agent_rows = [
        [
            Paragraph("Posture & Compliance Auditor", td_bold),
            Paragraph("agent-posture-01", td_code),
            Paragraph("Enterprise User", td_text),
            Paragraph("Audits drift against NIST/ISO controls, generates dynamic ReportLab CISO audit PDFs, and escalates low scores (<50) to SOC Agent.", td_text)
        ],
        [
            Paragraph("Fraud Investigation Agent", td_bold),
            Paragraph("agent-fraud-02", td_code),
            Paragraph("Checkout Pipeline", td_text),
            Paragraph("Calculates transaction monetary Z-scores, checks velocity, and quarantines suspicious payments (risk >= 60) for Human-In-The-Loop review.", td_text)
        ],
        [
            Paragraph("Autonomous SOC Responder", td_bold),
            Paragraph("agent-soc-03", td_code),
            Paragraph("Admin Command", td_text),
            Paragraph("Blocks prompt injection attempts with HTTP 403, isolates attacker sessions, drafts NIST incident playbooks, and alerts the CISO.", td_text)
        ],
        [
            Paragraph("License & Telemetry Watchdog", td_bold),
            Paragraph("agent-watchdog-04", td_code),
            Paragraph("Endpoint Nodes", td_text),
            Paragraph("Verifies Root-CA HMAC signatures, detects certificate tampering (TAMPER_ALERT), and ingests live agent heartbeats to reward posture.", td_text)
        ],
        [
            Paragraph("LLM Synthesis Engine", td_bold),
            Paragraph("Gemini / OpenAI API", td_code),
            Paragraph("Global Reasoning", td_text),
            Paragraph("Direct HTTP JSON completions endpoint over urllib.request providing situational reasoning with offline fallback heuristics.", td_text)
        ]
    ]
    story.append(make_table(["Agent Name", "Identifier", "Scope", "Capabilities & Autonomous Actions"], agent_rows, [115, 85, 75, 257]))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # 4. Security, Cryptography & Compliance
    story.append(Paragraph("4. Security Architecture, Cryptography & Zero-Trust", section_title))
    sec_rows = [
        [Paragraph("Digital License Signing", td_bold), Paragraph("HMAC-SHA256 (64-char)", td_code), Paragraph("Tamper-proof format: cnv1.<payload_b64>.<hmac_sha256_hex>. Verified with root secret key.", td_text)],
        [Paragraph("Password Hashing", td_bold), Paragraph("PBKDF2-HMAC-SHA256", td_code), Paragraph("260,000 hash iterations paired with 16-byte cryptographically secure random salts (secrets.token_hex(16)).", td_text)],
        [Paragraph("Multi-Factor Auth (2FA)", td_bold), Paragraph("Zero-Trust 6-Digit OTP", td_code), Paragraph("Cryptographically random 6-digit codes (secrets.randbelow) with strict 5-minute (300s) expiration window.", td_text)],
        [Paragraph("Session Management", td_bold), Paragraph("Bearer Tokens (8h Expiry)", td_code), Paragraph("URL-safe tokens (secrets.token_urlsafe(24)) with active session cleanup and token expiration verification.", td_text)],
        [Paragraph("AI Guardrails / WAF", td_bold), Paragraph("OWASP Top-10 LLM", td_code), Paragraph("Real-time regex & heuristic interceptor blocking jailbreak and prompt-injection patterns with HTTP 403.", td_text)],
        [Paragraph("Compliance Standards", td_bold), Paragraph("NIST CSF 2.0 & ISO 27001", td_code), Paragraph("Direct control mapping (NIST DE.CM-1, PR.AT-1, PR.DS-01, ISO-27001 A.8.16, A.8.24) in catalog and audit reports.", td_text)],
        [Paragraph("HTTP Security Headers", td_bold), Paragraph("Middleware Enforcement", td_code), Paragraph("Enforces X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy, and Permissions-Policy.", td_text)]
    ]
    story.append(make_table(["Domain", "Algorithm / Standard", "Implementation & Hardening"], sec_rows, [115, 120, 297]))
    story.append(Spacer(1, 8))

    # 5. Database & Persistence Layer
    story.append(Paragraph("5. Database & Persistence Architecture", section_title))
    db_rows = [
        [Paragraph("SQLite 3 Engine", td_bold), Paragraph("Standard Library", td_code), Paragraph("Embedded zero-config relational database; configured with check_same_thread=False and Row factories.", td_text)],
        [Paragraph("10 Relational Tables", td_bold), Paragraph("Normalized Schema", td_code), Paragraph("Tables: users, sessions, pending_2fa, products, orders, licenses, chat_messages, security_logs, agent_executions, smtp_settings.", td_text)],
        [Paragraph("Serverless Adapter", td_bold), Paragraph("Vercel /tmp Ephemeral", td_code), Paragraph("Auto-detects VERCEL environment; operates on /tmp/cybernova_v4.db with automated top-level self-initialization.", td_text)]
    ]
    story.append(make_table(["Component", "Engine", "Schema & Operational Behavior"], db_rows, [115, 120, 297]))
    story.append(Spacer(1, 8))

    # 6. Automated PDF Generation & Reporting
    story.append(Paragraph("6. Automated PDF Generation & Executive Reporting", section_title))
    pdf_rows = [
        [Paragraph("ReportLab 5.1+", td_bold), Paragraph("PDF Engine", td_code), Paragraph("Enterprise-grade document synthesis engine used to generate on-demand CISO Executive Security Dossiers.", td_text)],
        [Paragraph("Platypus Flowables", td_bold), Paragraph("Layout Pipeline", td_code), Paragraph("Renders dynamic SimpleDocTemplate, multi-column Tables, and Paragraph styles on Letter paper.", td_text)],
        [Paragraph("CISO Dossier Generator", td_bold), Paragraph("Posture Scoring", td_code), Paragraph("Automatically tabulates threat likelihoods, NIST framework alignment, and overall enterprise risk posture.", td_text)]
    ]
    story.append(make_table(["Tool / Library", "Module", "Application Details"], pdf_rows, [115, 120, 297]))
    story.append(Spacer(1, 8))

    # 7. Real-Time Communication & SMTP Gateway
    story.append(Paragraph("7. Real-Time Communication & SMTP Delivery", section_title))
    smtp_rows = [
        [Paragraph("smtplib & email.mime", td_bold), Paragraph("Python Standard Lib", td_code), Paragraph("Constructs multipart HTML/text emails with binary PDF attachments over TLS (Port 587) or SSL (Port 465).", td_text)],
        [Paragraph("Gmail SMTP Relay", td_bold), Paragraph("smtp.gmail.com:587", td_code), Paragraph("Dispatches real-time 2FA OTP codes directly to user inboxes using 16-character Google App Passwords.", td_text)],
        [Paragraph("In-App Relay Fallback", td_bold), Paragraph("Zero-Lockout Fallback", td_code), Paragraph("Provides built-in simulated relay codes when live credentials are absent, preventing developer lockout.", td_text)]
    ]
    story.append(make_table(["Protocol / Driver", "Port / Host", "Purpose & Redundancy"], smtp_rows, [115, 120, 297]))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # 8. Modern Frontend & Multi-Role Workstations
    story.append(Paragraph("8. Modern Frontend & Multi-Role Workstations", section_title))
    ui_rows = [
        [Paragraph("Vanilla JavaScript (ES6+)", td_bold), Paragraph("Zero Dependency", td_code), Paragraph("Pure native JavaScript utilizing async/await, fetch() API, and localStorage session synchronization.", td_text)],
        [Paragraph("Cyberpunk Dark Glassmorphism", td_bold), Paragraph("Custom CSS3", td_code), Paragraph("Custom design system with CSS custom properties: #070d19 (bg), #0e172a (panel), #06b6d4 (cyan), #10b981 (emerald).", td_text)],
        [Paragraph("Enterprise User Dashboard", td_bold), Paragraph("/dashboard/user", td_code), Paragraph("Security score circular gauge, live posture scanner, license ledger, marketplace with cart, and AI advisor chat.", td_text)],
        [Paragraph("SOC Consultant Desk", td_bold), Paragraph("/dashboard/consultant", td_code), Paragraph("Live agent execution feed, order risk inspection, security log text exporter, and multi-section SOC report generator.", td_text)],
        [Paragraph("Admin SOC Command Center", td_bold), Paragraph("/dashboard/admin", td_code), Paragraph("High-level KPIs, HITL AI fraud triage queue (Approve/Block), user directory, revenue breakdown, and SMTP management.", td_text)],
        [Paragraph("Store & Auth Portal", td_bold), Paragraph("templates/index.html", td_code), Paragraph("Security product store, real-time OTP modal dialog, live mail relay viewer, and role demo switcher.", td_text)]
    ]
    story.append(make_table(["UI Component", "Technology / Path", "Features & Interactive Capabilities"], ui_rows, [125, 110, 297]))
    story.append(Spacer(1, 8))

    # 9. DevOps, Containerization & Cloud Deployment
    story.append(Paragraph("9. DevOps, Containerization & Production Cloud", section_title))
    devops_rows = [
        [Paragraph("Docker", td_bold), Paragraph("python:3.11-slim", td_code), Paragraph("Production containerization with healthcheck probing /healthz and bytecode optimizations (PYTHONDONTWRITEBYTECODE=1).", td_text)],
        [Paragraph("Docker Compose", td_bold), Paragraph("docker-compose.yml", td_code), Paragraph("Single-command orchestration with port mapping (8000:8000), environment bindings, and automated restart policies.", td_text)],
        [Paragraph(".dockerignore", td_bold), Paragraph("Build Optimization", td_code), Paragraph("Excludes .git, .vercel, local .db SQLite files, and __pycache__ from Docker build contexts.", td_text)],
        [Paragraph("Vercel Serverless", td_bold), Paragraph("Live Cloud Runtime", td_code), Paragraph("Deployed at https://cybernova-solutions-v4.vercel.app via @vercel/python lambdas with bundled templates/**.", td_text)],
        [Paragraph("GitHub Repository", td_bold), Paragraph("Version Control", td_code), Paragraph("Hosted at https://github.com/hifza-kanwal-stack/cybernova_1 with automated commit synchronization.", td_text)]
    ]
    story.append(make_table(["Tool / Platform", "Configuration", "Deployment Function"], devops_rows, [115, 120, 297]))
    story.append(Spacer(1, 10))

    # 10. Summary Table
    story.append(Paragraph("10. Architecture Summary Matrix", section_title))
    summary_matrix = [
        [Paragraph("<b>Component</b>", th_style), Paragraph("<b>Primary Technology</b>", th_style), Paragraph("<b>Key Architectural Advantage</b>", th_style)],
        [Paragraph("Backend Framework", td_bold), Paragraph("Python 3.11 / FastAPI", td_text), Paragraph("Asynchronous execution, sub-millisecond response latency, robust typing.", td_text)],
        [Paragraph("AI Intelligence", td_bold), Paragraph("4 Autonomous Agents", td_text), Paragraph("Autonomous tool use, inter-agent escalation, automated compliance auditing.", td_text)],
        [Paragraph("Cryptographic Trust", td_bold), Paragraph("HMAC-SHA256 & PBKDF2", td_text), Paragraph("Tamper-proof signed software licenses, salted high-iteration password security.", td_text)],
        [Paragraph("User Authentication", td_bold), Paragraph("Real-Time Email 2FA", td_text), Paragraph("Zero-Trust 6-digit OTP codes delivered directly via TLS SMTP to user inboxes.", td_text)],
        [Paragraph("Frontend Interfaces", td_bold), Paragraph("Vanilla JS / Modern CSS3", td_text), Paragraph("Zero external bundle overhead, instant load times, 3 tailored role workstations.", td_text)],
        [Paragraph("Deployment Models", td_bold), Paragraph("Docker & Vercel Serverless", td_text), Paragraph("Dual compatibility: self-hosted containers or zero-maintenance serverless cloud.", td_text)]
    ]
    t_summary = Table(summary_matrix, colWidths=[120, 140, 272])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284c7")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(t_summary)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "CyberNova_Tech_Stack.pdf"
    build_pdf(out_file)
