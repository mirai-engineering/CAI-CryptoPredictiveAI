########################  Stage 1 – builder  ##########################
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set uv configuration for better performance and Docker compatibility
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_SYSTEM_PYTHON=1

# Install build dependencies for confluent-kafka and ta-lib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    librdkafka-dev \
    libssl-dev \
    pkg-config \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install ta-lib - optimize by combining commands to reduce layers
ENV TALIB_DIR=/usr/local
RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz && \
    tar -xzf ta-lib-0.6.4-src.tar.gz && \
    cd ta-lib-0.6.4/ && \
    ./configure --prefix=$TALIB_DIR && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf ta-lib-0.6.4-src.tar.gz ta-lib-0.6.4/ && \
    ldconfig

# Set the working directory
WORKDIR /app

# Copy the application source
COPY services/technical_indicators/ .

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e .

########################  Stage 2 – runtime  ##########################
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy ALL from /usr/local for proper library linkage
COPY --from=builder /usr/local/ /usr/local/

# Run ldconfig to update the shared library cache
RUN ldconfig

# Install runtime dependencies with minimal layer size
RUN apt-get update && apt-get install -y --no-install-recommends \
    librdkafka1 \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY services/technical_indicators/ /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create and use non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Use exec form for ENTRYPOINT to avoid shell requirement
ENTRYPOINT ["python", "/app/src/technical_indicators/main.py"]
