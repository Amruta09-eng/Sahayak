"""Genetic algorithm: order rescue sites to minimise priority-weighted arrival time."""
import itertools
import numpy as np

def mission_cost(order, D, prio):
    t, prev, total = 0.0, 0, 0.0           # D index 0 = base, site i -> i+1
    for i in order:
        t += D[prev][i + 1]; total += t * prio[i]; prev = i + 1
    return total

def order_crossover(p1, p2, rng):
    n = len(p1); a, b = sorted(rng.choice(n, 2, replace=False))
    mid = set(p1[a:b + 1]); fill = iter(g for g in p2 if g not in mid)
    return [p1[i] if a <= i <= b else next(fill) for i in range(n)]

def run_ga(D, prio, pop=100, gens=200, pc=0.9, pm=0.3, elite=2, seed=0):
    rng = np.random.default_rng(seed); n = len(prio)
    P = [list(rng.permutation(n)) for _ in range(pop)]
    best_hist = []
    for _ in range(gens):
        fit = [mission_cost(c, D, prio) for c in P]
        order = np.argsort(fit); best_hist.append(fit[order[0]])
        new = [P[i][:] for i in order[:elite]]                       # elitism
        pick = lambda: min((P[j] for j in rng.choice(pop, 3, replace=False)),
                           key=lambda c: mission_cost(c, D, prio))   # tournament k=3
        while len(new) < pop:
            a, b = pick(), pick()
            child = order_crossover(a, b, rng) if rng.random() < pc else a[:]
            if rng.random() < pm:                                    # inversion mutation
                i, j = sorted(rng.choice(n, 2, replace=False)); child[i:j + 1] = child[i:j + 1][::-1]
            new.append(child)
        P = new
    fit = [mission_cost(c, D, prio) for c in P]
    k = int(np.argmin(fit))
    return P[k], fit[k], best_hist

def brute_force(D, prio):
    return min(itertools.permutations(range(len(prio))), key=lambda o: mission_cost(o, D, prio))

def nearest_neighbour(D, n):
    left, cur, order = set(range(n)), 0, []
    while left:
        nxt = min(left, key=lambda i: D[cur][i + 1]); order.append(nxt); left.remove(nxt); cur = nxt + 1
    return order
