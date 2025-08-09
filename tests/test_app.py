import json
import threading
from http.server import HTTPServer
from urllib import request, error
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app import WibuHandler


def run_server():
    server = HTTPServer(("localhost", 0), WibuHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def post(server, payload):
    port = server.server_address[1]
    data = json.dumps(payload).encode()
    req = request.Request(
        f"http://localhost:{port}/wibu-score",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_wibu_score_success():
    server = run_server()
    status, data = post(server, {"answers": [True] * 5})
    assert status == 200
    assert data["score"] == 100
    assert data["description"] == "Dewa wibu"
    server.shutdown()


def test_wibu_score_invalid_length():
    server = run_server()
    status, data = post(server, {"answers": [True]})
    assert status == 400
    assert "error" in data
    server.shutdown()
