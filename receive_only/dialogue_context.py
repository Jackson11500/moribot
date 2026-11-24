"""Resolve OneBot quotations within the same group's recently received events."""

from collections import OrderedDict
from time import monotonic

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageEvent
from pydantic import TypeAdapter

MESSAGE = TypeAdapter(Message)


class RecentMessages:
    def __init__(self):
        self.groups = {}

    def remember(self, event):
        if type(event.get("message_id")) is not int or "message" not in event:
            return
        entries = self.groups.setdefault(int(event["group_id"]), OrderedDict())
        key = str(event["message_id"])
        now = monotonic()
        while entries and now - next(iter(entries.values()))[0] >= 1800:
            entries.popitem(last=False)
        entries[key] = (now, event)
        entries.move_to_end(key)
        if len(entries) > 256:
            entries.popitem(last=False)

    def get(self, group, message_id):
        entries = self.groups.get(group)
        if entries and message_id in entries:
            saved, source = entries[message_id]
            if monotonic() - saved < 1800:
                return source
            del entries[message_id]
        return None


def addressed_text(event: MessageEvent, recent: RecentMessages):
    parts = list(event.original_message)
    if not parts:
        return None
    if all(p.type == "text" for p in parts):
        return event.original_message.extract_plain_text(), False, None, None
    if not isinstance(event, GroupMessageEvent):
        return None
    quote_id = source = None
    if parts[0].type == "reply":
        quote_id = str(parts.pop(0).data.get("id", ""))
        digits = quote_id.removeprefix("-")
        if not digits.isascii() or not digits.isdecimal() or quote_id == str(event.message_id):
            return None
        source = recent.get(event.group_id, quote_id)

    mentions = [(i, str(p.data.get("qq"))) for i, p in enumerate(parts) if p.type == "at"]
    if any(p.type not in ("text", "at") for p in parts) or not mentions:
        return None
    # Some QQ clients insert an @ of the quoted author ahead of the user's own @.
    if len(mentions) == 2 and source and mentions[0][1] == str(source.get("user_id")):
        auto_index, _ = mentions[0]
        if any(p.data.get("text", "").strip() for p in parts[:auto_index]):
            return None
        parts.pop(auto_index)
        mentions = [(mentions[1][0] - 1, mentions[1][1])]
    if len(mentions) != 1 or mentions[0][1] != str(event.self_id):
        return None
    idx = mentions[0][0]
    before = "".join(p.data["text"] for p in parts[:idx]).strip()
    after = "".join(p.data["text"] for p in parts[idx + 1:]).strip()
    if before and after:
        return None
    return before or after, True, quote_id, source


def message_info(event, text):
    sender = event.get("sender") or {}
    card, nick = sender.get("card"), sender.get("nickname")
    return {
        "group_id": event["group_id"], "message_id": event["message_id"],
        "time_unix": event["time"], "message_type": event["message_type"],
        "sender": {"user_id": event.get("user_id"), "nickname": nick, "group_card": card,
                   "display_name": card or nick or None, "role": sender.get("role")},
        "text": text,
    }


def model_context(event, text, quote_id, source):
    quote = None
    if quote_id is not None:
        quote = {"message_id": quote_id, "status": "unavailable"}
    if source is not None:
        chunks = []
        for part in MESSAGE.validate_python(source["message"]):
            if part.type == "text":
                chunks.append(part.data["text"])
            elif part.type == "at":
                chunks.append("@" + str(part.data.get("qq")))
            else:
                chunks.append("[" + part.type + "]")
        quote = {"status": "resolved", **message_info(source, "".join(chunks))}
    return {"bot_id": event["self_id"], "current": message_info(event, text), "quote": quote}
