#!/usr/bin/env python3
"""Persistent OneBot transcripts and a read-only viewer for the host operator."""

import argparse
from contextlib import closing
from datetime import date, datetime, time, timedelta, timezone
import json
from pathlib import Path
import sqlite3

from dialogue_log import encode, now, printable


LOCAL_TIME = timezone(timedelta(hours=8))
DEFAULT_DB = Path("/var/lib/moribot-dialogue/messages.sqlite3")


def conversation_id(event, owner_id):
    """Accept reported groups and the operator's own friend conversation."""
    if event.get("post_type") not in ("message", "message_sent") or "message" not in event:
        return None
    if any(type(event.get(k)) is not int for k in ("self_id", "message_id", "user_id", "time")):
        return None
    sent = event["post_type"] == "message_sent"
    if sent and event["user_id"] != event["self_id"]:
        return None
    if event.get("message_type") == "group":
        group = event.get("group_id")
        return group if type(group) is int and group > 0 else None
    if event.get("message_type") == "private" and event.get("sub_type") == "friend":
        peer = event.get("target_id") if sent else event["user_id"]
        if owner_id is not None and peer == owner_id:
            return peer
    return None


class MessageArchive:
    def __init__(self, path, calls_path, access):
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, timeout=0.5)
        path.chmod(0o600)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY, bot INTEGER NOT NULL, kind TEXT NOT NULL, chat INTEGER NOT NULL,
            message_id INTEGER NOT NULL, sender INTEGER NOT NULL, sent_at INTEGER NOT NULL,
            post_type TEXT NOT NULL, event TEXT NOT NULL, source TEXT NOT NULL,
            quick_reply TEXT, reply_at TEXT,
            UNIQUE(bot,kind,chat,message_id,sender,sent_at,post_type))""")
        self.db.execute("CREATE INDEX IF NOT EXISTS chat_time ON messages(kind,chat,sent_at,id)")
        self.db.execute("CREATE INDEX IF NOT EXISTS all_time ON messages(sent_at,id)")
        if self.db.execute("PRAGMA user_version").fetchone()[0] == 0:
            # Recover only original events that the previous model journal actually saved.
            with self.db:
                if calls_path.is_file() and access:
                    with closing(sqlite3.connect(calls_path.resolve().as_uri() + "?mode=ro", uri=True)) as calls:
                        for pair in calls.execute("SELECT quote_event,event FROM calls ORDER BY id"):
                            for raw in filter(None, pair):
                                event = json.loads(raw)
                                chat = conversation_id(event, access.user_id)
                                if chat is not None and event["self_id"] == access.bot_id:
                                    self._insert(event, chat, "model_journal")
                self.db.execute("PRAGMA user_version=1")

    def _insert(self, event, chat, source):
        key = (event["self_id"], event["message_type"], chat, event["message_id"],
               event["user_id"], event["time"], event["post_type"])
        cursor = self.db.execute("""INSERT INTO messages
            (bot,kind,chat,message_id,sender,sent_at,post_type,event,source)
            VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT DO NOTHING""", (*key, encode(event), source))
        if cursor.rowcount:
            return cursor.lastrowid, False
        return self.db.execute("""SELECT id,quick_reply IS NOT NULL FROM messages
            WHERE bot=? AND kind=? AND chat=? AND message_id=? AND sender=? AND sent_at=? AND post_type=?""", key).fetchone()

    def record(self, event, chat):
        with self.db:
            return self._insert(event, chat, "onebot")

    def quick_reply(self, row_id, operation):
        with self.db:
            self.db.execute("UPDATE messages SET quick_reply=?,reply_at=? WHERE id=?",
                            (encode(operation), now(), row_id))

    async def close(self):
        self.db.close()


def preview(message):
    if isinstance(message, str):
        return message
    pieces = []
    for part in message:
        kind, data = part["type"], part.get("data", {})
        if kind == "text":
            pieces.append(data.get("text", ""))
        elif kind == "at":
            pieces.append("@" + str(data.get("qq", "")))
        elif kind == "reply":
            pieces.append("[引用 " + str(data.get("id", "")) + "]")
        else:
            pieces.append("[" + kind + "]")
    return "".join(pieces)


def main():
    parser = argparse.ArgumentParser(description="查看茉莉长期保存的 OneBot 消息。日期按北京时间。")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--groups", action="store_true", help="列出已归档群号及上报消息数")
    parser.add_argument("--id", type=int, help="按本地归档编号定位一条消息")
    parser.add_argument("--group", type=int, help="按群号筛选")
    parser.add_argument("--date", type=date.fromisoformat, help="北京时间 YYYY-MM-DD，默认读取当天全部记录")
    count = parser.add_mutually_exclusive_group()
    count.add_argument("--limit", type=int, help="最近 N 条，未指定日期时默认 20")
    count.add_argument("--all", action="store_true", help="按时间顺序读取全部匹配记录")
    parser.add_argument("--jsonl", action="store_true", help="逐条输出完整 JSON")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit 必须为正整数")
    if args.groups and (args.group is not None or args.date or args.limit or args.all or args.jsonl or args.id is not None):
        parser.error("--groups 单独使用")
    if not args.db.is_file():
        parser.exit(1, "尚未创建消息归档库。\n")
    with closing(sqlite3.connect(args.db.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        if args.groups:
            for chat, total in db.execute("SELECT chat, count(*) FROM messages WHERE kind='group' GROUP BY chat ORDER BY chat"):
                print(f"{chat}\t{total}")
            return
        filters, params = [], []
        if args.id is not None:
            filters.append("id=?")
            params.append(args.id)
        if args.group is not None:
            filters.append("kind='group' AND chat=?")
            params.append(args.group)
        if args.date:
            start = datetime.combine(args.date, time.min, LOCAL_TIME)
            filters.append("sent_at>=? AND sent_at<?")
            params.extend([int(start.timestamp()), int((start + timedelta(days=1)).timestamp())])
        query = "SELECT id,kind,chat,sent_at,event,source,quick_reply,reply_at FROM messages"
        if filters:
            query += " WHERE " + " AND ".join(filters)
        if args.all or (args.date and args.limit is None):
            query += " ORDER BY sent_at,id"
        else:
            query += " ORDER BY sent_at DESC,id DESC LIMIT ?"
            params.append(args.limit or 20)
        for row_id, kind, chat, stamp, raw, source, reply, reply_at in db.execute(query, params):
            event = json.loads(raw)
            operation = json.loads(reply) if reply else None
            if args.jsonl:
                print(encode({"id": row_id, "source": source, "event": event,
                              "quick_reply": operation, "reply_at": reply_at}))
                continue
            sender = event.get("sender") or {}
            name = sender.get("card") or sender.get("nickname") or event["user_id"]
            stamp = datetime.fromtimestamp(stamp, LOCAL_TIME).strftime("%Y-%m-%d %H:%M:%S")
            place = "群" if kind == "group" else "私聊"
            print(printable(f"#{row_id} {stamp} {place} {chat} | {name}：{preview(event['message'])}"))
            if operation:
                print(printable("  茉莉快速回复：" + preview(operation["reply"])))


if __name__ == "__main__":
    main()
