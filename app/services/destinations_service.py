from fastapi import Query
from typing import Optional, Tuple, List, Dict, Any
from app.utils.data_loader import load_data

# Load data from CSV
tourism_data = load_data()

def get_data_filtered(
    limit: Optional[int] = Query(None, description="Limit the number of results"),
    place: Optional[str] = Query(None, description="Search by place name"),
    category: Optional[str] = Query(None, description="Search by category"),
    city: Optional[str] = Query(None, description="Search by city"),
    min_rating: Optional[float] = Query(None, description="Minimum rating filter"),
    max_price: Optional[int] = Query(None, description="Maximum price filter")
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    
    """
    Filter tourism data based on query parameters.
    
    Returns:
        filtered_data: List of places matching filters
        metadata: Information about available filters for the results
    """

    filtered = tourism_data.copy()

    # Filter by place name
    if place:
        filtered = [
            p for p in filtered
            if place.lower() in (p.get('Place_Name') or '').lower()
        ]

    # Filter by category
    if category:
        filtered = [
            p for p in filtered
            if category.lower() in (p.get('Category') or '').lower()
        ]

    # Filter by city
    if city:
        filtered = [
            p for p in filtered
            if city.lower() in (p.get('City') or '').lower()
        ]

    # Filter by minimum rating
    if min_rating is not None:
        filtered = [p for p in filtered if p['Rating'] >= min_rating]

    # Filter by maximum price
    if max_price is not None:
        filtered = [p for p in filtered if p['Price'] <= max_price]

    # Sort by rating (highest first)
    filtered.sort(key=lambda x: x['Rating'], reverse=True)

    # Apply result limit
    if limit:
        filtered = filtered[:limit]

    # Metadata for filter options in the response
    metadata = {
        'categories': sorted(set(p['Category'] for p in tourism_data)),
        'cities': sorted(set(p['City'] for p in tourism_data)),
        'rating_range': [
            min(p['Rating'] for p in tourism_data),
            max(p['Rating'] for p in tourism_data)
        ],
        'price_range': [
            min(p['Price'] for p in tourism_data),
            max(p['Price'] for p in tourism_data)
        ]
    }

    return filtered, metadata


def get_data_by_id(place_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a specific tourism place by its ID with related recommendations.
    
    Returns:
        dict containing place details, similar places, nearby places, and travel recommendations.
    """
    # Find main place
    place = next((p for p in tourism_data if p['Place_Id'] == place_id), None)
    if not place:
        return None

    # Find similar places (same category, different place)
    similar_places = [
        p for p in tourism_data
        if p['Category'] == place['Category'] and p['Place_Id'] != place_id
    ][:3]

    # Find nearby places (same city, different place)
    nearby_places = [
        p for p in tourism_data
        if p['City'] == place['City'] and p['Place_Id'] != place_id
    ][:3]

    # Travel tips based on category
    recommendations = {
        'best_time_to_visit': (
            'Year round' if place['Category'] in ['Budaya', 'Belanja']
            else 'Dry season'
        ),
        'suggested_duration': (
            '2-4 hours' if place['Category'] in ['Monumen', 'Budaya']
            else 'Full day'
        ),
        'difficulty_level': (
            'Easy' if place['Category'] in ['Pantai', 'Belanja']
            else 'Moderate'
        )
    }

    return {
        'place': place,
        'similar_places': similar_places,
        'nearby_places': nearby_places,
        'recommendations': recommendations
    }
