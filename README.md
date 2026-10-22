# SAHAYAK 2.0: Hybrid AI & Soft Computing Disaster-Response Planner
**Course:** Artificial Intelligence & Soft Computing (AISC) | **Topic:** Algorithmic Implementation of AI Approaches
All six core techniques are implemented **from scratch** (NumPy only, zero ML/black-box libraries) and chained into an autonomous decision-making pipeline.

## Problem
After a severe flood event, an autonomous rescue vehicle starts at a base headquarters and must navigate a damaged, non-uniform road network to evacuate affected civilian sites.
- **Which sites first?** Handled by Neural Net Severity prediction + Mamdani Fuzzy Logic prioritization.
- **Which roads?** Handled by admissible Heuristic A* Search.
- **Optimal visiting order?** Soft Computing combinatorial optimization: Evolutionary Genetic Algorithm (GA) vs. Swarm Ant Colony Optimization (ACO).
- **What if roads keep collapsing dynamically?** Minimax adversarial search with Alpha-Beta pruning + real-time dynamic A* replanning.

## Architecture & Techniques
| Stage | Technique | File | Role & Formulation |
|---|---|---|---|
| 1 | Neural network (Backpropagation) | `neural.py` | 4-8-1 MLP predicts site flood severity (0–10) from rainfall, water level, structural density, elevation. |
| 2 | Heuristic search (A*) | `search.py` | Optimal pathfinding on weighted grid; compared directly against Dijkstra ($h=0$). |
| 3 | Fuzzy logic (Mamdani) | `fuzzy.py` | Multi-criteria reasoning: Severity + Population + Accessibility $\to$ Criticality Priority (0–100). |
| 4a | Genetic Algorithm (GA) | `genetic.py` | Permutation chromosome, Order Crossover (OX), Inversion Mutation, Tournament Selection ($k=3$), Elitism. |
| 4b | Ant Colony Optimization (ACO) | `aco.py` | Swarm intelligence: Pheromone evaporation ($\rho$), desirability heuristic ($\eta = \text{priority}/D$), and elitist reinforcement. |
| 5 | Adversarial search ($\alpha$-$\beta$) | `adversarial.py` | Rescuer (MAX) vs Road-Collapsing Disaster (MIN) with tabu list to prevent horizon dithering. |
| 6 | Interactive Visual Simulator | `simulator.html` | Real-time browser command center with live A* replanning and click-to-collapse obstacle testing. |

**Data Pipeline:**
$$\text{Sensors} \xrightarrow{\text{MLP}} \text{Severity} \xrightarrow{\text{Mamdani Fuzzy}} \text{Priority} \xrightarrow{\text{A* Search}} D \text{ Matrix} \xrightarrow{\text{GA / ACO}} \text{Tour Order} \xrightarrow{\text{Minimax / Replanning}} \text{Execution}$$

---

## How to Run

### 1. Terminal Run & Matplotlib Dashboard:
```bash
python main.py
```
- Prints terminal benchmark for all algorithms.
- Updates and saves `sahayak_dashboard.png` (2x3 panel including GA vs ACO convergence curves).

### 2. Interactive Web Simulator:
Double-click `simulator.html` in your file explorer or open it in any browser:
```bash
# Or open directly in browser:
start simulator.html
```
- **Watch the rescue vehicle** move cell-by-cell along the optimal route.
- **Click any cell on the grid** to collapse a road dynamically.
- **Watch real-time dynamic A\* replanning** recalculate the detour automatically with collision detection.
- **Switch between routing strategies** (GA, ACO, Nearest-Neighbor, Priority-Only).

---

## Experimental Benchmark Results (Seed 7, 20x20 City Grid, 8 Sites)
- **Neural Network:** Test $R^2 = 0.964$, $\text{MAE} = 0.291$ (scale 0–10).
- **A\* vs Dijkstra:** A* expanded **3,743 nodes** vs Dijkstra's **6,862 nodes** (**45.5% reduction** in search space) with 100% identical optimal path costs.
- **Soft Computing Optimization (GA vs ACO vs Baselines):**
  - **Brute-Force Global Optimum (8! = 40,320 permutations):** Cost = **34,813**
  - **Genetic Algorithm (GA):** Cost = **34,813** (**0.00% gap** to global optimum)
  - **Ant Colony Optimization (ACO):** Cost = **34,813** (**0.00% gap** to global optimum)
  - **Nearest-Neighbour Greedy:** Cost = **35,577** (GA/ACO are 2.1% better)
  - **Priority-Only Ordering:** Cost = **62,816** (GA/ACO are **44.6% better** by avoiding spatial zigzagging)
- **Adversarial Resilience:** Under road destruction, minimax with alpha-beta achieved a mission cost of **198** vs **210** for naive replanning (**+5.7% travel efficiency saved**).

---

## Viva & Examination Cheat-Sheet

1. **Why use both GA and ACO? What is the difference?**
   - *GA (Evolutionary Computation):* Operates on a population of complete candidate solutions using genetic operators (selection, crossover, mutation). Crossover exchanges sub-tours between parents.
   - *ACO (Swarm Intelligence):* Models constructive agents. Each ant builds a tour step-by-step using local pheromone trails ($\tau$) and heuristic visibility ($\eta$). Pheromone reinforces high-quality edges over iterations.
   - *Key takeaway:* Both converged to the identical global optimum ($34,813$), confirming metaheuristic robustness on NP-hard permutation spaces.

2. **Why is Manhattan Distance admissible for A\* on a grid?**
   - An admissible heuristic never overestimates the true remaining cost ($h(n) \le h^*(n)$). Because our minimum terrain cell cost is $1.0$, the Manhattan distance $\Delta x + \Delta y$ is the theoretical lower bound of grid travel distance. Thus, $A^*$ is mathematically guaranteed to return the optimal path.

3. **How does Mamdani Fuzzy Inference work in SAHAYAK?**
   - Inputs: Predicted Severity ($0-10$), Population ($0-1$), Accessibility ($0-1$).
   - Fuzzification via trapezoidal membership functions (`trap()`).
   - Rule evaluation uses Zadeh min-operator for AND clauses across 13 domain rules.
   - Aggregation uses max-operator to merge rule consequences.
   - Defuzzification calculates the centroid (center of gravity) across the output domain ($0-100$).

4. **Why not just sort sites by Priority?**
   - Sorting purely by priority results in a cost of $62,816$ because the rescuer zigzags across opposite ends of the city. GA/ACO balance urgency and travel distance, cutting mission latency down to $34,813$ (**44.6% improvement**).

5. **How does Alpha-Beta Pruning improve Minimax?**
   - Alpha ($\alpha$) is the minimum score the MAX player is guaranteed; Beta ($\beta$) is the maximum score the MIN player is guaranteed. When $\beta \le \alpha$, further child nodes along that branch cannot influence the final root decision and are pruned, reducing search complexity from $O(b^d)$ towards $O(b^{d/2})$ with proper move ordering.
