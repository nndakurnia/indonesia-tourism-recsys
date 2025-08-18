from fastapi import APIRouter
from app.api.endpoints import health, destinations, statistics, recommendations

# Main API router
# This is the central router that combines all endpoint routers
api_router = APIRouter()

# Healthcheck endpoints (used to check API availability)
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Healthcheck"]
)

# Destinations endpoints (tourism places CRUD & queries)
api_router.include_router(
    destinations.router,
    prefix="/destinations",
    tags=["Destinations"]
)

# Statistic
api_router.include_router(
    statistics.router,
    prefix="/statistics", 
    tags=["Statistics"]
)

# Statistic
# api_router.include_router(
#     recommendations.router,
#     prefix="/recommendation", 
#     tags=["Recommendation"]
# )
