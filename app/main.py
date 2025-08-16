from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.api_router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & shutdown events for the application."""
    # Startup
    print("Starting up: Initializing ML recommendation service...")

    # Application runs here
    yield  

    # Shutdown
    print("Shutting down...")



def get_application() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        description=settings.description,
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(api_router, prefix="/api")

    # Root endpoint
    @app.get("/")
    async def read_root():
        """
        Root endpoint for testing if API is alive.
        Returns API name, version, and docs URL.
        """
        return {
            "message": "Tourism Recommendation API",
            "version": settings.version,
            "docs_url": "/docs"
        }

    return app


# Initialize FastAPI app
app = get_application()
