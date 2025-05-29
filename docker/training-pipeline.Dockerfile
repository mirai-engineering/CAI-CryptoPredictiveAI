########################  Stage 1 – builder  ##########################
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set uv configuration for better performance and Docker compatibility
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_SYSTEM_PYTHON=1

# Install build dependencies for confluent-kafka and data science libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    librdkafka-dev \
    libssl-dev \
    pkg-config \
    git \ 
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy predictor service source (pyproject.toml, uv.lock, source code, etc.)
COPY services/predictor/ .

# Install dependencies using uv (respects pyproject.toml + uv.lock)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e . 

# Create writable directory (if needed by code)
RUN mkdir -p /app/state && chmod -R 777 /app/state

########################  Stage 2 – runtime  ##########################
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install runtime dependencies (minimal required libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    librdkafka1 \
    libssl3 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

# Copy the app source itself
COPY --from=builder /app/ /app/

# Set envs
ENV PYTHONUNBUFFERED=1

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set the predictor entrypoint
ENTRYPOINT ["python", "/app/src/predictor/train.py"]
