# Multi-stage build for Pickup Soccer application
FROM eclipse-temurin:17-jdk-jammy AS base

# Install Python 3.11
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY *.py ./
COPY *.html ./
COPY start.sh ./

# Make startup script executable
RUN chmod +x start.sh

# Set environment variables
ENV JAVA_HOME=/opt/java/openjdk
ENV PYSPARK_PYTHON=python3.11
ENV PYSPARK_DRIVER_PYTHON=python3.11
ENV PYTHONUNBUFFERED=1

# Expose ports
EXPOSE 8000 8501

# Start API server with dynamic port support
CMD ["./start.sh"]
