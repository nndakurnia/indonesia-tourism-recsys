from pydantic import BaseModel
from typing import Optional


class DestinationBase(BaseModel):
    """Shared properties for Destination schema"""
    place_id: int
    place_name: str
    description: Optional[str] = None
    category: Optional[str] = None
    city: Optional[str] = None
    price: Optional[int] = None
    rating: Optional[float] = None
    time_minutes: Optional[float] = None
    coordinate: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    price_category: Optional[str] = None
    place_total_ratings: Optional[int] = None
    place_is_popular: Optional[int] = None
    place_is_highly_rated: Optional[int] = None
    place_is_consistent: Optional[int] = None
    place_is_niche: Optional[int] = None
    popularity_score: Optional[float] = None


class DestinationResponse(DestinationBase):
    """Schema for returning destination data (read-only)"""
    class Config:
        from_attributes = True  # allow loading from SQLAlchemy models
