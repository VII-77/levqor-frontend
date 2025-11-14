"""
Tests for Intelligence Status Endpoint
Validates logging, error handling, and request tracking
"""
import pytest
import json
from unittest.mock import patch, MagicMock


def test_status_ok_with_correlation_id(client):
    """Test successful status response includes correlation ID and timing"""
    with patch('api.routes.intelligence.get_intelligence_summary') as mock_summary, \
         patch('api.routes.intelligence.get_recent_events') as mock_events, \
         patch('api.routes.intelligence.get_recent_actions') as mock_actions, \
         patch('api.routes.intelligence.get_recent_recommendations') as mock_recs:
        
        mock_summary.return_value = {
            "anomalies_24h": 0,
            "actions_24h": 0,
            "latest_forecast": None,
            "health": {"avg_latency_ms": 3, "error_rate": 0.0, "total_checks": 10}
        }
        mock_events.return_value = []
        mock_actions.return_value = []
        mock_recs.return_value = []
        
        rv = client.get('/api/intelligence/status', headers={"X-Request-ID": "test-123"})
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["ok"] is True
        assert data["status"] == "operational"
        assert data["meta"]["correlation_id"] == "test-123"
        assert data["meta"]["duration_ms"] >= 0
        assert "version" in data["meta"]


def test_status_generates_correlation_id_if_missing(client):
    """Test that correlation ID is auto-generated when not provided"""
    with patch('api.routes.intelligence.get_intelligence_summary') as mock_summary, \
         patch('api.routes.intelligence.get_recent_events') as mock_events, \
         patch('api.routes.intelligence.get_recent_actions') as mock_actions, \
         patch('api.routes.intelligence.get_recent_recommendations') as mock_recs:
        
        mock_summary.return_value = {"anomalies_24h": 0, "actions_24h": 0, "latest_forecast": None, "health": {"avg_latency_ms": 3, "error_rate": 0.0, "total_checks": 10}}
        mock_events.return_value = []
        mock_actions.return_value = []
        mock_recs.return_value = []
        
        rv = client.get('/api/intelligence/status')
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert "correlation_id" in data["meta"]
        assert len(data["meta"]["correlation_id"]) > 0


def test_status_error_without_debug(client, monkeypatch):
    """Test error response without trace when debug is off"""
    monkeypatch.setenv("INTEL_DEBUG_ERRORS", "false")
    
    with patch('api.routes.intelligence.get_intelligence_summary') as mock_summary:
        mock_summary.side_effect = RuntimeError("Database connection failed")
        
        rv = client.get('/api/intelligence/status', headers={"X-Request-ID": "error-test"})
        
        assert rv.status_code == 500
        data = rv.get_json()
        assert data["ok"] is False
        assert data["error"]["type"] == "RuntimeError"
        assert "Database connection failed" in data["error"]["message"]
        assert data["meta"]["correlation_id"] == "error-test"
        assert "trace_tail" not in data["error"]


def test_status_error_with_debug(client, monkeypatch):
    """Test error response includes trace when debug is enabled"""
    monkeypatch.setenv("INTEL_DEBUG_ERRORS", "true")
    
    with patch('api.routes.intelligence.get_intelligence_summary') as mock_summary:
        mock_summary.side_effect = ValueError("Invalid parameter")
        
        rv = client.get('/api/intelligence/status')
        
        assert rv.status_code == 500
        data = rv.get_json()
        assert data["ok"] is False
        assert data["error"]["type"] == "ValueError"
        assert "trace_tail" in data["error"]
        assert isinstance(data["error"]["trace_tail"], list)


def test_anomalies_endpoint(client):
    """Test anomalies endpoint with correlation tracking"""
    with patch('api.routes.intelligence.get_recent_events') as mock_events:
        mock_events.return_value = [
            {"id": 1, "event": "latency_spike", "value": 500, "mean": 200, "ts": "2025-11-11T16:00:00"}
        ]
        
        rv = client.get('/api/intelligence/anomalies?limit=10', headers={"X-Request-ID": "anom-123"})
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["ok"] is True
        assert data["count"] == 1
        assert data["meta"]["correlation_id"] == "anom-123"
        assert data["meta"]["duration_ms"] >= 0


def test_forecasts_endpoint(client):
    """Test forecasts endpoint with latest forecast"""
    with patch('api.routes.intelligence.get_recent_forecasts') as mock_forecasts:
        mock_forecasts.return_value = [
            {"id": 1, "predicted_revenue": 50000, "churn_rate": 0.05, "horizon_days": 30, "ts": "2025-11-11T16:00:00"}
        ]
        
        rv = client.get('/api/intelligence/forecasts')
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["ok"] is True
        assert data["count"] == 1
        assert data["latest"] is not None
        assert data["latest"]["predicted_revenue"] == 50000


def test_health_endpoint(client):
    """Test health logs endpoint"""
    with patch('api.routes.intelligence.get_recent_health_logs') as mock_logs:
        mock_logs.return_value = [
            {"id": 1, "source": "monitor", "frontend": 1, "backend": 1, "latency_ms": 50, "error": None, "timestamp": "2025-11-11T16:00:00"}
        ]
        
        rv = client.get('/api/intelligence/health?limit=20')
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["ok"] is True
        assert data["count"] == 1


def test_recommendations_endpoint(client):
    """Test recommendations endpoint"""
    with patch('api.routes.intelligence.get_recent_recommendations') as mock_recs:
        mock_recs.return_value = [
            {"id": 1, "recommendations": [{"action": "scale_up", "confidence": 0.9}], "ts": "2025-11-11T16:00:00"}
        ]
        
        rv = client.get('/api/intelligence/recommendations')
        
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["ok"] is True
        assert data["count"] == 1
