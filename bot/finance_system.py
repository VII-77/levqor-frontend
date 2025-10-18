"""
Finance & Revenue Tracking System
Handles P&L, revenue dashboards, margin calculations, and valuation
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from notion_client import Client
import statistics


class FinanceSystem:
    """Comprehensive finance tracking and reporting"""
    
    def __init__(self, notion_client=None):
        self.notion = notion_client or Client(auth=os.getenv('NOTION_TOKEN'))
        self.finance_db_id = os.getenv('NOTION_FINANCE_DB_ID')
        self.job_log_db_id = os.getenv('JOB_LOG_DB_ID')
        self.client_db_id = os.getenv('NOTION_CLIENT_DB_ID')
    
    def record_transaction(
        self,
        transaction_type: str,
        amount: float,
        currency: str = "USD",
        client: str = None,
        job_id: str = None,
        category: str = None,
        stripe_payment_id: str = None,
        notes: str = None
    ) -> Dict[str, Any]:
        """Record a financial transaction"""
        
        if not self.finance_db_id:
            return {"ok": False, "error": "Finance database not configured"}
        
        try:
            transaction_id = f"TXN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            properties = {
                "Transaction ID": {"title": [{"text": {"content": transaction_id}}]},
                "Date": {"date": {"start": datetime.utcnow().isoformat()}},
                "Type": {"select": {"name": transaction_type}},
                "Amount": {"number": amount},
                "Currency": {"select": {"name": currency}},
            }
            
            if client:
                properties["Client"] = {"rich_text": [{"text": {"content": client}}]}
            if job_id:
                properties["Job ID"] = {"rich_text": [{"text": {"content": job_id}}]}
            if category:
                properties["Category"] = {"select": {"name": category}}
            if stripe_payment_id:
                properties["Stripe Payment ID"] = {"rich_text": [{"text": {"content": stripe_payment_id}}]}
            if notes:
                properties["Notes"] = {"rich_text": [{"text": {"content": notes}}]}
            
            page = self.notion.pages.create(
                parent={"database_id": self.finance_db_id},
                properties=properties
            )
            
            return {"ok": True, "transaction_id": transaction_id, "page_id": page['id']}
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def get_revenue_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get revenue summary for specified period"""
        
        if not self.finance_db_id:
            return {"ok": False, "error": "Finance database not configured"}
        
        try:
            start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            # Query finance database
            response = self.notion.databases.query(
                database_id=self.finance_db_id,
                filter={
                    "and": [
                        {"property": "Date", "date": {"on_or_after": start_date}},
                        {"property": "Type", "select": {"equals": "Revenue"}}
                    ]
                }
            )
            
            total_revenue = sum(
                page['properties']['Amount']['number'] or 0
                for page in response['results']
            )
            
            return {
                "ok": True,
                "period_days": days,
                "total_revenue": total_revenue,
                "transaction_count": len(response['results']),
                "currency": "USD"
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def get_costs_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get costs summary for specified period"""
        
        if not self.finance_db_id:
            return {"ok": False, "error": "Finance database not configured"}
        
        try:
            start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            response = self.notion.databases.query(
                database_id=self.finance_db_id,
                filter={
                    "and": [
                        {"property": "Date", "date": {"on_or_after": start_date}},
                        {"property": "Type", "select": {"equals": "Cost"}}
                    ]
                }
            )
            
            total_costs = sum(
                page['properties']['Amount']['number'] or 0
                for page in response['results']
            )
            
            # Break down by category
            by_category = {}
            for page in response['results']:
                category = page['properties'].get('Category', {}).get('select', {}).get('name', 'Uncategorized')
                amount = page['properties']['Amount']['number'] or 0
                by_category[category] = by_category.get(category, 0) + amount
            
            return {
                "ok": True,
                "period_days": days,
                "total_costs": total_costs,
                "by_category": by_category,
                "transaction_count": len(response['results']),
                "currency": "USD"
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def calculate_margin(self, days: int = 30) -> Dict[str, Any]:
        """Calculate profit margin for period"""
        
        revenue_summary = self.get_revenue_summary(days)
        costs_summary = self.get_costs_summary(days)
        
        if not revenue_summary['ok'] or not costs_summary['ok']:
            return {"ok": False, "error": "Could not fetch revenue or costs"}
        
        revenue = revenue_summary['total_revenue']
        costs = costs_summary['total_costs']
        profit = revenue - costs
        margin_pct = (profit / revenue * 100) if revenue > 0 else 0
        
        return {
            "ok": True,
            "period_days": days,
            "revenue": revenue,
            "costs": costs,
            "profit": profit,
            "margin_pct": round(margin_pct, 2),
            "currency": "USD"
        }
    
    def get_refund_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get refund statistics"""
        
        if not self.finance_db_id:
            return {"ok": False, "error": "Finance database not configured"}
        
        try:
            start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            response = self.notion.databases.query(
                database_id=self.finance_db_id,
                filter={
                    "and": [
                        {"property": "Date", "date": {"on_or_after": start_date}},
                        {"property": "Type", "select": {"equals": "Refund"}}
                    ]
                }
            )
            
            total_refunds = sum(
                page['properties']['Amount']['number'] or 0
                for page in response['results']
            )
            
            # Get revenue for comparison
            revenue_summary = self.get_revenue_summary(days)
            revenue = revenue_summary.get('total_revenue', 0) if revenue_summary['ok'] else 0
            
            refund_pct = (total_refunds / revenue * 100) if revenue > 0 else 0
            
            return {
                "ok": True,
                "period_days": days,
                "total_refunds": total_refunds,
                "refund_count": len(response['results']),
                "refund_pct": round(refund_pct, 2),
                "currency": "USD"
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def generate_pl_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate Profit & Loss report"""
        
        margin = self.calculate_margin(days)
        refunds = self.get_refund_stats(days)
        costs = self.get_costs_summary(days)
        
        if not margin['ok']:
            return {"ok": False, "error": "Could not generate P&L"}
        
        return {
            "ok": True,
            "report_type": "P&L Statement",
            "period_days": days,
            "period_end": datetime.utcnow().strftime("%Y-%m-%d"),
            "revenue": {
                "gross_revenue": margin['revenue'],
                "refunds": refunds.get('total_refunds', 0) if refunds['ok'] else 0,
                "net_revenue": margin['revenue'] - (refunds.get('total_refunds', 0) if refunds['ok'] else 0)
            },
            "costs": {
                "total_costs": margin['costs'],
                "breakdown": costs.get('by_category', {}) if costs['ok'] else {}
            },
            "profit": {
                "gross_profit": margin['profit'],
                "margin_pct": margin['margin_pct']
            },
            "kpis": {
                "refund_rate": refunds.get('refund_pct', 0) if refunds['ok'] else 0
            },
            "currency": "USD"
        }
    
    def calculate_valuation_dcf(self, monthly_revenue: float, growth_rate: float = 0.05, discount_rate: float = 0.1, years: int = 5) -> Dict[str, Any]:
        """Calculate company valuation using Discounted Cash Flow (DCF)"""
        
        # Simple DCF model
        cash_flows = []
        for year in range(1, years + 1):
            revenue = monthly_revenue * 12 * ((1 + growth_rate) ** year)
            # Assume 30% profit margin (adjust based on actual)
            profit = revenue * 0.30
            discounted = profit / ((1 + discount_rate) ** year)
            cash_flows.append({
                "year": year,
                "revenue": round(revenue, 2),
                "profit": round(profit, 2),
                "discounted_cf": round(discounted, 2)
            })
        
        dcf_value = sum(cf['discounted_cf'] for cf in cash_flows)
        
        # Terminal value (perpetuity growth model)
        terminal_growth = 0.02
        terminal_cf = cash_flows[-1]['profit'] * (1 + terminal_growth)
        terminal_value = terminal_cf / (discount_rate - terminal_growth)
        discounted_terminal = terminal_value / ((1 + discount_rate) ** years)
        
        total_value = dcf_value + discounted_terminal
        
        return {
            "ok": True,
            "method": "DCF (Discounted Cash Flow)",
            "assumptions": {
                "monthly_revenue": monthly_revenue,
                "growth_rate": growth_rate,
                "discount_rate": discount_rate,
                "years": years,
                "profit_margin": 0.30
            },
            "cash_flows": cash_flows,
            "dcf_value": round(dcf_value, 2),
            "terminal_value": round(discounted_terminal, 2),
            "total_valuation": round(total_value, 2),
            "currency": "USD"
        }
    
    def calculate_valuation_saas_multiple(self, monthly_revenue: float, multiple: float = 10) -> Dict[str, Any]:
        """Calculate valuation using SaaS revenue multiple"""
        
        arr = monthly_revenue * 12  # Annual Recurring Revenue
        valuation = arr * multiple
        
        return {
            "ok": True,
            "method": "SaaS Revenue Multiple",
            "monthly_revenue": monthly_revenue,
            "arr": round(arr, 2),
            "multiple": multiple,
            "valuation": round(valuation, 2),
            "currency": "USD",
            "note": "Industry multiples range from 5x (early stage) to 20x+ (high growth)"
        }
    
    def generate_valuation_pack(self, days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive valuation report"""
        
        # Get recent revenue
        revenue_summary = self.get_revenue_summary(days)
        
        if not revenue_summary['ok']:
            return {"ok": False, "error": "Could not fetch revenue data"}
        
        monthly_revenue = revenue_summary['total_revenue'] * (30 / days)  # Normalize to 30 days
        
        # Calculate both valuations
        dcf = self.calculate_valuation_dcf(monthly_revenue)
        saas_multiple = self.calculate_valuation_saas_multiple(monthly_revenue)
        
        # Get P&L for context
        pl = self.generate_pl_report(days)
        
        return {
            "ok": True,
            "report_type": "Valuation Pack",
            "generated_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "period_analyzed": f"Last {days} days",
            "financial_summary": pl if pl['ok'] else {},
            "valuations": {
                "dcf_model": dcf,
                "saas_multiple_model": saas_multiple,
                "valuation_range": {
                    "low": round(min(dcf['total_valuation'], saas_multiple['valuation']), 2),
                    "high": round(max(dcf['total_valuation'], saas_multiple['valuation']), 2),
                    "mid": round((dcf['total_valuation'] + saas_multiple['valuation']) / 2, 2)
                }
            },
            "currency": "USD"
        }
    
    def sync_stripe_to_finance(self, stripe_payment: Dict[str, Any]) -> Dict[str, Any]:
        """Sync Stripe payment to finance database"""
        
        amount = stripe_payment.get('amount', 0) / 100  # Stripe amounts are in cents
        customer = stripe_payment.get('customer', 'Unknown')
        payment_id = stripe_payment.get('id')
        
        return self.record_transaction(
            transaction_type="Revenue",
            amount=amount,
            currency="USD",
            client=customer,
            category="Service Revenue",
            stripe_payment_id=payment_id,
            notes=f"Stripe payment - {payment_id}"
        )
    
    def record_ai_cost(self, job_id: str, cost: float, model: str, tokens: int) -> Dict[str, Any]:
        """Record AI processing cost"""
        
        return self.record_transaction(
            transaction_type="Cost",
            amount=cost,
            currency="USD",
            job_id=job_id,
            category="AI Costs",
            notes=f"Model: {model}, Tokens: {tokens}"
        )


# Singleton instance
_finance_system = None

def get_finance_system() -> FinanceSystem:
    """Get or create finance system instance"""
    global _finance_system
    if _finance_system is None:
        _finance_system = FinanceSystem()
    return _finance_system
