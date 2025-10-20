"""
API v1 router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import campaigns, keywords

api_router = APIRouter()

# Kampány végpontok
api_router.include_router(
    campaigns.router,
    prefix="/campaigns",
    tags=["Campaigns"]
)

# Kulcsszó végpontok
api_router.include_router(
    keywords.router,
    prefix="/keywords",
    tags=["Keywords"]
)

