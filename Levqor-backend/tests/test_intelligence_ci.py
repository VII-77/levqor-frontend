"""
CI Smoke Tests for Intelligence Layer
Tests write→read operations on PostgreSQL tables
"""
import pytest
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

@pytest.fixture
def db_connection():
    """PostgreSQL connection fixture"""
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )
    yield conn
    conn.close()

def test_system_health_log_write_read(db_connection):
    """Test write→read on system_health_log"""
    with db_connection.cursor() as cur:
        # Write
        cur.execute("""
            INSERT INTO system_health_log (source, frontend, backend, latency_ms, error)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, ('ci_test', 200, 200, 100, None))
        
        inserted_id = cur.fetchone()['id']
        db_connection.commit()
        
        # Read
        cur.execute("""
            SELECT id, source, frontend, backend, latency_ms, error
            FROM system_health_log
            WHERE id = %s
        """, (inserted_id,))
        
        row = cur.fetchone()
        
        # Assert
        assert row is not None
        assert row['source'] == 'ci_test'
        assert row['frontend'] == 200
        assert row['backend'] == 200
        assert row['latency_ms'] == 100
        assert row['error'] is None
        
        # Cleanup
        cur.execute("DELETE FROM system_health_log WHERE id = %s", (inserted_id,))
        db_connection.commit()

def test_intel_events_write_read(db_connection):
    """Test write→read on intel_events"""
    with db_connection.cursor() as cur:
        # Write
        cur.execute("""
            INSERT INTO intel_events (event, value, mean)
            VALUES (%s, %s, %s)
            RETURNING id
        """, ('latency_spike', 500.0, 200.0))
        
        inserted_id = cur.fetchone()['id']
        db_connection.commit()
        
        # Read
        cur.execute("""
            SELECT id, event, value, mean
            FROM intel_events
            WHERE id = %s
        """, (inserted_id,))
        
        row = cur.fetchone()
        
        # Assert
        assert row is not None
        assert row['event'] == 'latency_spike'
        assert float(row['value']) == 500.0
        assert float(row['mean']) == 200.0
        
        # Cleanup
        cur.execute("DELETE FROM intel_events WHERE id = %s", (inserted_id,))
        db_connection.commit()

def test_intel_actions_jsonb(db_connection):
    """Test JSONB metadata in intel_actions"""
    metadata = {
        "action_type": "restart",
        "subsystem": "backend",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    with db_connection.cursor() as cur:
        # Write
        cur.execute("""
            INSERT INTO intel_actions (action, meta)
            VALUES (%s, %s)
            RETURNING id
        """, ('auto_heal_backend', json.dumps(metadata)))
        
        inserted_id = cur.fetchone()['id']
        db_connection.commit()
        
        # Read
        cur.execute("""
            SELECT id, action, meta
            FROM intel_actions
            WHERE id = %s
        """, (inserted_id,))
        
        row = cur.fetchone()
        
        # Assert
        assert row is not None
        assert row['action'] == 'auto_heal_backend'
        assert row['meta']['action_type'] == 'restart'
        assert row['meta']['subsystem'] == 'backend'
        
        # Cleanup
        cur.execute("DELETE FROM intel_actions WHERE id = %s", (inserted_id,))
        db_connection.commit()

def test_intelligence_endpoints(client=None):
    """Test intelligence API endpoints (requires Flask app)"""
    if client is None:
        from run import app
        client = app.test_client()
    
    # Test /api/intelligence/status
    response = client.get('/api/intelligence/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'operational'
    assert 'timestamp' in data
    assert 'summary' in data
    
    # Test /api/intelligence/forecasts
    response = client.get('/api/intelligence/forecasts')
    assert response.status_code == 200
    data = response.get_json()
    assert 'forecasts' in data
    assert 'count' in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
