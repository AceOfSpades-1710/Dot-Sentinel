class Campaign:
    """
    A Campaign is a group of similar Events (flows).
    """
    def __init__(self, campaign_id, events):
        self.campaign_id = campaign_id
        self.events = events  # list of Event objects


class CampaignSummary:
    """
    Human-readable summary of a Campaign.
    """
    def __init__(self, campaign_id):
        self.campaign_id = campaign_id

        self.size = 0
        self.avg_attack_prob = 0.0
        self.avg_anomaly_score = 0.0
        self.dominant_attack_type = None

    def to_dict(self):
        return {
            "campaign_id": self.campaign_id,
            "size": self.size,
            "avg_attack_prob": self.avg_attack_prob,
            "avg_anomaly_score": self.avg_anomaly_score,
            "dominant_attack_type": self.dominant_attack_type
        }
