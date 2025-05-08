########################  Stage 1 – builder  ##########################
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set uv configuration for better performance and Docker compatibility
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_SYSTEM_PYTHON=1

# Install build dependencies for confluent-kafka
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    librdkafka-dev \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application source
COPY services/candles/ .

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e .

# Create state directory with proper permissions
RUN mkdir -p /app/state && chmod -R 777 /app/state

########################  Stage 2 – runtime  ##########################
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install runtime dependencies for confluent-kafka
RUN apt-get update && apt-get install -y --no-install-recommends \
    librdkafka1 \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

# Copy application files
COPY --from=builder /app/ /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create and use non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Use exec form for ENTRYPOINT to avoid shell requirement
ENTRYPOINT ["python", "/app/src/candles/main.py"]
