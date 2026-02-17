from sklearn.cluster import DBSCAN
from collections import defaultdict

from ml.campaign.vectorizer import EventVectorizer


class CampaignBuilder:
    def __init__(self, eps=0.06, min_samples=10):
        self.eps = eps
        self.min_samples = min_samples
        self.vectorizer = EventVectorizer()

    def build_campaigns(self, events):
        """
        Cluster events into campaigns using DBSCAN
        """
        X = self.vectorizer.vectorize(events)

        clustering = DBSCAN(
            eps=self.eps,
            min_samples=self.min_samples
        ).fit(X)

        labels = clustering.labels_

        campaigns = defaultdict(list)

        for event, label in zip(events, labels):
            if label == -1:
                continue  # noise
            campaigns[label].append(event.to_dict())

        return campaigns
