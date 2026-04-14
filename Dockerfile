FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /workspace

# Install the uv package manager
RUN pip install uv

# Copy ONLY the dependency files first to leverage Docker caching
COPY pyproject.toml uv.lock ./

# Sync dependencies (This creates the .venv inside the container)
RUN uv sync --frozen

# Note: We do not COPY the source code here because docker-compose 
# will mount it dynamically via volumes.