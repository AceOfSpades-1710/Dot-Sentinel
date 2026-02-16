class Event:
    def __init__(self, flow_id):
        self.flow_id = flow_id

        self.attack_prob = None
        self.attack_type = None
        self.anomaly_score = None

    def to_dict(self):
        return {
            "flow_id": self.flow_id,
            "attack_prob": self.attack_prob,
            "attack_type": self.attack_type,
            "anomaly_score": self.anomaly_score
        }
