from ml.agents.agent3 import Agent3CorrelationEngine

# =========================
# Create fake test events
# =========================

events = []

# ---- Test Case 1: Recon Scan ----
t = 1000
for i in range(30):
    events.append({
        "stime": t + i,
        "srcip": "1.1.1.1",
        "dstip": f"10.0.0.{i}",
        "is_attack": True,
        "uncertainty": "LOW",
        "attack_type": "Reconnaissance"
    })

# ---- Test Case 2: DoS Flood ----
t = 2000
for i in range(120):
    events.append({
        "stime": t + i,
        "srcip": "2.2.2.2",
        "dstip": "10.0.0.5",
        "is_attack": True,
        "uncertainty": "LOW",
        "attack_type": "DoS"
    })

# ---- Test Case 3: Multi-stage Attack ----
t = 3000
for i in range(15):
    events.append({
        "stime": t + i,
        "srcip": "3.3.3.3",
        "dstip": "10.0.0.8",
        "is_attack": True,
        "uncertainty": "MEDIUM",
        "attack_type": "Reconnaissance"
    })

for i in range(15):
    events.append({
        "stime": t + 20 + i,
        "srcip": "3.3.3.3",
        "dstip": "10.0.0.8",
        "is_attack": True,
        "uncertainty": "MEDIUM",
        "attack_type": "Exploits"
    })

for i in range(15):
    events.append({
        "stime": t + 40 + i,
        "srcip": "3.3.3.3",
        "dstip": "10.0.0.8",
        "is_attack": True,
        "uncertainty": "MEDIUM",
        "attack_type": "Generic"
    })

# =========================
# Run Agent 3
# =========================

agent3 = Agent3CorrelationEngine(time_window=300)

incidents = agent3.correlate(events)

print("\n==============================")
print("   CORRELATED INCIDENTS")
print("==============================\n")

for inc in incidents:
    print(inc)
