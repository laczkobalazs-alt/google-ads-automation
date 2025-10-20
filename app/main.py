"""
Google Ads Automation API - Fő alkalmazás
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.config import settings
from app.api.v1 import api_router

# Logging konfiguráció
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)
logger.add(
    settings.LOG_FILE,
    rotation="10 MB",
    retention="30 days",
    level=settings.LOG_LEVEL
)

# FastAPI alkalmazás létrehozása
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="""
    Google Ads Automation API - Átfogó adatelemzés és automatizáció
    
    ## Funkciók
    
    * **Kampány elemzés**: Részletes teljesítmény riportok
    * **Kulcsszó elemzés**: Kulcsszavak hatékonyságának mérése
    * **Automatikus optimalizálás**: Bid és költségvetés optimalizálás
    * **Riasztások**: Automatikus értesítések teljesítmény változásokról
    
    ## Használat
    
    1. Konfiguráld a Google Ads API hozzáférést
    2. Használd az API végpontokat az adatok lekérdezéséhez
    3. Engedélyezd az automatizációs funkciókat igény szerint
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Éles környezetben korlátozd ezt!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API router hozzáadása
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Főoldal - API státusz"""
    return {
        "message": "Google Ads Automation API",
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Egészségügyi ellenőrzés"""
    from app.services.google_ads import get_google_ads_service
    
    google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
    
    return {
        "status": "healthy",
        "google_ads_configured": google_ads_service.is_configured()
    }


@app.on_event("startup")
async def startup_event():
    """Alkalmazás indításkor futó műveletek"""
    logger.info("Google Ads Automation API indítása...")
    logger.info(f"Debug mód: {settings.DEBUG}")
    logger.info(f"API verzió: {settings.API_VERSION}")


@app.on_event("shutdown")
async def shutdown_event():
    """Alkalmazás leállításkor futó műveletek"""
    logger.info("Google Ads Automation API leállítása...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

