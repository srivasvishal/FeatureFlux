FROM python:3.9-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything into /app
COPY . .

# Debug: list all files
RUN ls -R /app

EXPOSE 8000
CMD ["uvicorn", "src.service.server:app", "--host", "0.0.0.0", "--port", "8000"]