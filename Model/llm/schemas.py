from dataclasses import dataclass
from typing import Dict

@dataclass
class CampaignSummary:
    campaign_id: int
    num_flows: int
    dominant_attack: str
    avg_attack_prob: float
    avg_anomaly_score: float
    confidence_distribution: Dict[str, int]
