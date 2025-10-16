FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Use gunicorn for production (same as Replit)
CMD gunicorn --worker-class gthread --workers 1 --threads 2 --timeout 120 --bind 0.0.0.0:$PORT run:app
