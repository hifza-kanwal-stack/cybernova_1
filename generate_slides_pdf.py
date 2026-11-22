import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class SlideCanvas(canvas.Canvas):
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
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, page_count):
        self.saveState()
        # Top banner line
        self.setStrokeColor(colors.HexColor("#0284c7"))
        self.setLineWidth(2)
        self.line(40, 565, 752, 565)
        
        # Bottom footer line
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(40, 35, 752, 35)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(40, 24, "CYBERNOVA SOLUTIONS v4.0 | MASTER ARCHITECTURE & PLATFORM DECK")
        
        self.setFont("Helvetica", 8)
        page_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(752, 24, page_str)
        self.restoreState()

def build_slides_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=35,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    slide_num_style = ParagraphStyle(
        'SlideNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=2
    )
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10
    )
    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#334155")
    )
    th_style = ParagraphStyle(
        'SlideTH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    td_bold = ParagraphStyle(
        'SlideTDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )
    td_code = ParagraphStyle(
        'SlideTDCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#0369a1")
    )
    td_text = ParagraphStyle(
        'SlideTDText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
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
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ]))
        return t

    story = []

    # Slide 1: Title & Executive Introduction
    story.append(Paragraph("SLIDE 01 | EXECUTIVE INTRODUCTION", slide_num_style))
    story.append(Paragraph("CyberNova Solutions v4.0 / v5.0", slide_title_style))
    story.append(Paragraph("<b>Autonomous Zero-Trust Cybersecurity & AI Governance Platform</b>", ParagraphStyle('Sub1', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor("#0284c7"), spaceAfter=14)))
    
    meta_data = [
        [Paragraph("<b>Status:</b> Production Verified • Live on Vercel", td_text), Paragraph("<b>Live URL:</b> https://cybernova-solutions-v4.vercel.app", td_text)],
        [Paragraph("<b>Author / Lead:</b> Hifza Kanwal", td_text), Paragraph("<b>GitHub:</b> https://github.com/hifza-kanwal-stack/cybernova_1", td_text)],
        [Paragraph("<b>Framework:</b> Python 3.11+ / FastAPI / ASGI", td_text), Paragraph("<b>Standards:</b> NIST CSF 2.0 & ISO/IEC 27001", td_text)]
    ]
    t1 = Table(meta_data, colWidths=[356, 356])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t1)
    story.append(Spacer(1, 14))
    story.append(Paragraph("CyberNova Solutions is a next-generation enterprise security platform combining asynchronous Python microservices, an autonomous mesh of 4 specialized AI agents, and Root-CA cryptographic licensing. It eliminates compliance blind spots, automates real-time threat response, and protects digital software licensing with verifiable mathematics.", body_style))
    story.append(PageBreak())

    # Slide 2: Industry Challenges & The Solution Paradigm
    story.append(Paragraph("SLIDE 02 | PROBLEM & SOLUTION PARADIGM", slide_num_style))
    story.append(Paragraph("Moving from Reactive Checklists to Autonomous AI Governance", slide_title_style))
    p_rows = [
        [Paragraph("Manual Compliance Auditing", td_bold), Paragraph("Weeks wasted manually compiling static evidence for NIST and ISO audits.", td_text), Paragraph("Continuous Autonomous Auditing: Instant 0-100 posture scoring and dynamic CISO PDF dossiers.", td_text)],
        [Paragraph("SOC Alert Fatigue", td_bold), Paragraph("Analysts overwhelmed by thousands of un-triaged events daily; slow response times.", td_text), Paragraph("Self-Triaging AI SOC: Real-time prompt-injection defense (<1s) and automated session isolation.", td_text)],
        [Paragraph("Software Tampering & Piracy", td_bold), Paragraph("Traditional license keys easily reverse-engineered or modified in client memory.", td_text), Paragraph("Root-CA HMAC-SHA256 mathematical signatures (cnv1.<payload>.<sig>) guarantee authenticity.", td_text)],
        [Paragraph("Checkout & Digital Fraud", td_bold), Paragraph("High chargebacks, fraudulent card transactions, and rapid crypto velocity abuse.", td_text), Paragraph("Statistical monetary Z-score scoring auto-quarantines suspicious orders (>=60 risk).", td_text)]
    ]
    story.append(make_table(["Operational Domain", "Legacy Vulnerability (Problem)", "CyberNova Autonomous Paradigm (Solution)"], p_rows, [160, 260, 292]))
    story.append(PageBreak())

    # Slide 3: High-Level Platform Architecture
    story.append(Paragraph("SLIDE 03 | ARCHITECTURE BLUEPRINT", slide_num_style))
    story.append(Paragraph("High-Level Platform Architecture & Tech Stack", slide_title_style))
    arch_rows = [
        [Paragraph("Presentation Layer", td_bold), Paragraph("Vanilla JS (ES6+) & Modern CSS3", td_code), Paragraph("Zero external JavaScript bundle overhead; 3 dedicated role dashboards with cyberpunk glassmorphism.", td_text)],
        [Paragraph("Web Service / ASGI Core", td_bold), Paragraph("FastAPI + Uvicorn (Python 3.11+)", td_code), Paragraph("Asynchronous routing, lifespan initialization, db_conn connection pooling, and hardened security headers.", td_text)],
        [Paragraph("AI Multi-Agent Mesh", td_bold), Paragraph("4 Autonomous Agents + Heuristics", td_code), Paragraph("Specialized workers for compliance auditing, fraud detection, SOC defense, and license watchdog.", td_text)],
        [Paragraph("Cryptographic Trust", td_bold), Paragraph("HMAC-SHA256 & PBKDF2", td_code), Paragraph("Root-CA license signing, 260,000 PBKDF2 password hashing rounds, and 5-minute hardware-entropy 2FA OTPs.", td_text)],
        [Paragraph("Persistence & Storage", td_bold), Paragraph("SQLite 3 (10 Relational Tables)", td_code), Paragraph("Normalized relational persistence with dynamic /tmp adapter for Vercel serverless cloud.", td_text)],
        [Paragraph("Cloud & DevOps", td_bold), Paragraph("Docker & Vercel Serverless", td_code), Paragraph("Dual portability: self-hosted lightweight containers with healthchecks or global Vercel serverless edge.", td_text)]
    ]
    story.append(make_table(["Architectural Layer", "Primary Technology", "Functional Responsibility"], arch_rows, [140, 180, 392]))
    story.append(PageBreak())

    # Slide 4: The 4 Autonomous AI Agents
    story.append(Paragraph("SLIDE 04 | ARTIFICIAL INTELLIGENCE", slide_num_style))
    story.append(Paragraph("The Autonomous 4-Agent Mesh", slide_title_style))
    agent_rows = [
        [Paragraph("Posture Auditor", td_bold), Paragraph("agent-posture-01", td_code), Paragraph("Enterprise User", td_text), Paragraph("Audits control drift against NIST CSF 2.0 & ISO 27001; builds CISO PDFs; escalates score <50 to SOC Agent.", td_text)],
        [Paragraph("Fraud Investigator", td_bold), Paragraph("agent-fraud-02", td_code), Paragraph("Checkout Pipeline", td_text), Paragraph("Calculates monetary Z-scores and crypto velocity; auto-quarantines orders with risk >= 60 for HITL review.", td_text)],
        [Paragraph("SOC Responder", td_bold), Paragraph("agent-soc-03", td_code), Paragraph("Admin SOC", td_text), Paragraph("Blocks prompt injections with HTTP 403, isolates attacker sessions, drafts NIST playbooks, and alerts CISO.", td_text)],
        [Paragraph("License Watchdog", td_bold), Paragraph("agent-watchdog-04", td_code), Paragraph("Endpoint Nodes", td_text), Paragraph("Verifies Root-CA HMAC signatures, detects counterfeit keys (TAMPER_ALERT), and ingests node heartbeats.", td_text)]
    ]
    story.append(make_table(["Agent Name", "Identifier", "Operational Scope", "Autonomous Capabilities & Tool Actions"], agent_rows, [130, 120, 110, 352]))
    story.append(PageBreak())

    # Slide 5: Cryptography, Root-CA & Zero-Trust Security
    story.append(Paragraph("SLIDE 05 | CRYPTOGRAPHY & SECURITY", slide_num_style))
    story.append(Paragraph("Cryptographic Root-of-Trust & Hardened Security", slide_title_style))
    sec_rows = [
        [Paragraph("Root-CA Digital License Minting", td_bold), Paragraph("HMAC-SHA256 (64-char Hex)", td_code), Paragraph("Custom format: cnv1.<payload_b64>.<hmac_sha256_hex>. Verified with root secret key. Eliminates software cracking.", td_text)],
        [Paragraph("Password Hashing", td_bold), Paragraph("PBKDF2-HMAC-SHA256", td_code), Paragraph("260,000 hash iterations paired with 16-byte cryptographically secure random salts (secrets.token_hex(16)).", td_text)],
        [Paragraph("Zero-Trust 2FA (OTP)", td_bold), Paragraph("Hardware-Entropy 6-Digit OTP", td_code), Paragraph("Cryptographically random 6-digit challenge codes with strict 5-minute (300s) expiration window.", td_text)],
        [Paragraph("Session Bearer Tokens", td_bold), Paragraph("Bearer Tokens (8h Expiry)", td_code), Paragraph("32-byte URL-safe cryptographic tokens with enforced 8-hour expiration and automatic database cleanup.", td_text)],
        [Paragraph("HTTP Security Headers", td_bold), Paragraph("Middleware Enforcement", td_code), Paragraph("Enforces X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy, and Permissions-Policy.", td_text)]
    ]
    story.append(make_table(["Security Domain", "Algorithm / Standard", "Implementation & Hardening"], sec_rows, [170, 170, 372]))
    story.append(PageBreak())

    # Slide 6: Real-Time Authentication & Zero-Trust 2FA
    story.append(Paragraph("SLIDE 06 | AUTHENTICATION PIPELINE", slide_num_style))
    story.append(Paragraph("Real-Time Email 2FA & Challenge Pipeline", slide_title_style))
    auth_rows = [
        [Paragraph("1. Password Verification", td_bold), Paragraph("PBKDF2 Hash Match", td_code), Paragraph("User submits credentials; backend validates salted PBKDF2 hash with constant-time comparison.", td_text)],
        [Paragraph("2. 2FA Challenge Generation", td_bold), Paragraph("secrets.randbelow()", td_code), Paragraph("Generates 6-digit code tied to unique challenge_id with strict 300s expiration in pending_2fa table.", td_text)],
        [Paragraph("3. Real-Time SMTP Dispatch", td_bold), Paragraph("smtp.gmail.com:587 TLS", td_code), Paragraph("Dispatches OTP directly to user's real email inbox via TLS/STARTTLS with Google App Password.", td_text)],
        [Paragraph("4. Zero-Lockout Fallback", td_bold), Paragraph("In-App Mail Viewer", td_code), Paragraph("Exposes code in local developer relay viewer when live SMTP credentials are unconfigured.", td_text)],
        [Paragraph("5. Bearer Session Grant", td_bold), Paragraph("8-Hour Session Token", td_code), Paragraph("Upon OTP verification, user receives bearer token and auto-redirects to their dedicated role dashboard.", td_text)]
    ]
    story.append(make_table(["Authentication Step", "Mechanism / Protocol", "Operational Behavior"], auth_rows, [150, 160, 402]))
    story.append(PageBreak())

    # Slide 7: Dedicated Multi-Role Workstations
    story.append(Paragraph("SLIDE 07 | OPERATIONAL WORKSTATIONS", slide_num_style))
    story.append(Paragraph("Tailored Role-Based Workstations (RBAC)", slide_title_style))
    ui_rows = [
        [Paragraph("Enterprise User Dashboard", td_bold), Paragraph("/dashboard/user", td_code), Paragraph("Zero-Trust security score gauge (0-100), live posture scanner, software license ledger with copyable keys, software store, and AI advisor chat.", td_text)],
        [Paragraph("SOC Consultant Desk", td_bold), Paragraph("/dashboard/consultant", td_code), Paragraph("Live agent execution audit stream, order risk telemetry analyzer, one-click raw security log text file exporter, and multi-section SOC report builder.", td_text)],
        [Paragraph("Admin SOC Command Center", td_bold), Paragraph("/dashboard/admin", td_code), Paragraph("Global KPIs (users, revenue, quarantined orders), Human-In-The-Loop AI fraud triage queue (Approve/Block), user directory with role badges, and SMTP settings.", td_text)],
        [Paragraph("Main Storefront & Auth Portal", td_bold), Paragraph("templates/index.html", td_code), Paragraph("Curated security software catalog, multi-rail checkout modal, real-time OTP challenge dialog, and role demo switcher.", td_text)]
    ]
    story.append(make_table(["Workstation Portal", "Route / Path", "Features & Interactive Capabilities"], ui_rows, [160, 150, 402]))
    story.append(PageBreak())

    # Slide 8: E-Commerce, Multi-Rail Payments & Fraud Scoring
    story.append(Paragraph("SLIDE 08 | E-COMMERCE & PAYMENTS", slide_num_style))
    story.append(Paragraph("Enterprise Store & AI-Scored Payment Pipeline", slide_title_style))
    pay_rows = [
        [Paragraph("Curated Security Catalog", td_bold), Paragraph("NIST & ISO Aligned", td_code), Paragraph("Products mapped to NIST CSF and ISO 27001 controls (Endpoint Guardian, Zero-Trust Gateway, AI Compliance Bot).", td_text)],
        [Paragraph("Multi-Rail Checkout", td_bold), Paragraph("Card & Cryptocurrency", td_code), Paragraph("Supports Corporate Credit Cards as well as Cryptocurrency rails (BTC, ETH, USDC) with mock verification engines.", td_text)],
        [Paragraph("Agent 2 Statistical Fraud Engine", td_bold), Paragraph("Monetary Z-Score", td_code), Paragraph("Calculates price deviations against catalog baseline and monitors rapid repeated checkout velocity.", td_text)],
        [Paragraph("Human-In-The-Loop (HITL) Guard", td_bold), Paragraph("Risk >= 60 Quarantine", td_code), Paragraph("High-risk transactions are quarantined as QUARANTINED_PENDING_REVIEW; held for Admin approval before license minting.", td_text)],
        [Paragraph("Automated License Minting", td_bold), Paragraph("Instant Root-CA Sign", td_code), Paragraph("Approved transactions immediately trigger Root-CA HMAC signing and license key vault storage.", td_text)]
    ]
    story.append(make_table(["Checkout Stage", "Mechanism", "Operational Purpose"], pay_rows, [160, 150, 402]))
    story.append(PageBreak())

    # Slide 9: Automated Reporting & PDF Generation Engine
    story.append(Paragraph("SLIDE 09 | REPORTING & DOCUMENTATION", slide_num_style))
    story.append(Paragraph("Automated CISO Security Dossier PDF Engine", slide_title_style))
    doc_rows = [
        [Paragraph("ReportLab 5.1+ Engine", td_bold), Paragraph("Platypus Flowables", td_code), Paragraph("Utilizes SimpleDocTemplate, multi-column Tables, and Paragraph styles on Letter paper with zero external PDF binaries.", td_text)],
        [Paragraph("Dynamic Data Population", td_bold), Paragraph("Live SQLite Telemetry", td_code), Paragraph("Queries live organization profile, current posture score, active licenses, and recent threat events.", td_text)],
        [Paragraph("Executive Risk Matrices", td_bold), Paragraph("NIST & ISO Crosswalk", td_code), Paragraph("Formats threat likelihood matrices, control coverage tables, and posture progress gauges.", td_text)],
        [Paragraph("Dual Delivery Architecture", td_bold), Paragraph("Download & SMTP Attach", td_code), Paragraph("Direct in-browser download via /api/audit/report/pdf and automated binary MIME attachment email delivery to CISO.", td_text)]
    ]
    story.append(make_table(["Reporting Component", "Technology", "Executive Function"], doc_rows, [160, 150, 402]))
    story.append(PageBreak())

    # Slide 10: Autonomous AI Guardrails & OWASP WAF
    story.append(Paragraph("SLIDE 10 | DEFENSIVE GUARDRAILS", slide_num_style))
    story.append(Paragraph("Autonomous AI Guardrails & Prompt-Injection Firewall", slide_title_style))
    waf_rows = [
        [Paragraph("OWASP LLM01: Prompt Injection", td_bold), Paragraph("Regex & Heuristic Filter", td_code), Paragraph("Detects and blocks jailbreaks ('ignore all previous instructions', 'act as an unrestricted AI') with HTTP 403.", td_text)],
        [Paragraph("OWASP LLM02: Data Disclosure", td_bold), Paragraph("Exfiltration Defense", td_code), Paragraph("Blocks queries attempting to reveal system instructions, database schemas, or secret keys.", td_text)],
        [Paragraph("Automated Attacker Containment", td_bold), Paragraph("Agent 3 SOC Responder", td_code), Paragraph("Immediately isolates offending session tokens and logs critical security incidents in security_logs table.", td_text)],
        [Paragraph("NIST Incident Playbook", td_bold), Paragraph("Autonomous Synthesis", td_code), Paragraph("Drafts targeted containment playbooks and alerts CISO in real-time via the consultant telemetry feed.", td_text)]
    ]
    story.append(make_table(["Threat Category", "Detection & Defense", "Autonomous Remediation Action"], waf_rows, [160, 150, 402]))
    story.append(PageBreak())

    # Slide 11: DevOps, Containerization & Production Cloud
    story.append(Paragraph("SLIDE 11 | DEVOPS & INFRASTRUCTURE", slide_num_style))
    story.append(Paragraph("Dual-Target Architecture: Docker Containers & Vercel Cloud", slide_title_style))
    dev_rows = [
        [Paragraph("Vercel Serverless Platform", td_bold), Paragraph("@vercel/python /tmp DB", td_code), Paragraph("Deployed at https://cybernova-solutions-v4.vercel.app with bundled templates/** and global edge CDN.", td_text)],
        [Paragraph("Docker Containerization", td_bold), Paragraph("python:3.11-slim", td_code), Paragraph("Production container with bytecode optimizations and automated healthcheck probes on /healthz.", td_text)],
        [Paragraph("Docker Compose", td_bold), Paragraph("docker-compose.yml", td_code), Paragraph("Single-command launch (docker-compose up -d) with port 8000:8000 mapping and restart: unless-stopped.", td_text)],
        [Paragraph("GitHub Repository", td_bold), Paragraph("hifza-kanwal-stack/cybernova_1", td_code), Paragraph("Full version control with automated commit synchronization across code, documentation, and Docker configs.", td_text)]
    ]
    story.append(make_table(["Infrastructure Target", "Configuration", "Deployment Characteristics"], dev_rows, [160, 160, 392]))
    story.append(PageBreak())

    # Slide 12: Business Impact, Value Proposition & Roadmap
    story.append(Paragraph("SLIDE 12 | VALUE PROPOSITION & ROADMAP", slide_num_style))
    story.append(Paragraph("Business Impact, ROI & Future Roadmap", slide_title_style))
    val_rows = [
        [Paragraph("90% Audit Time Reduction", td_bold), Paragraph("Compliance Efficiency", td_code), Paragraph("Accelerates NIST CSF 2.0 and ISO 27001 audit preparation from 3 weeks to under 5 minutes.", td_text)],
        [Paragraph("$150,000+ Annual Savings", td_bold), Paragraph("SecOps Automation", td_code), Paragraph("Autonomous triage of L1 security alerts, prompt injections, and e-commerce fraud reduces analyst workloads.", td_text)],
        [Paragraph("100% Cryptographic Trust", td_bold), Paragraph("Zero Counterfeit Loss", td_code), Paragraph("Unforgeable Root-CA HMAC software licenses protect proprietary intellectual property from cracking or replication.", td_text)],
        [Paragraph("Strategic Roadmap (v5.1+)", td_bold), Paragraph("Future Capabilities", td_code), Paragraph("Native Stripe/PayPal payment on-ramps, on-chain crypto smart contracts, and multi-tenant PostgreSQL clustering.", td_text)]
    ]
    story.append(make_table(["Enterprise Value Driver", "Impact Category", "Operational & Financial Outcome"], val_rows, [160, 150, 402]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Live Production Endpoint:</b> <font color='#0284c7'><u>https://cybernova-solutions-v4.vercel.app</u></font>  |  <b>GitHub:</b> <font color='#0284c7'><u>https://github.com/hifza-kanwal-stack/cybernova_1</u></font>", body_style))

    doc.build(story, canvasmaker=SlideCanvas)
    print(f"Slides PDF successfully built: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "CyberNova_12_Slides_Presentation.pdf"
    build_slides_pdf(out_file)
