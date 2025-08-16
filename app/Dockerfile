# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- Set working directory ----------
WORKDIR /app

# ---------- Install system dependencies ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---------- Copy requirements ----------
COPY requirements.txt .

# ---------- Install Python dependencies ----------
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy app ----------
COPY ./app ./app
COPY ./app/ml ./app/ml

# ---------- Expose port ----------
EXPOSE 8000

# ---------- Command ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
