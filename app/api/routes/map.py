
from fastapi import APIRouter, Depends

from app.api.dependencies import get_map_service
from app.models.map import MapInput
from app.services.map_service import MapService


router = APIRouter()


@router.post("/")
async def map_website(input: MapInput, map_service: MapService = Depends(get_map_service)):
    """Map a website starting from the given URL"""
    result = await map_service.map_website(input.start_url, input.max_depth)
    return result
