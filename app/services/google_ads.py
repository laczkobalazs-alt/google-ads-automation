"""
Google Ads API integráció
"""
from typing import Optional, List, Dict, Any
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from loguru import logger
import os


class GoogleAdsService:
    """Google Ads API szolgáltatás osztály"""
    
    def __init__(self, config_file: str = "google-ads.yaml"):
        """
        Inicializálja a Google Ads klienst
        
        Args:
            config_file: Google Ads konfiguráció fájl elérési útja
        """
        self.config_file = config_file
        self.client: Optional[GoogleAdsClient] = None
        
        if os.path.exists(config_file):
            try:
                self.client = GoogleAdsClient.load_from_storage(config_file)
                logger.info("Google Ads kliens sikeresen inicializálva")
            except Exception as e:
                logger.error(f"Hiba a Google Ads kliens inicializálásakor: {e}")
                self.client = None
        else:
            logger.warning(f"Google Ads konfiguráció fájl nem található: {config_file}")
    
    def is_configured(self) -> bool:
        """Ellenőrzi, hogy a kliens konfigurálva van-e"""
        return self.client is not None
    
    def get_campaigns(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Lekérdezi az összes kampányt egy ügyfél fiókból
        
        Args:
            customer_id: Google Ads ügyfél azonosító
            
        Returns:
            Kampányok listája
        """
        if not self.is_configured():
            raise ValueError("Google Ads kliens nincs konfigurálva")
        
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            query = """
                SELECT
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    campaign.advertising_channel_type,
                    campaign.bidding_strategy_type,
                    campaign_budget.amount_micros
                FROM campaign
                ORDER BY campaign.name
            """
            
            response = ga_service.search(customer_id=customer_id, query=query)
            
            campaigns = []
            for row in response:
                campaign = row.campaign
                budget = row.campaign_budget
                
                campaigns.append({
                    "id": campaign.id,
                    "name": campaign.name,
                    "status": campaign.status.name,
                    "channel_type": campaign.advertising_channel_type.name,
                    "bidding_strategy": campaign.bidding_strategy_type.name,
                    "budget_micros": budget.amount_micros if budget else None,
                    "budget": budget.amount_micros / 1_000_000 if budget and budget.amount_micros else None
                })
            
            logger.info(f"{len(campaigns)} kampány lekérdezve az ügyfél {customer_id} fiókból")
            return campaigns
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API hiba: {ex}")
            raise
        except Exception as e:
            logger.error(f"Hiba a kampányok lekérdezésekor: {e}")
            raise
    
    def get_campaign_performance(
        self, 
        customer_id: str, 
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> List[Dict[str, Any]]:
        """
        Lekérdezi a kampány teljesítmény adatokat
        
        Args:
            customer_id: Google Ads ügyfél azonosító
            campaign_id: Kampány azonosító (opcionális, ha nincs megadva, minden kampányt lekérdez)
            date_range: Dátum tartomány (pl. LAST_7_DAYS, LAST_30_DAYS, THIS_MONTH)
            
        Returns:
            Teljesítmény adatok listája
        """
        if not self.is_configured():
            raise ValueError("Google Ads kliens nincs konfigurálva")
        
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
            
            query = f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.ctr,
                    metrics.average_cpc,
                    metrics.cost_micros,
                    metrics.conversions,
                    metrics.conversions_value,
                    metrics.cost_per_conversion,
                    metrics.conversion_rate
                FROM campaign
                WHERE segments.date DURING {date_range}
                {campaign_filter}
                ORDER BY metrics.impressions DESC
            """
            
            response = ga_service.search(customer_id=customer_id, query=query)
            
            performance_data = []
            for row in response:
                campaign = row.campaign
                metrics = row.metrics
                
                performance_data.append({
                    "campaign_id": campaign.id,
                    "campaign_name": campaign.name,
                    "impressions": metrics.impressions,
                    "clicks": metrics.clicks,
                    "ctr": metrics.ctr,
                    "average_cpc": metrics.average_cpc / 1_000_000 if metrics.average_cpc else 0,
                    "cost": metrics.cost_micros / 1_000_000 if metrics.cost_micros else 0,
                    "conversions": metrics.conversions,
                    "conversions_value": metrics.conversions_value,
                    "cost_per_conversion": metrics.cost_per_conversion / 1_000_000 if metrics.cost_per_conversion else 0,
                    "conversion_rate": metrics.conversion_rate,
                    "roas": (metrics.conversions_value / (metrics.cost_micros / 1_000_000)) if metrics.cost_micros > 0 else 0
                })
            
            logger.info(f"Teljesítmény adatok lekérdezve: {len(performance_data)} rekord")
            return performance_data
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API hiba: {ex}")
            raise
        except Exception as e:
            logger.error(f"Hiba a teljesítmény adatok lekérdezésekor: {e}")
            raise
    
    def get_keywords_performance(
        self,
        customer_id: str,
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> List[Dict[str, Any]]:
        """
        Lekérdezi a kulcsszavak teljesítményét
        
        Args:
            customer_id: Google Ads ügyfél azonosító
            campaign_id: Kampány azonosító (opcionális)
            date_range: Dátum tartomány
            
        Returns:
            Kulcsszó teljesítmény adatok listája
        """
        if not self.is_configured():
            raise ValueError("Google Ads kliens nincs konfigurálva")
        
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
            
            query = f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    ad_group.id,
                    ad_group.name,
                    ad_group_criterion.keyword.text,
                    ad_group_criterion.keyword.match_type,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.ctr,
                    metrics.average_cpc,
                    metrics.cost_micros,
                    metrics.conversions,
                    metrics.conversions_value,
                    metrics.quality_score
                FROM keyword_view
                WHERE segments.date DURING {date_range}
                {campaign_filter}
                AND ad_group_criterion.status = 'ENABLED'
                ORDER BY metrics.impressions DESC
                LIMIT 1000
            """
            
            response = ga_service.search(customer_id=customer_id, query=query)
            
            keywords_data = []
            for row in response:
                campaign = row.campaign
                ad_group = row.ad_group
                keyword = row.ad_group_criterion.keyword
                metrics = row.metrics
                
                keywords_data.append({
                    "campaign_id": campaign.id,
                    "campaign_name": campaign.name,
                    "ad_group_id": ad_group.id,
                    "ad_group_name": ad_group.name,
                    "keyword": keyword.text,
                    "match_type": keyword.match_type.name,
                    "impressions": metrics.impressions,
                    "clicks": metrics.clicks,
                    "ctr": metrics.ctr,
                    "average_cpc": metrics.average_cpc / 1_000_000 if metrics.average_cpc else 0,
                    "cost": metrics.cost_micros / 1_000_000 if metrics.cost_micros else 0,
                    "conversions": metrics.conversions,
                    "conversions_value": metrics.conversions_value,
                    "quality_score": metrics.quality_score if hasattr(metrics, 'quality_score') else None
                })
            
            logger.info(f"Kulcsszó teljesítmény adatok lekérdezve: {len(keywords_data)} rekord")
            return keywords_data
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API hiba: {ex}")
            raise
        except Exception as e:
            logger.error(f"Hiba a kulcsszó adatok lekérdezésekor: {e}")
            raise


# Singleton instance
_google_ads_service: Optional[GoogleAdsService] = None


def get_google_ads_service(config_file: str = "google-ads.yaml") -> GoogleAdsService:
    """
    Visszaadja a Google Ads szolgáltatás singleton instance-t
    
    Args:
        config_file: Konfiguráció fájl elérési útja
        
    Returns:
        GoogleAdsService instance
    """
    global _google_ads_service
    if _google_ads_service is None:
        _google_ads_service = GoogleAdsService(config_file)
    return _google_ads_service

