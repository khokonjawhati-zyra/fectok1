FROM python:3.11-slim-bookworm
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    httpx \
    pydantic \
    python-dotenv \
    websockets \
    google-auth \
    google-api-python-client \
    google-auth-oauthlib \
    google-auth-httplib2 \
    python-multipart \
    requests

# Copy local code
COPY . .

# Sovereign V15: Expose Backend Pulse
EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
