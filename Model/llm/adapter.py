from collections import Counter
from llm.schemas import CampaignSummary

def build_campaign_summary(campaign_id, flows):
    attack_types = [f["attack_type"] for f in flows]
    dominant_attack = Counter(attack_types).most_common(1)[0][0]

    avg_attack_prob = sum(f["attack_prob"] for f in flows) / len(flows)
    avg_anomaly_score = sum(f["anomaly_score"] for f in flows) / len(flows)

    confidence_distribution = Counter(
        "HIGH" if f["attack_prob"] >= 0.85
        else "MEDIUM" if f["attack_prob"] >= 0.65
        else "LOW"
        for f in flows
    )

    return CampaignSummary(
        campaign_id=int(campaign_id),
        num_flows=len(flows),
        dominant_attack=dominant_attack,
        avg_attack_prob=round(avg_attack_prob, 3),
        avg_anomaly_score=round(avg_anomaly_score, 3),
        confidence_distribution=dict(confidence_distribution)
    )
