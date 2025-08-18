from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.destination import Destination


class StatisticService:
    def __init__(self, db: Session):
        self.db = db

    def get_statistics(self) -> dict:
        """Return aggregated statistics and distributions for destinations."""

        # --- Summary ---
        total_destinations = self.db.query(func.count(Destination.place_id)).scalar()
        total_cities = self.db.query(func.count(func.distinct(Destination.city))).scalar()
        avg_rating = self.db.query(func.avg(Destination.rating)).scalar() or 0
        free_places = (
            self.db.query(func.count(Destination.place_id))
            .filter(Destination.price == 0)
            .scalar()
        )

        # --- Distribution by city ---
        city_counts = (
            self.db.query(Destination.city, func.count(Destination.place_id))
            .group_by(Destination.city)
            .order_by(func.count(Destination.place_id).desc())
            .all()
        )
        city_distribution = [
            {"city": city, "count": count} for city, count in city_counts
        ]

        # --- Distribution by category ---
        category_counts = (
            self.db.query(Destination.category, func.count(Destination.place_id))
            .group_by(Destination.category)
            .order_by(func.count(Destination.place_id).desc())
            .all()
        )
        category_distribution = [
            {"category": category, "count": count} for category, count in category_counts
        ]

        # --- Distribution by price (fixed order) ---
        price_buckets = [
            ("Free", Destination.price == 0),
            ("<50k", and_(Destination.price > 0, Destination.price < 50000)),
            ("50k-100k", Destination.price.between(50000, 100000)),
            (">100k", Destination.price > 100000),
        ]
        price_distribution = []
        for label, condition in price_buckets:
            count = self.db.query(func.count(Destination.place_id)).filter(condition).scalar()
            price_distribution.append({"range": label, "count": count})

        # --- Distribution by rating (fixed order high→low) ---
        rating_buckets = [
            ("4.5-5", Destination.rating.between(4.5, 5)),
            ("4-4.4", Destination.rating.between(4, 4.4)),
            ("3.5-3.9", Destination.rating.between(3.5, 3.9)),
            ("3-3.4", Destination.rating.between(3, 3.4)),
            ("<3", Destination.rating < 3),
        ]
        rating_distribution = []
        for label, condition in rating_buckets:
            count = self.db.query(func.count(Destination.place_id)).filter(condition).scalar()
            rating_distribution.append({"range": label, "count": count})

        return {
            "summary": {
                "total_destinations": total_destinations,
                "total_cities": total_cities,
                "average_rating": round(float(avg_rating), 2),
                "free_places": free_places,
            },
            "distribution": {
                "by_city": city_distribution,
                "by_category": category_distribution,
                "by_price": price_distribution,
                "by_rating": rating_distribution,
            },
        }
