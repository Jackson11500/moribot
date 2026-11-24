"""Configure the dedicated LLBot 8.3.2 portable installation before login."""

import json
from pathlib import Path
import secrets


RUNTIME = Path(__file__).resolve().parent / ".runtime"
LLBOT = RUNTIME / "windows" / "bin" / "llbot"


def configure():
    default = LLBOT / "default_config.json"
    config = json.loads(default.read_text(encoding="utf-8"))
    secret_file = RUNTIME / "post-secret"
    if not secret_file.exists():
        with secret_file.open("x", encoding="ascii") as stream:
            stream.write(secrets.token_hex(32))
    secret = secret_file.read_text(encoding="ascii").strip()
    if len(secret) != 64:
        raise ValueError("Invalid local signing secret")

    config["webui"]["enable"] = False
    config["milky"]["enable"] = False
    config["satori"]["enable"] = False
    config["log"] = False
    config["ob11"] = {
        "enable": True,
        "connect": [{
            "type": "http-post",
            "enable": True,
            "url": "http://127.0.0.1:18765/onebot/v11/http",
            "token": secret,
            "enableHeart": True,
            "heartInterval": 60000,
            "reportSelfMessage": False,
            "reportOfflineMessage": False,
            "messageFormat": "array",
            "debug": False,
        }],
    }
    # New accounts inherit the default. Returning accounts load their own file.
    for path in [default, *(LLBOT / "data").glob("config_*.json")]:
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(config, indent=2), encoding="utf-8")
        temporary.replace(path)


if __name__ == "__main__":
    configure()
