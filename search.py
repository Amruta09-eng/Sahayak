"""Heuristic search: A* on a weighted grid (h_weight=0 turns it into Dijkstra)."""
import heapq
from city import DIRS

def astar(cost, blocked, start, goal, h_weight=1.0):
    n = cost.shape[0]
    h = lambda p: h_weight * (abs(p[0] - goal[0]) + abs(p[1] - goal[1]))  # admissible: min cell cost = 1
    openq, g, parent, closed, expanded = [(h(start), 0.0, start)], {start: 0.0}, {}, set(), 0
    while openq:
        _, gc, u = heapq.heappop(openq)
        if u in closed:
            continue
        closed.add(u); expanded += 1
        if u == goal:
            path = [u]
            while u in parent:
                u = parent[u]; path.append(u)
            return path[::-1], gc, expanded
        for dx, dy in DIRS:
            v = (u[0] + dx, u[1] + dy)
            if 0 <= v[0] < n and 0 <= v[1] < n and not blocked[v]:
                ng = gc + cost[v]
                if ng < g.get(v, 1e18):
                    g[v] = ng; parent[v] = u
                    heapq.heappush(openq, (ng + h(v), ng, v))
    return None, float("inf"), expanded
