import pandas as pd

# Load packet-level CSV
df = pd.read_csv("raw_csv/packets.csv", encoding="utf-16")

# Merge TCP and UDP ports
df["tcp.srcport"] = df["tcp.srcport"].fillna(df["udp.srcport"])
df["tcp.dstport"] = df["tcp.dstport"].fillna(df["udp.dstport"])

# Rename columns
df.rename(columns={
    "ip.src": "src_ip",
    "ip.dst": "dst_ip",
    "tcp.srcport": "src_port",
    "tcp.dstport": "dst_port",
    "frame.len": "packet_len",
    "frame.time_epoch": "time"
}, inplace=True)

# Drop incomplete rows
df.dropna(subset=["src_ip", "dst_ip", "src_port", "dst_port"], inplace=True)

# IMPORTANT: Convert to string before concatenation
df["src_ip"] = df["src_ip"].astype(str)
df["dst_ip"] = df["dst_ip"].astype(str)
df["src_port"] = df["src_port"].astype(str)
df["dst_port"] = df["dst_port"].astype(str)

# Create flow identifier
df["flow_id"] = (
    df["src_ip"] + "-" +
    df["dst_ip"] + "-" +
    df["src_port"] + "-" +
    df["dst_port"]
)

# Aggregate packet data into flows
flows = df.groupby("flow_id").agg({
    "packet_len": ["count", "sum", "mean"],
    "time": lambda x: x.max() - x.min()
})

# Flatten column names
flows.columns = [
    "packet_count",
    "total_bytes",
    "avg_packet_size",
    "flow_duration"
]

flows.reset_index(inplace=True)

# Save flow-level features
flows.to_csv("features/flow_features.csv", index=False)

print("✅ Flow feature extraction complete")
