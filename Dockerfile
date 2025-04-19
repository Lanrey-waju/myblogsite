# Use a more slim base image
FROM python:3.12-slim-bookworm AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy requirements files
COPY requirements.txt requirements.dev.txt* ./

# Install Python dependencies
RUN pip install -r requirements.txt \
  && if [ -f requirements.dev.txt ]; then \
  pip install -r requirements.dev.txt; \
  fi

# Final stage
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Create user and directories
RUN useradd -m -s /bin/bash lanrey \
  && mkdir -p /vol/web/static \
  && mkdir -p /vol/web/media \
  && chown -R lanrey:lanrey /vol \
  && chmod -R 755 /vol

# Copy virtual environment and application files
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=lanrey:lanrey . .

# Expose port
EXPOSE 8000

# Switch to non-root user
USER lanrey

# Use entrypoint script
CMD ["/scripts/run.sh"]
