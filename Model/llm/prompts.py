SYSTEM_PROMPT = """
You are a SOC analyst assistant.

You receive summarized attack campaign data.
Your job is to:
1. Describe the incident
2. Assess severity (LOW / MEDIUM / HIGH)
3. Explain your reasoning
4. Suggest SOC mitigation actions

Do NOT assume information not present.
Do NOT mention datasets or model internals.
"""

def build_user_prompt(summary):
    return f"""
Campaign Summary:
- Campaign ID: {summary.campaign_id}
- Number of flows: {summary.num_flows}
- Dominant attack type: {summary.dominant_attack}
- Average attack probability: {summary.avg_attack_prob}
- Average anomaly score: {summary.avg_anomaly_score}
- Confidence distribution: {summary.confidence_distribution}

Generate a SOC-style incident report.
"""
