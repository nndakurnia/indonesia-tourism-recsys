from minio import Minio
from app.core.config import settings


def get_minio_client() -> Minio:
    """
    Create and return a MinIO client instance.
    """
    return Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False,  # kalau mau https, bisa buat env MINIO_SECURE
    )
