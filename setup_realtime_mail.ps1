$ErrorActionPreference = "Stop"
Write-Host "=== CyberNova Solutions v4.0 — Real-Time Gmail 2FA Setup ===" -ForegroundColor Cyan
$email = Read-Host "Enter your real Gmail address (e.g. hifza@gmail.com)"
$appPass = Read-Host "Enter your 16-character Google App Password (without spaces)"
$appPassClean = $appPass -replace "\s+", ""

@"
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=$email
SMTP_PASS=$appPassClean
SMTP_FROM_NAME=CyberNova Autonomous SOC
"@ | Out-File -FilePath ".env" -Encoding utf8

Write-Host "Saved real-time Gmail SMTP settings to .env!" -ForegroundColor Green
Start-Process "http://127.0.0.1:8085"
python -m uvicorn main:app --host 127.0.0.1 --port 8085
