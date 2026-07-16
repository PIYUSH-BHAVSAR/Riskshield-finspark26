import sys
import os
from datetime import datetime

# Add project root directory to path to allow importing backend modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Fix Windows console encoding to support unicode output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient
from backend.app import app
from backend.database import get_db, SessionLocal
from backend.models import User

# TestClient lets us test endpoints without spinning up a live server
client = TestClient(app)

def test_analytics():
    print("Testing /api/analytics endpoint...")
    response = client.get("/api/analytics")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "total_alerts" in data, "Response missing total_alerts"
    assert "critical_alerts" in data, "Response missing critical_alerts"
    assert "risk_distribution" in data, "Response missing risk_distribution"
    print("[PASS] Analytics endpoint verified successfully.")
    print(f"       Dashboard Stats: Total Alerts={data['total_alerts']}, Critical={data['critical_alerts']}, Risk Avg={(data['average_risk_score']*100):.1f}%")

def test_login():
    print("Testing /api/auth/login endpoint...")
    response = client.post(
        "/api/auth/login",
        data={"username": "admin@riskshield.com", "password": "admin123"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    token_data = response.json()
    assert "access_token" in token_data, "Response missing access_token"
    assert token_data["token_type"] == "bearer", "Token type must be bearer"
    print("[PASS] Authentication endpoint verified successfully.")
    return token_data["access_token"]

def test_alerts(token):
    print("Testing /api/alerts & graph endpoints...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/alerts")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    alerts = response.json()
    print(f"[PASS] Alert list endpoint verified. Found {len(alerts)} alerts.")
    
    if len(alerts) > 0:
        alert = alerts[0]
        alert_id = alert["id"]
        
        # Test alert detail graph
        graph_response = client.get(f"/api/alerts/{alert_id}/graph")
        assert graph_response.status_code == 200, f"Expected 200, got {graph_response.status_code}"
        graph_data = graph_response.json()
        assert "nodes" in graph_data, "Graph response missing nodes"
        assert "edges" in graph_data, "Graph response missing edges"
        print("[PASS] Alert D3 Graph data endpoint verified successfully.")
        print(f"       Alert #AL-{alert_id} Network: Nodes={len(graph_data['nodes'])}, Links={len(graph_data['edges'])}")

def test_transactions():
    print("Testing /api/transactions endpoint...")
    response = client.get("/api/transactions")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    txns = response.json()
    print(f"[PASS] Transactions endpoint verified. Found {len(txns)} transactions.")

if __name__ == "__main__":
    print("=" * 50)
    print("  RISKSHIELD-BFSI-X API INTEGRATION TESTS")
    print("=" * 50)
    print()
    try:
        test_analytics()
        token = test_login()
        test_alerts(token)
        test_transactions()
        print()
        print("=" * 50)
        print("  ALL BACKEND API TESTS PASSED!")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n[FAIL] ASSERTION ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        import traceback
        print(f"\n[ERROR] UNEXPECTED ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
