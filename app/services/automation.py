"""
Automatizációs szolgáltatások
"""
from typing import List, Dict, Any, Optional
from loguru import logger
from datetime import datetime
import json


class AutomationService:
    """Automatizációs szolgáltatás osztály"""
    
    def __init__(self):
        """Inicializálja az automatizációs szolgáltatást"""
        self.automation_rules = {}
        self.automation_history = []
    
    def create_bid_optimization_rule(
        self,
        customer_id: str,
        campaign_id: str,
        target_roas: Optional[float] = None,
        target_cpa: Optional[float] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Létrehoz egy bid optimalizálási szabályt
        
        Args:
            customer_id: Google Ads ügyfél azonosító
            campaign_id: Kampány azonosító
            target_roas: Cél ROAS érték
            target_cpa: Cél CPA érték
            enabled: Szabály engedélyezve van-e
            
        Returns:
            Létrehozott szabály adatai
        """
        rule_id = f"bid_opt_{customer_id}_{campaign_id}_{datetime.now().timestamp()}"
        
        rule = {
            "rule_id": rule_id,
            "type": "bid_optimization",
            "customer_id": customer_id,
            "campaign_id": campaign_id,
            "target_roas": target_roas,
            "target_cpa": target_cpa,
            "enabled": enabled,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "status": "active" if enabled else "paused"
        }
        
        self.automation_rules[rule_id] = rule
        
        logger.info(f"Bid optimalizálási szabály létrehozva: {rule_id}")
        
        return {
            "success": True,
            "message": "Bid optimalizálási szabály sikeresen létrehozva",
            "rule": rule
        }
    
    def apply_bid_optimization(
        self,
        rule_id: str,
        performance_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Alkalmaz egy bid optimalizálási szabályt
        
        Args:
            rule_id: Szabály azonosító
            performance_data: Kampány teljesítmény adatok
            
        Returns:
            Optimalizálás eredménye
        """
        if rule_id not in self.automation_rules:
            return {
                "success": False,
                "message": "Szabály nem található"
            }
        
        rule = self.automation_rules[rule_id]
        
        if not rule["enabled"]:
            return {
                "success": False,
                "message": "Szabály nincs engedélyezve"
            }
        
        recommendations = []
        
        # ROAS alapú optimalizálás
        if rule["target_roas"] is not None:
            current_roas = performance_data.get("roas", 0)
            
            if current_roas < rule["target_roas"]:
                # ROAS alacsony - csökkenteni kell a bid-et
                bid_adjustment = -10  # 10% csökkentés
                recommendations.append({
                    "action": "decrease_bid",
                    "reason": f"ROAS ({current_roas:.2f}) alacsonyabb mint a cél ({rule['target_roas']:.2f})",
                    "adjustment_percent": bid_adjustment,
                    "priority": "high"
                })
            elif current_roas > rule["target_roas"] * 1.5:
                # ROAS nagyon magas - növelni lehet a bid-et
                bid_adjustment = 15  # 15% növelés
                recommendations.append({
                    "action": "increase_bid",
                    "reason": f"ROAS ({current_roas:.2f}) jelentősen magasabb mint a cél ({rule['target_roas']:.2f})",
                    "adjustment_percent": bid_adjustment,
                    "priority": "medium"
                })
        
        # CPA alapú optimalizálás
        if rule["target_cpa"] is not None:
            current_cpa = performance_data.get("cost_per_conversion", 0)
            
            if current_cpa > rule["target_cpa"]:
                # CPA magas - csökkenteni kell a bid-et
                bid_adjustment = -15  # 15% csökkentés
                recommendations.append({
                    "action": "decrease_bid",
                    "reason": f"CPA ({current_cpa:.2f}) magasabb mint a cél ({rule['target_cpa']:.2f})",
                    "adjustment_percent": bid_adjustment,
                    "priority": "high"
                })
            elif current_cpa < rule["target_cpa"] * 0.7:
                # CPA alacsony - növelni lehet a bid-et
                bid_adjustment = 10  # 10% növelés
                recommendations.append({
                    "action": "increase_bid",
                    "reason": f"CPA ({current_cpa:.2f}) jelentősen alacsonyabb mint a cél ({rule['target_cpa']:.2f})",
                    "adjustment_percent": bid_adjustment,
                    "priority": "medium"
                })
        
        # Szabály frissítése
        rule["last_run"] = datetime.now().isoformat()
        
        # Történet mentése
        self.automation_history.append({
            "rule_id": rule_id,
            "timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "performance_data": performance_data
        })
        
        logger.info(f"Bid optimalizálás alkalmazva: {rule_id}, {len(recommendations)} ajánlás")
        
        return {
            "success": True,
            "message": "Bid optimalizálás sikeresen alkalmazva",
            "recommendations": recommendations,
            "rule": rule
        }
    
    def create_budget_optimization_rule(
        self,
        customer_id: str,
        campaign_ids: List[str],
        total_budget: float,
        optimization_goal: str = "maximize_conversions",
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Létrehoz egy költségvetés optimalizálási szabályt
        
        Args:
            customer_id: Google Ads ügyfél azonosító
            campaign_ids: Kampány azonosítók listája
            total_budget: Teljes elérhető költségvetés
            optimization_goal: Optimalizálási cél
            enabled: Szabály engedélyezve van-e
            
        Returns:
            Létrehozott szabály adatai
        """
        rule_id = f"budget_opt_{customer_id}_{datetime.now().timestamp()}"
        
        rule = {
            "rule_id": rule_id,
            "type": "budget_optimization",
            "customer_id": customer_id,
            "campaign_ids": campaign_ids,
            "total_budget": total_budget,
            "optimization_goal": optimization_goal,
            "enabled": enabled,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "status": "active" if enabled else "paused"
        }
        
        self.automation_rules[rule_id] = rule
        
        logger.info(f"Költségvetés optimalizálási szabály létrehozva: {rule_id}")
        
        return {
            "success": True,
            "message": "Költségvetés optimalizálási szabály sikeresen létrehozva",
            "rule": rule
        }
    
    def create_alert_rule(
        self,
        customer_id: str,
        campaign_id: Optional[str] = None,
        metric: str = "roas",
        threshold: float = 2.0,
        condition: str = "below",  # below, above
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Létrehoz egy riasztási szabályt
        
        Args:
            customer_id: Google Ads ügyfél azonosító
            campaign_id: Kampány azonosító (opcionális)
            metric: Metrika (roas, cpa, ctr, stb.)
            threshold: Küszöbérték
            condition: Feltétel (below, above)
            enabled: Szabály engedélyezve van-e
            
        Returns:
            Létrehozott szabály adatai
        """
        rule_id = f"alert_{customer_id}_{metric}_{datetime.now().timestamp()}"
        
        rule = {
            "rule_id": rule_id,
            "type": "alert",
            "customer_id": customer_id,
            "campaign_id": campaign_id,
            "metric": metric,
            "threshold": threshold,
            "condition": condition,
            "enabled": enabled,
            "created_at": datetime.now().isoformat(),
            "last_triggered": None,
            "status": "active" if enabled else "paused"
        }
        
        self.automation_rules[rule_id] = rule
        
        logger.info(f"Riasztási szabály létrehozva: {rule_id}")
        
        return {
            "success": True,
            "message": "Riasztási szabály sikeresen létrehozva",
            "rule": rule
        }
    
    def check_alert_rules(
        self,
        performance_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Ellenőrzi a riasztási szabályokat a teljesítmény adatok alapján
        
        Args:
            performance_data: Kampány teljesítmény adatok
            
        Returns:
            Kiváltott riasztások listája
        """
        triggered_alerts = []
        
        for rule_id, rule in self.automation_rules.items():
            if rule["type"] != "alert" or not rule["enabled"]:
                continue
            
            metric = rule["metric"]
            threshold = rule["threshold"]
            condition = rule["condition"]
            
            for campaign_data in performance_data:
                # Ha van megadva campaign_id, csak azt ellenőrizzük
                if rule["campaign_id"] and str(campaign_data.get("campaign_id")) != str(rule["campaign_id"]):
                    continue
                
                if metric not in campaign_data:
                    continue
                
                metric_value = campaign_data[metric]
                
                triggered = False
                if condition == "below" and metric_value < threshold:
                    triggered = True
                elif condition == "above" and metric_value > threshold:
                    triggered = True
                
                if triggered:
                    alert = {
                        "rule_id": rule_id,
                        "campaign_id": campaign_data.get("campaign_id"),
                        "campaign_name": campaign_data.get("campaign_name"),
                        "metric": metric,
                        "metric_value": metric_value,
                        "threshold": threshold,
                        "condition": condition,
                        "message": f"{metric.upper()} ({metric_value:.2f}) is {condition} threshold ({threshold:.2f})",
                        "triggered_at": datetime.now().isoformat()
                    }
                    
                    triggered_alerts.append(alert)
                    
                    # Szabály frissítése
                    rule["last_triggered"] = datetime.now().isoformat()
        
        if triggered_alerts:
            logger.warning(f"{len(triggered_alerts)} riasztás kiváltva")
        
        return triggered_alerts
    
    def get_automation_rules(
        self,
        rule_type: Optional[str] = None,
        enabled_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Lekérdezi az automatizálási szabályokat
        
        Args:
            rule_type: Szabály típus szűrő (opcionális)
            enabled_only: Csak az engedélyezett szabályok
            
        Returns:
            Szabályok listája
        """
        rules = list(self.automation_rules.values())
        
        if rule_type:
            rules = [r for r in rules if r["type"] == rule_type]
        
        if enabled_only:
            rules = [r for r in rules if r["enabled"]]
        
        return rules
    
    def update_automation_rule(
        self,
        rule_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Frissít egy automatizálási szabályt
        
        Args:
            rule_id: Szabály azonosító
            updates: Frissítendő mezők
            
        Returns:
            Frissített szabály
        """
        if rule_id not in self.automation_rules:
            return {
                "success": False,
                "message": "Szabály nem található"
            }
        
        rule = self.automation_rules[rule_id]
        
        # Frissítések alkalmazása
        for key, value in updates.items():
            if key in rule:
                rule[key] = value
        
        rule["updated_at"] = datetime.now().isoformat()
        
        logger.info(f"Automatizálási szabály frissítve: {rule_id}")
        
        return {
            "success": True,
            "message": "Szabály sikeresen frissítve",
            "rule": rule
        }
    
    def delete_automation_rule(self, rule_id: str) -> Dict[str, Any]:
        """
        Töröl egy automatizálási szabályt
        
        Args:
            rule_id: Szabály azonosító
            
        Returns:
            Törlés eredménye
        """
        if rule_id not in self.automation_rules:
            return {
                "success": False,
                "message": "Szabály nem található"
            }
        
        del self.automation_rules[rule_id]
        
        logger.info(f"Automatizálási szabály törölve: {rule_id}")
        
        return {
            "success": True,
            "message": "Szabály sikeresen törölve"
        }
    
    def get_automation_history(
        self,
        rule_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Lekérdezi az automatizálási történetet
        
        Args:
            rule_id: Szabály azonosító szűrő (opcionális)
            limit: Maximum rekordok száma
            
        Returns:
            Történet rekordok listája
        """
        history = self.automation_history
        
        if rule_id:
            history = [h for h in history if h["rule_id"] == rule_id]
        
        # Legutóbbi rekordok először
        history = sorted(history, key=lambda x: x["timestamp"], reverse=True)
        
        return history[:limit]


# Singleton instance
_automation_service: Optional[AutomationService] = None


def get_automation_service() -> AutomationService:
    """
    Visszaadja az automatizációs szolgáltatás singleton instance-t
    
    Returns:
        AutomationService instance
    """
    global _automation_service
    if _automation_service is None:
        _automation_service = AutomationService()
    return _automation_service

