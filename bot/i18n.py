"""
Boss Mode Phase 11: Internationalization (i18n) Foundation
Provides multi-language support for EchoPilot UI
"""

import os
import json
from pathlib import Path

TRANSLATIONS_DIR = Path("locales")
DEFAULT_LOCALE = "en"

# Foundation translations
TRANSLATIONS = {
    "en": {
        "app_name": "EchoPilot AI",
        "tagline": "Autonomous Enterprise Operations",
        "dashboard": "Dashboard",
        "payments": "Payments",
        "about": "About",
        "health": "Health",
        "status_live": "Live",
        "status_offline": "Offline",
        "actions": "Actions",
        "create_job": "Create Job",
        "run_pulse": "Run Pulse",
        "view_metrics": "View Metrics",
        "loading": "Loading...",
        "error": "Error",
        "success": "Success"
    },
    "es": {
        "app_name": "EchoPilot AI",
        "tagline": "Operaciones Empresariales Autónomas",
        "dashboard": "Panel de Control",
        "payments": "Pagos",
        "about": "Acerca de",
        "health": "Salud",
        "status_live": "En Vivo",
        "status_offline": "Fuera de Línea",
        "actions": "Acciones",
        "create_job": "Crear Trabajo",
        "run_pulse": "Ejecutar Pulso",
        "view_metrics": "Ver Métricas",
        "loading": "Cargando...",
        "error": "Error",
        "success": "Éxito"
    },
    "ur": {
        "app_name": "EchoPilot AI",
        "tagline": "خودمختار انٹرپرائز آپریشنز",
        "dashboard": "ڈیش بورڈ",
        "payments": "ادائیگیاں",
        "about": "کے بارے میں",
        "health": "صحت",
        "status_live": "لائیو",
        "status_offline": "آف لائن",
        "actions": "اعمال",
        "create_job": "کام بنائیں",
        "run_pulse": "پلس چلائیں",
        "view_metrics": "میٹرکس دیکھیں",
        "loading": "لوڈ ہو رہا ہے...",
        "error": "خرابی",
        "success": "کامیابی"
    }
}

def get_translation(key: str, locale: str = None):
    """Get translated string for key"""
    locale = locale or os.getenv("DEFAULT_LOCALE", DEFAULT_LOCALE)
    
    if locale not in TRANSLATIONS:
        locale = DEFAULT_LOCALE
    
    return TRANSLATIONS[locale].get(key, TRANSLATIONS[DEFAULT_LOCALE].get(key, key))

def get_supported_locales():
    """Get list of supported locales"""
    return {
        "ok": True,
        "locales": [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "es", "name": "Spanish", "native": "Español"},
            {"code": "ur", "name": "Urdu", "native": "اردو"}
        ],
        "default": DEFAULT_LOCALE
    }

def get_locale_strings(locale: str = None):
    """Get all translations for a locale"""
    locale = locale or DEFAULT_LOCALE
    
    if locale not in TRANSLATIONS:
        locale = DEFAULT_LOCALE
    
    return {
        "ok": True,
        "locale": locale,
        "strings": TRANSLATIONS[locale]
    }
