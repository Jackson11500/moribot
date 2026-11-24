"""Receive signed OneBot events and optionally answer one allowlisted greeting."""

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import (
    Adapter, Bot, Event, GroupMessageEvent, MessageEvent, PrivateMessageEvent,
)
from nonebot.adapters.onebot.v11.exception import ApiNotAvailable
from nonebot.drivers import Driver, Request, Response
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor


RUNTIME = Path(__file__).resolve().parent / ".runtime"
PORT = 18765
GREETING = "茉莉酱"
GREETING_REPLY = "主人找我有什么事呢？"


@dataclass(frozen=True)
class GreetingAccess:
    bot_id: int
    user_id: int
    group_id: int

    @classmethod
    def load(cls, path: Path):
        try:
            access = cls(**json.loads(path.read_text(encoding="utf-8")))
            if any(type(v) is not int or v <= 0 for v in vars(access).values()):
                raise ValueError("Invalid ID")
            if access.bot_id == access.user_id:
                raise ValueError("Bot cannot be its own caller")
            return access
        except FileNotFoundError:
            return None
        except (OSError, TypeError, ValueError):
            nonebot.logger.warning("Invalid greeting access file. Replies disabled.")
            return None

    def allows(self, event: Event) -> bool:
        if not isinstance(event, (PrivateMessageEvent, GroupMessageEvent)):
            return False
        if event.self_id != self.bot_id or event.user_id != self.user_id:
            return False
        if isinstance(event, PrivateMessageEvent):
            return event.sub_type == "friend"
        return (
            event.group_id == self.group_id
            and event.sub_type == "normal"
            and event.anonymous is None
        )


class ReceiveOnlyAdapter(Adapter):
    def __init__(self, driver: Driver, access: GreetingAccess | None):
        self.access = access
        self.recent_greetings = deque(maxlen=256)
        self.greeting_responses = 0
        super().__init__(driver)

    async def _call_api(self, bot: Bot, api: str, **data):
        # Also blocks automatic lookups, e.g. get_msg for quoted messages.
        raise ApiNotAvailable

    async def _handle_http(self, request: Request) -> Response:
        # The parent verifies the HMAC and schedules ordinary inbound processing.
        response = await super()._handle_http(request)
        if response.status_code != 204 or self.access is None:
            return response
        if request.headers.get("x-self-id") != str(self.access.bot_id):
            return response
        payload = json.loads(request.content)
        if not isinstance(payload, dict) or payload.get("post_type") != "message":
            return response
        if str(payload.get("user_id")) != str(self.access.user_id):
            return response
        event = self.json_to_event(payload)
        if not isinstance(event, MessageEvent) or not self.access.allows(event):
            return response
        if str(event.original_message) != GREETING:
            return response
        key = (event.get_session_id(), event.message_id, event.time)
        if key in self.recent_greetings:
            return response
        self.recent_greetings.append(key)
        self.greeting_responses += 1
        # OpenQQ selects the destination from its original event.
        operation = {"reply": GREETING_REPLY, "at_sender": False, "auto_escape": True}
        return Response(
            200, headers={"Content-Type": "application/json"}, content=json.dumps(operation)
        )


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
    access = GreetingAccess.load(RUNTIME / "greeting-access.json")
    nonebot.get_driver().register_adapter(ReceiveOnlyAdapter, access=access)
    adapter = nonebot.get_adapter(ReceiveOnlyAdapter)
    status = {"events": 0, "messages": 0, "last_event_utc": None}

    @event_preprocessor
    async def count_event(bot: Bot, event: Event):
        status["events"] += 1
        if isinstance(event, MessageEvent):
            status["messages"] += 1
        status["last_event_utc"] = datetime.now(timezone.utc).isoformat()
        if access and (bot.self_id != str(access.bot_id) or not access.allows(event)):
            raise IgnoredException("Outside the configured test conversations")

    @nonebot.get_asgi().get("/status")
    async def get_status():
        return {
            **status,
            "greeting_enabled": access is not None,
            "greeting_responses": adapter.greeting_responses,
        }

    # A scoped greeting uses the POST response; no outbound action API is needed.
    nonebot.run(ws="none", access_log=False)


if __name__ == "__main__":
    start()
