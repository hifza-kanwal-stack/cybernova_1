# CyberNova Solutions — Complete Production Deployment Guide

**Document Version:** 1.0 (Production Verified)  
**Target Environments:** Vercel Serverless Edge, Docker Containers, Bare-Metal / On-Premise  
**Live Endpoint:** [https://cybernova-solutions-v4.vercel.app](https://cybernova-solutions-v4.vercel.app)  
**GitHub Repository:** [https://github.com/hifza-kanwal-stack/cybernova_1](https://github.com/hifza-kanwal-stack/cybernova_1)  
**Health Check Probe:** `/healthz`  

---

## 1. Executive Deployment Overview

CyberNova Solutions is architected for **zero-dependency portability** across both self-hosted container infrastructure and cloud-native serverless runtimes. The backend runs on an asynchronous Python ASGI engine (FastAPI + Uvicorn) with zero heavy JavaScript client-side build steps.

| Deployment Target | Primary Technology | Recommended Use Case |
| :--- | :--- | :--- |
| **Vercel Serverless Cloud** | `@vercel/python` + `/tmp` SQLite | Cloud-native production, global CDN edge, zero maintenance. |
| **Docker Containerization** | `python:3.11-slim` + Docker Compose | Air-gapped on-premise, AWS ECS/EKS, Kubernetes, or sovereign cloud. |
| **Local Bare-Metal** | Python 3.11 Virtual Environment | Development, debugging, security audits, and local demonstration. |

---

## 2. Environment Variables & Secret Configuration

Create a `.env` file in the root directory (or configure these in your Vercel Dashboard / Docker environment):

```bash
# -------------------------------------------------------------
# REQUIRED: Root-CA Cryptographic Secret Key
# Used to mint and verify 64-character HMAC-SHA256 digital licenses
# -------------------------------------------------------------
CYBERNOVA_ROOT_CA_SECRET="cnv-root-ca-sec-key-0x88921f00a98b7762e541-super-secret-hex"

# -------------------------------------------------------------
# OPTIONAL: Production CORS Origins (Comma-separated)
# In development, leave blank or "*" to allow localhost testing
# -------------------------------------------------------------
ALLOWED_ORIGINS="https://cybernova-solutions-v4.vercel.app,http://localhost:8000,http://127.0.0.1:8000"

# -------------------------------------------------------------
# OPTIONAL: Live Gmail SMTP Relay Configuration
# Enables real-time 2FA OTP delivery directly to user inboxes
# (If unconfigured, the built-in in-app mail viewer acts as zero-lockout fallback)
# -------------------------------------------------------------
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-organization-email@gmail.com"
SMTP_PASS="abcd efgh ijkl mnop"   # 16-character Google App Password
SMTP_FROM="your-organization-email@gmail.com"
```

---

## 3. Target 1: Vercel Serverless Deployment (Live Production)

CyberNova Solutions is pre-configured with a specialized [`vercel.json`](file:///c:/Users/Hifza%20Kanwal/Desktop/gene%20cybernova/cybernova-solutions-v4/vercel.json) configuration:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python",
      "config": {
        "includeFiles": ["templates/**"]
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

### Vercel Deployment Steps:
1. **Automated Git Push:** Every commit pushed to `main` on [hifza-kanwal-stack/cybernova_1](https://github.com/hifza-kanwal-stack/cybernova_1) automatically triggers a Vercel build if linked.
2. **Manual Vercel CLI Deployment:**
   ```bash
   vercel --prod
   ```
3. **Serverless Ephemeral Storage Handling:**
   - In Vercel serverless environments, the filesystem is read-only except for `/tmp`.
   - `main.py` detects `os.environ.get("VERCEL")` and dynamically binds SQLite to `/tmp/cybernova_v4.db`.
   - Top-level module execution initializes the database schema automatically upon cold starts.

---

## 4. Target 2: Docker & Docker Compose Containerization

### Dockerfile Specification
```dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1
CMD ["python", "main.py"]
```

### Single-Command Launch with Docker Compose
```bash
# 1. Build and start the container in detached mode
docker-compose up --build -d

# 2. View real-time container logs
docker-compose logs -f

# 3. Verify health status
docker ps
```
The application will be accessible at `http://localhost:8000`.

---

## 5. Target 3: Local Bare-Metal Setup

```powershell
# 1. Clone repository
git clone https://github.com/hifza-kanwal-stack/cybernova_1.git
cd cybernova_1

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start server
python main.py
# (Or using uvicorn directly: uvicorn main:app --port 8000)
```

---

## 6. Pre-Flight Verification & Health Check Checklist

Execute the following automated health checks to verify complete platform integrity:

| Verification Step | Command / Endpoint | Expected Response |
| :--- | :--- | :--- |
| **Service Health Probe** | `GET /healthz` | `{"status":"healthy","service":"cybernova-solutions-v4","agents_active":4}` |
| **System Bootstrap** | `GET /api/bootstrap` | Returns seeded product catalog, system status, and active user list. |
| **2FA Challenge Check** | `POST /api/auth/login` | Returns `{"challenge_id":"...","status":"2FA_REQUIRED"}` (No OTP leakage). |
| **Prompt Injection WAF** | Test injection query | Returns HTTP `403 Forbidden` with defense explanation. |
| **CISO PDF Generation** | `GET /api/audit/report/pdf` | Returns binary `application/pdf` stream with Letter formatting. |

---

## 7. Pre-Seeded Demonstration Credentials

| Role | Email | Password | Dedicated Workstation |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin@cybernova.io` | `Admin@123` | `/dashboard/admin` |
| **SOC Consultant** | `consultant@cybernova.io` | `Consult@123` | `/dashboard/consultant` |
| **Enterprise User** | `hifza@cybernova.io` | `Cyber@123` | `/dashboard/user` |

---
