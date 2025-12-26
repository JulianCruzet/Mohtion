FROM python:3.12-slim

WORKDIR /app

# Install git (needed for GitPython)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml .
COPY README.md .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY mohtion/ mohtion/

# Default command (can be overridden in docker-compose)
CMD ["uvicorn", "mohtion.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
