# 🌊 SAHAYAK 2.0: Hybrid AI & Soft Computing Disaster-Response Planner

**Course:** Artificial Intelligence & Soft Computing (AISC)  
**Topic:** Algorithmic Implementation of AI Approaches

**SAHAYAK 2.0** is an AI-powered disaster-response planning system that combines six AI and soft computing techniques into an autonomous decision-making pipeline. The core algorithms are implemented from scratch using NumPy, without ready-made machine-learning or optimization libraries.

## 🌐 Live Website

**[🚀 Launch SAHAYAK 2.0 — Live Web Simulator](https://amruta09-eng.github.io/Sahayak/)**

Explore the interactive disaster-response simulator directly in your browser.

---

## 📌 Problem Statement

After a severe flood, an autonomous rescue vehicle must navigate a damaged, non-uniform road network to evacuate people from affected locations.

The system addresses four key challenges:

- **Which sites should be rescued first?** Neural Network severity prediction + Mamdani Fuzzy Logic prioritization.
- **Which roads should the vehicle take?** A* heuristic search on a weighted grid.
- **What is the optimal visiting order?** Genetic Algorithm (GA) vs. Ant Colony Optimization (ACO).
- **What if roads collapse dynamically?** Minimax adversarial search with Alpha-Beta pruning + dynamic A* replanning.

## 🏗️ Architecture & Techniques

| Stage | Technique | File | Role |
|---|---|---|---|
| 1 | Neural Network (Backpropagation) | `neural.py` | A 4-8-1 MLP predicts flood severity (0–10) from rainfall, water level, structural density, and elevation. |
| 2 | A* Heuristic Search | `search.py` | Finds optimal paths on a weighted grid and compares performance with Dijkstra's algorithm (`h = 0`). |
| 3 | Mamdani Fuzzy Logic | `fuzzy.py` | Combines severity, population, and accessibility to calculate criticality priority (0–100). |
| 4a | Genetic Algorithm (GA) | `genetic.py` | Optimizes visiting order using permutation chromosomes, Order Crossover (OX), inversion mutation, tournament selection (`k = 3`), and elitism. |
| 4b | Ant Colony Optimization (ACO) | `aco.py` | Optimizes visiting order using pheromone evaporation, heuristic visibility, and elitist reinforcement. |
| 5 | Minimax with Alpha-Beta Pruning | `adversarial.py` | Models the rescuer (MAX) against a road-collapsing disaster (MIN), using a tabu list to prevent horizon dithering. |
| 6 | Interactive Visual Simulator | `simulator.html` | Provides a browser-based command center with route visualization, dynamic A* replanning, and click-to-collapse road testing. |

### 🔄 Data Pipeline

```text
Sensors
   ↓
Neural Network → Flood Severity
   ↓
Mamdani Fuzzy Logic → Rescue Priority
   ↓
A* Search → Distance Matrix
   ↓
Genetic Algorithm / Ant Colony Optimization
   ↓
Optimized Rescue Tour
   ↓
Minimax + Dynamic A* Replanning
   ↓
Rescue Execution
```

---

## 🚀 How to Access and Run

### 1. Live Website (Recommended)

Open the deployed website:

**[https://amruta09-eng.github.io/Sahayak/](https://amruta09-eng.github.io/Sahayak/)**

No local Python installation is required to access the deployed website.

### 2. Run the Python Algorithms and Dashboard

Ensure Python and the required dependencies, including NumPy and Matplotlib, are installed.

Run the following command from the project directory:

```bash
python main.py
```

This runs the algorithmic benchmarks and generates or updates `sahayak_dashboard.png`, a 2×3 visualization panel that includes GA and ACO convergence curves.

### 3. Run the Local Interactive Simulator

Open `simulator.html` in a web browser.

On Windows, you can also run:

```bash
start simulator.html
```

**Simulator features:**

- Watch the rescue vehicle move along the planned route.
- Click a grid cell to simulate a road collapse.
- Observe dynamic A* replanning to find an alternative route when one exists.
- Switch between routing strategies: GA, ACO, Nearest-Neighbor, and Priority-Only.

---

## 📊 Experimental Benchmark Results

**Experimental setup:** Seed 7, 20×20 city grid, 8 rescue sites.

### Neural Network Performance

- Test \(R^2 = 0.964\)
- Mean Absolute Error (MAE) = 0.291 on the 0–10 severity scale.

### A* vs. Dijkstra

| Metric | A* Search | Dijkstra |
|---|---:|---:|
| Nodes expanded | 3,743 | 6,862 |
| Optimal path cost | Identical | Identical |

A* expanded approximately **45.5% fewer nodes** while achieving the same optimal path costs in the reported experiment.

### Soft Computing Optimization

The visiting-order algorithms were compared against brute-force search and simpler baselines.

| Algorithm | Mission Cost | Result |
|---|---:|---|
| Brute-force global optimum | 34,813 | Reference optimum |
| Genetic Algorithm (GA) | 34,813 | 0.00% optimality gap |
| Ant Colony Optimization (ACO) | 34,813 | 0.00% optimality gap |
| Nearest-Neighbor Greedy | 35,577 | Slightly higher cost |
| Priority-Only Ordering | 62,816 | Significantly higher cost |

Brute-force search evaluates all \(8! = 40,320\) possible visiting orders.

In this experiment, GA and ACO matched the reported global optimum and improved the mission cost by approximately **44.6% compared with Priority-Only Ordering**.

### Adversarial Resilience

| Strategy | Mission Cost |
|---|---:|
| Minimax with Alpha-Beta Pruning | 198 |
| Naive replanning | 210 |

The adversarial strategy achieved a lower reported mission cost under the simulated road-destruction conditions.

*Note: These figures describe the stated experimental setup and should be reproducible from the project code before being presented as verified results. Matching the optimum for eight locations does not guarantee that GA or ACO will always find a global optimum.*

---

## 🎓 Viva & Examination Cheat-Sheet

### 1. Why use both GA and ACO?

- **Genetic Algorithm:** Evolves a population of complete candidate solutions using selection, crossover, and mutation.
- **Ant Colony Optimization:** Builds candidate routes using pheromone trails and heuristic visibility. Better routes receive reinforcement.
- **Why compare them?** They use different search strategies to solve the same combinatorial optimization problem.

Both algorithms reportedly reached the same global optimum in the eight-site experiment.

### 2. Why is Manhattan Distance admissible for A*?

An admissible heuristic never overestimates the true remaining cost:

\[
h(n) \leq h^*(n)
\]

For a four-directional grid with a minimum terrain movement cost of 1.0, Manhattan distance provides a lower bound:

\[
h(n)=|x_n-x_g|+|y_n-y_g|
\]

Provided the movement model and cost assumptions hold, this heuristic allows A* to find an optimal path.

### 3. How does Mamdani Fuzzy Inference work?

**Inputs:** Predicted severity (0–10), population (0–1), and accessibility (0–1).

The process consists of:

1. **Fuzzification:** Converts numerical inputs into fuzzy categories using membership functions.
2. **Rule evaluation:** Applies 13 domain rules using the minimum operator for AND conditions.
3. **Aggregation:** Combines rule outputs using the maximum operator.
4. **Defuzzification:** Uses the centroid method to calculate a final priority score between 0 and 100.

### 4. Why not simply sort sites by priority?

Priority-only sorting considers urgency but ignores the travel cost between locations. It may cause the vehicle to zigzag across the city.

GA and ACO balance the overall route cost when determining the visiting order, reducing unnecessary travel in the reported experiment.

### 5. How does Alpha-Beta Pruning improve Minimax?

- **Alpha (α):** The best score MAX can guarantee so far.
- **Beta (β):** The best score MIN can guarantee so far.
- **Pruning condition:** When \(\alpha \geq \beta\), the remaining branch can be skipped because it cannot change the decision.

Minimax has a worst-case time complexity of \(O(b^d)\). With effective move ordering, alpha-beta pruning can reduce the number of explored nodes substantially, with best-case time complexity of \(O(b^{d/2})\).

---

## 💡 Key Takeaway

**SAHAYAK 2.0 combines prediction, fuzzy decision-making, heuristic pathfinding, evolutionary optimization, swarm intelligence, and adversarial planning into a unified disaster-response system.**

The project demonstrates how different AI approaches can work together to prioritize rescue sites, optimize visiting order, and respond to changing road conditions.

### 🔗 Project Links

- **Live Website:** https://amruta09-eng.github.io/Sahayak/
- **GitHub Repository:** [Sahayak](https://github.com/amruta09-eng/Sahayak)

