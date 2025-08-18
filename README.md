# 🌏 Indonesia Tourism Recommendation System - Captone Project DeployCamp

Backend service untuk **Tourism Recommendation System** berbasis **FastAPI** dengan dukungan **Machine Learning Model** untuk rekomendasi destinasi wisata di Indonesia.

[![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)
[![MLflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=flat&logo=numpy&logoColor=blue)](https://mlflow.org)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=Prometheus&logoColor=white)](https://prometheus.io)

## 👥 TEAM 13
- **Keizia Duma Caterina Purba (Machine Learning)**
- **Nanda Kurnia Agusmawati (DevOps)**

---

## 📌 Fitur Utama

### 🔧 Core Features
- ✅ **CRUD Destinasi Wisata** - Manajemen data destinasi untuk admin
- ✅ **Public API** - Akses daftar destinasi tanpa autentikasi
- ✅ **ML-Powered Recommendations** - Rekomendasi personal menggunakan machine learning
- ✅ **Health Monitoring** - Status checking untuk database dan storage
- ✅ **Real-time Monitoring** - Prometheus & Grafana integration
- ✅ **Experiment Tracking** - MLflow untuk model versioning

### 🎯 User Types
- **Public Users** - Melihat destinasi dan mendapatkan rekomendasi
- **Admin Users** - Mengelola data destinasi wisata

---

## ⚙️ Arsitektur Sistem

```mermaid
flowchart TD
    A[User / Frontend] -->|HTTP Request| B[FastAPI Backend]
    B -->|SQL Query| C[(PostgreSQL Database)]
    B -->|Store/Retrieve ML Assets| D[(MinIO Object Storage)]
    B -->|Model Prediction| E[ML Model Pipeline]
    
    E --> E1[model.pkl]
    E --> E2[scaler.pkl] 
    E --> E3[label_encoder.pkl]
    
    F[Prometheus] -->|Scrape Metrics| B
    G[Grafana Dashboard] -->|Query Metrics| F
    H[MLflow UI] -->|Track Experiments| D
    
    subgraph "ML Pipeline"
        E1
        E2
        E3
    end
    
    subgraph "Monitoring Stack"
        F
        G
    end
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | FastAPI | REST API server |
| **Package Manager** | uv | Python dependency management |
| **Database** | PostgreSQL | Data persistence |
| **Object Storage** | MinIO | ML artifacts storage |
| **Machine Learning** | scikit-learn | Model training & prediction |
| **Experiment Tracking** | MLflow | Model versioning & tracking |
| **Monitoring** | Prometheus + Grafana | System metrics & visualization |
| **Serialization** | Pickle | Model persistence |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose (untuk MinIO, Prometheus, Grafana)
- uv package manager

### 1. Installation

#### Install uv (jika belum ada)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Clone Repository
```bash
git clone https://github.com/nndakurnia/indonesia-tourism-recsys.git
cd indonesia-tourism-recsys
```

#### Setup Python Environment
```bash
# Install dependencies dengan uv
uv pip install -r requirements.txt

# Atau jika menggunakan pyproject.toml
uv pip install -e .
```

### 2. Environment Configuration

Buat file `.env` di root directory:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/tourism_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tourism_db
DB_USER=tourism_user
DB_PASSWORD=your_secure_password

# MinIO Configuration
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=ml-models
MINIO_SECURE=false

# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=tourism-recommendation

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Database Setup

```bash
# Buat database
createdb -h localhost -U postgres tourism_db

# Run migrations (jika menggunakan Alembic)
alembic upgrade head

# Atau manual setup
python scripts/init_db.py
```

### 4. Infrastructure Setup

```bash
# Start supporting services
docker-compose up -f infra/docker-compose-base.yml -d

# Verify services
docker-compose ps
```

### 5. ML Model Preparation

```bash
# Download atau train model
python scripts/prepare_models.py

# Upload model ke MinIO
python scripts/upload_models.py
```

### 6. Run Application

```bash
# Development mode
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UnicornWorker
```

---

## 📋 API Documentation

### Base URL
```
Development: http://localhost:8000
Production: http://103.150.98.118:3010/docs
```

## 🔗 API Endpoints

### 🏠 Health & Status

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-08-18T10:30:00Z",
  "services": {
    "database": "ok",
    "minio": "ok",
  }
}
```

### 🏝️ Destinations Management

#### Get All Destinations
```http
GET /destinations
```

**Query Parameters:**
- `limit` (int, optional): Jumlah data per halaman (default: 10)
- `offset` (int, optional): Offset untuk pagination (default: 0)
- `province` (string, optional): Filter berdasarkan provinsi
- `category` (string, optional): Filter berdasarkan kategori

**Request:**
```bash
curl "http://103.150.98.118:3010/api/destinations?limit=5&province=Bali"
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Pantai Kuta",
      "description": "Pantai terkenal di Bali dengan sunset yang menawan",
      "province": "Bali",
      "city": "Badung",
      "category": "Pantai",
      "rating": 4.5,
      "price_range": "Budget",
      "facilities": ["Parking", "Restaurant", "Toilet"],
      "latitude": -8.7184,
      "longitude": 115.1686,
      "created_at": "2024-08-18T10:30:00Z",
      "updated_at": "2024-08-18T10:30:00Z"
    }
  ],
  "total": 150,
  "limit": 5,
  "offset": 0
}
```

#### Get Destination by ID
```http
GET /destinations/{id}
```

**Request:**
```bash
curl "http://103.150.98.118:3010/api/destinations/1"
```

**Response:**
```json
{
  "id": 1,
  "name": "Pantai Kuta",
  "description": "Pantai terkenal di Bali dengan sunset yang menawan",
  "province": "Bali",
  "city": "Badung",
  "category": "Pantai",
  "rating": 4.5,
  "price_range": "Budget",
  "facilities": ["Parking", "Restaurant", "Toilet"],
  "latitude": -8.7184,
  "longitude": 115.1686,
  "images": [
    "https://example.com/kuta1.jpg",
    "https://example.com/kuta2.jpg"
  ],
  "created_at": "2024-08-18T10:30:00Z",
  "updated_at": "2024-08-18T10:30:00Z"
}
```

### 🤖 ML Recommendations

#### Get Recommendations
```http
POST /recommendations
```

**Request Body:**
```json
{
  "user_preferences": {
    "preferred_category": "Pantai",
    "budget": "Medium",
    "preferred_province": "Bali",
    "activity_type": "Relaxation",
    "group_size": "Family"
  },
  "limit": 5
}
```

**Request:**
```bash
curl -X POST "http://103.150.98.118:3010/api/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_preferences": {
      "preferred_category": "Pantai",
      "budget": "Medium",
      "preferred_province": "Bali",
      "activity_type": "Relaxation",
      "group_size": "Family"
    },
    "limit": 5
  }'
```

**Response:**
```json
{
  "recommendations": [
    {
      "destination": {
        "id": 1,
        "name": "Pantai Kuta",
        "province": "Bali",
        "category": "Pantai",
        "rating": 4.5,
        "price_range": "Budget"
      },
      "confidence_score": 0.87,
      "match_reasons": [
        "Category match: Pantai",
        "Location preference: Bali",
        "Family-friendly facilities"
      ]
    },
    {
      "destination": {
        "id": 15,
        "name": "Pantai Sanur",
        "province": "Bali",
        "category": "Pantai",
        "rating": 4.3,
        "price_range": "Medium"
      },
      "confidence_score": 0.82,
      "match_reasons": [
        "Category match: Pantai",
        "Budget alignment: Medium",
        "Calm environment for families"
      ]
    }
  ],
  "model_info": {
    "model_version": "v1.2.0",
    "prediction_time": "0.145s",
    "features_used": ["category", "budget", "province", "activity_type", "group_size"]
  }
}
```

#### Get Similar Destinations
```http
GET /destinations/{id}/similar
```

**Request:**
```bash
curl "http://localhost:8000/destinations/1/similar?limit=3"
```

**Response:**
```json
{
  "similar_destinations": [
    {
      "destination": {
        "id": 25,
        "name": "Pantai Jimbaran",
        "province": "Bali",
        "category": "Pantai"
      },
      "similarity_score": 0.94
    }
  ]
}
```

### 📊 Analytics & Metrics

#### Get Destinations Statistic
```http
GET /statistic
```

---

## 🏗️ Project Structure

```
indonesia-tourism-recsys/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── config.py          # Environment configuration
│   │   ├── database.py        # Database connection
│   │   └── security.py        # Authentication & authorization
│   ├── models/
│   │   ├── destination.py     # SQLAlchemy models
│   │   └── user.py
│   ├── schemas/
│   │   ├── destination.py     # Pydantic schemas
│   │   └── recommendation.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py    # API dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── destinations.py
│   │       ├── recommendations.py
│   │       └── health.py
│   ├── services/
│   │   ├── destination_service.py
│   │   ├── ml_service.py      # ML model integration
│   │   └── minio_service.py   # Object storage service
│   └── utils/
│       ├── logger.py
│       └── metrics.py         # Prometheus metrics
├── ml_models/
│   ├── model.pkl
│   ├── scaler.pkl
│   └── label_encoder.pkl
├── scripts/
│   ├── init_db.py
│   ├── prepare_models.py
│   └── upload_models.py
├── tests/
│   ├── __init__.py
│   ├── test_destinations.py
│   └── test_recommendations.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection URL | - | ✅ |
| `MINIO_ENDPOINT` | MinIO server endpoint | localhost:9000 | ✅ |
| `MINIO_ACCESS_KEY` | MinIO access key | minioadmin | ✅ |
| `MINIO_SECRET_KEY` | MinIO secret key | minioadmin | ✅ |
| `MLFLOW_TRACKING_URI` | MLflow tracking server | http://localhost:5000 | ✅ |
| `SECRET_KEY` | JWT secret key | - | ✅ |
| `DEBUG` | Debug mode | false | ❌ |


## 📊 Monitoring & Observability

### Prometheus Metrics
- HTTP request duration and count
- Database connection pool status
- ML model prediction time
- Memory and CPU usage

### Grafana Dashboards
1. **API Performance** - Request rates, response times, error rates
2. **System Resources** - CPU, memory, disk usage
3. **Business Metrics** - Popular destinations, recommendation accuracy

### MLflow Tracking
- Model experiments and versions
- Training metrics and parameters
- Model artifacts and dependencies

### Access URLs
- **API Documentation**: http://103.150.98.118:3010/docs
- **Grafana**: http://103.150.98.118:3000 (admin/admin)
- **Prometheus**: http://103.150.98.118:9090
- **MLflow UI**: http://103.150.98.118:5000
- **MinIO Console**: http://103.150.98.118:9001 (minioadmin/minioadmin)

---


## 🤝 Contributing

### Development Workflow
1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards
- Follow PEP 8 style guide
- Add type hints for all functions
- Write docstrings for all modules/functions
- Maintain test coverage >80%

### Pre-commit Hooks
```bash
# Install pre-commit
uv pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Keizia Purba** & **Nanda Kurnia**

---

**Made with ❤️ for DeployCamp Capstone Project**