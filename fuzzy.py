"""Fuzzy logic: Mamdani inference (min-AND, max-aggregation, centroid defuzzification)."""
import numpy as np

def trap(x, a, b, c, d):
    return np.maximum(np.minimum(np.minimum((x - a) / (b - a + 1e-9), 1), (d - x) / (d - c + 1e-9)), 0)

SEV = {"low": (-1, 0, 2, 5), "med": (2, 4, 6, 8), "high": (5, 8, 10, 11)}              # 0-10
POP = {"few": (-1, 0, .2, .5), "some": (.2, .45, .55, .8), "many": (.5, .8, 1, 2)}      # 0-1
ACC = {"poor": (-1, 0, .2, .5), "fair": (.2, .45, .55, .8), "good": (.5, .8, 1, 2)}     # 0-1
OUT = {"low": (-1, 0, 15, 35), "med": (20, 40, 60, 80), "high": (60, 75, 85, 95),
       "critical": (80, 92, 100, 101)}                                                    # 0-100
RULES = [  # (severity, population, accessibility, -> priority); None = don't care
    ("high", "many", None, "critical"), ("high", "some", None, "high"), ("high", "few", None, "high"),
    ("high", None, "good", "critical"), ("med", "many", None, "high"), ("med", "some", None, "med"),
    ("med", "few", "good", "med"), ("med", "few", "poor", "low"), ("med", None, "good", "high"),
    ("low", "many", None, "med"), ("low", "some", None, "low"), ("low", "few", None, "low"),
    ("low", None, "poor", "low"),
]
X = np.linspace(0, 100, 501)

def priority(sev, pop, acc):
    """sev 0-10, pop 0-1 (normalised), acc 0-1 (1 = easy to reach) -> priority 0-100."""
    agg = np.zeros_like(X)
    for s, p, a, o in RULES:
        w = 1.0
        for name, tab, val in ((s, SEV, sev), (p, POP, pop), (a, ACC, acc)):
            if name:
                w = min(w, float(trap(val, *tab[name])))
        agg = np.maximum(agg, np.minimum(w, trap(X, *OUT[o])))
    return float((X * agg).sum() / agg.sum()) if agg.sum() > 0 else 50.0
