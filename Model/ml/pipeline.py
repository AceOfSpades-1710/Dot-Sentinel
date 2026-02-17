# ml/pipeline.py

import os
import pandas as pd

from ml.core.event import Event
from ml.core.model_loader import ModelLoader
from ml.core.preprocessor import Preprocessor
from ml.supervised.detector import SupervisedDetector
from ml.anomaly.anomaly_model import AnomalyDetector
from ml.campaign.builder import CampaignBuilder
from llm.adapter import build_campaign_summary
from llm.analyzer import analyze_campaign



def run_pipeline(csv_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, "model")

    print("[*] Loading models and preprocessor...")
    loader = ModelLoader(MODEL_DIR)
    preprocessor = Preprocessor(MODEL_DIR)
    detector = SupervisedDetector(loader.binary_model, loader.multiclass_model)

    print("[*] Loading CSV...")
    df = pd.read_csv(csv_path)

    print("[*] Preprocessing features...")
    X = preprocessor.transform(df)

    print("[*] Running supervised models...")
    attack_probs, attack_types = detector.analyze(X)

    print("[*] Running anomaly detection...")
    anomaly_model_path = "ml/anomaly/models/anomaly_model.pkl"
    anomaly_detector = AnomalyDetector(anomaly_model_path)
    anomaly_scores = anomaly_detector.predict(X)

    print("[*] Building Event objects...")
    events = []

    for i in range(len(df)):
        flow_id = int(df["id"].iloc[i]) if "id" in df.columns else i

        ev = Event(flow_id)
        ev.attack_prob = float(attack_probs[i])
        ev.attack_type = str(attack_types[i])
        ev.anomaly_score = float(anomaly_scores[i])
        events.append(ev)
    
    print("\n[*] Sample events:")
    for e in events[:5]:
        print(e.to_dict())

    
    print("[*] Clustering campaigns...")
    campaign_builder = CampaignBuilder(
        eps=0.15,
        min_samples=10
    )

    campaigns = campaign_builder.build_campaigns(events)

    print(f"[+] Detected {len(campaigns)} campaigns\n")

    # Campaign summaries
    from collections import Counter

    for cid, flows in campaigns.items():
        avg_prob = sum(f["attack_prob"] for f in flows) / len(flows)
        avg_anom = sum(f["anomaly_score"] for f in flows) / len(flows)

        attack_types = [f["attack_type"] for f in flows]
        dominant_attack = Counter(attack_types).most_common(1)[0][0]

        print({
            "campaign_id": int(cid),
            "size": len(flows),
            "avg_attack_prob": round(avg_prob, 3),
            "avg_anomaly_score": round(avg_anom, 3),
            "dominant_attack_type": dominant_attack
        })
    print("\n[*] LLM SOC Analysis:\n")

    for cid, flows in campaigns.items():
        summary = build_campaign_summary(cid, flows)
        explanation = analyze_campaign(summary)

        print(f"=== Campaign {cid} ===")
        print(explanation)
        print()



    

    print("\n[*] Pipeline completed successfully.")
    return events


if __name__ == "__main__":
    run_pipeline("data/unsw_sample.csv")
