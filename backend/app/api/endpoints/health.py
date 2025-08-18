from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.client import get_minio_client
from app.core.config import settings

router = APIRouter()


def check_postgres(db: Session):
    try:
        db.execute(text("SELECT 1"))
        return "ok"
    except Exception as e:
        return f"error: {str(e)}"


def check_minio():
    try:
        client = get_minio_client()
        if client.bucket_exists(settings.minio_bucket):
            return "ok"
        return f"error: bucket '{settings.minio_bucket}' not found"
    except Exception as e:
        return f"error: {str(e)}"


@router.get("/", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    db_status = check_postgres(db)
    minio_status = check_minio()

    overall_status = status.HTTP_200_OK if db_status == "ok" and minio_status == "ok" else status.HTTP_500_INTERNAL_SERVER_ERROR

    return {
        "status": "ok" if overall_status == status.HTTP_200_OK else "error",
        "database": db_status,
        "minio": minio_status,
    }
