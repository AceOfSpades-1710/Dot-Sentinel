import pandas as pd
import os
import uuid
import time
from scapy.all import PcapReader, IP, TCP, UDP, ICMP

class PcapParser:
    def __init__(self):
        pass
        
    def parse_pcap_to_csv(self, pcap_path, output_csv_path):
        print(f"[*] Streaming pcap with scapy: {pcap_path}")
        data = []
        
        # Use PcapReader instead of rdpcap to prevent memory hanging
        with PcapReader(pcap_path) as reader:
            for pkt in reader:
                if IP not in pkt:
                    continue
                    
                row = {
                    "time": float(pkt.time),
                    "len": len(pkt),
                    "srcip": pkt[IP].src,
                    "dstip": pkt[IP].dst,
                    "proto": pkt[IP].proto,
                    "sport": pkt[TCP].sport if TCP in pkt else (pkt[UDP].sport if UDP in pkt else 0),
                    "dport": pkt[TCP].dport if TCP in pkt else (pkt[UDP].dport if UDP in pkt else 0),
                    "ttl": pkt[IP].ttl,
                    "swin": pkt[TCP].window if TCP in pkt else 0
                }
                data.append(row)
                
                # Safety break for massive files in free tier
                if len(data) > 20000: 
                    break
                    
        df = pd.DataFrame(data)
        df.to_csv(output_csv_path, index=False)
        return output_csv_path

    def aggregate_flows(self, packet_csv_path):
        """
        Aggregates packet-level CSV into flow-level features compatible with the model.
        """
        try:
            df = pd.read_csv(packet_csv_path)
        except pd.errors.EmptyDataError:
            print("[!] CSV is empty. No packets found.")
            return pd.DataFrame()

        if df.empty:
            return pd.DataFrame()

        # Ensure types
        df["srcip"] = df["srcip"].astype(str)
        df["dstip"] = df["dstip"].astype(str)
        df["sport"] = df["sport"].fillna(0).astype(int).astype(str)
        df["dport"] = df["dport"].fillna(0).astype(int).astype(str)
        df["proto"] = df["proto"].fillna(0).astype(int)

        # Create flow ID
        df["flow_id"] = df["srcip"] + "-" + df["dstip"] + "-" + df["sport"] + "-" + df["dport"] + "-" + df["proto"].astype(str)

        # Group by flow
        agg_funcs = {
            "time": ["min", "max", "count"],
            "len": ["sum"],
            "ttl": ["mean"]
        }
        
        flows = df.groupby("flow_id").agg(agg_funcs)
        
        if flows.empty:
            return pd.DataFrame()

        flows.columns = ["stime", "ltime", "Spkts", "sbytes", "sttl"]
        flows.reset_index(inplace=True)

        # Feature Engineering (Approximations for UNSW-NB15)
        flows["dur"] = flows["ltime"] - flows["stime"]
        flows["dur"] = flows["dur"].apply(lambda x: x if x > 0 else 0.000001) # Avoid div by zero
        
        flows["sload"] = (flows["sbytes"] * 8) / flows["dur"]
        flows["dload"] = 0 
        
        # Missing features mapping (fill with defaults)
        required_cols = [
            "proto", "service", "state", "spkts", "dpkts", "sbytes", "dbytes", 
            "sttl", "dttl", "sload", "dload", "sloss", "dloss", "sinpkt", "dinpkt", 
            "sjit", "djit", "swin", "stcpb", "dtcpb", "dwin", "tcprtt", "synack", 
            "ackdat", "smean", "dmean", "trans_depth", "response_body_len", 
            "ct_srv_src", "ct_state_ttl", "ct_dst_ltm", "ct_src_dport_ltm", 
            "ct_dst_sport_ltm", "ct_dst_src_ltm", "is_ftp_login", "ct_ftp_cmd", 
            "ct_flw_http_mthd", "ct_src_ltm", "ct_srv_dst", "is_sm_ips_ports"
        ]

        # Extract proto, srcip, dstip from flow_id for context
        flows["proto"] = flows["flow_id"].apply(lambda x: x.split("-")[4])
        flows["srcip"] = flows["flow_id"].apply(lambda x: x.split("-")[0])
        flows["dstip"] = flows["flow_id"].apply(lambda x: x.split("-")[1])
        
        # Map protocol numbers to names if possible or keep as is
        proto_map = {6: "tcp", 17: "udp", 1: "icmp"}
        flows["proto"] = flows["proto"].astype(int).map(proto_map).fillna("udp") # Default to udp

        # Defaults for missing complex features
        flows["service"] = "-" 
        flows["state"] = "INT" # Default state
        flows["dpkts"] = 0
        flows["dbytes"] = 0
        flows["dttl"] = 0
        flows["spkts"] = flows["Spkts"]
        
        # Fill rest with 0
        for col in required_cols:
            if col not in flows.columns:
                flows[col] = 0

        # Determine service (simple heuristic)
        flows["service"] = flows.apply(self._infer_service, axis=1)

        return flows

    def _infer_service(self, row):
        # Basic port-based service inference
        ports = row["flow_id"].split("-")[2:4]
        if "80" in ports or "8080" in ports: return "http"
        if "443" in ports: return "ssl"
        if "21" in ports: return "ftp"
        if "53" in ports: return "dns"
        if "22" in ports: return "ssh"
        if "25" in ports: return "smtp"
        return "-"
