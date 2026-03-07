import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] == True

def test_analyze_pcap():
    # Use existing sample.pcap
    pcap_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "parser", "pcaps", "sample.pcap")
    
    # If file doesn't exist, create a dummy one (but checking first)
    if not os.path.exists(pcap_path):
        pytest.skip(f"Sample PCAP not found at {pcap_path}")

    with open(pcap_path, "rb") as f:
        # Create a copy in memory or temp file handled by TestClient
        response = client.post(
            "/analyze",
            files={"file": ("test.pcap", f, "application/vnd.tcpdump.pcap")}
        )
    
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert data["status"] == "success"
    assert "total_flows" in data
    assert "anomalous_flows" in data
    assert len(data["all_flows"]) == data["total_flows"]
    
    # Check flow structure
    if data["total_flows"] > 0:
        flow = data["all_flows"][0]
        assert "flow_id" in flow
        assert "attack_prob" in flow
        assert "anomaly_score" in flow
        assert "bytes" in flow
        assert "packets" in flow
