# CyberNova Solutions — Complete Project Tech Stack

A comprehensive architectural breakdown of all technologies, frameworks, libraries, protocols, and deployment environments utilized in **CyberNova Solutions v4.0 / v5.0**.

---

## 🏛️ 1. Core Backend Architecture

| Technology | Version / Spec | Purpose & Usage |
| :--- | :--- | :--- |
| **Python** | `3.11+` | Primary programming language powering the entire backend, multi-agent engine, and cryptographic verification pipelines. |
| **FastAPI** | `>=0.115.0` | High-performance asynchronous ASGI web framework. Utilized for RESTful routing, dependency injection (`Depends()`), automatic request validation, and HTTP exception handling. |
| **Uvicorn** | `>=0.32.0` | Lightning-fast ASGI web server implementation used to run the FastAPI application both locally and in production containers. |
| **Pydantic** | `>=2.9.0` | Data validation and settings management using Python type annotations for all API request/response payloads (`RegisterReq`, `LoginReq`, `CheckoutReq`, etc.). |
| **Contextlib / Lifespan** | Python Standard Lib | Manages application lifespan (`@asynccontextmanager`) and database connection contexts (`db_conn()`) for safe resource allocation and cold-start handling. |

---

## 🤖 2. Autonomous Multi-Agent AI Mesh

The platform is driven by an autonomous mesh of 4 specialized AI agents capable of autonomous tool invocation and inter-agent handoffs:

| Agent Name | Identifier | Role Scope | Autonomous Capabilities & Tools |
| :--- | :--- | :--- | :--- |
| **Posture & Compliance Auditor Agent** | `agent-posture-01` | Enterprise User | `scan_control_drift()`, `map_nist_iso_controls()`, `generate_ciso_pdf_dossier()`. Calculates 0–100 risk score and escalates critical exposure to Agent 3. |
| **Fraud Investigation Agent** | `agent-fraud-02` | Checkout Pipeline | `compute_monetary_zscore()`, `inspect_crypto_velocity()`, `correlate_auth_anomalies()`, `quarantine_hitl_order()`. Automatically flags and quarantines suspicious transactions ($\ge 60$ risk). |
| **Autonomous SOC Responder Agent** | `agent-soc-03` | Admin SOC & Guardrails | `block_prompt_injection()`, `isolate_attacker_session()`, `draft_nist_ir_playbook()`, `dispatch_ciso_alert_email()`. Defends against prompt injections and enforces brute-force lockout. |
| **License & Telemetry Watchdog Agent** | `agent-watchdog-04` | Deployed SDKs / Nodes | `verify_root_ca_hmac()`, `ingest_agent_heartbeat()`, `recalculate_live_posture()`, `detect_certificate_tampering()`. Dynamically boosts posture scores upon valid telemetry. |
| **LLM Enrichment Engine** | OpenAI / Gemini API Compatible | Optional dynamic reasoning synthesis via JSON payload chat completions over `urllib.request`. |

---

## 🔐 3. Security, Cryptography & Compliance

| Security Domain | Standard / Algorithm | Implementation Details |
| :--- | :--- | :--- |
| **Digital License Signing** | **HMAC-SHA256 (64-char Hex)** | Custom Root-CA certificate format (`cnv1.<base64-payload>.<hmac-sha256>`). Tamper-proof, cryptographically signed software licenses. |
| **Password Hashing** | **PBKDF2-HMAC-SHA256** | 260,000 hash iterations paired with 16-byte cryptographically secure random hexadecimal salts (`secrets.token_hex(16)`). |
| **Two-Factor Authentication (2FA)** | **Zero-Trust 6-Digit OTP** | Cryptographically random challenge IDs and 6-digit codes (`secrets.randbelow()`) with a strict 300-second (5-minute) expiration window. |
| **Session Management** | **Bearer Tokens (8-Hour Expiry)** | Cryptographically secure URL-safe tokens (`secrets.token_urlsafe(24)`) with enforced expiration and automated cleanup. |
| **Compliance Mapping** | **NIST CSF 2.0 & ISO/IEC 27001** | Direct control mapping in product catalog and audit dossiers (`NIST DE.CM-1`, `PR.AT-1`, `PR.DS-01`, `ID.RA-01`, `ISO-27001 A.8.16`, `A.8.24`). |
| **AI Firewall & Guardrails** | **OWASP Top-10 LLM / AI RMF** | Pattern interceptor blocking prompt injections (`"ignore all previous instructions"`, `"reveal secrets"`, `"dump database"`) with HTTP `403 Forbidden`. |
| **HTTP Security Headers** | Middleware Enforcement | Enforces `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Permissions-Policy`. |

---

## 🗄️ 4. Database & Persistence Layer

| Technology | Purpose | Schema & Architecture |
| :--- | :--- | :--- |
| **SQLite 3** | Relational Database Engine | Embedded, zero-configuration database operating with `check_same_thread=False` and `Row` dictionary factories. |
| **Database Schema** | 10 Relational Tables | `users`, `sessions`, `pending_2fa`, `products`, `orders`, `licenses`, `chat_messages`, `security_logs`, `agent_executions`, `smtp_settings`, `email_outbox`. |
| **Serverless Ephemeral Storage** | Vercel `/tmp` Adapter | Dynamic path resolution detecting `VERCEL` environment variable to operate within `/tmp/cybernova_v4.db` with automated top-level self-initialization. |

---

## 📄 5. Automated PDF Document Generation

| Technology | Version / Module | Implementation |
| :--- | :--- | :--- |
| **ReportLab** | `>=4.2.0` | Professional PDF generation engine. |
| **ReportLab Platypus** | `SimpleDocTemplate`, `Table`, `Paragraph` | Formats dynamic Executive CISO Security Audit dossiers, threat likelihood tables, and posture score badges on standard Letter paper. |
| **ReportLab Lib Styles** | `getSampleStyleSheet`, `ParagraphStyle`, `colors` | Custom enterprise typography, color palettes (`#0f172a`, `#0369a1`), and formatted grid borders. |

---

## 📧 6. Real-Time Email Delivery & SMTP

| Technology | Protocol / Port | Purpose |
| :--- | :--- | :--- |
| **Python smtplib** | Standard Library | Native SMTP client supporting TLS / STARTTLS authentication over Port `587` and SSL over Port `465`. |
| **Python email.mime** | `MIMEMultipart`, `MIMEText`, `MIMEApplication` | Crafts responsive HTML alert templates, plain-text backups, and handles binary attachment of CISO PDF reports. |
| **Gmail SMTP Relay** | `smtp.gmail.com:587` | Real-time OTP dispatch directly to real Gmail inboxes using 16-character Google App Passwords. |
| **In-App Relay Fallback** | Automated Fallback | Provides simulated relay codes when live SMTP credentials are not yet saved, preventing authentication lockout. |

---

## 🎨 7. Frontend & UI Architecture

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Core Web Tech** | **HTML5 & Vanilla JavaScript (ES6+)** | Pure zero-dependency modern JavaScript using the native `fetch()` API and `localStorage` session synchronization. |
| **Styling & Theme** | **Modern CSS3 (Cyberpunk Dark)** | Custom design system using CSS variables: `--bg: #070d19`, `--panel: #0e172a`, `--cyan: #06b6d4`, `--emerald: #10b981`, `--rose: #f43f5e`, `--indigo: #6366f1`. |
| **User Dashboard** | `templates/dashboard_user.html` | Zero-Trust security score gauge, posture scanner, license ledger, marketplace with cart, and AI advisor chat. |
| **Consultant Desk** | `templates/dashboard_consultant.html` | Live agent execution feed, order risk inspection, security log text exporter, and multi-section SOC report generator. |
| **Admin SOC Command** | `templates/dashboard_admin.html` | High-level KPIs, HITL AI fraud triage queue (Approve/Block), user directory, revenue breakdown, and SMTP management. |
| **Main Portal & Store** | `templates/index.html` | Cyber store catalog, recommendation engine, real-time mail inspector, and multi-role login dialog. |

---

## ☁️ 8. DevOps, Containerization & Cloud Deployment

| System | Tooling / Configuration | Purpose |
| :--- | :--- | :--- |
| **Containerization** | **Docker (`python:3.11-slim`)** | Production container packaging with healthchecks querying `/healthz` and bytecode optimizations (`PYTHONDONTWRITEBYTECODE=1`). |
| **Orchestration** | **Docker Compose (`docker-compose.yml`)** | Single-command multi-container orchestration with port mappings (`8000:8000`) and automatic restart policies (`unless-stopped`). |
| **Build Optimization** | **`.dockerignore`** | Excludes `.git`, `.vercel`, local `.db` databases, and `__pycache__` from Docker build contexts. |
| **Cloud Hosting** | **Vercel Serverless Platform** | Deployed at `https://cybernova-solutions-v4.vercel.app` via `@vercel/python` serverless lambdas with bundled `templates/**`. |
| **Version Control** | **Git & GitHub** | Hosted at `https://github.com/hifza-kanwal-stack/cybernova_1`. |
