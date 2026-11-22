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
            self.drawString(40, 760, "CYBERNOVA SOLUTIONS | FORMAL ENTERPRISE PROJECT PROPOSAL")
            self.setFont("Helvetica", 8)
            self.drawRightString(572, 760, "CONFIDENTIAL & PROPRIETARY")

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(40, 40, 572, 40)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(40, 28, "CYBERNOVA SOLUTIONS v4.0 — AUTONOMOUS ZERO-TRUST AI GOVERNANCE")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 28, page_str)
        self.restoreState()

def build_proposal_pdf(filename):
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

    # Title & Header
    story.append(Paragraph("CYBERNOVA SOLUTIONS", subtitle_style))
    story.append(Paragraph("Formal Enterprise Project Proposal", title_style))
    story.append(Paragraph("Autonomous Zero-Trust Cybersecurity & AI Governance Platform", ParagraphStyle(
        'SubSub', fontName='Helvetica', fontSize=8.8, leading=12, textColor=colors.HexColor("#475569"), spaceAfter=8
    )))

    # Metadata Table
    meta_data = [
        [
            Paragraph("<b>Target Audience:</b> Enterprise CISOs, CTOs & Procurement", td_text),
            Paragraph("<b>Live URL:</b> <font color='#0284c7'><u>https://cybernova-solutions-v4.vercel.app</u></font>", td_text)
        ],
        [
            Paragraph("<b>Author / Lead:</b> Hifza Kanwal (Engineering Lead)", td_text),
            Paragraph("<b>GitHub:</b> <font color='#0284c7'><u>https://github.com/hifza-kanwal-stack/cybernova_1</u></font>", td_text)
        ],
        [
            Paragraph("<b>Document Version:</b> 1.0 (Production Verified)", td_text),
            Paragraph("<b>Publication Date:</b> " + datetime.now().strftime("%B %d, %Y"), td_text)
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

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", section_title))
    exec_summary = (
        "Modern enterprise security organizations face an unsustainable paradox: as threat vectors expand through "
        "automated attack tools and generative AI, defense teams remain hindered by fragmented manual audits, alert fatigue "
        "in the Security Operations Center (SOC), unverified software distribution, and static compliance spreadsheets. "
        "<b>CyberNova Solutions</b> is an enterprise-grade autonomous cybersecurity ecosystem engineered to solve this dilemma. "
        "Built upon an asynchronous Python ASGI microservice architecture, CyberNova combines an autonomous mesh of four specialized "
        "AI agents, a cryptographic Root-CA license signing engine, real-time email 2FA authentication, and three purpose-built "
        "operational workstations. The platform continuously audits compliance against NIST CSF 2.0 and ISO/IEC 27001, intercepts "
        "OWASP LLM prompt injection attacks with sub-second latency, isolates unauthorized sessions, prevents e-commerce payment fraud "
        "via statistical Z-score algorithms, and issues cryptographically unforgeable digital software licenses."
    )
    story.append(Paragraph(exec_summary, body_text))
    story.append(Spacer(1, 6))

    # 2. Problem Statement & Solution Paradigm
    story.append(Paragraph("2. Problem Statement & The CyberNova Paradigm", section_title))
    problem_rows = [
        [Paragraph("Manual Compliance Auditing", td_bold), Paragraph("Weeks wasted gathering static evidence across disparate systems for NIST/ISO audits.", td_text), Paragraph("Instant continuous posture scoring (0-100) and automated CISO PDF dossiers.", td_text)],
        [Paragraph("SOC Alert Fatigue & Delayed MTTR", td_bold), Paragraph("Analysts overwhelmed by thousands of un-triaged events daily; delayed containment.", td_text), Paragraph("Autonomous SOC Agent intercepts prompt attacks in <1s and isolates sessions.", td_text)],
        [Paragraph("Software Tampering & Piracy", td_bold), Paragraph("Traditional license keys easily reverse-engineered or modified in client memory.", td_text), Paragraph("Root-CA HMAC-SHA256 mathematical signatures (cnv1.<payload>.<sig>) guarantee authenticity.", td_text)],
        [Paragraph("E-Commerce & Digital Fraud", td_bold), Paragraph("High chargebacks, fraudulent card transactions, and rapid crypto velocity abuse.", td_text), Paragraph("Statistical monetary Z-score scoring auto-quarantines suspicious orders (>=60 risk).", td_text)]
    ]
    story.append(make_table(["Industry Bottleneck", "Legacy Vulnerability", "CyberNova Autonomous Solution"], problem_rows, [125, 195, 212]))
    story.append(Spacer(1, 6))

    # 3. Project Objectives
    story.append(Paragraph("3. Project Objectives & Quantitative Success Criteria", section_title))
    obj_rows = [
        [Paragraph("Audit Cycle Automation", td_bold), Paragraph("Reduce compliance preparation time by >= 90%", td_code), Paragraph("Accelerates audit readiness from 3 weeks to under 5 minutes.", td_text)],
        [Paragraph("Sub-Second Threat Response", td_bold), Paragraph("< 1.0 second prompt-injection interception", td_code), Paragraph("Guarantees zero successful LLM jailbreaks; triggers session revocation.", td_text)],
        [Paragraph("Fraud Prevention (HITL)", td_bold), Paragraph("100% of high-risk checkouts quarantined", td_code), Paragraph("Transactions with risk >= 60 held for Admin review prior to license minting.", td_text)],
        [Paragraph("Cryptographic Software Integrity", td_bold), Paragraph("100% cryptographic license verification", td_code), Paragraph("Zero forged licenses; node heartbeat telemetry rewarded dynamically.", td_text)],
        [Paragraph("High Platform Availability", td_bold), Paragraph("99.9% uptime across Docker & Serverless", td_code), Paragraph("Verified zero-deadlock cold starts on Vercel and local containers.", td_text)]
    ]
    story.append(make_table(["Strategic Objective", "Target Performance Metric", "Enterprise Business Impact"], obj_rows, [125, 175, 232], header_color="#0369a1"))
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # 4. Scope of Work (SOW)
    story.append(Paragraph("4. Technical Scope of Work (SOW)", section_title))
    sow_text = (
        "The CyberNova implementation spans six integrated functional modules, delivering a unified zero-trust platform:"
    )
    story.append(Paragraph(sow_text, body_text))
    story.append(Spacer(1, 4))

    sow_rows = [
        [Paragraph("Module 1: ASGI Core Gateway", td_bold), Paragraph("Python 3.11+, FastAPI, Uvicorn, contextlib", td_code), Paragraph("Asynchronous routing, lifespan initialization, thread-safe connection pooling (db_conn), and hardened security headers (X-Frame-Options, nosniff).", td_text)],
        [Paragraph("Module 2: Autonomous AI Mesh", td_bold), Paragraph("4 Autonomous Agents + LLM Heuristics", td_code), Paragraph("Multi-agent architecture: Posture Auditor, Fraud Investigator, SOC Responder, and License Watchdog with inter-agent escalation.", td_text)],
        [Paragraph("Module 3: Cryptography & 2FA", td_bold), Paragraph("HMAC-SHA256, PBKDF2, Zero-Trust OTP", td_code), Paragraph("Root-CA license signing, 260,000 PBKDF2 hash iterations, 5-minute hardware-entropy 2FA OTPs, and 8-hour bearer session management.", td_text)],
        [Paragraph("Module 4: Multi-Role Workstations", td_bold), Paragraph("Vanilla JS ES6+, Cyberpunk CSS3", td_code), Paragraph("Dedicated portals: Enterprise User (/dashboard/user), SOC Consultant (/dashboard/consultant), and Admin Command (/dashboard/admin).", td_text)],
        [Paragraph("Module 5: Automated CISO Dossiers", td_bold), Paragraph("ReportLab 5.1+ Platypus Engine", td_code), Paragraph("Dynamic generation of executive PDF security dossiers with risk gauges, threat likelihood tables, and compliance crosswalks.", td_text)],
        [Paragraph("Module 6: Cloud & DevOps", td_bold), Paragraph("Docker, Compose, Vercel Serverless", td_code), Paragraph("Lightweight python:3.11-slim container with healthchecks and live production deployment on Vercel's global edge network.", td_text)]
    ]
    story.append(make_table(["Functional Module", "Underlying Tech Stack", "Scope of Implementation"], sow_rows, [125, 160, 247]))
    story.append(Spacer(1, 6))

    # 5. Autonomous AI Sentinel Mesh
    story.append(Paragraph("5. The Autonomous AI Sentinel Mesh", section_title))
    agent_rows = [
        [Paragraph("Posture & Compliance Auditor", td_bold), Paragraph("agent-posture-01", td_code), Paragraph("Enterprise User", td_text), Paragraph("Audits controls against NIST CSF 2.0 & ISO 27001; builds CISO PDFs; escalates score <50 to Agent 3.", td_text)],
        [Paragraph("Fraud Investigation Agent", td_bold), Paragraph("agent-fraud-02", td_code), Paragraph("Checkout Pipeline", td_text), Paragraph("Calculates monetary Z-scores and crypto velocity; auto-quarantines orders with risk >= 60 for HITL review.", td_text)],
        [Paragraph("Autonomous SOC Responder", td_bold), Paragraph("agent-soc-03", td_code), Paragraph("Admin SOC", td_text), Paragraph("Blocks prompt injections with HTTP 403, isolates attacker sessions, drafts NIST playbooks, and alerts CISO.", td_text)],
        [Paragraph("License Watchdog Agent", td_bold), Paragraph("agent-watchdog-04", td_code), Paragraph("Endpoint Nodes", td_text), Paragraph("Verifies Root-CA HMAC signatures, detects counterfeit keys (TAMPER_ALERT), and ingests node heartbeats.", td_text)]
    ]
    story.append(make_table(["Agent Name", "Identifier", "Operational Scope", "Autonomous Capabilities & Tool Actions"], agent_rows, [115, 85, 75, 257]))
    story.append(Spacer(1, 6))

    # 6. Implementation Timeline & Completed Milestones
    story.append(Paragraph("6. Implementation Timeline & Verified Milestones", section_title))
    milestone_rows = [
        [Paragraph("Phase 1: Security Audit & Hardening", td_bold), Paragraph("Verified Complete", td_code), Paragraph("Remediated CORS wildcard, removed OTP exposure, enforced 5-min OTP and 8-hr session timeouts, upgraded HMAC to 64-char SHA-256.", td_text)],
        [Paragraph("Phase 2: Multi-Role Workstations", td_bold), Paragraph("Verified Complete", td_code), Paragraph("Designed and implemented dedicated User (793L), Consultant (1,370L), and Admin (723L) dashboards with automatic role-based routing.", td_text)],
        [Paragraph("Phase 3: Autonomous AI Mesh", td_bold), Paragraph("Verified Complete", td_code), Paragraph("Engineered 4 autonomous AI agents with inter-agent escalation, ReportLab PDF dossier generation, and prompt injection firewall.", td_text)],
        [Paragraph("Phase 4: Production Cloud Deployment", td_bold), Paragraph("Verified Complete", td_code), Paragraph("Deployed live to Vercel at https://cybernova-solutions-v4.vercel.app with serverless /tmp ephemeral SQLite persistence.", td_text)],
        [Paragraph("Phase 5: Docker & Handover Suite", td_bold), Paragraph("Verified Complete", td_code), Paragraph("Authored Dockerfile, docker-compose.yml, synced GitHub repo hifza-kanwal-stack/cybernova_1, and compiled full documentation.", td_text)]
    ]
    story.append(make_table(["Implementation Phase", "Execution Status", "Key Deliverables & Verified Outcomes"], milestone_rows, [130, 95, 307], header_color="#0369a1"))
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # 7. Risk Assessment & Mitigation
    story.append(Paragraph("7. Enterprise Risk Assessment & Mitigation Matrix", section_title))
    risk_rows = [
        [Paragraph("Serverless Cold-Start Latency", td_bold), Paragraph("Medium", td_code), Paragraph("Top-level module DB initialization with db_conn() context manager and /tmp path resolver.", td_text)],
        [Paragraph("LLM Prompt Injection / Jailbreaks", td_bold), Paragraph("High", td_code), Paragraph("Inline AI WAF blocking prompt injection strings with HTTP 403 and immediate attacker session revocation.", td_text)],
        [Paragraph("Email Deliverability Failure", td_bold), Paragraph("Medium", td_code), Paragraph("Dual-path SMTP: live Gmail TLS relay combined with automatic fallback to local in-app mail viewer.", td_text)],
        [Paragraph("Database Concurrency Deadlocks", td_bold), Paragraph("Low", td_code), Paragraph("Thread-safe connection pooling with check_same_thread=False and isolated short-lived query lifetimes.", td_text)],
        [Paragraph("License Key Forgery", td_bold), Paragraph("Critical", td_code), Paragraph("Full 64-character HMAC-SHA256 cryptographic signatures tied to the root CA secret key.", td_text)]
    ]
    story.append(make_table(["Identified Operational Risk", "Inherent Severity", "Mitigation Strategy Implemented in CyberNova"], risk_rows, [130, 75, 327]))
    story.append(Spacer(1, 6))

    # 8. Return on Investment (ROI)
    story.append(Paragraph("8. Business Justification & Return on Investment (ROI)", section_title))
    roi_text = (
        "Implementing CyberNova Solutions yields measurable operational and financial returns across four primary axes:"
    )
    story.append(Paragraph(roi_text, body_text))
    story.append(Spacer(1, 4))

    roi_rows = [
        [Paragraph("Audit Cost Reduction", td_bold), Paragraph("90% Preparation Reduction", td_code), Paragraph("Eliminates weeks of manual spreadsheet cross-referencing by generating dynamic CISO compliance dossiers on demand.", td_text)],
        [Paragraph("SecOps Cost Savings", td_bold), Paragraph("$150,000+ Annual Savings", td_code), Paragraph("Autonomous triage of L1 security alerts, prompt injections, and e-commerce fraud reduces analyst workloads.", td_text)],
        [Paragraph("Revenue Assurance", td_bold), Paragraph("Zero Counterfeit Loss", td_code), Paragraph("Unforgeable Root-CA HMAC software licenses protect proprietary intellectual property from cracking or replication.", td_text)],
        [Paragraph("Zero Framework Overhead", td_bold), Paragraph("$0 Recurring Framework Fees", td_code), Paragraph("Powered entirely by Python, open-source libraries, and vanilla web standards—zero recurring client licensing fees.", td_text)]
    ]
    story.append(make_table(["Value Driver", "Quantified ROI Metric", "Financial & Operational Impact"], roi_rows, [115, 125, 292], header_color="#0f766e"))
    story.append(Spacer(1, 8))

    # 9. Deliverables & Sign-Off
    story.append(Paragraph("9. Deliverables Package & Acceptance", section_title))
    deliverables_text = (
        "<b>Complete Handover Package includes:</b><br/>"
        "1. <b>Source Code:</b> Synchronized at <font color='#0284c7'><u>https://github.com/hifza-kanwal-stack/cybernova_1</u></font><br/>"
        "2. <b>Live Cloud Environment:</b> Active on Vercel at <font color='#0284c7'><u>https://cybernova-solutions-v4.vercel.app</u></font><br/>"
        "3. <b>Container Configurations:</b> Production Dockerfile, docker-compose.yml, and .dockerignore<br/>"
        "4. <b>Documentation Suite:</b> PROJECT_PROPOSAL.md, TECH_STACK.md, CyberNova_Tech_Stack.pdf, PRESENTATION_12_SLIDES.md<br/>"
        "5. <b>Pre-configured Test Profiles:</b> System Admin, SOC Consultant, and Enterprise User credentials for immediate UAT."
    )
    story.append(Paragraph(deliverables_text, body_text))
    story.append(Spacer(1, 10))

    # Sign-off box
    sign_data = [
        [
            Paragraph("<b>Submitted By:</b> Hifza Kanwal<br/>Engineering Lead, CyberNova Solutions", td_text),
            Paragraph("<b>Client Acceptance:</b><br/>Authorized Representative Signature: _____________________", td_text)
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
    print(f"Proposal PDF successfully built: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "CyberNova_Project_Proposal.pdf"
    build_proposal_pdf(out_file)
