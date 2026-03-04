from fastapi import Depends
from app.services.map_service import MapService
from app.services.user_service import UserService


def get_map_service() -> MapService:
    """Dependency for MapService"""
    return MapService()


def get_user_service() -> UserService:
    """Dependency for UserService"""
    return UserService()
