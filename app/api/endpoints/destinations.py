from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.destination_service import DestinationService
from app.schemas.destination import DestinationResponse

router = APIRouter()


@router.get(
    "/",
    response_model=list[DestinationResponse],
    summary="List all destinations",
    description="Retrieve a list of destinations with optional filters for search, category, city, price range, and minimum rating.",
)
def list_destinations(
    search: str | None = Query(None, description="Search by place name"),
    category: str | None = Query(None, description="Filter by category"),
    city: str | None = Query(None, description="Filter by city"),
    min_price: int | None = Query(None, description="Minimum price filter"),
    max_price: int | None = Query(None, description="Maximum price filter"),
    min_rating: float | None = Query(None, description="Minimum rating filter"),
    limit: int = Query(20, ge=1, le=100, description="Max number of results to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    db: Session = Depends(get_db),
):
    """
    Get a paginated list of tourism destinations.  
    Supports searching by **name**, filtering by **category, city, price range, and rating**.
    """
    service = DestinationService(db)
    return service.get_all_destinations(
        search=search,
        category=category,
        city=city,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{place_id}",
    response_model=DestinationResponse,
    summary="Get destination by ID",
    description="Retrieve detailed information about a specific destination by its ID.",
)
def get_destination(
    place_id: int,
    db: Session = Depends(get_db),
):
    """
    Get detailed information for a single destination by its **place_id**.
    """
    service = DestinationService(db)
    return service.get_destination_by_id(place_id)
