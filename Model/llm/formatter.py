from collections import Counter
from llm.schemas import CampaignSummary

def build_campaign_summary(campaign):
    events = campaign.events

    attack_types = [e.attack_type for e in events]
    confidences = [e.confidence for e in events]

    dominant_attack = Counter(attack_types).most_common(1)[0][0]
    confidence_dist = Counter(confidences)

    avg_attack_prob = sum(e.attack_prob for e in events) / len(events)
    avg_anomaly_score = sum(e.anomaly_score for e in events) / len(events)

    return CampaignSummary(
        campaign_id=campaign.campaign_id,
        num_flows=len(events),
        dominant_attack=dominant_attack,
        avg_attack_prob=round(avg_attack_prob, 3),
        avg_anomaly_score=round(avg_anomaly_score, 3),
        confidence_distribution=dict(confidence_dist)
    )
