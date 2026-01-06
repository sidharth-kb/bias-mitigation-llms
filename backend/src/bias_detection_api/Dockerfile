FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source (but exclude private/ via .dockerignore)
COPY . .

EXPOSE 8080

# rest_api.py must expose `app`
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "rest_api:app"]
