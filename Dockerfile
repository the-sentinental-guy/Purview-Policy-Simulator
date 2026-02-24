# ============================================================
# Stage 1: build – install dependencies into a virtual env
# ============================================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build tools
RUN pip install --upgrade pip

# Copy only dependency manifests first (layer caching)
COPY requirements.txt .

# Create a virtual environment and install runtime deps
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ============================================================
# Stage 2: runtime – minimal production image
# ============================================================
FROM python:3.12-slim AS runtime

# Security: run as a non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --no-create-home appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application source
COPY app/ ./app/
COPY run.py .

# Ensure the venv binaries are on PATH
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Application defaults (can be overridden at runtime)
    PORT=8000 \
    CORS_ORIGINS="*"

# Switch to unprivileged user
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

CMD ["python", "-m", "uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "*"]
