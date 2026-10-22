"""SAHAYAK - hybrid AI disaster-response planner. Run: python main.py"""
import time
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from city import make_city
from search import astar
from neural import MLP, make_dataset, true_severity
from fuzzy import priority, SEV, POP, OUT, trap, X as FX
from genetic import run_ga, brute_force, nearest_neighbour, mission_cost
from aco import run_aco
from adversarial import simulate_leg, pruning_demo

city = make_city(); cost, blocked, base, sites = city["cost"], city["blocked"], city["base"], city["sites"]
n = len(sites); line = lambda t: print("\n" + "=" * 8, t, "=" * 8)

# 1. NEURAL NETWORK -------------------------------------------------------------
line("1. NEURAL NETWORK (backpropagation): sensors -> severity")
Xd, yd = make_dataset(); split = 600
net = MLP(); loss = net.fit(Xd[:split], yd[:split])
pred = net.predict(Xd[split:]); truth = yd[split:].ravel() * 10
mae = np.abs(pred - truth).mean(); r2 = 1 - ((pred - truth) ** 2).sum() / ((truth - truth.mean()) ** 2).sum()
print(f"Train MSE {loss[-1]:.5f} | Test MAE {mae:.3f} (scale 0-10) | Test R^2 {r2:.3f}")
severity = np.clip(net.predict(city["sensors"]), 0, 10)

# 2. HEURISTIC SEARCH (A*) ------------------------------------------------------
line("2. HEURISTIC SEARCH: A* vs Dijkstra")
pts = [base] + sites; D = np.zeros((n + 1, n + 1)); exp_a = exp_d = 0; paths = {}
for i in range(n + 1):
    for j in range(i + 1, n + 1):
        p, c, ea = astar(cost, blocked, pts[i], pts[j]); _, c2, ed = astar(cost, blocked, pts[i], pts[j], 0)
        assert abs(c - c2) < 1e-9                               # A* is optimal (same cost as Dijkstra)
        D[i][j] = D[j][i] = c; paths[(i, j)] = p; paths[(j, i)] = p[::-1]; exp_a += ea; exp_d += ed
print(f"Nodes expanded over {n*(n+1)//2} routes: A* {exp_a} vs Dijkstra {exp_d} "
      f"({100*(1-exp_a/exp_d):.0f}% fewer), identical optimal costs")

# 3. FUZZY LOGIC ----------------------------------------------------------------
line("3. FUZZY LOGIC (Mamdani): severity + population + accessibility -> priority")
pop_n = city["population"] / 1000; acc = 1 - D[0, 1:] / (1.25 * D[0, 1:].max())
prio = np.array([priority(severity[i], pop_n[i], acc[i]) for i in range(n)])
print(f"{'Site':<5}{'Cell':<9}{'Severity':>9}{'Pop':>6}{'Access':>8}{'Priority':>10}")
for i in range(n):
    print(f"S{i+1:<4}{str(sites[i]):<9}{severity[i]:>9.2f}{city['population'][i]:>6}{acc[i]:>8.2f}{prio[i]:>10.1f}")

# 4. EVOLUTIONARY & SWARM OPTIMIZATION (GA vs ACO) ------------------------------
line("4. SOFT COMPUTING OPTIMIZATION: Genetic Algorithm vs Ant Colony (ACO)")
order, best, hist = run_ga(D, prio)
aco_order, aco_best, aco_hist = run_aco(D, prio)
opt = brute_force(D, prio); c_opt = mission_cost(opt, D, prio)
nn = nearest_neighbour(D, n); c_nn = mission_cost(nn, D, prio)
c_pr = mission_cost(list(np.argsort(-prio)), D, prio)
print(f"GA cost: {best:.0f} | ACO cost: {aco_best:.0f} | Brute-force optimum: {c_opt:.0f} | Nearest-neighbour: {c_nn:.0f}")
print(f"GA gap to optimum: {100*(best-c_opt)/c_opt:.2f}% | ACO gap to optimum: {100*(aco_best-c_opt)/c_opt:.2f}%")
print("GA Route order : Base -> " + " -> ".join(f"S{i+1}" for i in order))
print("ACO Route order: Base -> " + " -> ".join(f"S{i+1}" for i in aco_order))

# 5. ADVERSARIAL SEARCH ---------------------------------------------------------
line("5. ADVERSARIAL SEARCH: minimax + alpha-beta vs disaster that blocks roads")
pd_ = pruning_demo(cost, blocked, base, sites[order[0]])
print(f"Same decision value ({pd_['minimax'][1]:.1f}): minimax {pd_['minimax'][0]} nodes vs alpha-beta {pd_['alphabeta'][0]} nodes")
t0 = time.time(); stops = [base] + [sites[i] for i in order]; tot = {"astar": 0, "minimax": 0}; trails = []
for r in tot:
    for a, b in zip(stops[:-1], stops[1:]):
        c, tr = simulate_leg(cost, blocked, a, b, r); tot[r] += c
        if r == "minimax": trails.append(tr)
print(f"Mission travel cost under attack: naive A* replanning {tot['astar']:.0f} | minimax rescuer {tot['minimax']:.0f} "
      f"({100*(tot['astar']-tot['minimax'])/tot['astar']:+.1f}%)  [{time.time()-t0:.0f}s]")

# DASHBOARD ---------------------------------------------------------------------
fig, ax = plt.subplots(2, 3, figsize=(17, 10)); fig.suptitle("SAHAYAK: Hybrid AI Disaster-Response Planner", fontsize=16, weight="bold")
a = ax[0, 0]; a.imshow(np.where(blocked, np.nan, cost), cmap="YlOrBr", origin="upper"); a.imshow(np.where(blocked, 1, np.nan), cmap="gray_r", vmin=0, vmax=1.5)
seq = [0] + [i + 1 for i in order]
for u, v in zip(seq[:-1], seq[1:]):
    p = paths[(u, v)]; a.plot([c[1] for c in p], [c[0] for c in p], "b-", lw=1.8)
a.scatter(base[1], base[0], c="green", s=200, marker="s", zorder=5, label="Base")
for k, i in enumerate(order):
    s = sites[i]; a.scatter(s[1], s[0], c="red", s=60 + prio[i] * 4, zorder=5); a.text(s[1] + .4, s[0] - .4, f"{k+1}:S{i+1}", weight="bold")
a.set_title("GA-ordered A* route (size = fuzzy priority)"); a.legend(loc="lower left")
ax[0, 1].plot(loss); ax[0, 1].set_yscale("log"); ax[0, 1].set_title(f"Neural net training loss (test R²={r2:.2f})"); ax[0, 1].set_xlabel("epoch"); ax[0, 1].set_ylabel("MSE")
sv, pp = np.meshgrid(np.linspace(0, 10, 25), np.linspace(0, 1, 25))
Z = np.array([[priority(s, p, 0.5) for s in sv[0]] for p in pp[:, 0]])
c = ax[0, 2].contourf(sv, pp * 1000, Z, 15, cmap="RdYlGn_r"); fig.colorbar(c, ax=ax[0, 2]); ax[0, 2].set_xlabel("severity"); ax[0, 2].set_ylabel("population"); ax[0, 2].set_title("Fuzzy priority surface (accessibility=0.5)")
ax[1, 0].plot(hist, label="GA best", color="tab:blue")
ax[1, 0].plot(aco_hist, label="ACO best", color="tab:orange", ls="-.")
ax[1, 0].axhline(c_opt, color="g", ls="--", label="optimum (brute force)")
ax[1, 0].axhline(c_nn, color="r", ls=":", label="nearest neighbour")
ax[1, 0].legend()
ax[1, 0].set_title("Optimization convergence: GA vs ACO")
ax[1, 0].set_xlabel("generation / iteration")
ax[1, 1].bar(["Dijkstra", "A*"], [exp_d, exp_a], color=["gray", "tab:blue"]); ax[1, 1].set_title("Heuristic search: nodes expanded")
ax[1, 2].bar(["Naive A*", "Minimax\n(alpha-beta)"], [tot["astar"], tot["minimax"]], color=["gray", "tab:red"]); ax[1, 2].set_title("Mission cost under road-blocking adversary")
plt.tight_layout(); plt.savefig("sahayak_dashboard.png", dpi=110); print("\nSaved sahayak_dashboard.png")
