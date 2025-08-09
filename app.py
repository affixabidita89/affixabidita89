import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List

QUESTIONS = [
    "Do you watch anime weekly?",
    "Do you speak Japanese phrases in conversation?",
    "Have you attended an anime convention?",
    "Do you collect manga or figures?",
    "Do you have an anime profile picture?",
]


def describe(percentage: int) -> str:
    if percentage == 0:
        return "Bukan wibu"
    if percentage < 40:
        return "Sedikit wibu"
    if percentage < 70:
        return "Cukup wibu"
    if percentage < 100:
        return "Wibu sejati"
    return "Dewa wibu"


def calculate_score(answers: List[bool]) -> int:
    score = sum(1 for ans in answers if ans)
    return int(score / len(QUESTIONS) * 100)


class WibuHandler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict, status: int):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/wibu-score":
            self._send_json({"error": "not found"}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
        except Exception:
            self._send_json({"error": "invalid json"}, 400)
            return
        answers = payload.get("answers", [])
        if len(answers) != len(QUESTIONS):
            self._send_json({"error": f"expected {len(QUESTIONS)} answers"}, 400)
            return
        percentage = calculate_score(answers)
        self._send_json({
            "score": percentage,
            "description": describe(percentage),
        }, 200)


def run(port: int = 8000):
    server = HTTPServer(("", port), WibuHandler)
    print(f"Serving on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
