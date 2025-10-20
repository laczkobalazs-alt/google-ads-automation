"""
API v1 router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import campaigns, keywords, analytics, automation

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

# Elemzési végpontok
api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)

# Automatizációs végpontok
api_router.include_router(
    automation.router,
    prefix="/automation",
    tags=["Automation"]
)

