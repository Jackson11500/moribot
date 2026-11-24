"""Receive signed OneBot v11 HTTP events on the loopback interface."""

from datetime import datetime, timezone
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Adapter, Bot, Event, MessageEvent
from nonebot.adapters.onebot.v11.exception import ApiNotAvailable
from nonebot.message import event_preprocessor


RUNTIME = Path(__file__).resolve().parent / ".runtime"
PORT = 18765


class ReceiveOnlyAdapter(Adapter):
    async def _call_api(self, bot: Bot, api: str, **data):
        # Also blocks automatic lookups, e.g. get_msg for quoted messages.
        raise ApiNotAvailable


def start():
    secret = (RUNTIME / "post-secret").read_text(encoding="ascii").strip()
    if not secret:
        raise RuntimeError("Empty OneBot HTTP signing secret")

    nonebot.init(
        driver="~fastapi",
        host="127.0.0.1",
        port=PORT,
        log_level="INFO",
        onebot_v11_secret=secret,
        onebot_v11_ws_urls=[],
        onebot_v11_api_roots={},
    )
    nonebot.get_driver().register_adapter(ReceiveOnlyAdapter)
    status = {"events": 0, "messages": 0, "last_event_utc": None}

    @event_preprocessor
    async def count_event(event: Event):
        status["events"] += 1
        if isinstance(event, MessageEvent):
            status["messages"] += 1
        status["last_event_utc"] = datetime.now(timezone.utc).isoformat()

    @nonebot.get_asgi().get("/status")
    async def get_status():
        return status

    # Only the adapter's HTTP POST endpoint is needed. No QQ action transport.
    nonebot.run(ws="none", access_log=False)


if __name__ == "__main__":
    start()
