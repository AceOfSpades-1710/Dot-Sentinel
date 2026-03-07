import os
import sys

from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser.main import app


def test():
    with TestClient(app) as client:
        print("Testing /health...")
        try:
            response = client.get("/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Health check failed: {e}")

        print("\nTesting /analyze...")
        pcap_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "parser", "pcaps", "valid_test.pcap")
        if not os.path.exists(pcap_path):
            print(f"Sample PCAP not found at {pcap_path}")
            return

        try:
            with open(pcap_path, "rb") as f:
                response = client.post(
                    "/analyze",
                    files={"file": ("test.pcap", f, "application/vnd.tcpdump.pcap")}
                )
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
            else:
                data = response.json()
                print(f"Result Status: {data.get('status')}")
                print(f"Total Flows: {data.get('total_flows')}")
                if data.get('anomalous_flows'):
                    print(f"Anomalous Flows: {len(data['anomalous_flows'])}")
                print("Analyze test passed!")
                
        except Exception as e:
            print(f"Analyze check failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test()
