# Simple Docker build for MCP server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create pytest cache directory with proper permissions
RUN mkdir -p /app/.pytest_cache && chown -R appuser:appuser /app/.pytest_cache

# Security: run as non-root user
USER appuser

# Expose port
EXPOSE 7860

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860')" || exit 1

# Run the application with proper signal handling
CMD ["python", "-u", "app.py"]