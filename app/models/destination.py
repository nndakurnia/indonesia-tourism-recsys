from sqlalchemy import Column, BigInteger, Text, Float
from app.core.database import Base


class Destination(Base):
    """
    SQLAlchemy model representing a tourism destination.

    This maps directly to the table `tourism_places_clean` inside
    the schema `tourism_data`.
    """

    __tablename__ = "tourism_places_clean"
    __table_args__ = {"schema": "tourism_data"}

    # Primary Key
    place_id = Column("Place_Id", BigInteger, primary_key=True, index=True)

    # Basic Information
    place_name = Column("Place_Name", Text, nullable=False)
    description = Column("Description", Text)
    category = Column("Category", Text, index=True)
    city = Column("City", Text, index=True)

    # Price & Rating
    price = Column("Price", BigInteger)
    rating = Column("Rating", Float)

    # Visit Duration
    time_minutes = Column("Time_Minutes", Float)

    # Location
    coordinate = Column("Coordinate", Text)
    lat = Column("Lat", Float)
    long = Column("Long", Float)

    # Derived Features / Tags
    price_category = Column("price_category", Text)
    place_total_ratings = Column("place_total_ratings", BigInteger)
    place_is_popular = Column("place_is_popular", BigInteger)
    place_is_highly_rated = Column("place_is_highly_rated", BigInteger)
    place_is_consistent = Column("place_is_consistent", BigInteger)  # Fixed typo (removed trailing space)
    place_is_niche = Column("place_is_niche", BigInteger)

    # Computed Score
    popularity_score = Column("popularity_score", Float)
