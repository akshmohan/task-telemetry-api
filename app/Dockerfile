FROM python:3.11-slim

WORKDIR /app

# 1. Patch the OS vulnerabilities identified by Trivy
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# 2. Upgrade packaging tools to fix CVE-2026-24049 (wheel)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 3. Standard dependency install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy app code (Note: ensure your file structure matches)
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]