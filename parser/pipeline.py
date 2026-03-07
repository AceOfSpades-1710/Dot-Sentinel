import os
import sys
import pandas as pd
import json

# Add Model directory to sys.path to import ml modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_ROOT = os.path.join(os.path.dirname(BASE_DIR), "Model")
sys.path.append(MODEL_ROOT)

from ml.core.model_loader import ModelLoader
from ml.core.preprocessor import Preprocessor
from ml.supervised.detector import SupervisedDetector
from ml.anomaly.anomaly_model import AnomalyDetector
from parser.parser import PcapParser
from ml.core.event import Event
from ml.campaign.builder import CampaignBuilder
from llm.adapter import build_campaign_summary
from llm.analyzer import analyze_campaign

class Pipeline:
    def __init__(self):
        print("[*] Initializing Pipeline...")
        self.parser = PcapParser()
        
        # Load models
        model_dir = os.path.join(MODEL_ROOT, "ml", "model")
        print(f"[*] Loading models from {model_dir}")
        
        self.loader = ModelLoader(model_dir)
        self.preprocessor = Preprocessor(model_dir)
        # Using binary model for anomaly scoring if specific anomaly detector unused or complimentary
        self.detector = SupervisedDetector(self.loader.binary_model, self.loader.multiclass_model) 
        
        # Load independent anomaly detector if available (as per reference pipeline.py)
        anomaly_model_path = os.path.join(MODEL_ROOT, "ml", "anomaly", "models", "anomaly_model.pkl")
        if os.path.exists(anomaly_model_path):
             self.anomaly_detector = AnomalyDetector(anomaly_model_path)
        else:
             print(f"[!] Warning: Anomaly model not found at {anomaly_model_path}")
             self.anomaly_detector = None
             
        # Initialize Campaign Builder
        self.campaign_builder = CampaignBuilder(eps=0.15, min_samples=2) # Adjust min_samples for smaller pcaps

    def process_pcap(self, pcap_path, temp_dir="temp"):
        """
        Full pipeline: PCAP -> CSV -> Features -> Inference -> Clustering -> LLM -> JSON
        """
        # 1. Parse PCAP
        os.makedirs(temp_dir, exist_ok=True)
        csv_path = os.path.join(temp_dir, os.path.basename(pcap_path) + ".csv")
        self.parser.parse_pcap_to_csv(pcap_path, csv_path)
        
        # 2. Extract Features (Aggregated Flow Data)
        flows_df = self.parser.aggregate_flows(csv_path)
        
        if flows_df.empty:
            return {
                "status": "success", 
                "total_flows": 0,
                "campaigns": [],
                "message": "No flows detected"
            }

        # 3. Preprocess
        try:
            X = self.preprocessor.transform(flows_df)
        except Exception as e:
            print(f"[!] Preprocessing error: {e}")
            return {"status": "error", "message": f"Preprocessing failed: {str(e)}"}

        # 4. Inference
        # Supervised Detection
        probs, types = self.detector.analyze(X)
        
        # Anomaly Detection
        if self.anomaly_detector:
            anomaly_scores = self.anomaly_detector.predict(X)
        else:
            anomaly_scores = [0.0] * len(flows_df)
            
        # 5. Build Events
        events = []
        for i in range(len(flows_df)):
            flow_id = flows_df.iloc[i].get("flow_id", f"flow_{i}")
            
            ev = Event(flow_id)
            ev.attack_prob = float(probs[i])
            ev.attack_type = str(types[i])
            ev.anomaly_score = float(anomaly_scores[i])
            
            # Attach raw flow data for frontend contextualization
            ev.raw_flow = flows_df.iloc[i].to_dict()
            
            events.append(ev)
            
        # 6. Cluster Campaigns
        print("[*] Clustering campaigns...")
        try:
            raw_campaigns = self.campaign_builder.build_campaigns(events)
            print(f"[+] Detected {len(raw_campaigns)} campaigns.")
        except Exception as e:
            print(f"[!] Campaign clustering error: {e}")
            raw_campaigns = {0: [e.to_dict() for e in events]} # Fallback cluster everything if it fails
            
        # 7. Generate LLM Analysis
        print("[*] Running LLM Analysis...")
        formatted_campaigns = []
        for cid, campaign_flows in raw_campaigns.items():
            
            # Reconstruct flow level details for frontend
            augmented_flows = []
            for flow_dict in campaign_flows:
                # Find the matching original event to inject contextual UI details
                matching_ev = next((e for e in events if e.flow_id == flow_dict['flow_id']), None)
                if matching_ev:
                    flow_dict['src_ip'] = matching_ev.raw_flow.get("srcip", "unknown")
                    flow_dict['dst_ip'] = matching_ev.raw_flow.get("dstip", "unknown")
                    flow_dict['bytes'] = int(matching_ev.raw_flow.get("sbytes", 0) + matching_ev.raw_flow.get("dbytes", 0))
                    flow_dict['packets'] = int(matching_ev.raw_flow.get("spkts", 0) + matching_ev.raw_flow.get("dpkts", 0))
                augmented_flows.append(flow_dict)
                
            try:
                summary = build_campaign_summary(cid, augmented_flows)
                explanation = analyze_campaign(summary)
            except Exception as e:
                print(f"[!] LLM API Error for campaign {cid}: {e}")
                explanation = "LLM Analysis unavailable. Please verify your GEMINI_API_KEY environment variable is set."
                
            formatted_campaigns.append({
                "campaign_id": cid,
                "flows": augmented_flows,
                "llm_explanation": explanation
            })
            
        # 8. Construct Final Response
        return {
            "status": "success", 
            "total_flows": len(events),
            "campaigns": formatted_campaigns
        }
