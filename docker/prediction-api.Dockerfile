#
# Chef stage
#
FROM lukemathwalker/cargo-chef:latest-rust-1 AS chef

WORKDIR /app/

# TODO: Not sure which of these are needed
RUN apt update && \
    apt install -y pkg-config libssl-dev lld clang libclang-dev && \
    rm -rf /var/lib/apt/lists/*

#
# Planner stage
#
FROM chef AS planner

COPY . .

RUN cargo chef prepare --recipe-path recipe.json

#
# Builder stage
#
FROM chef AS builder

COPY --from=planner /app/recipe.json recipe.json

RUN cargo chef cook --release --recipe-path recipe.json

COPY . .

RUN cargo build --release --bin prediction-api

#
# Runtime stage
#
FROM debian:bookworm-slim AS runtime
# FROM scratch AS runtime

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends openssl ca-certificates \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* 

COPY --from=builder /app/target/release/prediction-api /prediction-api

CMD ["/prediction-api"]
# CMD ["/bin/bash", "-c", "sleep 999999"]