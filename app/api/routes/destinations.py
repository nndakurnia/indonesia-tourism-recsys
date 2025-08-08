from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.destinations_service import (
    get_data_filtered,
    get_data_by_id,
)

router = APIRouter()


@router.get("/", summary="Get all destinations")
def list_places(
    limit: int = None,
    place: str = None,
    category: str = None,
    city: str = None,
    min_rating: float = None,
    max_price: int = None,
):
    """
    Get a list of destinations with optional filters.
    """
    filtered, available_filters = get_data_filtered(
        limit, place, category, city, min_rating, max_price
    )

    return {
        "total_places": len(filtered),
        "places": filtered,
        "filters_applied": {
            "limit": limit,
            "place": place,
            "category": category,
            "city": city,
            "min_rating": min_rating,
            "max_price": max_price,

        },
        "available_filters": available_filters,
    }


@router.get("/{destination_id}", summary="Get a destination by ID")
def place_detail(destination_id: int):
    """
    Retrieve a specific destination by its ID.
    """
    detail = get_data_by_id(destination_id)
    if not detail:
        raise HTTPException(
            status_code=404, detail=f"Destination with ID {destination_id} not found"
        )
    return detail
