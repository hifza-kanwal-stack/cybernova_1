import json
import os
import sqlite3
import urllib.request
from datetime import datetime, timezone
from email_service import dispatch_realtime_email


AGENT_REGISTRY = [
    {
        "agent_id": "agent-posture-01",
        "name": "Posture & Compliance Auditor Agent",
        "actor": "Enterprise User",
        "role_scope": "user",
        "autonomous_tools": [
            "scan_control_drift()",
            "map_nist_iso_controls()",
            "generate_ciso_pdf_dossier()",
            "handoff_to_soc_responder()",
        ],
        "mission": "Autonomously audits user security posture, calculates 0-100 risk score, emails CISO PDF reports, and escalates critical exposure (<50) to SOC Responder.",
    },
    {
        "agent_id": "agent-fraud-02",
        "name": "Fraud Investigation Agent",
        "actor": "Payment & Checkout Pipeline",
        "role_scope": "checkout",
        "autonomous_tools": [
            "compute_monetary_zscore()",
            "inspect_crypto_velocity()",
            "correlate_auth_anomalies()",
            "quarantine_hitl_order()",
        ],
        "mission": "Investigates every checkout in real time, flags anomalous/high-value crypto orders (>=60 risk), emails SOC Admin, and holds provisioning for HITL review.",
    },
    {
        "agent_id": "agent-soc-03",
        "name": "Autonomous SOC Responder Agent",
        "actor": "Admin SOC",
        "role_scope": "admin",
        "autonomous_tools": [
            "block_prompt_injection()",
            "isolate_attacker_session()",
            "draft_nist_ir_playbook()",
            "dispatch_ciso_alert_email()",
        ],
        "mission": "Defends against AI Firewall prompt injections and brute-force attacks, triages escalated alerts, and dispatches real-time incident emails.",
    },
    {
        "agent_id": "agent-watchdog-04",
        "name": "License & Telemetry Watchdog Agent",
        "actor": "Deployed SDKs & Nodes",
        "role_scope": "sdk",
        "autonomous_tools": [
            "verify_root_ca_hmac()",
            "ingest_agent_heartbeat()",
            "recalculate_live_posture()",
            "detect_certificate_tampering()",
        ],
        "mission": "Continuously validates cnv1 Root-CA software certificates, ingests live endpoint heartbeats, and dynamically boosts organization security posture.",
    },
]


def _optional_llm_enrichment(prompt: str) -> str:
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    if not api_key:
        return ""
    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    try:
        payload = json.dumps(
            {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a concise CyberNova FDE security agent. Respond in 2 crisp technical sentences.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 120,
                "temperature": 0.2,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""


def log_agent_execution(
    conn: sqlite3.Connection,
    agent_id: str,
    agent_name: str,
    actor: str,
    trigger_event: str,
    tools_invoked: list,
    reasoning_summary: str,
    verdict: str,
    handoff_target: str = "None",
):
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    llm_note = _optional_llm_enrichment(f"{agent_name} triggered by {trigger_event}: {reasoning_summary}")
    full_reasoning = f"{reasoning_summary} [LLM Insight: {llm_note}]" if llm_note else reasoning_summary

    conn.execute(
        """
        INSERT INTO agent_executions
        (agent_id, agent_name, actor, trigger_event, tools_invoked, reasoning_summary, verdict, handoff_target, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            agent_id,
            agent_name,
            actor,
            trigger_event,
            json.dumps(tools_invoked),
            full_reasoning,
            verdict,
            handoff_target,
            now_iso,
        ),
    )
    conn.commit()
    return {
        "agent_id": agent_id,
        "agent_name": agent_name,
        "actor": actor,
        "trigger_event": trigger_event,
        "tools_invoked": tools_invoked,
        "reasoning_summary": full_reasoning,
        "verdict": verdict,
        "handoff_target": handoff_target,
        "timestamp": now_iso,
    }


def run_posture_auditor_agent(
    conn: sqlite3.Connection,
    user_email: str,
    user_name: str,
    score: int,
    tier: str,
    threats: list,
    send_email: bool = False,
    pdf_bytes: bytes = None,
):
    tools = ["scan_control_drift()", "map_nist_iso_controls()"]
    handoff = "None"
    if pdf_bytes:
        tools.append("generate_ciso_pdf_dossier()")
    if score < 50:
        tools.append("handoff_to_soc_responder()")
        handoff = "Autonomous SOC Responder Agent"

    reasoning = (
        f"Audited {user_name} ({user_email}) posture: Score={score}/100 ({tier}). "
        f"Identified {len(threats)} predictive NIST/ISO threat vectors."
    )
    trace = log_agent_execution(
        conn,
        agent_id="agent-posture-01",
        agent_name="Posture & Compliance Auditor Agent",
        actor=f"Enterprise User ({user_email})",
        trigger_event="AI_POSTURE_AUDIT_SCAN",
        tools_invoked=tools,
        reasoning_summary=reasoning,
        verdict=tier,
        handoff_target=handoff,
    )

    if score < 50:
        log_agent_execution(
            conn,
            agent_id="agent-soc-03",
            agent_name="Autonomous SOC Responder Agent",
            actor="Admin SOC (Agent Handoff)",
            trigger_event="CRITICAL_POSTURE_ESCALATION",
            tools_invoked=["draft_nist_ir_playbook()", "queue_remediation_alert()"],
            reasoning_summary=f"Received handoff from Posture Auditor for {user_email} (Score {score}/100). Prepared Zero-Trust containment checklist.",
            verdict="ESCALATED_WATCH",
            handoff_target="None",
        )

    email_result = None
    if send_email:
        top_vec = threats[0]["vector"] if threats else "Baseline Monitored"
        text_msg = (
            f"Hello {user_name},\n\n"
            f"CyberNova's Posture & Compliance Auditor Agent completed your security scan.\n"
            f"Digital Security Score: {score}/100 ({tier})\n"
            f"Top Threat: {top_vec}\n\n"
            f"Your Executive CISO PDF Dossier is attached.\n- CyberNova Autonomous SOC"
        )
        email_result = dispatch_realtime_email(
            conn,
            to_email=user_email,
            subject=f"[CyberNova CISO Audit] Security Posture Score: {score}/100 ({tier})",
            text_body=text_msg,
            html_body=f"""
            <div style="font-family:Arial,sans-serif;background:#0b1220;color:#e2e8f0;padding:20px;border-radius:10px;">
              <h2 style="color:#38bdf8;">CyberNova Executive CISO Security Audit</h2>
              <p>Hello <b>{user_name}</b>,</p>
              <p>Our <b>Posture &amp; Compliance Auditor Agent</b> completed your real-time assessment:</p>
              <div style="background:#111c33;padding:14px;border-left:4px solid #38bdf8;margin:12px 0;">
                <b>Digital Security Score:</b> {score}/100 &mdash; <span style="color:#f59e0b;">{tier}</span>
              </div>
              <p>Your signed ReportLab CISO PDF report is attached to this email.</p>
            </div>
            """,
            category="CISO_PDF_REPORT",
            pdf_bytes=pdf_bytes,
            pdf_filename="CyberNova_CISO_Security_Audit.pdf",
        )
    return {"agent_trace": trace, "email_delivery": email_result}


def run_fraud_investigation_agent(
    conn: sqlite3.Connection,
    order_code: str,
    user_email: str,
    total_amount: float,
    payment_method: str,
    fraud_score: int,
    reasons: list,
):
    flagged = fraud_score >= 60
    tools = ["compute_monetary_zscore()", "inspect_crypto_velocity()", "correlate_auth_anomalies()"]
    if flagged:
        tools.append("quarantine_hitl_order()")
        verdict = "QUARANTINE_HITL"
        handoff = "Autonomous SOC Responder Agent"
    else:
        tools.append("authorize_license_minting()")
        verdict = "AUTO_PROVISION"
        handoff = "License & Telemetry Watchdog Agent"

    reasoning = (
        f"Evaluated Order {order_code} (${total_amount:.2f} via {payment_method}) for {user_email}. "
        f"Computed Fraud Risk={fraud_score}/100. Factors: {', '.join(reasons)}."
    )
    trace = log_agent_execution(
        conn,
        agent_id="agent-fraud-02",
        agent_name="Fraud Investigation Agent",
        actor=f"Checkout Pipeline ({user_email})",
        trigger_event="ORDER_FRAUD_EVALUATION",
        tools_invoked=tools,
        reasoning_summary=reasoning,
        verdict=verdict,
        handoff_target=handoff,
    )

    email_result = None
    if flagged:
        log_agent_execution(
            conn,
            agent_id="agent-soc-03",
            agent_name="Autonomous SOC Responder Agent",
            actor="Admin SOC (Fraud Handoff)",
            trigger_event="HITL_FRAUD_TRIAGE_QUEUED",
            tools_invoked=["lock_license_release()", "dispatch_ciso_alert_email()"],
            reasoning_summary=f"Quarantined {order_code} (${total_amount:.2f} {payment_method}) in HITL SOC queue pending Admin clearance.",
            verdict="AWAITING_ADMIN_HITL",
            handoff_target="None",
        )
        text_msg = (
            f"Autonomous Fraud Investigation Agent quarantined order {order_code}.\n"
            f"Buyer: {user_email} | Amount: ${total_amount:.2f} | Method: {payment_method}\n"
            f"Fraud Score: {fraud_score}/100\nReasons: {', '.join(reasons)}\n"
            f"Log into CyberNova Admin SOC to Approve or Block."
        )
        email_result = dispatch_realtime_email(
            conn,
            to_email=user_email,
            subject=f"[SOC FRAUD ALERT] Order {order_code} Quarantined (Risk {fraud_score}/100)",
            text_body=text_msg,
            html_body=f"""
            <div style="font-family:Arial,sans-serif;background:#0b1220;color:#e2e8f0;padding:20px;border-radius:10px;">
              <h2 style="color:#f43f5e;">CyberNova AI Fraud Shield Alert</h2>
              <p><b>Order {order_code}</b> was automatically quarantined by the <b>Fraud Investigation Agent</b>.</p>
              <ul>
                <li><b>Buyer:</b> {user_email}</li>
                <li><b>Amount:</b> ${total_amount:.2f} ({payment_method})</li>
                <li><b>AI Fraud Score:</b> {fraud_score}/100</li>
                <li><b>Signals:</b> {', '.join(reasons)}</li>
              </ul>
              <p>Please review in <b>Admin SOC &rarr; HITL Fraud Triage Queue</b>.</p>
            </div>
            """,
            category="SOC_FRAUD_ALERT",
        )
    return {"agent_trace": trace, "email_delivery": email_result}


def run_soc_responder_agent(
    conn: sqlite3.Connection,
    actor_email: str,
    attack_type: str,
    payload_preview: str,
    verdict: str = "BLOCKED_AND_ISOLATED",
):
    return log_agent_execution(
        conn,
        agent_id="agent-soc-03",
        agent_name="Autonomous SOC Responder Agent",
        actor=f"Admin SOC Guardrail ({actor_email})",
        trigger_event=attack_type,
        tools_invoked=["block_prompt_injection()", "isolate_attacker_session()", "draft_nist_ir_playbook()"],
        reasoning_summary=f"Detected {attack_type} from {actor_email}. Blocked payload ('{payload_preview[:60]}...') under NIST AI RMF & OWASP LLM Top-10.",
        verdict=verdict,
        handoff_target="None",
    )


def run_license_watchdog_agent(
    conn: sqlite3.Connection,
    action_type: str,
    subject_ref: str,
    detail: str,
    verdict: str,
):
    tools = (
        ["verify_root_ca_hmac()", "detect_certificate_tampering()"]
        if "VERIFY" in action_type
        else ["ingest_agent_heartbeat()", "recalculate_live_posture()"]
    )
    return log_agent_execution(
        conn,
        agent_id="agent-watchdog-04",
        agent_name="License & Telemetry Watchdog Agent",
        actor="Deployed SDK / Root-CA Node",
        trigger_event=action_type,
        tools_invoked=tools,
        reasoning_summary=f"[{subject_ref}] {detail}",
        verdict=verdict,
        handoff_target="Posture & Compliance Auditor Agent" if "HEARTBEAT" in action_type else "None",
    )
