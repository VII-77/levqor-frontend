"""
Intelligence API Endpoints
Provides access to intelligence layer data and insights
"""
from flask import Blueprint, jsonify, request
from modules.auto_intel.db_adapter import (
    get_intelligence_summary,
    get_recent_events,
    get_recent_actions,
    get_recent_recommendations,
    get_recent_forecasts,
    get_recent_health_logs
)
from datetime import datetime

bp = Blueprint('intelligence', __name__, url_prefix='/api/intelligence')

@bp.route('/status', methods=['GET'])
def get_intelligence_status():
    """
    Get comprehensive intelligence dashboard status
    
    Returns:
        JSON with all intelligence metrics
    """
    try:
        summary = get_intelligence_summary()
        events = get_recent_events(limit=5)
        actions = get_recent_actions(limit=5)
        recommendations = get_recent_recommendations(limit=3)
        
        return jsonify({
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "summary": summary,
            "recent_events": events,
            "recent_actions": actions,
            "recommendations": recommendations
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@bp.route('/anomalies', methods=['GET'])
def get_anomalies():
    """Get recent anomaly events"""
    limit = request.args.get('limit', 20, type=int)
    events = get_recent_events(limit=limit)
    return jsonify({"events": events, "count": len(events)})

@bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get recent decision engine recommendations"""
    limit = request.args.get('limit', 5, type=int)
    recs = get_recent_recommendations(limit=limit)
    return jsonify({"recommendations": recs, "count": len(recs)})

@bp.route('/forecasts', methods=['GET'])
def get_forecasts():
    """Get AI forecasts (revenue, churn predictions)"""
    limit = request.args.get('limit', 10, type=int)
    forecasts = get_recent_forecasts(limit=limit)
    return jsonify({
        "forecasts": forecasts,
        "count": len(forecasts),
        "latest": forecasts[0] if forecasts else None
    })

@bp.route('/health', methods=['GET'])
def get_health_logs():
    """Get system health monitoring logs"""
    limit = request.args.get('limit', 50, type=int)
    logs = get_recent_health_logs(limit=limit)
    return jsonify({
        "logs": logs,
        "count": len(logs)
    })
