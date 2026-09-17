FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    PROJECT_ID=ai-cartridge \
    PROJECT_NUM=850196904392 \
    ENGINE_ID=aigents \
    AGENT_ID=finance_research

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application assets
COPY index.html server.py ./
COPY tests/ ./tests/
COPY agent_registry/ ./agent_registry/
COPY docs/ ./docs/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/api/status || exit 1

CMD ["python3", "server.py"]
