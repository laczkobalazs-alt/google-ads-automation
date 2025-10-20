"""
Elemzési API végpontok
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from loguru import logger

from app.services.google_ads import get_google_ads_service
from app.services.analytics import get_analytics_service
from app.config import settings
from app.api.v1.models.schemas import AnalyticsInsight

router = APIRouter()


@router.get("/campaign-insights")
async def get_campaign_insights(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    campaign_id: Optional[str] = Query(None, description="Kampány azonosító (opcionális)"),
    date_range: str = Query("LAST_30_DAYS", description="Dátum tartomány"),
    min_roas: float = Query(2.0, description="Minimum ROAS küszöb"),
    max_cpa: float = Query(50.0, description="Maximum CPA küszöb"),
    min_ctr: float = Query(0.01, description="Minimum CTR küszöb")
):
    """
    Kampány teljesítmény elemzés és betekintések
    
    Ez az endpoint lekérdezi a kampány teljesítményt és részletes elemzést végez,
    amely tartalmazza:
    - Teljesítmény betekintéseket (insights)
    - Összefoglaló statisztikákat
    - Optimalizálási ajánlásokat
    
    A küszöbértékek alapján azonosítja:
    - Alacsony ROAS-ú kampányokat
    - Magas CPA-jú kampányokat
    - Alacsony CTR-ű kampányokat
    - Konverzió nélküli kampányokat
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        analytics_service = get_analytics_service()
        
        if not google_ads_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Google Ads API nincs konfigurálva."
            )
        
        # Teljesítmény adatok lekérdezése
        performance_data = google_ads_service.get_campaign_performance(
            customer_id=customer_id,
            campaign_id=campaign_id,
            date_range=date_range
        )
        
        # Elemzés futtatása
        thresholds = {
            "min_roas": min_roas,
            "max_cpa": max_cpa,
            "min_ctr": min_ctr
        }
        
        analysis_result = analytics_service.analyze_campaign_performance(
            performance_data=performance_data,
            thresholds=thresholds
        )
        
        return analysis_result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hiba a kampány elemzéskor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.get("/keyword-insights")
async def get_keyword_insights(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    campaign_id: Optional[str] = Query(None, description="Kampány azonosító (opcionális)"),
    date_range: str = Query("LAST_30_DAYS", description="Dátum tartomány"),
    min_impressions: int = Query(100, description="Minimum impressions szűrő")
):
    """
    Kulcsszó teljesítmény elemzés és betekintések
    
    Ez az endpoint elemzi a kulcsszavak teljesítményét és azonosítja:
    - Top teljesítő kulcsszavakat
    - Alulteljesítő kulcsszavakat (magas költség, alacsony konverzió)
    - Alacsony Quality Score-ú kulcsszavakat
    - Match type teljesítmény eloszlást
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        analytics_service = get_analytics_service()
        
        if not google_ads_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Google Ads API nincs konfigurálva."
            )
        
        # Kulcsszó adatok lekérdezése
        keywords_data = google_ads_service.get_keywords_performance(
            customer_id=customer_id,
            campaign_id=campaign_id,
            date_range=date_range
        )
        
        # Elemzés futtatása
        analysis_result = analytics_service.analyze_keyword_performance(
            keywords_data=keywords_data,
            min_impressions=min_impressions
        )
        
        return analysis_result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hiba a kulcsszó elemzéskor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.get("/compare-campaigns")
async def compare_campaigns(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    date_range: str = Query("LAST_30_DAYS", description="Dátum tartomány"),
    metric: str = Query("roas", description="Összehasonlítási metrika (roas, ctr, cost_per_conversion)")
):
    """
    Kampányok összehasonlítása egy adott metrika alapján
    
    Visszaadja:
    - Legjobb és legrosszabb kampányt
    - Átlag, medián, szórás értékeket
    - Teljes rangsorolást
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        analytics_service = get_analytics_service()
        
        if not google_ads_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Google Ads API nincs konfigurálva."
            )
        
        # Teljesítmény adatok lekérdezése
        performance_data = google_ads_service.get_campaign_performance(
            customer_id=customer_id,
            date_range=date_range
        )
        
        # Összehasonlítás
        comparison_result = analytics_service.compare_campaigns(
            performance_data=performance_data,
            metric=metric
        )
        
        return comparison_result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hiba a kampány összehasonlításkor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.post("/budget-allocation")
async def calculate_budget_allocation(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    total_budget: float = Query(..., description="Teljes elérhető költségvetés"),
    date_range: str = Query("LAST_30_DAYS", description="Dátum tartomány"),
    optimization_goal: str = Query("maximize_conversions", description="Optimalizálási cél")
):
    """
    Optimális költségvetés elosztás számítása
    
    Az előző időszak teljesítménye alapján kiszámítja az optimális
    költségvetés elosztást a kampányok között.
    
    Optimalizálási célok:
    - **maximize_conversions**: Konverziók maximalizálása
    - **maximize_roas**: ROAS maximalizálása
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        analytics_service = get_analytics_service()
        
        if not google_ads_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Google Ads API nincs konfigurálva."
            )
        
        # Teljesítmény adatok lekérdezése
        performance_data = google_ads_service.get_campaign_performance(
            customer_id=customer_id,
            date_range=date_range
        )
        
        # Költségvetés elosztás számítása
        allocation_result = analytics_service.calculate_budget_allocation(
            performance_data=performance_data,
            total_budget=total_budget,
            optimization_goal=optimization_goal
        )
        
        return allocation_result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hiba a költségvetés elosztás számításakor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")

