# CyberNova Solutions — Autonomous Multi-Agent Mesh & Real-Time SOC

> **Live Production Deployment:** [https://cybernova-solutions-v4.vercel.app](https://cybernova-solutions-v4.vercel.app)

An enterprise cybersecurity platform backed by an autonomous multi-agent mesh, cryptographic software license provisioning (HMAC-SHA256 Root-CA), real-time 2FA authentication via Gmail SMTP, and role-segregated operational workstations.

---

## 🚀 Key Features

### 1. Autonomous 4-Agent Mesh & Inter-Agent Handoffs
- **Agent 1: Posture & Compliance Auditor (`agent-posture-01`)**
  - Audits organizational controls against NIST CSF 2.0 and ISO-27001.
  - Generates signed ReportLab Executive CISO PDF dossiers.
  - Automatically escalates critical exposure (<50/100) to the SOC Responder Agent.
- **Agent 2: Fraud Investigation Agent (`agent-fraud-02`)**
  - Real-time monetary Z-score evaluation and cryptocurrency velocity checks.
  - Automatically quarantines anomalous orders (risk $\ge 60$) into the Admin HITL queue.
- **Agent 3: Autonomous SOC Responder (`agent-soc-03`)**
  - Guardrail defense against OWASP LLM prompt injection and brute-force attacks.
  - Executes Human-in-the-Loop (HITL) order clearances and security triage.
- **Agent 4: License & Telemetry Watchdog (`agent-watchdog-04`)**
  - Validates full 64-character HMAC-SHA256 Root-CA license certificates.
  - Ingests endpoint telemetry heartbeats and dynamically boosts posture scores.

### 2. Role-Segregated Dashboards & Access Control
- **👤 Enterprise User Dashboard (`/dashboard/user`)**: Security score gauge, posture scanner, CISO PDF download, software license vault, encrypted marketplace with checkout, and AI security advisor chat.
- **🛡️ SOC Consultant Workstation (`/dashboard/consultant`)**: Threat intelligence feed, read-only order risk review, security event logs with text export, posture analytics, and automated SOC consultant report generator.
- **🚨 Admin SOC Command Center (`/dashboard/admin`)**: Command center KPIs, HITL fraud triage queue with one-click clearance, enterprise user directory, revenue analytics, real-time Gmail SMTP configuration, and live security audit logs.

### 3. Real-Time Authentication
- Zero-Trust 2-step verification (6-digit OTP).
- Live email dispatch via Gmail SMTP over TLS/STARTTLS.
- In-app relay fallback for instant testing when SMTP credentials are not yet configured.
- 5-minute OTP challenge expiry and 8-hour session lifetime enforcement.

---

## 🛠️ Technology Stack
- **Backend:** FastAPI, Python 3.11+, Pydantic v2, ReportLab, SQLite
- **Deployment:** Vercel Serverless (with `@vercel/python`)
- **Security:** PBKDF2-HMAC-SHA256 password hashing, HMAC-SHA256 Root-CA signing, OWASP guardrails

---

## 🏁 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/hifza-kanwal-stack/cybernova_1.git
cd cybernova_1
pip install -r requirements.txt
```

### 2. Configure Environment (Optional for Live Gmail 2FA)
Copy `.env.example` to `.env` or set:
```ini
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-16-char-app-password
SMTP_FROM_NAME=CyberNova Autonomous SOC
CYBERNOVA_ROOT_CA_SECRET=your-secret-key-here
ALLOWED_ORIGINS=*
```

### 3. Run Locally
```bash
uvicorn main:app --reload --port 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🔑 Default Seed Profiles
- **System Admin:** `admin@cybernova.io` | `Admin@123` $\rightarrow$ `/dashboard/admin`
- **SOC Consultant:** `consultant@cybernova.io` | `Consult@123` $\rightarrow$ `/dashboard/consultant`
- **Enterprise User:** `hifza@cybernova.io` | `Cyber@123` $\rightarrow$ `/dashboard/user`
