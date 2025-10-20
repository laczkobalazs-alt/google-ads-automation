"""
Automatizációs API végpontok
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from loguru import logger

from app.services.google_ads import get_google_ads_service
from app.services.automation import get_automation_service
from app.config import settings
from app.api.v1.models.schemas import (
    BidOptimizationRequest,
    BudgetOptimizationRequest,
    AutomationStatus,
    APIResponse
)

router = APIRouter()


@router.post("/bid-optimization/create", response_model=APIResponse)
async def create_bid_optimization(request: BidOptimizationRequest):
    """
    Létrehoz egy automatikus bid optimalizálási szabályt
    
    A szabály létrehozása után az API automatikusan figyelni fogja a kampány
    teljesítményét és ajánlásokat fog adni a bid módosításokhoz.
    
    - **target_roas**: Ha meg van adva, ROAS alapú optimalizálást végez
    - **target_cpa**: Ha meg van adva, CPA alapú optimalizálást végez
    - **enabled**: Ha True, a szabály azonnal aktív lesz
    """
    try:
        automation_service = get_automation_service()
        
        result = automation_service.create_bid_optimization_rule(
            customer_id=request.customer_id,
            campaign_id=request.campaign_id,
            target_roas=request.target_roas,
            target_cpa=request.target_cpa,
            enabled=request.enabled
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Hiba a bid optimalizálási szabály létrehozásakor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.post("/bid-optimization/apply/{rule_id}", response_model=APIResponse)
async def apply_bid_optimization(
    rule_id: str,
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    campaign_id: str = Query(..., description="Kampány azonosító"),
    date_range: str = Query("LAST_7_DAYS", description="Dátum tartomány")
):
    """
    Alkalmaz egy bid optimalizálási szabályt
    
    Lekérdezi a kampány aktuális teljesítményét és ajánlásokat ad
    a bid módosításokhoz a beállított szabály alapján.
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        automation_service = get_automation_service()
        
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
        
        if not performance_data:
            raise HTTPException(
                status_code=404,
                detail="Nem található teljesítmény adat a kampányhoz"
            )
        
        # Optimalizálás alkalmazása
        result = automation_service.apply_bid_optimization(
            rule_id=rule_id,
            performance_data=performance_data[0]
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Hiba a bid optimalizálás alkalmazásakor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.post("/budget-optimization/create", response_model=APIResponse)
async def create_budget_optimization(request: BudgetOptimizationRequest):
    """
    Létrehoz egy automatikus költségvetés optimalizálási szabályt
    
    A szabály több kampány között osztja el optimálisan a költségvetést
    a megadott cél alapján.
    
    Optimalizálási célok:
    - **maximize_conversions**: Konverziók maximalizálása
    - **maximize_roas**: ROAS maximalizálása
    """
    try:
        automation_service = get_automation_service()
        
        result = automation_service.create_budget_optimization_rule(
            customer_id=request.customer_id,
            campaign_ids=request.campaign_ids,
            total_budget=request.total_budget,
            optimization_goal=request.optimization_goal,
            enabled=True
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Hiba a költségvetés optimalizálási szabály létrehozásakor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.post("/alert/create", response_model=APIResponse)
async def create_alert_rule(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    campaign_id: Optional[str] = Query(None, description="Kampány azonosító (opcionális)"),
    metric: str = Query(..., description="Metrika (roas, cpa, ctr, stb.)"),
    threshold: float = Query(..., description="Küszöbérték"),
    condition: str = Query("below", description="Feltétel (below, above)"),
    enabled: bool = Query(True, description="Engedélyezve")
):
    """
    Létrehoz egy riasztási szabályt
    
    A szabály automatikusan figyeli a megadott metrikát és riasztást küld,
    ha az érték a küszöb alá/fölé kerül.
    
    Példa használat:
    - Riasztás ha ROAS < 2.0
    - Riasztás ha CPA > 50.0
    - Riasztás ha CTR < 0.01
    """
    try:
        automation_service = get_automation_service()
        
        result = automation_service.create_alert_rule(
            customer_id=customer_id,
            campaign_id=campaign_id,
            metric=metric,
            threshold=threshold,
            condition=condition,
            enabled=enabled
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Hiba a riasztási szabály létrehozásakor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.post("/alert/check", response_model=List[dict])
async def check_alerts(
    customer_id: str = Query(..., description="Google Ads ügyfél azonosító"),
    date_range: str = Query("LAST_7_DAYS", description="Dátum tartomány")
):
    """
    Ellenőrzi a riasztási szabályokat
    
    Lekérdezi a kampányok teljesítményét és ellenőrzi az összes aktív
    riasztási szabályt. Visszaadja a kiváltott riasztásokat.
    """
    try:
        google_ads_service = get_google_ads_service(settings.GOOGLE_ADS_CONFIG_FILE)
        automation_service = get_automation_service()
        
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
        
        # Riasztások ellenőrzése
        triggered_alerts = automation_service.check_alert_rules(performance_data)
        
        return triggered_alerts
        
    except Exception as e:
        logger.error(f"Hiba a riasztások ellenőrzésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.get("/rules", response_model=List[dict])
async def get_automation_rules(
    rule_type: Optional[str] = Query(None, description="Szabály típus (bid_optimization, budget_optimization, alert)"),
    enabled_only: bool = Query(False, description="Csak engedélyezett szabályok")
):
    """
    Lekérdezi az automatizálási szabályokat
    
    Szűrési lehetőségek:
    - **rule_type**: Szabály típus szerint szűrés
    - **enabled_only**: Csak az aktív szabályok
    """
    try:
        automation_service = get_automation_service()
        
        rules = automation_service.get_automation_rules(
            rule_type=rule_type,
            enabled_only=enabled_only
        )
        
        return rules
        
    except Exception as e:
        logger.error(f"Hiba a szabályok lekérdezésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.put("/rules/{rule_id}", response_model=APIResponse)
async def update_automation_rule(
    rule_id: str,
    enabled: Optional[bool] = Query(None, description="Engedélyezve"),
    target_roas: Optional[float] = Query(None, description="Cél ROAS"),
    target_cpa: Optional[float] = Query(None, description="Cél CPA"),
    threshold: Optional[float] = Query(None, description="Küszöbérték")
):
    """
    Frissít egy automatizálási szabályt
    
    Csak a megadott mezőket frissíti, a többi változatlan marad.
    """
    try:
        automation_service = get_automation_service()
        
        updates = {}
        if enabled is not None:
            updates["enabled"] = enabled
        if target_roas is not None:
            updates["target_roas"] = target_roas
        if target_cpa is not None:
            updates["target_cpa"] = target_cpa
        if threshold is not None:
            updates["threshold"] = threshold
        
        result = automation_service.update_automation_rule(
            rule_id=rule_id,
            updates=updates
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Hiba a szabály frissítésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.delete("/rules/{rule_id}", response_model=APIResponse)
async def delete_automation_rule(rule_id: str):
    """
    Töröl egy automatizálási szabályt
    """
    try:
        automation_service = get_automation_service()
        
        result = automation_service.delete_automation_rule(rule_id)
        
        return result
        
    except Exception as e:
        logger.error(f"Hiba a szabály törlésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")


@router.get("/history", response_model=List[dict])
async def get_automation_history(
    rule_id: Optional[str] = Query(None, description="Szabály azonosító"),
    limit: int = Query(100, description="Maximum rekordok száma")
):
    """
    Lekérdezi az automatizálási történetet
    
    Visszaadja az automatizálási műveletek történetét, beleértve
    az alkalmazott ajánlásokat és eredményeket.
    """
    try:
        automation_service = get_automation_service()
        
        history = automation_service.get_automation_history(
            rule_id=rule_id,
            limit=limit
        )
        
        return history
        
    except Exception as e:
        logger.error(f"Hiba a történet lekérdezésekor: {e}")
        raise HTTPException(status_code=500, detail=f"Belső szerver hiba: {str(e)}")

