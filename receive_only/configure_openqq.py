"""Configure the dedicated OpenQQ v0.5.0 portable release for inbound events."""

import json
from pathlib import Path
import secrets


RUNTIME = Path(__file__).resolve().parent / ".runtime"
OPENQQ = RUNTIME / "openqq" / "openqq-v0.5.0-win-x64"


def configure():
    path = OPENQQ / "config" / "openqq.json"
    config = json.loads((path.parent / "openqq.example.json").read_text(encoding="utf-8"))
    secret = (RUNTIME / "post-secret").read_text(encoding="ascii").strip()
    if not secret:
        raise ValueError("Missing receiver signing secret")
    if path.exists():
        config["accessToken"] = json.loads(path.read_text(encoding="utf-8"))["accessToken"]
    else:
        config["accessToken"] = secrets.token_hex(32)
    config["ws"]["enabled"] = False
    config["reverseWs"] = []
    config["http"]["enabled"] = False
    config["httpPost"] = [{
        "enabled": True,
        "url": "http://127.0.0.1:18765/onebot/v11/http",
        "secret": secret,
    }]
    config["reportSelfMessage"] = False
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(config, indent=2), encoding="utf-8")
    temp.replace(path)


if __name__ == "__main__":
    configure()
