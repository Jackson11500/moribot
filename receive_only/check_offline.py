"""Exercise the real HTTP receiver on a temporary port without starting LLBot."""

import hashlib
import hmac
import json
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener


def check():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    client = build_opener(ProxyHandler({}))

    def status():
        with client.open(base + "/status", timeout=2) as response:
            return json.load(response)

    with tempfile.TemporaryDirectory() as directory:
        key = secrets.token_hex(32)
        (Path(directory) / "post-secret").write_text(key, encoding="ascii")
        code = (
            "from pathlib import Path; import receiver, sys; "
            "receiver.RUNTIME = Path(sys.argv[1]); receiver.PORT = int(sys.argv[2]); "
            "receiver.start()"
        )
        process = subprocess.Popen(
            [sys.executable, "-c", code, directory, str(port)], cwd=Path(__file__).parent
        )
        try:
            for _ in range(100):
                if process.poll() is not None:
                    raise RuntimeError("Receiver exited before the check")
                try:
                    if status()["events"] == 0:
                        break
                except URLError:
                    time.sleep(0.1)
            else:
                raise RuntimeError("Receiver did not become ready")

            event = {
                "time": int(time.time()), "self_id": 10000, "post_type": "message",
                "message_type": "group", "sub_type": "normal", "group_id": 20000,
                "message_id": 1, "user_id": 30000, "sender": {"user_id": 30000},
                "message": [{"type": "text", "data": {"text": "签到"}}],
                "raw_message": "签到", "font": 0,
            }
            body = json.dumps(event).encode()
            request = Request(base + "/onebot/v11/http", data=body, headers={
                "Content-Type": "application/json", "X-Self-ID": "10000",
            })
            try:
                client.open(request, timeout=2).close()
            except HTTPError as exc:
                assert exc.code == 401
            else:
                raise AssertionError("Unsigned event accepted")
            signature = hmac.new(key.encode(), body, hashlib.sha1).hexdigest()
            request.add_header("X-Signature", "sha1=" + signature)
            with client.open(request, timeout=2) as response:
                assert (response.status, response.read()) == (204, b"")
            for _ in range(40):
                counts = status()
                if counts["events"] == counts["messages"] == 1:
                    break
                time.sleep(0.05)
            else:
                raise AssertionError(counts)
            print("PASS: unsigned event rejected; signed message counted; empty HTTP 204")
        finally:
            process.terminate()
            process.wait(timeout=5)


if __name__ == "__main__":
    check()
