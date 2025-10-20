"""
Kulcsszó elemzés API végpontok
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from loguru import logger

from app.services.google_ads import get_google_ads_service
from app.config import settings
from app.api.v1.models.schemas import KeywordPerformance

router = APIRouter()


@router.get("/performance", response_model=List[KeywordPerformance])
async def get_keywords_performance(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    campaign_id: Optional[str] = Query(None, description="Kampány azonosító (opcionális)"),
    date_range: str = Query("LAST_30_DAYS", description="Dátum tartomány")
):
    """
    Lekérdezi a kulcsszavak teljesítményét
    
    - **customer_id**: Google Ads ügyfél azonosító
    - **campaign_id**: Specifikus kampány azonosító (opcionális)
    - **date_range**: Dátum tartomány (LAST_7_DAYS, LAST_30_DAYS, stb.)
    
    ## Visszaadott metrikák:
    - Kulcsszó szöveg és match type
    - Impressions (megjelenések)
    - Clicks (kattintások)
    - CTR (kattintási arány)
    - Average CPC (átlagos kattintási költség)
    - Cost (költség)
    - Conversions (konverziók)
    - Quality Score (minőségi pontszám)
    
    Maximum 1000 kulcsszót ad vissza, impressions szerint rendezve.
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        
        if not google_ads_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Google Ads API nincs konfigurálva. Kérlek állítsd be a google-ads.yaml fájlt."
            )
        
        keywords_data = google_ads_service.get_keywords_performance(
            customer_id=customer_id,
            campaign_id=campaign_id,
            date_range=date_range
        )
        
        return keywords_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hiba a kulcsszó adatok lekérdezésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")

