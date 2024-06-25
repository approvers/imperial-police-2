# Copied from https://github.com/astral-sh/rye/discussions/239#discussioncomment-6033855 and modified
FROM python:3.12.3 AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH="/workspace/src:$PYTHONPATH"

# The virtual environment is created in the working directory where rye is run
# so the development and production environments must be in the same directory respectively.
WORKDIR /workspace

RUN \
  --mount=type=cache,target=/var/lib/apt/lists \
  --mount=type=cache,target=/var/cache/apt/archives \
  apt-get update \
  && apt-get install -y --no-install-recommends build-essential

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

# RYE_INSTALL_OPTION is required to build.
# See: https://github.com/mitsuhiko/rye/issues/246
RUN curl -sSf https://rye.astral.sh/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a bind mount to some files to avoid having to copy them into
# into this layer.
COPY pyproject.toml pyproject.toml
COPY requirements.lock requirements.lock
COPY .python-version .python-version
COPY README.md README.md

# Use a cache mount for the rye cache to improve build performance.
RUN --mount=type=cache,target=/root/.cache/rye rye sync --no-dev --no-lock

RUN . .venv/bin/activate

# Stage for development.
# The development environment assumes a devcontainer and the environment is
# closed inside the container, so you don't need to be aware of the virtual environment
FROM base AS dev

# Re-copy only if necessary to optimize caching
COPY pyproject.toml pyproject.toml
COPY requirements.lock requirements.lock
COPY requirements-dev.lock requirements-dev.lock

# Check if dependencies have changed to decide whether to re-run rye sync
RUN \
    if cmp -s requirements.lock requirements.lock.new; then \
        echo "Dependencies have not changed, using cache."; \
    else \
        echo "Dependencies have changed, running rye sync."; \
        cp requirements.lock requirements.lock.new; \
        rye sync --no-lock; \
    fi

# Stage for production
FROM base AS run

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to the non-privileged user to run the application.
USER appuser
