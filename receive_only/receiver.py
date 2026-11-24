"""Receive signed OneBot events and answer commands in allowlisted conversations."""

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

from legacy_commands import command_reply


RUNTIME = Path(__file__).resolve().parent / ".runtime"
PORT = 18765


@dataclass(frozen=True)
class GreetingAccess:
    bot_id: int
    user_id: int
    group_ids: frozenset[int]

    @classmethod
    def load(cls, path: Path):
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(config, dict):
                raise ValueError("Expected an access object")
            if config.keys() == {"bot_id", "user_id", "group_id"}:
                groups = [config["group_id"]]
            elif config.keys() == {"bot_id", "user_id", "group_ids"}:
                groups = config["group_ids"]
            else:
                raise ValueError("Invalid access fields")
            if not isinstance(groups, list) or not groups:
                raise ValueError("Expected a non-empty group list")
            bot, user = config["bot_id"], config["user_id"]
            if any(type(v) is not int or v <= 0 for v in (bot, user, *groups)):
                raise ValueError("Invalid ID")
            if bot == user:
                raise ValueError("Bot cannot be its own caller")
            return cls(bot, user, frozenset(groups))
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
            event.group_id in self.group_ids
            and event.sub_type == "normal"
            and event.anonymous is None
        )


class ReceiveOnlyAdapter(Adapter):
    def __init__(self, driver: Driver, access: GreetingAccess | None):
        self.access = access
        self.recent_commands = deque(maxlen=256)
        self.greeting_responses = 0
        self.command_responses = 0
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
        message = event.original_message
        if not message or any(segment.type != "text" for segment in message):
            return response
        key = (event.get_session_id(), event.message_id, event.time)
        if key in self.recent_commands:
            return response
        text = message.extract_plain_text()
        reply = command_reply(text, group=isinstance(event, GroupMessageEvent))
        if reply is None:
            return response
        self.recent_commands.append(key)
        self.command_responses += 1
        if text == "茉莉酱":
            self.greeting_responses += 1
        # OpenQQ selects the destination from its original event.
        operation = {"reply": reply, "at_sender": False, "auto_escape": True}
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
            "command_responses": adapter.command_responses,
        }

    # OpenQQ executes quick replies from this signed event's response.
    nonebot.run(ws="none", access_log=False)


if __name__ == "__main__":
    start()
