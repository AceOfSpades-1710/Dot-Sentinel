from ml.agents.agent2 import UncertaintyReasoningAgent

agent = UncertaintyReasoningAgent()

test_probs = [0.95, 0.78, 0.62, 0.40]

for p in test_probs:
    result = agent.assess(p)
    print(f"P_attack={p:.2f} →", result)
