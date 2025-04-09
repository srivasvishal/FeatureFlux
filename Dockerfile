FROM python:3.9-slim

WORKDIR /app
ENV PYTHONPATH=/app/src

# Install system dependencies needed for building packages (e.g., for PySpark, etc.)
#RUN apt-get update && apt-get install -y build-essential openjdk-17-jre-headless
RUN apt-get update && apt-get install -y build-essential default-jre-headless

# Copy requirements file and install Python dependencies
COPY pyproject.toml setup.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into /app
COPY . .

# Debug: list all files (optional, remove in production)
RUN ls -R /app

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Run the FastAPI server (using uvicorn) from the service package
CMD ["uvicorn", "service.server:app", "--host", "0.0.0.0", "--port", "8000"]