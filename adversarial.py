"""Adversarial search: rescuer (MAX) vs. disaster (MIN) that closes roads. Alpha-beta pruning."""
import math
from city import DIRS
from search import astar

def _blocked(base, extra):
    b = base.copy()
    for c in extra:
        b[c] = True
    return b

def ab(pos, goal, cost, base, extra, budget, acc, depth, alpha, beta, maxi, stats, prune=True):
    """Value = -(travelled + remaining A* cost). Depth counts plies."""
    stats["nodes"] += 1
    if pos == goal:
        return -acc
    path, c, _ = astar(cost, _blocked(base, extra), pos, goal)
    if path is None:
        return -1e4
    if depth == 0:
        return -(acc + c)
    n = cost.shape[0]
    if maxi:                                            # rescuer moves one cell
        bl = _blocked(base, extra); best = -math.inf
        moves = [(pos[0] + dx, pos[1] + dy) for dx, dy in DIRS]
        moves = [v for v in moves if 0 <= v[0] < n and 0 <= v[1] < n and not bl[v]]
        moves.sort(key=lambda v: abs(v[0] - goal[0]) + abs(v[1] - goal[1]))
        for v in moves:
            best = max(best, ab(v, goal, cost, base, extra, budget, acc + cost[v], depth - 1,
                                alpha, beta, False, stats, prune))
            alpha = max(alpha, best)
            if prune and beta <= alpha:
                break
        return best
    best = math.inf                                     # disaster closes one road (or passes)
    options = [None] + ([c for c in path[1:7] if c != goal] if budget > 0 else [])
    for cell in options:
        if cell is None:
            val = ab(pos, goal, cost, base, extra, budget, acc, depth - 1, alpha, beta, True, stats, prune)
        else:
            ex = extra | {cell}
            if astar(cost, _blocked(base, ex), pos, goal)[0] is None:
                continue                                # roads can't be sealed completely
            val = ab(pos, goal, cost, base, ex, budget - 1, acc, depth - 1, alpha, beta, True, stats, prune)
        best = min(best, val); beta = min(beta, best)
        if prune and beta <= alpha:
            break
    return best

def best_move(cost, base, pos, goal, budget, depth=3, avoid=()):
    """avoid = recently visited cells (tabu list) to stop horizon-effect dithering."""
    n = cost.shape[0]; bl = base; best, arg = -math.inf, None
    cands = [(pos[0] + dx, pos[1] + dy) for dx, dy in DIRS]
    cands = [v for v in cands if 0 <= v[0] < n and 0 <= v[1] < n and not bl[v]]
    cands = [v for v in cands if v not in avoid] or cands
    for v in cands:
        if True:
            val = ab(v, goal, cost, base, frozenset(), budget, cost[v], depth - 1,
                     -math.inf, math.inf, False, {"nodes": 0})
            if val > best:
                best, arg = val, v
    return arg

def adversary_block(cost, bl, pos, goal):
    """Greedy worst-case disaster: close the road cell that hurts the rescuer most."""
    path, base_c, _ = astar(cost, bl, pos, goal)
    worst, cell = base_c, None
    for c in path[1:7]:
        if c == goal:
            continue
        p2, c2, _ = astar(cost, _blocked(bl, {c}), pos, goal)
        if p2 is not None and c2 > worst:
            worst, cell = c2, c
    return cell

def simulate_leg(cost, blocked, start, goal, rescuer="astar", budget=2, depth=3):
    bl, pos, total, steps, trail = blocked.copy(), start, 0.0, 0, [start]
    while pos != goal and steps < 500:
        if rescuer == "minimax":
            nxt = best_move(cost, bl, pos, goal, budget, depth, avoid=set(trail[-6:]))
        else:
            nxt = astar(cost, bl, pos, goal)[0][1]
        total += cost[nxt]; pos = nxt; steps += 1; trail.append(pos)
        if budget > 0 and pos != goal:
            c = adversary_block(cost, bl, pos, goal)
            if c is not None:
                bl[c] = True; budget -= 1
    return total, trail

def pruning_demo(cost, blocked, start, goal, depth=3, budget=2):
    out = {}
    for prune in (False, True):
        st = {"nodes": 0}
        v = ab(start, goal, cost, blocked, frozenset(), budget, 0.0, depth, -math.inf, math.inf, True, st, prune)
        out["alphabeta" if prune else "minimax"] = (st["nodes"], v)
    return out
