from pydantic import BaseModel
from typing import Dict


class CityDistribution(BaseModel):
    city: str
    count: int


class CategoryDistribution(BaseModel):
    category: str
    count: int


class DestinationSummary(BaseModel):
    total_destinations: int
    total_cities: int
    average_rating: float
    free_places: int


class DestinationStats(BaseModel):
    summary: DestinationSummary
    distribution: Dict[str, object]
