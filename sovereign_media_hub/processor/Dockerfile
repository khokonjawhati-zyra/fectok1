FROM python:3.12-slim-bookworm

# Sovereign V15: Security Hardening Pulse
# Upgrading base packages to patch known vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements if any (processor engine uses standard libs mostly)
# For V15, we'll just install common needs
RUN pip install python-dotenv

COPY . .

# Environment sensing
ENV IS_DOCKER=True
ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "processor_engine.py"]
