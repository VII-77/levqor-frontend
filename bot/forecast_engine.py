"""
Forecast Engine - 30-day predictions for load and revenue
Uses historical data to predict future trends
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from notion_client import Client
import statistics


class ForecastEngine:
    """Predictive analytics for revenue and system load"""
    
    def __init__(self, notion_client=None):
        self.notion = notion_client or Client(auth=os.getenv('NOTION_TOKEN'))
        self.forecast_db_id = os.getenv('NOTION_FORECAST_DB_ID')
        self.job_log_db_id = os.getenv('JOB_LOG_DB_ID')
        self.finance_db_id = os.getenv('NOTION_FINANCE_DB_ID')
    
    def get_historical_load(self, days: int = 90) -> List[Dict[str, Any]]:
        """Get historical job load data"""
        if not self.job_log_db_id:
            return []
        
        try:
            start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            response = self.notion.databases.query(
                database_id=self.job_log_db_id,
                filter={"property": "Created Time", "date": {"on_or_after": start_date}}
            )
            
            # Group by day
            daily_counts = {}
            for page in response['results']:
                created = page['properties'].get('Created Time', {}).get('date', {}).get('start', '')
                if created:
                    date_key = created[:10]  # YYYY-MM-DD
                    daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
            
            # Convert to list
            historical = [
                {"date": date, "count": count}
                for date, count in sorted(daily_counts.items())
            ]
            
            return historical
        
        except Exception as e:
            print(f"Error getting historical load: {e}")
            return []
    
    def predict_load(self, historical_data: List[Dict[str, Any]], days_ahead: int = 30) -> List[Dict[str, Any]]:
        """Predict future load using simple linear regression"""
        
        if not historical_data or len(historical_data) < 7:
            return []
        
        # Extract counts
        counts = [d['count'] for d in historical_data]
        
        # Calculate trend using moving average
        window = min(7, len(counts))
        moving_avg = []
        for i in range(len(counts) - window + 1):
            window_data = counts[i:i+window]
            moving_avg.append(sum(window_data) / window)
        
        # Simple trend: difference between last and first moving average
        if len(moving_avg) >= 2:
            trend = (moving_avg[-1] - moving_avg[0]) / len(moving_avg)
        else:
            trend = 0
        
        # Recent average
        recent_avg = statistics.mean(counts[-14:]) if len(counts) >= 14 else statistics.mean(counts)
        
        # Generate predictions
        predictions = []
        last_date = datetime.strptime(historical_data[-1]['date'], "%Y-%m-%d")
        
        for day in range(1, days_ahead + 1):
            pred_date = last_date + timedelta(days=day)
            pred_value = max(0, recent_avg + (trend * day))
            
            predictions.append({
                "date": pred_date.strftime("%Y-%m-%d"),
                "predicted_count": round(pred_value, 2),
                "confidence": "Medium" if len(counts) >= 30 else "Low"
            })
        
        return predictions
    
    def predict_revenue(self, days_ahead: int = 30, avg_job_revenue: float = 10.0) -> List[Dict[str, Any]]:
        """Predict revenue based on load forecast"""
        
        historical = self.get_historical_load(90)
        load_forecast = self.predict_load(historical, days_ahead)
        
        revenue_forecast = []
        for pred in load_forecast:
            revenue = pred['predicted_count'] * avg_job_revenue
            revenue_forecast.append({
                "date": pred['date'],
                "predicted_revenue": round(revenue, 2),
                "predicted_jobs": round(pred['predicted_count']),
                "confidence": pred['confidence'],
                "currency": "USD"
            })
        
        return revenue_forecast
    
    def save_forecast(self, forecast_type: str, date: str, predicted_value: float, confidence: str = "Medium") -> Dict[str, Any]:
        """Save forecast to Notion database"""
        
        if not self.forecast_db_id:
            return {"ok": False, "error": "Forecast database not configured"}
        
        try:
            properties = {
                "Date": {"title": [{"text": {"content": date}}]},
                "Forecast Type": {"select": {"name": forecast_type}},
                "Predicted Value": {"number": predicted_value},
                "Confidence": {"select": {"name": confidence}},
                "Model Used": {"rich_text": [{"text": {"content": "Moving Average + Trend"}}]},
            }
            
            page = self.notion.pages.create(
                parent={"database_id": self.forecast_db_id},
                properties=properties
            )
            
            return {"ok": True, "page_id": page['id']}
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def generate_30day_forecast(self) -> Dict[str, Any]:
        """Generate comprehensive 30-day forecast"""
        
        # Get historical data
        historical_load = self.get_historical_load(90)
        
        if not historical_load:
            return {
                "ok": False,
                "error": "Insufficient historical data (need at least 7 days)"
            }
        
        # Generate forecasts
        load_forecast = self.predict_load(historical_load, 30)
        revenue_forecast = self.predict_revenue(30)
        
        # Calculate totals
        total_predicted_jobs = sum(f['predicted_jobs'] for f in revenue_forecast)
        total_predicted_revenue = sum(f['predicted_revenue'] for f in revenue_forecast)
        
        # Save key forecasts to database
        if self.forecast_db_id:
            for i, rev_pred in enumerate(revenue_forecast):
                if i % 7 == 0:  # Save weekly snapshots
                    self.save_forecast(
                        forecast_type="Revenue",
                        date=rev_pred['date'],
                        predicted_value=rev_pred['predicted_revenue'],
                        confidence=rev_pred['confidence']
                    )
        
        return {
            "ok": True,
            "generated_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "forecast_period": "30 days",
            "historical_data_points": len(historical_load),
            "summary": {
                "total_predicted_jobs": round(total_predicted_jobs),
                "total_predicted_revenue": round(total_predicted_revenue, 2),
                "avg_daily_jobs": round(total_predicted_jobs / 30, 2),
                "avg_daily_revenue": round(total_predicted_revenue / 30, 2),
                "currency": "USD"
            },
            "daily_forecasts": {
                "load": load_forecast,
                "revenue": revenue_forecast
            }
        }
    
    def get_forecast_chart_data(self) -> Dict[str, Any]:
        """Get forecast data in chart-friendly format (JSON + CSV)"""
        
        forecast = self.generate_30day_forecast()
        
        if not forecast['ok']:
            return forecast
        
        # JSON format
        chart_json = {
            "labels": [f['date'] for f in forecast['daily_forecasts']['revenue']],
            "datasets": [
                {
                    "label": "Predicted Revenue ($)",
                    "data": [f['predicted_revenue'] for f in forecast['daily_forecasts']['revenue']]
                },
                {
                    "label": "Predicted Jobs",
                    "data": [f['predicted_jobs'] for f in forecast['daily_forecasts']['revenue']]
                }
            ]
        }
        
        # CSV format
        csv_lines = ["Date,Predicted Jobs,Predicted Revenue ($),Confidence"]
        for f in forecast['daily_forecasts']['revenue']:
            csv_lines.append(f"{f['date']},{f['predicted_jobs']},{f['predicted_revenue']},{f['confidence']}")
        csv_data = "\n".join(csv_lines)
        
        return {
            "ok": True,
            "format": "Chart Data",
            "json": chart_json,
            "csv": csv_data,
            "summary": forecast['summary']
        }


# Singleton
_forecast_engine = None

def get_forecast_engine() -> ForecastEngine:
    """Get or create forecast engine instance"""
    global _forecast_engine
    if _forecast_engine is None:
        _forecast_engine = ForecastEngine()
    return _forecast_engine
