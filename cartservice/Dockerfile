FROM python:3.10-slim

# Good defaults for containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Run as non-root (security best practice)
RUN useradd -m appuser
USER appuser

# Expose service port (change per service)
# user-service: 5001, product-service: 5002, cart-service: 5003, payment-service: 5004
EXPOSE 5003

CMD ["python", "app.py"]
