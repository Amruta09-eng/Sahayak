"""Ant Colony Optimization (ACO): Swarm intelligence for priority-weighted site ordering."""
import numpy as np
from genetic import mission_cost

def run_aco(D, prio, n_ants=30, n_iters=100, alpha=1.0, beta=2.0, rho=0.1, Q=1000.0, seed=0):
    """
    Ant System with elitist pheromone reinforcement.
    D: distance matrix (size (n+1, n+1), index 0 = base, sites 1..n)
    prio: priority array for sites 0..n-1
    """
    rng = np.random.default_rng(seed)
    n = len(prio)
    
    # Heuristic matrix eta: higher priority and shorter distance gives higher desirability
    eta = np.zeros((n + 1, n + 1))
    for u in range(n + 1):
        for v in range(n):
            dist = max(D[u][v + 1], 1e-4)
            # Heuristic combines speed of reaching (1/dist) with urgent priority
            eta[u][v + 1] = (1.0 + prio[v] / 25.0) / dist

    # Initial pheromone levels
    pheromone = np.ones((n + 1, n + 1)) * 1.0
    
    best_order = None
    best_cost = float("inf")
    best_hist = []

    for it in range(n_iters):
        iteration_orders = []
        iteration_costs = []
        
        for ant in range(n_ants):
            unvisited = set(range(n))
            current = 0  # starts at base
            order = []
            
            while unvisited:
                unv_list = list(unvisited)
                probs = []
                for v in unv_list:
                    tau = pheromone[current][v + 1] ** alpha
                    heuristic = eta[current][v + 1] ** beta
                    probs.append(tau * heuristic)
                
                probs = np.array(probs, dtype=float)
                prob_sum = probs.sum()
                if prob_sum <= 0 or np.isnan(prob_sum):
                    p_norm = np.ones(len(unv_list)) / len(unv_list)
                else:
                    p_norm = probs / prob_sum
                
                chosen = rng.choice(unv_list, p=p_norm)
                order.append(chosen)
                unvisited.remove(chosen)
                current = chosen + 1
                
            cost = mission_cost(order, D, prio)
            iteration_orders.append(order)
            iteration_costs.append(cost)
            
            if cost < best_cost:
                best_cost = cost
                best_order = order[:]

        best_hist.append(best_cost)
        
        # Pheromone evaporation
        pheromone *= (1.0 - rho)
        pheromone = np.clip(pheromone, 1e-4, 100.0)
        
        # Pheromone deposit by all ants in this iteration
        for order, cost in zip(iteration_orders, iteration_costs):
            deposit = Q / (cost + 1e-6)
            prev = 0
            for v in order:
                pheromone[prev][v + 1] += deposit
                prev = v + 1

        # Elitist reinforcement for global best
        if best_order is not None:
            elite_deposit = 2.0 * (Q / (best_cost + 1e-6))
            prev = 0
            for v in best_order:
                pheromone[prev][v + 1] += elite_deposit
                prev = v + 1

    return best_order, best_cost, best_hist
