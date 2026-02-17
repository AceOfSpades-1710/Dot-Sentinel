import pandas as pd
from agents.agent1 import InputValidationAgent

agent = InputValidationAgent()

# -------------------------
# Test 1: Valid input
# -------------------------
valid_df = pd.DataFrame([{
    "proto": "tcp",
    "service": "http",
    "state": "FIN",
    "dur": 1.2,
    "sbytes": 300,
    "dbytes": 500
}])

result = agent.validate(valid_df)
print("Test 1 (Valid):", result)

# -------------------------
# Test 2: Missing column
# -------------------------
missing_col_df = pd.DataFrame([{
    "proto": "tcp",
    "state": "FIN",
    "dur": 1.2,
    "sbytes": 300,
    "dbytes": 500
}])

result = agent.validate(missing_col_df)
print("Test 2 (Missing column):", result)

# -------------------------
# Test 3: Invalid values
# -------------------------
invalid_df = pd.DataFrame([{
    "proto": "tcp",
    "service": "http",
    "state": "FIN",
    "dur": -5,
    "sbytes": -100,
    "dbytes": 500
}])

result = agent.validate(invalid_df)
print("Test 3 (Invalid values):", result)
