# nourrir_flask/Dockerfile

FROM python:3.11-slim

# Fix encoding issues and install dependencies
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy dependencies first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Port 8080 exposed
EXPOSE 8080

# Use Gunicorn for production (adjust workers as needed)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
