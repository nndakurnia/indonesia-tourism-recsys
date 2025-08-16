from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # -----------------------
    # App
    # -----------------------
    project_name: str = "Tourism Recommendation System"
    version: str = "1.0.0"
    description: str = "Description"
    debug: bool = True

    # -----------------------
    # Database
    # -----------------------
    database_url: str

    # -----------------------
    # MinIO
    # -----------------------
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str = "ml-models"

    # -----------------------
    # MLflow
    # -----------------------
    mlflow_tracking_uri: str  # URL MLflow server
    mlflow_run_id: str        # run_id dari MLflow
    mlflow_artifact_path: str # nama folder/artifact saat log_model, misal "model"

    # -----------------------
    # ML Files
    # -----------------------
    ml_folder: str = str(BASE_DIR / "ml")
    model_file: str = "model.pkl"
    encoder_file: str = "label_encoders.pkl"
    scaler_file: str = "scaler.pkl"
    feature_names_file: str = "feature_names.json"

    # -----------------------
    # Model Paths
    # -----------------------
    recsys_model_path: str
    recsys_scaler_path: str
    recsys_encoder_path: str

    # -----------------------
    # CORS
    # -----------------------
    frontend_url: str = "*"  # Example for Vite/React

    # -----------------------
    # Config
    # -----------------------
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
