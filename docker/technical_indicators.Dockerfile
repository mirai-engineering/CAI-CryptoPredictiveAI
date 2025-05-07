# Stage 1: Builder - using an image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install ta-lib
ENV TALIB_DIR=/usr/local
RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz && \
    tar -xzf ta-lib-0.6.4-src.tar.gz && \
    cd ta-lib-0.6.4/ && \
    ./configure --prefix=$TALIB_DIR && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf ta-lib-0.6.4-src.tar.gz ta-lib-0.6.4/

# Ensure TA-Lib is linked correctly
RUN ldconfig

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation and set link mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Set service name as build argument
ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

# Copy project configuration files
COPY pyproject.toml uv.lock ./

# Copy only the required services directories 
COPY services/${SERVICE_NAME} /app/services/${SERVICE_NAME}


# Install build tools if needed for any compile steps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv && \
    # Skip installing main project (which would install all services)
    # Instead, only install the specific service and its direct dependencies
    uv pip install -e ./services/${SERVICE_NAME}

# Stage 2: Runtime image - minimal size
FROM python:3.12-slim

# Install only essential runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

WORKDIR /app

# Set SERVICE_NAME again for the runtime stage
# Set service name as build argument
ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}
ENV PYTHONUNBUFFERED=1

# Copy only the virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy only the required service from builder
COPY --from=builder /app/services/${SERVICE_NAME} /app/services/${SERVICE_NAME}

# Create state directory with appropriate permissions
# This provides a fallback if no volume is mounted
RUN mkdir -p /app/state && chown -R appuser:appuser /app/state

# Set up environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Switch to non-root user
USER appuser

# Run the service directly
CMD ["sh", "-c", "python /app/services/${SERVICE_NAME}/src/${SERVICE_NAME}/main.py"]