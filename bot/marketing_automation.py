"""
Marketing Automation - Growth Metrics, Outreach, and Referral System
Implements minimum viable marketing features for customer acquisition
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
try:
    from bot.notion_api import get_notion_client
except:
    get_notion_client = None


class MarketingAutomation:
    """Marketing automation for growth and customer acquisition"""
    
    def __init__(self, notion_client=None):
        self.notion = notion_client
        if not self.notion and get_notion_client:
            try:
                self.notion = get_notion_client()
            except:
                pass
        
        self.growth_db_id = os.getenv('NOTION_GROWTH_METRICS_DB_ID')
        self.referrals_db_id = os.getenv('NOTION_REFERRALS_DB_ID')
        self.clients_db_id = os.getenv('NOTION_CLIENT_DB_ID')
    
    def track_growth_metric(
        self,
        metric_type: str,
        value: float,
        source: str = "Organic",
        campaign: str = "",
        cost: float = 0.0
    ) -> Dict[str, Any]:
        """
        Track a growth metric (Leads, Conversions, CAC, LTV, Churn)
        
        Args:
            metric_type: Type of metric (Leads, Conversions, CAC, LTV, Churn)
            value: Metric value
            source: Traffic source (Organic, Paid Ads, Referral, Partnership, Email)
            campaign: Campaign name (optional)
            cost: Cost associated with this metric
        
        Returns:
            Result dict with ok status
        """
        if not self.growth_db_id or not self.notion:
            return {"ok": False, "error": "Growth Metrics database not configured"}
        
        try:
            # Calculate ROI if applicable
            roi_pct = 0.0
            if cost > 0 and metric_type in ["Conversions", "LTV"]:
                roi_pct = ((value - cost) / cost) * 100
            
            properties = {
                "Date": {"title": [{"text": {"content": datetime.now().strftime("%Y-%m-%d")}}]},
                "Metric": {"select": {"name": metric_type}},
                "Value": {"number": value},
                "Source": {"select": {"name": source}},
                "Cost": {"number": cost},
                "ROI %": {"number": roi_pct}
            }
            
            if campaign:
                properties["Campaign"] = {"rich_text": [{"text": {"content": campaign}}]}
            
            self.notion.pages.create(
                parent={"database_id": self.growth_db_id},
                properties=properties
            )
            
            return {"ok": True, "metric": metric_type, "value": value}
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def create_referral_code(
        self,
        referrer: str,
        credit_amount: float = 10.0
    ) -> Dict[str, Any]:
        """
        Create a referral code for a customer
        
        Args:
            referrer: Customer name/email
            credit_amount: Credit amount in USD
        
        Returns:
            Dict with referral code and details
        """
        if not self.referrals_db_id or not self.notion:
            return {"ok": False, "error": "Referrals database not configured"}
        
        try:
            # Generate simple code (first 4 chars of name + random digits)
            import random
            code = f"{referrer[:4].upper()}{random.randint(1000, 9999)}"
            
            properties = {
                "Referral Code": {"title": [{"text": {"content": code}}]},
                "Referrer": {"rich_text": [{"text": {"content": referrer}}]},
                "Status": {"select": {"name": "Pending"}},
                "Credit Amount": {"number": credit_amount},
                "Applied": {"checkbox": False},
                "Created Date": {"date": {"start": datetime.now().isoformat()}}
            }
            
            self.notion.pages.create(
                parent={"database_id": self.referrals_db_id},
                properties=properties
            )
            
            return {
                "ok": True,
                "code": code,
                "credit": credit_amount,
                "referrer": referrer
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def apply_referral_credit(
        self,
        referral_code: str,
        referred_customer: str
    ) -> Dict[str, Any]:
        """
        Apply referral credit when a referred customer converts
        
        Args:
            referral_code: The referral code used
            referred_customer: New customer name/email
        
        Returns:
            Result dict with credit details
        """
        if not self.referrals_db_id or not self.notion:
            return {"ok": False, "error": "Referrals database not configured"}
        
        try:
            # Find referral code
            response = self.notion.databases.query(
                database_id=self.referrals_db_id,
                filter={
                    "property": "Referral Code",
                    "title": {"equals": referral_code}
                }
            )
            
            if not response['results']:
                return {"ok": False, "error": "Referral code not found"}
            
            page = response['results'][0]
            
            # Update with referred customer and mark as active
            self.notion.pages.update(
                page_id=page['id'],
                properties={
                    "Referred Customer": {"rich_text": [{"text": {"content": referred_customer}}]},
                    "Status": {"select": {"name": "Active"}},
                    "Conversion Date": {"date": {"start": datetime.now().isoformat()}}
                }
            )
            
            credit = page['properties'].get('Credit Amount', {}).get('number', 0)
            
            return {
                "ok": True,
                "code": referral_code,
                "credit_applied": credit,
                "customer": referred_customer
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def get_growth_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        Get growth metrics summary for last N days
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Dict with growth metrics summary
        """
        if not self.growth_db_id or not self.notion:
            return {
                "ok": True,
                "days": days,
                "leads": 0,
                "conversions": 0,
                "avg_cac": 0,
                "avg_ltv": 0,
                "roi_pct": 0,
                "note": "Growth Metrics database not configured"
            }
        
        try:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            response = self.notion.databases.query(
                database_id=self.growth_db_id,
                filter={
                    "property": "Date",
                    "date": {"on_or_after": start_date}
                }
            )
            
            # Aggregate metrics
            leads = 0
            conversions = 0
            total_cac = 0
            cac_count = 0
            total_ltv = 0
            ltv_count = 0
            total_cost = 0
            total_revenue = 0
            
            for page in response['results']:
                props = page['properties']
                metric = props.get('Metric', {}).get('select', {}).get('name', '')
                value = props.get('Value', {}).get('number', 0)
                cost = props.get('Cost', {}).get('number', 0)
                
                if metric == "Leads":
                    leads += value
                elif metric == "Conversions":
                    conversions += value
                    total_revenue += value
                elif metric == "CAC":
                    total_cac += value
                    cac_count += 1
                elif metric == "LTV":
                    total_ltv += value
                    ltv_count += 1
                
                total_cost += cost
            
            avg_cac = total_cac / cac_count if cac_count > 0 else 0
            avg_ltv = total_ltv / ltv_count if ltv_count > 0 else 0
            roi_pct = ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
            
            return {
                "ok": True,
                "days": days,
                "leads": int(leads),
                "conversions": int(conversions),
                "avg_cac": round(avg_cac, 2),
                "avg_ltv": round(avg_ltv, 2),
                "roi_pct": round(roi_pct, 1),
                "total_cost": round(total_cost, 2),
                "total_revenue": round(total_revenue, 2)
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def get_active_referrals_count(self) -> int:
        """Get count of active referral codes"""
        if not self.referrals_db_id or not self.notion:
            return 0
        
        try:
            response = self.notion.databases.query(
                database_id=self.referrals_db_id,
                filter={
                    "property": "Status",
                    "select": {"equals": "Active"}
                }
            )
            return len(response.get('results', []))
        except:
            return 0


# Singleton instance
_marketing_instance = None


def get_marketing_automation() -> MarketingAutomation:
    """Get singleton instance of marketing automation"""
    global _marketing_instance
    if _marketing_instance is None:
        _marketing_instance = MarketingAutomation()
    return _marketing_instance


# Example usage
"""
from bot.marketing_automation import get_marketing_automation

marketing = get_marketing_automation()

# Track a new lead
marketing.track_growth_metric("Leads", 1, source="Organic", campaign="Blog Post")

# Track a conversion
marketing.track_growth_metric("Conversions", 1, source="Referral", cost=5.0)

# Create referral code
result = marketing.create_referral_code("john@example.com", credit_amount=10.0)
print(f"Referral code: {result['code']}")

# Apply referral credit
marketing.apply_referral_credit("JOHN1234", "jane@example.com")

# Get growth summary
summary = marketing.get_growth_summary(30)
print(f"Leads: {summary['leads']}, Conversions: {summary['conversions']}")
"""
