import os
import smtplib
import sqlite3
from datetime import datetime, timezone
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_local_env():
    env_path = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and v:
                os.environ[k] = v


load_local_env()


def get_smtp_config(conn: Optional[sqlite3.Connection] = None):
    # Check environment variables first
    env_user = os.environ.get("SMTP_USER", "").strip()
    env_pass = os.environ.get("SMTP_PASS", "").replace(" ", "").strip()
    env_host = os.environ.get("SMTP_HOST", "smtp.gmail.com").strip()
    env_port = int(os.environ.get("SMTP_PORT", "587"))
    env_name = os.environ.get("SMTP_FROM_NAME", "CyberNova Autonomous SOC").strip()

    if env_user and env_pass:
        return {
            "host": env_host,
            "port": env_port,
            "user": env_user,
            "pass": env_pass,
            "sender_name": env_name,
            "configured": True,
        }

    # Fallback to database settings if user configured in UI
    if conn:
        try:
            row = conn.execute(
                "SELECT smtp_host, smtp_port, smtp_user, smtp_pass, sender_name FROM smtp_settings WHERE id = 1"
            ).fetchone()
            if row and row["smtp_user"] and row["smtp_pass"]:
                return {
                    "host": row["smtp_host"] or env_host,
                    "port": int(row["smtp_port"] or env_port),
                    "user": row["smtp_user"].strip(),
                    "pass": row["smtp_pass"].replace(" ", "").strip(),
                    "sender_name": row["sender_name"] or env_name,
                    "configured": True,
                }
        except Exception:
            pass

    return {
        "host": env_host,
        "port": env_port,
        "user": env_user,
        "pass": "",
        "sender_name": env_name,
        "configured": False,
    }


def dispatch_realtime_email(
    conn: sqlite3.Connection,
    to_email: str,
    subject: str,
    html_body: str,
    text_body: str,
    category: str = "SECURITY_ALERT",
    pdf_bytes: bytes = None,
    pdf_filename: str = "CyberNova_CISO_Audit.pdf",
):
    cfg = get_smtp_config(conn)
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    delivery_mode = "REALTIME_SMTP_SENT"
    error_detail = ""

    if cfg["configured"]:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{cfg['sender_name']} <{cfg['user']}>"
            msg["To"] = to_email

            msg.attach(MIMEText(text_body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            if pdf_bytes:
                part = MIMEApplication(pdf_bytes, Name=pdf_filename)
                part["Content-Disposition"] = f'attachment; filename="{pdf_filename}"'
                msg.attach(part)

            if cfg["port"] == 465:
                server = smtplib.SMTP_SSL(cfg["host"], cfg["port"], timeout=12)
            else:
                server = smtplib.SMTP(cfg["host"], cfg["port"], timeout=12)
                server.ehlo()
                server.starttls()

            with server:
                server.ehlo()
                server.login(cfg["user"], cfg["pass"])
                server.sendmail(cfg["user"], [to_email], msg.as_string())
        except Exception as exc:
            delivery_mode = "SMTP_AUTH_OR_NETWORK_ERROR"
            error_detail = str(exc)[:220]
    else:
        delivery_mode = "LIVE_MAIL_RELAY_QUEUED"

    conn.execute(
        """
        INSERT INTO email_outbox (recipient, subject, text_preview, category, delivery_mode, error_detail, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (to_email, subject, text_body[:400], category, delivery_mode, error_detail, now_iso),
    )
    conn.commit()
    return {
        "recipient": to_email,
        "subject": subject,
        "delivery_mode": delivery_mode,
        "smtp_live": cfg["configured"] and delivery_mode == "REALTIME_SMTP_SENT",
        "error": error_detail,
        "timestamp": now_iso,
    }
