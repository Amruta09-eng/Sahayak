"""Synthetic city: terrain costs, blocked roads, rescue sites with sensor readings."""
import numpy as np
from collections import deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def make_city(n=20, n_sites=8, seed=7):
    rng = np.random.default_rng(seed)
    cost = rng.integers(1, 4, (n, n)).astype(float)      # terrain cost per cell (1-3)
    blocked = rng.random((n, n)) < 0.15                   # collapsed / flooded cells
    base = (0, 0)
    blocked[base] = False
    seen, q = {base}, deque([base])                       # keep only cells reachable from base
    while q:
        u = q.popleft()
        for dx, dy in DIRS:
            v = (u[0] + dx, u[1] + dy)
            if 0 <= v[0] < n and 0 <= v[1] < n and not blocked[v] and v not in seen:
                seen.add(v); q.append(v)
    cand = sorted(c for c in seen if c != base and c[0] + c[1] > n // 2)
    sites = [cand[i] for i in rng.choice(len(cand), n_sites, replace=False)]
    sensors = rng.random((n_sites, 4))   # rainfall, water level, building density, low-elevation
    population = rng.integers(50, 1000, n_sites)
    return dict(n=n, cost=cost, blocked=blocked, base=base, sites=sites,
                sensors=sensors, population=population)
