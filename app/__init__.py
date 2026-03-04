from fastapi import FastAPI
from app.api.routes import health, map


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Submission API",
        description="A FastAPI application",
        version="0.1.0",
    )

    # Include routes
    app.include_router(health.router, prefix="/api/health", tags=["health"])
    app.include_router(map.router, prefix="/api/map", tags=["map"])

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {"message": "Welcome to Submission API"}

    return app
