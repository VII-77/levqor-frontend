"""
Localization & Multi-Language Support
Translation, multi-currency, and regional compliance
"""

import os
from typing import Dict, List, Any, Optional


class LocalizationSystem:
    """Multi-language and regional compliance management"""
    
    def __init__(self, notion_client=None):
        if notion_client:
            self.notion = notion_client
        else:
            from bot.notion_api import get_notion_client
            self.notion = get_notion_client()
        self.region_db_id = os.getenv('NOTION_REGION_COMPLIANCE_DB_ID')
        
        # Translation dictionaries (simple approach - production would use i18n library)
        self.translations = {
            "en": {
                "task_completed": "Task completed successfully",
                "task_failed": "Task failed",
                "qa_score": "Quality Score",
                "welcome": "Welcome to EchoPilot",
                "payment_received": "Payment received",
                "refund_processed": "Refund processed"
            },
            "es": {
                "task_completed": "Tarea completada con éxito",
                "task_failed": "La tarea falló",
                "qa_score": "Puntuación de calidad",
                "welcome": "Bienvenido a EchoPilot",
                "payment_received": "Pago recibido",
                "refund_processed": "Reembolso procesado"
            },
            "ur": {
                "task_completed": "کام کامیابی سے مکمل ہو گیا",
                "task_failed": "کام ناکام ہو گیا",
                "qa_score": "معیار کا اسکور",
                "welcome": "EchoPilot میں خوش آمدید",
                "payment_received": "ادائیگی موصول ہوئی",
                "refund_processed": "رقم کی واپسی کی گئی"
            }
        }
        
        # Currency conversion rates (simplified - production would use live API)
        self.currency_rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79,
            "INR": 83.12,
            "PKR": 278.50
        }
    
    def translate(self, key: str, language: str = "en") -> str:
        """Translate a key to specified language"""
        
        lang = language.lower()
        if lang not in self.translations:
            lang = "en"  # Fallback to English
        
        return self.translations[lang].get(key, key)
    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate arbitrary text (simplified implementation)
        Production would use Google Translate API or similar
        """
        
        # For demo purposes, just return original text with language tag
        # In production, integrate with translation API
        if target_language == "en":
            return text
        
        return f"[{target_language.upper()}] {text}"
    
    def convert_currency(self, amount: float, from_currency: str = "USD", to_currency: str = "USD") -> Dict[str, Any]:
        """Convert amount between currencies"""
        
        if from_currency not in self.currency_rates or to_currency not in self.currency_rates:
            return {"ok": False, "error": "Currency not supported"}
        
        # Convert to USD first, then to target currency
        usd_amount = amount / self.currency_rates[from_currency]
        converted = usd_amount * self.currency_rates[to_currency]
        
        return {
            "ok": True,
            "original_amount": amount,
            "original_currency": from_currency,
            "converted_amount": round(converted, 2),
            "converted_currency": to_currency,
            "rate": round(self.currency_rates[to_currency] / self.currency_rates[from_currency], 4)
        }
    
    def get_regional_rules(self, country_code: str) -> Dict[str, Any]:
        """Get compliance rules for a region"""
        
        if not self.region_db_id:
            # Return defaults if database not configured
            return self._get_default_regional_rules(country_code)
        
        try:
            response = self.notion.databases.query(
                database_id=self.region_db_id,
                filter={
                    "property": "Country Code",
                    "rich_text": {"equals": country_code}
                }
            )
            
            if not response['results']:
                return self._get_default_regional_rules(country_code)
            
            region = response['results'][0]['properties']
            
            return {
                "ok": True,
                "country_code": country_code,
                "region": region.get('Region', {}).get('title', [{}])[0].get('text', {}).get('content', ''),
                "data_retention_days": region.get('Data Retention Days', {}).get('number', 30),
                "currency": region.get('Currency', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'USD'),
                "language": region.get('Language', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'en'),
                "timezone": region.get('Timezone', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'UTC'),
                "gdpr_required": region.get('GDPR Required', {}).get('checkbox', False),
                "ccpa_required": region.get('CCPA Required', {}).get('checkbox', False),
                "special_rules": region.get('Special Rules', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def _get_default_regional_rules(self, country_code: str) -> Dict[str, Any]:
        """Default regional rules if database not configured"""
        
        defaults = {
            "US": {"region": "United States", "retention": 30, "currency": "USD", "language": "en", "gdpr": False, "ccpa": True},
            "GB": {"region": "United Kingdom", "retention": 30, "currency": "GBP", "language": "en", "gdpr": True, "ccpa": False},
            "DE": {"region": "Germany", "retention": 30, "currency": "EUR", "language": "de", "gdpr": True, "ccpa": False},
            "FR": {"region": "France", "retention": 30, "currency": "EUR", "language": "fr", "gdpr": True, "ccpa": False},
            "IN": {"region": "India", "retention": 60, "currency": "INR", "language": "en", "gdpr": False, "ccpa": False},
            "PK": {"region": "Pakistan", "retention": 60, "currency": "PKR", "language": "ur", "gdpr": False, "ccpa": False},
        }
        
        rule = defaults.get(country_code, defaults["US"])
        
        return {
            "ok": True,
            "country_code": country_code,
            "region": rule["region"],
            "data_retention_days": rule["retention"],
            "currency": rule["currency"],
            "language": rule["language"],
            "timezone": "UTC",
            "gdpr_required": rule["gdpr"],
            "ccpa_required": rule["ccpa"],
            "special_rules": "",
            "note": "Using default rules (database not configured)"
        }
    
    def localize_email(self, template: str, language: str, data: Dict[str, Any]) -> str:
        """Localize email template"""
        
        # Translate standard keys in template
        localized = template
        for key in ["task_completed", "task_failed", "qa_score", "welcome", "payment_received"]:
            placeholder = f"{{{key}}}"
            if placeholder in localized:
                localized = localized.replace(placeholder, self.translate(key, language))
        
        # Replace data placeholders
        for key, value in data.items():
            placeholder = f"{{{key}}}"
            localized = localized.replace(placeholder, str(value))
        
        return localized
    
    def setup_region(
        self,
        region_name: str,
        country_code: str,
        data_retention_days: int,
        currency: str,
        language: str,
        timezone: str,
        gdpr_required: bool = False,
        ccpa_required: bool = False,
        special_rules: str = ""
    ) -> Dict[str, Any]:
        """Add a new region to compliance database"""
        
        if not self.region_db_id:
            return {"ok": False, "error": "Region compliance database not configured"}
        
        try:
            properties = {
                "Region": {"title": [{"text": {"content": region_name}}]},
                "Country Code": {"rich_text": [{"text": {"content": country_code}}]},
                "Data Retention Days": {"number": data_retention_days},
                "Currency": {"rich_text": [{"text": {"content": currency}}]},
                "Language": {"rich_text": [{"text": {"content": language}}]},
                "Timezone": {"rich_text": [{"text": {"content": timezone}}]},
                "GDPR Required": {"checkbox": gdpr_required},
                "CCPA Required": {"checkbox": ccpa_required},
                "Active": {"checkbox": True},
            }
            
            if special_rules:
                properties["Special Rules"] = {"rich_text": [{"text": {"content": special_rules}}]}
            
            page = self.notion.pages.create(
                parent={"database_id": self.region_db_id},
                properties=properties
            )
            
            return {"ok": True, "region_id": page['id']}
        
        except Exception as e:
            return {"ok": False, "error": str(e)}


# Singleton
_localization_system = None

def get_localization_system() -> LocalizationSystem:
    """Get or create localization system instance"""
    global _localization_system
    if _localization_system is None:
        _localization_system = LocalizationSystem()
    return _localization_system
