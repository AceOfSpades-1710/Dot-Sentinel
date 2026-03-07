
import pandas as pd
import numpy as np

def test_crash():
    # simulate the state before aggression
    df = pd.DataFrame(columns=[
        "time", "srcip", "dstip", "tcp.srcport", "udp.srcport", "tcp.dstport",
        "udp.dstport", "proto", "len", "tcp.flags", "ttl", "swin", "spot",
        "dsport", "flow_id"
    ])
    
    # df is empty
    print(f"Shape: {df.shape}")
    
    agg_funcs = {
        "time": ["min", "max", "count"],
        "len": ["sum"],
        "ttl": ["mean"]
    }
    
    flows = df.groupby("flow_id").agg(agg_funcs)
    print(f"Flows shape: {flows.shape}")
    print(f"Flows columns: {flows.columns}")
    
    try:
        flows.columns = ["stime", "ltime", "Spkts", "sbytes", "sttl"]
        print("Renamed successfully")
    except Exception as e:
        print(f"Caught expected error: {e}")

if __name__ == "__main__":
    test_crash()
