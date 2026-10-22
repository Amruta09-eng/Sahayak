"""Generates the standalone interactive visual simulator HTML."""
import json

def build_html():
    with open("sim_data.json", "r") as f:
        data = json.load(f)
    
    data_json_str = json.dumps(data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SAHAYAK: Interactive AI Disaster Response Simulator</title>
  <style>
    :root {{
      --bg: #0b1120;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --primary-hover: #0284c7;
      --accent: #f59e0b;
      --danger: #ef4444;
      --success: #10b981;
      --font: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
      padding: 18px 24px;
      min-height: 100vh;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 12px;
    }}
    .title-area h1 {{
      font-size: 1.6rem;
      font-weight: 700;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .badge {{
      font-size: 0.72rem;
      background: #0284c7;
      color: #fff;
      padding: 3px 8px;
      border-radius: 9999px;
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.5px;
    }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 0.88rem;
      margin-top: 2px;
    }}
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 12px 14px;
    }}
    .kpi-label {{
      font-size: 0.75rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }}
    .kpi-val {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--primary);
    }}
    .kpi-sub {{
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-top: 2px;
    }}
    .main-grid {{
      display: grid;
      grid-template-columns: 620px 1fr;
      gap: 18px;
    }}
    .canvas-panel {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    canvas {{
      background: #0f172a;
      border-radius: 6px;
      cursor: crosshair;
      border: 2px solid #334155;
    }}
    .canvas-legend {{
      display: flex;
      gap: 14px;
      margin-top: 10px;
      font-size: 0.75rem;
      color: var(--text-muted);
      flex-wrap: wrap;
      justify-content: center;
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .legend-color {{
      width: 12px;
      height: 12px;
      border-radius: 3px;
    }}
    .controls-panel {{
      margin-top: 12px;
      width: 100%;
      display: flex;
      gap: 8px;
      align-items: center;
      justify-content: center;
    }}
    button {{
      background: #334155;
      color: white;
      border: none;
      padding: 8px 14px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 600;
      transition: all 0.2s;
    }}
    button:hover {{
      background: #475569;
    }}
    button.btn-primary {{
      background: var(--primary);
      color: #0b1120;
    }}
    button.btn-primary:hover {{
      background: var(--primary-hover);
      color: white;
    }}
    button.btn-danger {{
      background: #dc2626;
    }}
    button.btn-danger:hover {{
      background: #b91c1c;
    }}
    .speed-select {{
      background: #334155;
      color: white;
      border: none;
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 0.85rem;
    }}
    .info-panel {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px 16px;
    }}
    .card-title {{
      font-size: 0.95rem;
      font-weight: 700;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .strategy-select {{
      width: 100%;
      background: #0f172a;
      color: white;
      border: 1px solid var(--card-border);
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 0.85rem;
      margin-bottom: 10px;
    }}
    .stats-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
    }}
    .stats-table th, .stats-table td {{
      padding: 6px 8px;
      text-align: left;
    }}
    .stats-table th {{
      color: var(--text-muted);
      border-bottom: 1px solid var(--card-border);
      font-size: 0.72rem;
      text-transform: uppercase;
    }}
    .stats-table tr:hover {{
      background: rgba(255, 255, 255, 0.03);
    }}
    .status-badge {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 600;
    }}
    .status-pending {{ background: #475569; color: #cbd5e1; }}
    .status-enroute {{ background: #d97706; color: #fef3c7; }}
    .status-rescued {{ background: #059669; color: #d1fae5; }}
    .alert-box {{
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid #ef4444;
      color: #fca5a5;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.8rem;
      margin-top: 8px;
      display: none;
    }}
    .hint-bar {{
      margin-top: 8px;
      font-size: 0.75rem;
      color: #38bdf8;
      text-align: center;
    }}
  </style>
</head>
<body>
  <header>
    <div class="title-area">
      <h1>🚨 SAHAYAK 2.0 <span class="badge">AISC Hybrid AI</span></h1>
      <div class="subtitle">Disaster-Response Autonomous Planner & Interactive Dynamic Replanning Simulator</div>
    </div>
    <div>
      <span style="font-size: 0.8rem; color: #10b981; font-weight: 600;">● SIMULATOR ACTIVE</span>
    </div>
  </header>

  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-label">Neural Net Severity</div>
      <div class="kpi-val" id="kpi-nn">R² = 0.96</div>
      <div class="kpi-sub">4-8-1 MLP Backpropagation</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Heuristic Search</div>
      <div class="kpi-val" id="kpi-search">45% Fewer Nodes</div>
      <div class="kpi-sub">A* (3,743) vs Dijkstra (6,862)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Soft Computing Optimization</div>
      <div class="kpi-val" id="kpi-opt">0.00% Gap</div>
      <div class="kpi-sub">GA & ACO hit Global Optimum</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Adversarial Minimax</div>
      <div class="kpi-val" id="kpi-adv">+5.7% Saved</div>
      <div class="kpi-sub">Alpha-Beta vs Road Collapse</div>
    </div>
  </div>

  <div class="main-grid">
    <!-- Left: Canvas & Controls -->
    <div class="canvas-panel">
      <canvas id="simCanvas" width="580" height="580"></canvas>
      
      <div class="canvas-legend">
        <div class="legend-item"><div class="legend-color" style="background: #10b981;"></div> Base (HQ)</div>
        <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> Rescue Sites</div>
        <div class="legend-item"><div class="legend-color" style="background: #1e293b; border: 1px solid #475569;"></div> Blocked Road</div>
        <div class="legend-item"><div class="legend-color" style="background: #e2e8f0;"></div> Cost 1</div>
        <div class="legend-item"><div class="legend-color" style="background: #cbd5e1;"></div> Cost 2</div>
        <div class="legend-item"><div class="legend-color" style="background: #94a3b8;"></div> Cost 3</div>
        <div class="legend-item"><div class="legend-color" style="background: #38bdf8;"></div> Path Trail</div>
      </div>

      <div class="hint-bar">
        💡 <b>Interactive Road-Collapse:</b> Click on any grid cell to dynamically collapse/clear a road and trigger real-time A* replanning!
      </div>

      <div class="controls-panel">
        <button id="btnPlay" class="btn-primary" onclick="togglePlay()">▶ Play Mission</button>
        <button id="btnStep" onclick="stepSim()">⏭ Step</button>
        <button id="btnReset" onclick="resetSim()">↺ Reset</button>
        <select id="speedSelect" class="speed-select" onchange="changeSpeed(this.value)">
          <option value="400">0.5x Speed</option>
          <option value="200" selected>1x Speed</option>
          <option value="100">2x Speed</option>
          <option value="40">5x Speed</option>
        </select>
        <button class="btn-danger" onclick="triggerRandomBlock()">⚡ Collapse Random Road</button>
      </div>

      <div id="alertBox" class="alert-box"></div>
    </div>

    <!-- Right: Telemetry & Table -->
    <div class="info-panel">
      <div class="card">
        <div class="card-title">
          <span>Routing Strategy</span>
          <span id="routeCostBadge" style="font-size: 0.8rem; color: #38bdf8;">Cost: 34,813</span>
        </div>
        <select id="strategySelect" class="strategy-select" onchange="changeStrategy(this.value)">
          <option value="ga">🧬 Genetic Algorithm (GA - OX Crossover) [Cost: 34,813]</option>
          <option value="aco">🐜 Ant Colony Optimization (ACO Pheromone) [Cost: 34,813]</option>
          <option value="nearest_neighbor">📍 Nearest-Neighbor Greedy [Cost: 35,577]</option>
          <option value="priority_first">⚠️ Priority-Only Descending [Cost: 62,816]</option>
        </select>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 6px;">
          <div>
            <div style="font-size: 0.7rem; color: var(--text-muted);">TRAVEL COST</div>
            <div id="tele-cost" style="font-size: 1.1rem; font-weight: 700; color: #38bdf8;">0</div>
          </div>
          <div>
            <div style="font-size: 0.7rem; color: var(--text-muted);">POPULATION SAVED</div>
            <div id="tele-pop" style="font-size: 1.1rem; font-weight: 700; color: #10b981;">0 / 5,040</div>
          </div>
          <div>
            <div style="font-size: 0.7rem; color: var(--text-muted);">REPLAN EVENTS</div>
            <div id="tele-replan" style="font-size: 1.1rem; font-weight: 700; color: #f59e0b;">0</div>
          </div>
        </div>
      </div>

      <div class="card" style="flex: 1; overflow-y: auto;">
        <div class="card-title">Rescue Sites Telemetry</div>
        <table class="stats-table">
          <thead>
            <tr>
              <th>Site</th>
              <th>Cell</th>
              <th>Severity (NN)</th>
              <th>Priority (Fuzzy)</th>
              <th>Pop</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="sitesTableBody">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>

      <div class="card">
        <div class="card-title">Soft Computing Summary</div>
        <div style="font-size: 0.78rem; line-height: 1.5; color: var(--text-muted);">
          • <b>GA & ACO Convergence:</b> Both metaheuristics achieved the exact 0.00% brute-force global optimum.<br>
          • <b>Heuristic Gain:</b> A* cut Dijkstra's node expansions by 45.5% while guaranteeing admissible optimality.<br>
          • <b>Adversarial Search:</b> Minimax with Alpha-Beta pruning prevented catastrophic bottlenecks under road destruction.
        </div>
      </div>
    </div>
  </div>

  <script>
    // Embedded simulation data exported directly from Python
    const SIM_DATA = {data_json_str};

    const canvas = document.getElementById('simCanvas');
    const ctx = canvas.getContext('2d');
    const N = SIM_DATA.grid_size;
    const cellSize = canvas.width / N;

    // Simulation state
    let currentStrategy = 'ga';
    let blockedMap = JSON.parse(JSON.stringify(SIM_DATA.blocked));
    let rescuerPos = [SIM_DATA.base[0], SIM_DATA.base[1]];
    let routeOrder = [...SIM_DATA.routes.ga];
    let currentLegIdx = 0;
    let fullLegPath = [];
    let legStepIdx = 0;
    let isPlaying = false;
    let playInterval = null;
    let speedMs = 200;
    let travelCost = 0;
    let savedPop = 0;
    let replanCount = 0;
    let visitedSites = new Set();
    let historyTrail = [[SIM_DATA.base[0], SIM_DATA.base[1]]];

    function initTable() {{
      const tbody = document.getElementById('sitesTableBody');
      tbody.innerHTML = '';
      SIM_DATA.sites.forEach((site, i) => {{
        const tr = document.createElement('tr');
        tr.id = `row-site-${{i}}`;
        tr.innerHTML = `
          <td><b>S${{i+1}}</b></td>
          <td>(${{site[0]}}, ${{site[1]}})</td>
          <td><span style="color: #f59e0b; font-weight: 600;">${{SIM_DATA.severity[i]}}</span>/10</td>
          <td><span style="color: #ef4444; font-weight: 600;">${{SIM_DATA.priority[i]}}</span></td>
          <td>${{SIM_DATA.population[i]}}</td>
          <td><span class="status-badge status-pending" id="badge-site-${{i}}">Pending</span></td>
        `;
        tbody.appendChild(tr);
      }});
      updateTableStatuses();
    }}

    function updateTableStatuses() {{
      SIM_DATA.sites.forEach((site, i) => {{
        const badge = document.getElementById(`badge-site-${{i}}`);
        if (!badge) return;
        if (visitedSites.has(i)) {{
          badge.className = 'status-badge status-rescued';
          badge.textContent = 'Rescued';
        }} else if (currentLegIdx < routeOrder.length && routeOrder[currentLegIdx] === i) {{
          badge.className = 'status-badge status-enroute';
          badge.textContent = 'En Route';
        }} else {{
          badge.className = 'status-badge status-pending';
          badge.textContent = 'Pending';
        }}
      }});
    }}

    // In-browser A* Search for live dynamic replanning
    function astarJS(start, goal) {{
      const h = (p) => Math.abs(p[0] - goal[0]) + Math.abs(p[1] - goal[1]);
      const openSet = [{{ pos: start, g: 0, f: h(start), path: [start] }}];
      const visited = new Map();
      const DIRS = [[1, 0], [-1, 0], [0, 1], [0, -1]];

      while (openSet.length > 0) {{
        openSet.sort((a, b) => a.f - b.f);
        const curr = openSet.shift();
        const key = `${{curr.pos[0]}}_${{curr.pos[1]}}`;
        if (curr.pos[0] === goal[0] && curr.pos[1] === goal[1]) {{
          return curr.path;
        }}
        if (visited.has(key) && visited.get(key) <= curr.g) continue;
        visited.set(key, curr.g);

        for (const [dx, dy] of DIRS) {{
          const nx = curr.pos[0] + dx;
          const ny = curr.pos[1] + dy;
          if (nx >= 0 && nx < N && ny >= 0 && ny < N && !blockedMap[nx][ny]) {{
            const ng = curr.g + SIM_DATA.cost[nx][ny];
            const nKey = `${{nx}}_${{ny}}`;
            if (!visited.has(nKey) || ng < visited.get(nKey)) {{
              openSet.push({{
                pos: [nx, ny],
                g: ng,
                f: ng + h([nx, ny]),
                path: [...curr.path, [nx, ny]]
              }});
            }}
          }}
        }}
      }}
      return null;
    }}

    function computeLegPath(start, goal) {{
      const path = astarJS(start, goal);
      return path ? path : [start];
    }}

    function prepareCurrentLeg() {{
      if (currentLegIdx >= routeOrder.length) return;
      const targetSiteIdx = routeOrder[currentLegIdx];
      const targetPos = SIM_DATA.sites[targetSiteIdx];
      fullLegPath = computeLegPath(rescuerPos, targetPos);
      legStepIdx = 0;
      updateTableStatuses();
    }}

    function render() {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 1. Draw Grid Cells
      for (let r = 0; r < N; r++) {{
        for (let c = 0; c < N; c++) {{
          const x = c * cellSize;
          const y = r * cellSize;
          
          if (blockedMap[r][c]) {{
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(x, y, cellSize, cellSize);
            // Draw cross
            ctx.strokeStyle = '#475569';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2); ctx.lineTo(x + cellSize - 2, y + cellSize - 2);
            ctx.moveTo(x + cellSize - 2, y + 2); ctx.lineTo(x + 2, y + cellSize - 2);
            ctx.stroke();
          }} else {{
            const cost = SIM_DATA.cost[r][c];
            ctx.fillStyle = cost === 1 ? '#334155' : (cost === 2 ? '#24334d' : '#172554');
            ctx.fillRect(x, y, cellSize, cellSize);
          }}
          ctx.strokeStyle = '#0f172a';
          ctx.lineWidth = 0.5;
          ctx.strokeRect(x, y, cellSize, cellSize);
        }}
      }}

      // 2. Draw History Trail
      if (historyTrail.length > 1) {{
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.5)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(historyTrail[0][1] * cellSize + cellSize / 2, historyTrail[0][0] * cellSize + cellSize / 2);
        for (let i = 1; i < historyTrail.length; i++) {{
          ctx.lineTo(historyTrail[i][1] * cellSize + cellSize / 2, historyTrail[i][0] * cellSize + cellSize / 2);
        }}
        ctx.stroke();
      }}

      // 3. Draw Active Remaining Leg Path
      if (fullLegPath.length > legStepIdx) {{
        ctx.strokeStyle = '#38bdf8';
        ctx.setLineDash([4, 4]);
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        const startPt = fullLegPath[legStepIdx];
        ctx.moveTo(startPt[1] * cellSize + cellSize / 2, startPt[0] * cellSize + cellSize / 2);
        for (let i = legStepIdx + 1; i < fullLegPath.length; i++) {{
          ctx.lineTo(fullLegPath[i][1] * cellSize + cellSize / 2, fullLegPath[i][0] * cellSize + cellSize / 2);
        }}
        ctx.stroke();
        ctx.setLineDash([]);
      }}

      // 4. Draw Base HQ
      const bx = SIM_DATA.base[1] * cellSize + cellSize / 2;
      const by = SIM_DATA.base[0] * cellSize + cellSize / 2;
      ctx.fillStyle = '#10b981';
      ctx.beginPath();
      ctx.arc(bx, by, cellSize * 0.45, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#0b1120';
      ctx.font = 'bold 11px system-ui';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('HQ', bx, by);

      // 5. Draw Rescue Sites
      SIM_DATA.sites.forEach((site, i) => {{
        const sx = site[1] * cellSize + cellSize / 2;
        const sy = site[0] * cellSize + cellSize / 2;
        const radius = cellSize * (0.32 + (SIM_DATA.priority[i] / 100) * 0.18);
        const isRescued = visitedSites.has(i);

        ctx.fillStyle = isRescued ? '#059669' : '#ef4444';
        ctx.beginPath();
        ctx.arc(sx, sy, radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 10px system-ui';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`S${{i+1}}`, sx, sy);
      }});

      // 6. Draw Rescuer
      const rx = rescuerPos[1] * cellSize + cellSize / 2;
      const ry = rescuerPos[0] * cellSize + cellSize / 2;
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath();
      ctx.arc(rx, ry, cellSize * 0.48, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.fillStyle = '#0b1120';
      ctx.font = 'bold 12px system-ui';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('🚑', rx, ry);
    }}

    function stepSim() {{
      if (currentLegIdx >= routeOrder.length) {{
        showAlert('Mission Completed! All 8 affected sites successfully reached.', '#10b981');
        pauseSim();
        return;
      }}

      if (!fullLegPath || legStepIdx >= fullLegPath.length - 1) {{
        // Site arrived!
        const reachedSite = routeOrder[currentLegIdx];
        if (!visitedSites.has(reachedSite)) {{
          visitedSites.add(reachedSite);
          savedPop += SIM_DATA.population[reachedSite];
          document.getElementById('tele-pop').textContent = `${{savedPop}} / 5,040`;
        }}
        currentLegIdx++;
        if (currentLegIdx >= routeOrder.length) {{
          showAlert('Mission Completed! All disaster sites evacuated.', '#10b981');
          pauseSim();
          render();
          return;
        }}
        prepareCurrentLeg();
      }}

      if (fullLegPath && legStepIdx < fullLegPath.length - 1) {{
        legStepIdx++;
        const nextPos = fullLegPath[legStepIdx];
        
        // Check if next step was dynamically blocked
        if (blockedMap[nextPos[0]][nextPos[1]]) {{
          replanCount++;
          document.getElementById('tele-replan').textContent = replanCount;
          showAlert(`Obstacle detected at (${{nextPos[0]}}, ${{nextPos[1]}})! Triggering A* Dynamic Replanning...`, '#ef4444');
          prepareCurrentLeg();
          return;
        }}

        rescuerPos = nextPos;
        historyTrail.push(rescuerPos);
        travelCost += SIM_DATA.cost[rescuerPos[0]][rescuerPos[1]];
        document.getElementById('tele-cost').textContent = Math.round(travelCost);
      }}

      render();
    }}

    function togglePlay() {{
      if (isPlaying) pauseSim();
      else playSim();
    }}

    function playSim() {{
      isPlaying = true;
      document.getElementById('btnPlay').textContent = '⏸ Pause';
      document.getElementById('btnPlay').className = 'btn-primary';
      playInterval = setInterval(stepSim, speedMs);
    }}

    function pauseSim() {{
      isPlaying = false;
      document.getElementById('btnPlay').textContent = '▶ Resume';
      document.getElementById('btnPlay').className = '';
      if (playInterval) clearInterval(playInterval);
    }}

    function resetSim() {{
      pauseSim();
      document.getElementById('btnPlay').textContent = '▶ Play Mission';
      document.getElementById('btnPlay').className = 'btn-primary';
      blockedMap = JSON.parse(JSON.stringify(SIM_DATA.blocked));
      rescuerPos = [SIM_DATA.base[0], SIM_DATA.base[1]];
      routeOrder = [...SIM_DATA.routes[currentStrategy]];
      currentLegIdx = 0;
      legStepIdx = 0;
      travelCost = 0;
      savedPop = 0;
      replanCount = 0;
      visitedSites.clear();
      historyTrail = [[SIM_DATA.base[0], SIM_DATA.base[1]]];
      document.getElementById('tele-cost').textContent = '0';
      document.getElementById('tele-pop').textContent = '0 / 5,040';
      document.getElementById('tele-replan').textContent = '0';
      hideAlert();
      initTable();
      prepareCurrentLeg();
      render();
    }}

    function changeSpeed(ms) {{
      speedMs = parseInt(ms);
      if (isPlaying) {{
        pauseSim();
        playSim();
      }}
    }}

    function changeStrategy(val) {{
      currentStrategy = val;
      const cost = SIM_DATA.costs[val] || 34813;
      document.getElementById('routeCostBadge').textContent = `Cost: ${{cost.toLocaleString()}}`;
      resetSim();
    }}

    function triggerRandomBlock() {{
      let candidates = [];
      for (let r = 0; r < N; r++) {{
        for (let c = 0; c < N; c++) {{
          if (!blockedMap[r][c] && !(r === 0 && c === 0)) {{
            candidates.push([r, c]);
          }}
        }}
      }}
      if (candidates.length > 0) {{
        const pick = candidates[Math.floor(Math.random() * candidates.length)];
        blockedMap[pick[0]][pick[1]] = true;
        replanCount++;
        document.getElementById('tele-replan').textContent = replanCount;
        showAlert(`⚡ Disaster event: Road at (${{pick[0]}}, ${{pick[1]}}) has collapsed! Dynamic Detour initiated.`, '#ef4444');
        prepareCurrentLeg();
        render();
      }}
    }}

    function showAlert(msg, color) {{
      const box = document.getElementById('alertBox');
      box.textContent = msg;
      box.style.display = 'block';
      box.style.borderColor = color;
      box.style.color = color;
    }}

    function hideAlert() {{
      document.getElementById('alertBox').style.display = 'none';
    }}

    // Canvas click event for toggling roadblocks
    canvas.addEventListener('click', (e) => {{
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const c = Math.floor(x / cellSize);
      const r = Math.floor(y / cellSize);

      if (r >= 0 && r < N && c >= 0 && c < N) {{
        // Don't block base or rescuer cell
        if (r === SIM_DATA.base[0] && c === SIM_DATA.base[1]) return;
        if (r === rescuerPos[0] && c === rescuerPos[1]) return;

        blockedMap[r][c] = !blockedMap[r][c];
        if (blockedMap[r][c]) {{
          replanCount++;
          document.getElementById('tele-replan').textContent = replanCount;
          showAlert(`User Action: Road collapsed at (${{r}}, ${{c}}). Re-routing via A*...`, '#f59e0b');
        }} else {{
          showAlert(`User Action: Road cleared at (${{r}}, ${{c}}).`, '#10b981');
        }}
        prepareCurrentLeg();
        render();
      }}
    }});

    // Initialize
    initTable();
    prepareCurrentLeg();
    render();
  </script>
</body>
</html>
"""
    with open("simulator.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated simulator.html successfully!")

if __name__ == "__main__":
    build_html()
