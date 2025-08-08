from fastapi import FastAPI
from app.api.api_router import api_router


def get_application() -> FastAPI:
    app = FastAPI(
        title="Tourism Recommendation API",
        version="1.0.0",
        description="API for recommending tourism destinations in Indonesia.",
    )

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()
