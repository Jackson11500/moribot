"""Receive signed OneBot events and answer commands in allowlisted conversations."""

from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

import nonebot
from nonebot.adapters.onebot.v11 import (
    Adapter, Bot, Event, GroupMessageEvent, MessageEvent, PrivateMessageEvent,
)
from nonebot.adapters.onebot.v11.exception import ApiNotAvailable
from nonebot.drivers import Driver, Request, Response
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor

from deepseek_dialogue import DeepSeekDialogue, UNAVAILABLE
from dialogue_context import RecentMessages, addressed_text, model_context
from dialogue_log import journal_path
from legacy_commands import ASK_MODEL, MODULE_LABELS, command_reply, module_names
from message_archive import MessageArchive, conversation_id


RUNTIME = Path(__file__).resolve().parent / ".runtime"
PORT = 18765


@dataclass(frozen=True)
class GreetingAccess:
    bot_id: int
    user_id: int
    groups: dict[int, str]
    profiles: dict[str, frozenset[str]]

    @classmethod
    def load(cls, path: Path):
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(config, dict):
                raise ValueError("Expected an access object")
            bot, user = config["bot_id"], config["user_id"]
            if any(type(v) is not int or v <= 0 for v in (bot, user)):
                raise ValueError("Invalid ID")
            if bot == user:
                raise ValueError("Bot cannot be its own caller")
            fields = config.keys() - {"bot_id", "user_id"}
            if fields == {"group_id"} or fields == {"group_ids"}:
                ids = config.get("group_ids", [config.get("group_id")])
                if not isinstance(ids, list) or not ids or any(type(i) is not int or i <= 0 for i in ids):
                    raise ValueError("Invalid legacy group IDs")
                # Preserve exactly the modules available before profiles existed.
                legacy = frozenset(("greeting", "little_game", "technique", "chatting",
                                    "someone_say", "random_pic", "user"))
                return cls(bot, user, dict.fromkeys(ids, "test"), {"test": legacy})
            if fields != {"profiles", "groups"}:
                raise ValueError("Invalid access fields")
            profiles = {}
            if not isinstance(config["profiles"], dict) or not isinstance(config["groups"], dict):
                raise ValueError("Expected profile and group maps")
            for name, modules in config["profiles"].items():
                if not name.strip() or not isinstance(modules, list) or not set(modules) <= MODULE_LABELS.keys():
                    raise ValueError("Invalid permission profile")
                profiles[name] = frozenset(modules)
            groups = {}
            for raw_id, profile in config["groups"].items():
                if not raw_id.isascii() or not raw_id.isdecimal() or raw_id.startswith("0"):
                    raise ValueError("Invalid group ID")
                if profile not in profiles:
                    raise ValueError("Unknown permission profile")
                groups[int(raw_id)] = profile
            return cls(bot, user, groups, profiles)
        except FileNotFoundError:
            return None
        except (OSError, KeyError, TypeError, ValueError):
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
            event.group_id in self.groups
            and event.sub_type == "normal"
            and event.anonymous is None
        )

    def reply(self, event: MessageEvent, text: str, *, mentioned: bool = False):
        group = event.group_id if isinstance(event, GroupMessageEvent) else None
        if text in ("群权限", "群组状态"):
            visible = self.groups if group is None else [group]
            lines = ["群权限（仅你可调用）"]
            for group_id in visible:
                profile = self.groups[group_id]
                title = f"群 {group_id}" if group is None else "本群"
                lines.append(f"{title} · {profile}\n已开：{module_names(self.profiles[profile])}")
            return "\n".join(lines)
        modules = None if group is None else self.profiles[self.groups[group]]
        return command_reply(text, group_modules=modules, mentioned=mentioned)


class ReceiveOnlyAdapter(Adapter):
    def __init__(self, driver: Driver, access: GreetingAccess | None, dialogue: DeepSeekDialogue | None,
                 archive: MessageArchive):
        self.access = access
        self.dialogue = dialogue
        self.archive = archive
        self.archive_errors = 0
        self.in_flight = set()
        self.recent_messages = RecentMessages()
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
        if response.status_code != 204:
            return response
        header_id = request.headers.get("x-self-id")
        if self.access and header_id != str(self.access.bot_id):
            return response
        payload = json.loads(request.content)
        if not isinstance(payload, dict) or str(payload.get("self_id")) != header_id:
            return response
        chat = conversation_id(payload, self.access.user_id if self.access else None)
        if chat is None:
            return response
        try:
            row_id, replied = self.archive.record(payload, chat)
        except sqlite3.Error:
            self.archive_errors += 1
            nonebot.logger.exception("Cannot persist incoming message")
            return Response(503)
        if replied or self.access is None or payload["post_type"] != "message":
            return response
        if payload["message_type"] == "group" and chat not in self.access.groups:
            return response
        # Adapter validation adds original_message to its input dictionary.
        event = self.json_to_event(deepcopy(payload))
        if (isinstance(event, GroupMessageEvent) and event.self_id == self.access.bot_id
                and event.group_id in self.access.groups and event.sub_type == "normal"
                and event.anonymous is None and "ai_dialogue" in self.access.profiles[self.access.groups[event.group_id]]):
            self.recent_messages.remember(payload)
        if not isinstance(event, MessageEvent) or not self.access.allows(event):
            return response
        addressed = addressed_text(event, self.recent_messages)
        if addressed is None:
            return response
        key = (event.get_session_id(), event.message_id, event.time)
        if key in self.recent_commands or key in self.in_flight:
            return response
        text, mentioned, quote_id, source = addressed
        reply = self.access.reply(event, text, mentioned=mentioned)
        if reply is None:
            return response
        if reply is ASK_MODEL:
            self.in_flight.add(key)
            try:
                if self.dialogue:
                    context = model_context(payload, text, quote_id, source)
                    reply = await self.dialogue.answer(context, payload, source)
                else:
                    reply = UNAVAILABLE
            finally:
                self.in_flight.discard(key)
        if isinstance(event, GroupMessageEvent):
            body = [{"type": "text", "data": {"text": reply}}] if isinstance(reply, str) else reply
            reply = [{"type": "reply", "data": {"id": str(event.message_id)}}, *body]
        # Store exactly the quick operation we give OpenQQ, independently of delivery.
        operation = {"reply": reply, "at_sender": False, "auto_escape": True}
        try:
            self.archive.quick_reply(row_id, operation)
        except sqlite3.Error:
            self.archive_errors += 1
            nonebot.logger.exception("Cannot persist quick reply")
            return Response(503)
        self.recent_commands.append(key)
        self.command_responses += 1
        if text == "茉莉酱":
            self.greeting_responses += 1
        # OpenQQ selects the destination from its original event.
        return Response(
            200, headers={"Content-Type": "application/json"}, content=json.dumps(operation)
        )


def start(*, model_transport=None):
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
    calls_path = journal_path(RUNTIME)
    archive = MessageArchive(calls_path.with_name("messages.sqlite3"), calls_path, access)
    dialogue = DeepSeekDialogue.load(RUNTIME, model_transport)
    driver = nonebot.get_driver()
    driver.on_shutdown(archive.close)
    if dialogue:
        driver.on_shutdown(dialogue.client.aclose)
        driver.on_shutdown(dialogue.close_journal)
    driver.register_adapter(ReceiveOnlyAdapter, access=access, dialogue=dialogue, archive=archive)
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
            "archive_errors": adapter.archive_errors,
            "ai_ready": dialogue is not None,
            "ai_requests": dialogue.requests if dialogue else 0,
            "ai_failures": dialogue.failures if dialogue else 0,
        }

    # OpenQQ executes quick replies from this signed event's response.
    nonebot.run(ws="none", access_log=False)


if __name__ == "__main__":
    start()
