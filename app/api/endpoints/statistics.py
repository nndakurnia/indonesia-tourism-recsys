from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.statistic import DestinationStats
from app.services.statistic_service import StatisticService
from app.core.database import get_db

router = APIRouter()


@router.get(
    "/",
    response_model=DestinationStats,
    summary="Get destination statistics",
    description="Retrieve statistics including totals, unique counts, and distributions by city, category, price, and rating.",
)
def get_statistics(db: Session = Depends(get_db)):
    service = StatisticService(db)
    return service.get_statistics()
