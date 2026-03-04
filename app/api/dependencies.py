from fastapi import Depends
from app.services.map_service import MapService


def get_map_service() -> MapService:
    """Dependency for MapService"""
    return MapService()
