"""
Pydantic modellek az API-hoz
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CampaignBase(BaseModel):
    """Kampány alap model"""
    id: int
    name: str
    status: str
    channel_type: str
    bidding_strategy: str
    budget: Optional[float] = None


class CampaignPerformance(BaseModel):
    """Kampány teljesítmény model"""
    campaign_id: int
    campaign_name: str
    impressions: int
    clicks: int
    ctr: float
    average_cpc: float
    cost: float
    conversions: float
    conversions_value: float
    cost_per_conversion: float
    conversion_rate: float
    roas: float


class KeywordPerformance(BaseModel):
    """Kulcsszó teljesítmény model"""
    campaign_id: int
    campaign_name: str
    ad_group_id: int
    ad_group_name: str
    keyword: str
    match_type: str
    impressions: int
    clicks: int
    ctr: float
    average_cpc: float
    cost: float
    conversions: float
    conversions_value: float
    quality_score: Optional[int] = None


class PerformanceRequest(BaseModel):
    """Teljesítmény lekérdezés request model"""
    customer_id: str = Field(..., description="Google Ads ügyfél azonosító")
    campaign_id: Optional[str] = Field(None, description="Kampány azonosító (opcionális)")
    date_range: str = Field("LAST_30_DAYS", description="Dátum tartomány (pl. LAST_7_DAYS, LAST_30_DAYS)")


class BidOptimizationRequest(BaseModel):
    """Bid optimalizálás request model"""
    customer_id: str = Field(..., description="Google Ads ügyfél azonosító")
    campaign_id: str = Field(..., description="Kampány azonosító")
    target_roas: Optional[float] = Field(None, description="Cél ROAS érték")
    target_cpa: Optional[float] = Field(None, description="Cél CPA érték")
    enabled: bool = Field(True, description="Optimalizálás engedélyezése")


class BudgetOptimizationRequest(BaseModel):
    """Költségvetés optimalizálás request model"""
    customer_id: str = Field(..., description="Google Ads ügyfél azonosító")
    campaign_ids: List[str] = Field(..., description="Kampány azonosítók listája")
    total_budget: float = Field(..., description="Teljes elérhető költségvetés")
    optimization_goal: str = Field("maximize_conversions", description="Optimalizálási cél")


class AutomationStatus(BaseModel):
    """Automatizálás státusz model"""
    automation_type: str
    enabled: bool
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    status: str


class AnalyticsInsight(BaseModel):
    """Elemzési betekintés model"""
    insight_type: str
    severity: str  # info, warning, critical
    message: str
    affected_campaigns: List[str]
    recommendation: str
    metric_value: Optional[float] = None


class APIResponse(BaseModel):
    """Általános API válasz model"""
    success: bool
    message: str
    data: Optional[dict] = None

