"""Export simulation data for the interactive web visualizer."""
import json
import numpy as np
from city import make_city
from search import astar
from neural import MLP, make_dataset
from fuzzy import priority
from genetic import run_ga, brute_force, nearest_neighbour, mission_cost
from aco import run_aco

def export_data():
    city = make_city()
    cost, blocked, base, sites = city["cost"], city["blocked"], city["base"], city["sites"]
    n = len(sites)
    
    # 1. Neural Net
    Xd, yd = make_dataset()
    net = MLP()
    net.fit(Xd[:600], yd[:600], epochs=1500)
    severity = np.clip(net.predict(city["sensors"]), 0, 10).tolist()
    
    # 2. Heuristic Search
    pts = [base] + sites
    D = np.zeros((n + 1, n + 1))
    paths = {}
    exp_a = exp_d = 0
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            p, c, ea = astar(cost, blocked, pts[i], pts[j])
            _, _, ed = astar(cost, blocked, pts[i], pts[j], 0)
            D[i][j] = D[j][i] = c
            paths[f"{i}_{j}"] = p
            paths[f"{j}_{i}"] = p[::-1]
            exp_a += ea
            exp_d += ed
            
    # 3. Fuzzy
    pop_n = city["population"] / 1000
    acc = 1 - D[0, 1:] / (1.25 * D[0, 1:].max())
    prio = [float(priority(severity[i], pop_n[i], acc[i])) for i in range(n)]
    
    # 4. GA & ACO
    prio_arr = np.array(prio)
    ga_order, ga_cost, _ = run_ga(D, prio_arr)
    aco_order, aco_cost, _ = run_aco(D, prio_arr)
    opt_order = brute_force(D, prio_arr)
    opt_cost = mission_cost(opt_order, D, prio_arr)
    nn_order = nearest_neighbour(D, n)
    nn_cost = mission_cost(nn_order, D, prio_arr)
    prio_order = [int(x) for x in np.argsort(-prio_arr)]
    prio_cost = mission_cost(prio_order, D, prio_arr)
    
    data = {
        "grid_size": int(cost.shape[0]),
        "cost": cost.tolist(),
        "blocked": blocked.tolist(),
        "base": list(base),
        "sites": [list(s) for s in sites],
        "population": [int(p) for p in city["population"]],
        "severity": [round(float(s), 2) for s in severity],
        "priority": [round(float(p), 1) for p in prio],
        "routes": {
            "ga": [int(x) for x in ga_order],
            "aco": [int(x) for x in aco_order],
            "nearest_neighbor": [int(x) for x in nn_order],
            "priority_first": [int(x) for x in prio_order],
            "optimum": [int(x) for x in opt_order]
        },
        "costs": {
            "ga": round(float(ga_cost), 1),
            "aco": round(float(aco_cost), 1),
            "nearest_neighbor": round(float(nn_cost), 1),
            "priority_first": round(float(prio_cost), 1),
            "optimum": round(float(opt_cost), 1)
        },
        "search_nodes": {
            "astar": int(exp_a),
            "dijkstra": int(exp_d),
            "savings_percent": round(100 * (1 - exp_a / exp_d), 1)
        },
        "paths": paths
    }
    
    with open("sim_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Exported sim_data.json successfully!")

if __name__ == "__main__":
    export_data()
