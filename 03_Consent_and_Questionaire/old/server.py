#!/usr/bin/env python3
"""
TRR Flow – Lokaler Speicher-Server
===================================
Legt JSON-Antworten der Fragebögen unter  ./json/<VP-ID>.json  ab.

Starten:
    python server.py          # läuft auf http://localhost:5050
    python server.py 8080     # alternativer Port

Beenden: Strg+C
"""

import http.server
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Konfiguration ─────────────────────────────────────────────────────────────

PORT      = int(sys.argv[1]) if len(sys.argv) > 1 else 5050
JSON_DIR  = Path(__file__).parent / "json"   # ./json/ relativ zur server.py

# ── Handler ───────────────────────────────────────────────────────────────────

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        """CORS preflight – wird vom Browser vor dem POST geschickt."""
        self._cors()
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path != "/save":
            self.send_error(404, "Not found")
            return

        # Daten lesen
        length  = int(self.headers.get("Content-Length", 0))
        raw     = self.rfile.read(length)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            self._respond(400, {"status": "error", "message": f"Ungültiges JSON: {e}"})
            return

        # VP-ID aus payload holen
        pid = (
            data.get("metadata", {}).get("participant_id")
            or data.get("participant_id")
            or f"unbekannt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        # Sonderzeichen aus Dateinamen entfernen (Sicherheit)
        safe_pid = "".join(c for c in pid if c.isalnum() or c in "-_").strip() or "unbekannt"

        # json/-Ordner anlegen falls nicht vorhanden
        JSON_DIR.mkdir(parents=True, exist_ok=True)

        # Datei schreiben  (bestehende Datei wird überschrieben – gewollt)
        out_path = JSON_DIR / f"{safe_pid}.json"
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"[{datetime.now().strftime('%H:%M:%S')}]  ✓  Gespeichert → {out_path}")
        self._respond(200, {"status": "ok", "file": str(out_path)})

    # ── Hilfsmethoden ──────────────────────────────────────────────────────────

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _respond(self, code: int, body: dict):
        payload = json.dumps(body).encode()
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type",   "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        # Nur eigene Ausgaben, keine HTTP-Log-Flut
        pass


# ── Start ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    print(f"""
╔══════════════════════════════════════════════════════╗
║   TRR-Flow Speicher-Server                          ║
║   http://localhost:{PORT:<5}                              ║
║   JSON-Zielordner: {str(JSON_DIR):<34}║
║   Beenden mit Strg+C                                ║
╚══════════════════════════════════════════════════════╝
""")
    with http.server.HTTPServer(("localhost", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer beendet.")
