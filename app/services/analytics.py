"""
Adatelemzési szolgáltatások
"""
from typing import List, Dict, Any, Optional
from loguru import logger
import pandas as pd
from datetime import datetime


class AnalyticsService:
    """Adatelemzési szolgáltatás osztály"""
    
    def __init__(self):
        """Inicializálja az elemzési szolgáltatást"""
        pass
    
    def analyze_campaign_performance(
        self,
        performance_data: List[Dict[str, Any]],
        thresholds: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Elemzi a kampány teljesítményt és betekintéseket ad
        
        Args:
            performance_data: Kampány teljesítmény adatok
            thresholds: Küszöbértékek (ROAS, CPA, CTR)
            
        Returns:
            Elemzési eredmények és ajánlások
        """
        if not performance_data:
            return {
                "insights": [],
                "summary": {},
                "recommendations": []
            }
        
        # Default küszöbértékek
        if thresholds is None:
            thresholds = {
                "min_roas": 2.0,
                "max_cpa": 50.0,
                "min_ctr": 0.01
            }
        
        df = pd.DataFrame(performance_data)
        
        insights = []
        recommendations = []
        
        # ROAS elemzés
        if 'roas' in df.columns:
            low_roas_campaigns = df[df['roas'] < thresholds['min_roas']]
            if not low_roas_campaigns.empty:
                insights.append({
                    "type": "low_roas",
                    "severity": "warning",
                    "message": f"{len(low_roas_campaigns)} kampány ROAS értéke a küszöb ({thresholds['min_roas']}) alatt van",
                    "affected_campaigns": low_roas_campaigns['campaign_name'].tolist(),
                    "metric_value": low_roas_campaigns['roas'].mean()
                })
                recommendations.append({
                    "type": "roas_optimization",
                    "message": "Fontold meg az alacsony ROAS-ú kampányok költségvetésének csökkentését vagy optimalizálását",
                    "campaigns": low_roas_campaigns['campaign_name'].tolist()
                })
        
        # CPA elemzés
        if 'cost_per_conversion' in df.columns:
            high_cpa_campaigns = df[df['cost_per_conversion'] > thresholds['max_cpa']]
            if not high_cpa_campaigns.empty:
                insights.append({
                    "type": "high_cpa",
                    "severity": "warning",
                    "message": f"{len(high_cpa_campaigns)} kampány CPA értéke a küszöb ({thresholds['max_cpa']}) felett van",
                    "affected_campaigns": high_cpa_campaigns['campaign_name'].tolist(),
                    "metric_value": high_cpa_campaigns['cost_per_conversion'].mean()
                })
                recommendations.append({
                    "type": "cpa_optimization",
                    "message": "Optimalizáld a magas CPA-jú kampányok kulcsszavait és ajánlatait",
                    "campaigns": high_cpa_campaigns['campaign_name'].tolist()
                })
        
        # CTR elemzés
        if 'ctr' in df.columns:
            low_ctr_campaigns = df[df['ctr'] < thresholds['min_ctr']]
            if not low_ctr_campaigns.empty:
                insights.append({
                    "type": "low_ctr",
                    "severity": "info",
                    "message": f"{len(low_ctr_campaigns)} kampány CTR értéke alacsony ({thresholds['min_ctr']} alatt)",
                    "affected_campaigns": low_ctr_campaigns['campaign_name'].tolist(),
                    "metric_value": low_ctr_campaigns['ctr'].mean()
                })
                recommendations.append({
                    "type": "ctr_improvement",
                    "message": "Javítsd a hirdetés szövegeket és relevanciát az alacsony CTR-ű kampányokban",
                    "campaigns": low_ctr_campaigns['campaign_name'].tolist()
                })
        
        # Költség elemzés
        if 'cost' in df.columns:
            total_cost = df['cost'].sum()
            top_spending = df.nlargest(5, 'cost')
            
            insights.append({
                "type": "spending_distribution",
                "severity": "info",
                "message": f"Top 5 kampány a teljes költség {(top_spending['cost'].sum() / total_cost * 100):.1f}%-át teszi ki",
                "affected_campaigns": top_spending['campaign_name'].tolist(),
                "metric_value": top_spending['cost'].sum()
            })
        
        # Konverzió elemzés
        if 'conversions' in df.columns and 'cost' in df.columns:
            zero_conversion_campaigns = df[df['conversions'] == 0]
            if not zero_conversion_campaigns.empty and zero_conversion_campaigns['cost'].sum() > 0:
                insights.append({
                    "type": "zero_conversions",
                    "severity": "critical",
                    "message": f"{len(zero_conversion_campaigns)} kampány nem generált konverziót, de költött {zero_conversion_campaigns['cost'].sum():.2f} egységet",
                    "affected_campaigns": zero_conversion_campaigns['campaign_name'].tolist(),
                    "metric_value": zero_conversion_campaigns['cost'].sum()
                })
                recommendations.append({
                    "type": "zero_conversion_action",
                    "message": "Vizsgáld felül vagy szüneteltesd a konverzió nélküli kampányokat",
                    "campaigns": zero_conversion_campaigns['campaign_name'].tolist()
                })
        
        # Összefoglaló statisztikák
        summary = {
            "total_campaigns": len(df),
            "total_cost": float(df['cost'].sum()) if 'cost' in df.columns else 0,
            "total_conversions": float(df['conversions'].sum()) if 'conversions' in df.columns else 0,
            "total_clicks": int(df['clicks'].sum()) if 'clicks' in df.columns else 0,
            "total_impressions": int(df['impressions'].sum()) if 'impressions' in df.columns else 0,
            "average_roas": float(df['roas'].mean()) if 'roas' in df.columns else 0,
            "average_ctr": float(df['ctr'].mean()) if 'ctr' in df.columns else 0,
            "average_cpc": float(df['average_cpc'].mean()) if 'average_cpc' in df.columns else 0
        }
        
        logger.info(f"Kampány teljesítmény elemzés kész: {len(insights)} betekintés, {len(recommendations)} ajánlás")
        
        return {
            "insights": insights,
            "summary": summary,
            "recommendations": recommendations,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def analyze_keyword_performance(
        self,
        keywords_data: List[Dict[str, Any]],
        min_impressions: int = 100
    ) -> Dict[str, Any]:
        """
        Elemzi a kulcsszavak teljesítményét
        
        Args:
            keywords_data: Kulcsszó teljesítmény adatok
            min_impressions: Minimum impressions szűrő
            
        Returns:
            Kulcsszó elemzési eredmények
        """
        if not keywords_data:
            return {
                "insights": [],
                "top_performers": [],
                "underperformers": [],
                "summary": {}
            }
        
        df = pd.DataFrame(keywords_data)
        
        # Szűrés minimum impressions alapján
        df_filtered = df[df['impressions'] >= min_impressions]
        
        insights = []
        
        # Top teljesítők (magas CTR és konverzió)
        top_performers = []
        if 'ctr' in df_filtered.columns and 'conversions' in df_filtered.columns:
            top_df = df_filtered.nlargest(10, 'conversions')
            top_performers = top_df.to_dict('records')
            
            insights.append({
                "type": "top_keywords",
                "severity": "info",
                "message": f"Top 10 kulcsszó generálta a konverziók {(top_df['conversions'].sum() / df['conversions'].sum() * 100):.1f}%-át",
                "metric_value": top_df['conversions'].sum()
            })
        
        # Alulteljesítők (magas költség, alacsony konverzió)
        underperformers = []
        if 'cost' in df_filtered.columns and 'conversions' in df_filtered.columns:
            # Kulcsszavak amelyek költöttek de nem konvertáltak
            underperform_df = df_filtered[(df_filtered['cost'] > 10) & (df_filtered['conversions'] == 0)]
            if not underperform_df.empty:
                underperformers = underperform_df.nlargest(10, 'cost').to_dict('records')
                
                insights.append({
                    "type": "underperforming_keywords",
                    "severity": "warning",
                    "message": f"{len(underperform_df)} kulcsszó költött de nem konvertált",
                    "metric_value": underperform_df['cost'].sum()
                })
        
        # Quality Score elemzés
        if 'quality_score' in df_filtered.columns:
            low_qs = df_filtered[df_filtered['quality_score'] < 5]
            if not low_qs.empty:
                insights.append({
                    "type": "low_quality_score",
                    "severity": "warning",
                    "message": f"{len(low_qs)} kulcsszó Quality Score-ja 5 alatt van",
                    "metric_value": low_qs['quality_score'].mean()
                })
        
        # Match type elemzés
        if 'match_type' in df.columns:
            match_type_performance = df.groupby('match_type').agg({
                'cost': 'sum',
                'conversions': 'sum',
                'clicks': 'sum'
            }).to_dict('index')
            
            insights.append({
                "type": "match_type_distribution",
                "severity": "info",
                "message": "Match type teljesítmény eloszlás",
                "data": match_type_performance
            })
        
        summary = {
            "total_keywords": len(df),
            "analyzed_keywords": len(df_filtered),
            "total_cost": float(df['cost'].sum()) if 'cost' in df.columns else 0,
            "total_conversions": float(df['conversions'].sum()) if 'conversions' in df.columns else 0,
            "average_ctr": float(df['ctr'].mean()) if 'ctr' in df.columns else 0,
            "average_quality_score": float(df['quality_score'].mean()) if 'quality_score' in df.columns else None
        }
        
        logger.info(f"Kulcsszó teljesítmény elemzés kész: {len(insights)} betekintés")
        
        return {
            "insights": insights,
            "top_performers": top_performers,
            "underperformers": underperformers,
            "summary": summary,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def compare_campaigns(
        self,
        performance_data: List[Dict[str, Any]],
        metric: str = "roas"
    ) -> Dict[str, Any]:
        """
        Összehasonlítja a kampányokat egy adott metrika alapján
        
        Args:
            performance_data: Kampány teljesítmény adatok
            metric: Összehasonlítási metrika (roas, ctr, cost_per_conversion, stb.)
            
        Returns:
            Összehasonlítási eredmények
        """
        if not performance_data:
            return {"error": "Nincs adat az összehasonlításhoz"}
        
        df = pd.DataFrame(performance_data)
        
        if metric not in df.columns:
            return {"error": f"A metrika '{metric}' nem található az adatokban"}
        
        # Rendezés a metrika szerint
        sorted_df = df.sort_values(by=metric, ascending=False)
        
        # Statisztikák
        stats = {
            "metric": metric,
            "best_campaign": {
                "name": sorted_df.iloc[0]['campaign_name'],
                "value": float(sorted_df.iloc[0][metric])
            },
            "worst_campaign": {
                "name": sorted_df.iloc[-1]['campaign_name'],
                "value": float(sorted_df.iloc[-1][metric])
            },
            "average": float(df[metric].mean()),
            "median": float(df[metric].median()),
            "std_dev": float(df[metric].std()),
            "rankings": sorted_df[['campaign_name', metric]].to_dict('records')
        }
        
        return stats
    
    def calculate_budget_allocation(
        self,
        performance_data: List[Dict[str, Any]],
        total_budget: float,
        optimization_goal: str = "maximize_conversions"
    ) -> Dict[str, Any]:
        """
        Kiszámítja az optimális költségvetés elosztást
        
        Args:
            performance_data: Kampány teljesítmény adatok
            total_budget: Teljes elérhető költségvetés
            optimization_goal: Optimalizálási cél (maximize_conversions, maximize_roas)
            
        Returns:
            Költségvetés elosztási javaslat
        """
        if not performance_data:
            return {"error": "Nincs adat a költségvetés elosztáshoz"}
        
        df = pd.DataFrame(performance_data)
        
        allocations = []
        
        if optimization_goal == "maximize_conversions":
            # Költségvetés elosztás konverziós arány alapján
            if 'conversion_rate' in df.columns and 'cost' in df.columns:
                df['weight'] = df['conversion_rate'] * df['cost']
                total_weight = df['weight'].sum()
                
                for _, row in df.iterrows():
                    allocated_budget = (row['weight'] / total_weight) * total_budget if total_weight > 0 else 0
                    allocations.append({
                        "campaign_id": row['campaign_id'],
                        "campaign_name": row['campaign_name'],
                        "current_budget": row.get('cost', 0),
                        "recommended_budget": round(allocated_budget, 2),
                        "change_percent": round(((allocated_budget - row.get('cost', 0)) / row.get('cost', 1)) * 100, 2) if row.get('cost', 0) > 0 else 0
                    })
        
        elif optimization_goal == "maximize_roas":
            # Költségvetés elosztás ROAS alapján
            if 'roas' in df.columns and 'cost' in df.columns:
                df['weight'] = df['roas'] * df['cost']
                total_weight = df['weight'].sum()
                
                for _, row in df.iterrows():
                    allocated_budget = (row['weight'] / total_weight) * total_budget if total_weight > 0 else 0
                    allocations.append({
                        "campaign_id": row['campaign_id'],
                        "campaign_name": row['campaign_name'],
                        "current_budget": row.get('cost', 0),
                        "recommended_budget": round(allocated_budget, 2),
                        "change_percent": round(((allocated_budget - row.get('cost', 0)) / row.get('cost', 1)) * 100, 2) if row.get('cost', 0) > 0 else 0
                    })
        
        return {
            "optimization_goal": optimization_goal,
            "total_budget": total_budget,
            "allocations": sorted(allocations, key=lambda x: x['recommended_budget'], reverse=True)
        }


# Singleton instance
_analytics_service: Optional[AnalyticsService] = None


def get_analytics_service() -> AnalyticsService:
    """
    Visszaadja az elemzési szolgáltatás singleton instance-t
    
    Returns:
        AnalyticsService instance
    """
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    return _analytics_service

