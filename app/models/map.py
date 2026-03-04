from typing import TypedDict, NamedTuple

from pydantic import BaseModel, Field
from enum import Enum


class MapInput(BaseModel):
    start_url: str
    max_depth: int = 3


class Link(TypedDict):
    """Data model for a link in the map"""
    href: str
    title: str | None


class LinkNode(NamedTuple):
    """Data model for a link node in the queue"""
    url: str
    depth: int
    title: str | None = None


class Node(BaseModel):
    """Data model for a node in the map"""
    url: str
    children: list[str] = []
    title: str | None = None
    summary: str | None = None


class MapResult(BaseModel):
    """Data model for map results"""
    start_url: str
    global_links: list[str] = []
    nodes: dict[str, Node] = {}


class SummaryModel(BaseModel):
    """Data model for the summary of a page"""
    summary: str = Field(
        ..., description="call to action of the page if any, or the summary of the page")

# Unused for now, but can be used in the future to allow users to specify custom authentication configurations


class TokenStorage(str, Enum):
    """Enum for token storage options"""
    COOKIES = "in_memory"
    LOCAL_STORAGE = "local_storage"

# Unused for now, but can be used in the future to allow users to specify custom authentication configurations


class AuthenticationType(str, Enum):
    """Enum for authentication types"""
    BASIC = "basic"
    TOKEN = "token"

# Unused for now, but can be used in the future to allow users to specify custom strategies for global URL identification


class GlobalURLIdentificationStrategy(str, Enum):
    """Enum for global URL identification strategies"""
    SD_OUTLIER_IDENTIFICATION = "sd_outlier_identification"
    PRESENCE_RATIO = "presence_ratio"

# Unused for now, but can be used in the future to allow users to specify custom authentication configurations


class Token(BaseModel):
    """Token model for authentication"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    storage: TokenStorage = TokenStorage.COOKIES

# Unused for now, but can be used in the future to allow users to specify custom authentication configurations


class Credential(BaseModel):
    """Credential model for authentication"""
    username: str
    password: str

# Unused for now, but can be used in the future to allow users to specify custom authentication configurations


class AuthenticationConfig(BaseModel):
    """Data model for authentication configuration"""
    auth_type: AuthenticationType
    configs: Credential | Token

# Unused for now, but can be used in the future to allow users to specify custom strategies for global URL identification


class MapCreateConfig(BaseModel):
    """Data model for creating a map"""
    start_url: str
    max_depth: int = 3
    max_pages: int = 100
    global_url_identification_strategy: GlobalURLIdentificationStrategy = GlobalURLIdentificationStrategy.PRESENCE_RATIO
    authentication: AuthenticationConfig | None = None
