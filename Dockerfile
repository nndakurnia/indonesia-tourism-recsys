# Gunakan base image Python versi ringan
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements.txt terlebih dahulu untuk memanfaatkan cache
COPY requirements.txt .

# Install dependencies tanpa cache agar image lebih kecil
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file project ke container
COPY . .

# Expose port untuk API
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
