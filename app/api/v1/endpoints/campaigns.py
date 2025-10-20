"""
Kampány kezelés API végpontok
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from loguru import logger

from app.services.google_ads import get_google_ads_service
from app.config import settings
from app.api.v1.models.schemas import (
    CampaignBase,
    CampaignPerformance,
    PerformanceRequest,
    APIResponse
)

router = APIRouter()


@router.get("/list", response_model=List[CampaignBase])
async def list_campaigns(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító")
):
    """
    Lekérdezi az összes kampányt egy ügyfél fiókból
    
    - **customer_id**: Google Ads ügyfél azonosító (10 számjegy, kötőjelek nélkül)
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        
        if not google_ads_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Google Ads API nincs konfigurálva. Kérlek állítsd be a google-ads.yaml fájlt."
            )
        
        campaigns = google_ads_service.get_campaigns(customer_id)
        return campaigns
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hiba a kampányok lekérdezésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.get("/performance", response_model=List[CampaignPerformance])
async def get_campaign_performance(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    campaign_id: Optional[str] = Query(None, description="Kampány azonosító (opcionális)"),
    date_range: str = Query("LAST_30_DAYS", description="Dátum tartomány")
):
    """
    Lekérdezi a kampány teljesítmény adatokat
    
    - **customer_id**: Google Ads ügyfél azonosító
    - **campaign_id**: Specifikus kampány azonosító (opcionális, ha nincs megadva, minden kampányt lekérdez)
    - **date_range**: Dátum tartomány (LAST_7_DAYS, LAST_30_DAYS, THIS_MONTH, LAST_MONTH, stb.)
    
    ## Visszaadott metrikák:
    - Impressions (megjelenések)
    - Clicks (kattintások)
    - CTR (kattintási arány)
    - Average CPC (átlagos kattintási költség)
    - Cost (költség)
    - Conversions (konverziók)
    - Conversion Rate (konverziós arány)
    - ROAS (megtérülés)
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        
        if not google_ads_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Google Ads API nincs konfigurálva. Kérlek állítsd be a google-ads.yaml fájlt."
            )
        
        performance_data = google_ads_service.get_campaign_performance(
            customer_id=customer_id,
            campaign_id=campaign_id,
            date_range=date_range
        )
        
        return performance_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hiba a teljesítmény adatok lekérdezésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.post("/performance", response_model=List[CampaignPerformance])
async def get_campaign_performance_post(request: PerformanceRequest):
    """
    Lekérdezi a kampány teljesítmény adatokat (POST metódus)
    
    Ez ugyanaz a funkció mint a GET /performance, de POST metódussal,
    ami hasznos lehet komplex lekérdezésekhez.
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        
        if not google_ads_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Google Ads API nincs konfigurálva."
            )
        
        performance_data = google_ads_service.get_campaign_performance(
            customer_id=request.customer_id,
            campaign_id=request.campaign_id,
            date_range=request.date_range
        )
        
        return performance_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hiba a teljesítmény adatok lekérdezésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")

