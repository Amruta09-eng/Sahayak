"""SAHAYAK Web Server: Serves the web portal and provides REST API endpoints using standard library http.server."""
import http.server
import socketserver
import json
import urllib.parse
import webbrowser
import os
import numpy as np

from city import make_city
from neural import MLP, make_dataset
from fuzzy import priority as fuzzy_prio
from search import astar

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Train model once on startup for the API
print("[Server] Initializing Neural Network and City Model...")
_city = make_city()
_Xd, _yd = make_dataset()
_net = MLP()
_net.fit(_Xd[:600], _yd[:600], epochs=1200)
print("[Server] Models initialized successfully!")

class SahayakRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            json_path = os.path.join(DIRECTORY, "sim_data.json")
            if os.path.exists(json_path):
                with open(json_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(json.dumps({"error": "sim_data.json not found"}).encode())
            return
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        
        try:
            req_json = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            req_json = {}

        if parsed.path == "/api/predict-severity":
            # Expects {"rainfall": float, "water_level": float, "density": float, "elevation": float}
            r = float(req_json.get("rainfall", 0.5))
            w = float(req_json.get("water_level", 0.5))
            d = float(req_json.get("density", 0.5))
            e = float(req_json.get("elevation", 0.5))
            X = np.array([[r, w, d, e]])
            sev = float(np.clip(_net.predict(X)[0], 0, 10))
            
            res = {"severity": round(sev, 2), "inputs": {"rainfall": r, "water_level": w, "density": d, "elevation": e}}
            self._send_json(res)
            return

        elif parsed.path == "/api/fuzzy-priority":
            # Expects {"severity": float, "population": float, "accessibility": float}
            sev = float(req_json.get("severity", 5.0))
            pop = float(req_json.get("population", 500)) / 1000.0  # normalize
            acc = float(req_json.get("accessibility", 0.5))
            prio = float(fuzzy_prio(sev, pop, acc))
            
            res = {"priority": round(prio, 1), "severity": sev, "population": pop * 1000, "accessibility": acc}
            self._send_json(res)
            return

        elif parsed.path == "/api/replan-route":
            # Expects {"start": [r, c], "goal": [r, c], "blocked": [[bool...]]}
            start = tuple(req_json.get("start", [0, 0]))
            goal = tuple(req_json.get("goal", [10, 10]))
            blocked = np.array(req_json.get("blocked", _city["blocked"]))
            cost = _city["cost"]
            
            path, gc, exp = astar(cost, blocked, start, goal)
            res = {
                "found": path is not None,
                "path": path if path else [],
                "cost": gc if path else float("inf"),
                "nodes_expanded": exp
            }
            self._send_json(res)
            return

        self.send_error(404, "Endpoint not found")

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

def run():
    with socketserver.TCPServer(("", PORT), SahayakRequestHandler) as httpd:
        print(f"\n=======================================================")
        print(f"🚀 SAHAYAK AI Command Portal Running At:")
        print(f"   Local URL: http://localhost:{PORT}")
        print(f"=======================================================\n")
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run()
