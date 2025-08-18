from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional

from app.models.destination import Destination


class DestinationService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_destinations(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        city: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        min_rating: Optional[float] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Destination]:
        """
        Get all destinations with optional search and filters.
        """

        query = self.db.query(Destination)

        # 🔍 Search by place name
        if search:
            query = query.filter(Destination.place_name.ilike(f"%{search}%"))

        # 📌 Filter by category
        if category:
            query = query.filter(Destination.category.ilike(f"%{category}%"))

        # 📌 Filter by city
        if city:
            query = query.filter(Destination.city.ilike(f"%{city}%"))

        # 💰 Filter by price range
        if min_price is not None and max_price is not None:
            query = query.filter(and_(Destination.price >= min_price, Destination.price <= max_price))
        elif min_price is not None:
            query = query.filter(Destination.price >= min_price)
        elif max_price is not None:
            query = query.filter(Destination.price <= max_price)

        # ⭐ Filter by minimal rating
        if min_rating is not None:
            query = query.filter(Destination.rating >= min_rating)

        return query.offset(offset).limit(limit).all()

    def get_destination_by_id(self, place_id: int) -> Optional[Destination]:
        """
        Get a single destination by ID.
        """
        return self.db.query(Destination).filter(Destination.place_id == place_id).first()
