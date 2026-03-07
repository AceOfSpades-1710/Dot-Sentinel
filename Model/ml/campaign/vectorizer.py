import numpy as np

ATTACK_TYPE_MAP = {
    "Reconnaissance": 0,
    "Exploits": 1,
    "Generic": 2,
    "Fuzzers": 3,
    "DoS": 4,
    "Analysis": 5,
    "Backdoor": 6,
    "Shellcode": 7,
    "Worms": 8,
}

class EventVectorizer:
    def vectorize(self, events):
        vectors = []

        for ev in events:
            attack_code = ATTACK_TYPE_MAP.get(ev.attack_type, -1)

            v = [
                ev.attack_prob,
                ev.anomaly_score if ev.anomaly_score is not None else 0.0,
                attack_code
            ]
            vectors.append(v)

        return np.array(vectors)
