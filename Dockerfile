FROM python:3.11-slim

LABEL maintainer="CyberNova Solutions <security@cybernova.io>" \
      version="4.0.0" \
      description="Autonomous Multi-Agent Cybersecurity Store & Real-Time SOC"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CYBERNOVA_ROOT_CA_SECRET=CyberNova-FDE-RootCA-2026-SecretKey \
    ALLOWED_ORIGINS=*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
