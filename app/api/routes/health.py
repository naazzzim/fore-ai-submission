from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@router.get("/live")
async def liveness():
    """Liveness probe"""
    return {"status": "alive"}


@router.get("/ready")
async def readiness():
    """Readiness probe"""
    return {"status": "ready"}
