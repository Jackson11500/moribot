#!/usr/bin/env python3
"""Private DeepSeek call journal. Run this file on the host to read it."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3


def journal_path(runtime: Path) -> Path:
    directory = Path(os.environ["STATE_DIRECTORY"]) if os.environ.get("STATE_DIRECTORY") else runtime / "dialogue"
    return directory / "calls.sqlite3"


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class DialogueLog:
    def __init__(self, path: Path):
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, timeout=0.2)
        path.chmod(0o600)
        with self.db:
            self.db.execute("""CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY, started TEXT NOT NULL, finished TEXT, status TEXT NOT NULL,
                event TEXT NOT NULL, quote_event TEXT, request TEXT NOT NULL, http_status INTEGER,
                response_body TEXT, reply TEXT, error TEXT)""")

    def begin(self, event, quote_event, request):
        with self.db:
            cursor = self.db.execute(
                "INSERT INTO calls(started,status,event,quote_event,request) VALUES(?,?,?,?,?)",
                (now(), "started", encode(event), None if quote_event is None else encode(quote_event), encode(request)),
            )
            return cursor.lastrowid

    def finish(self, record_id, status, http_status, response_body, reply, error):
        with self.db:
            self.db.execute(
                "UPDATE calls SET finished=?,status=?,http_status=?,response_body=?,reply=?,error=? WHERE id=?",
                (now(), status, http_status, response_body, reply, error, record_id),
            )


def read_calls(path, *, record_id=None, limit=10):
    db = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    try:
        if record_id is not None:
            rows = db.execute("SELECT * FROM calls WHERE id=?", (record_id,))
        elif limit is None:
            rows = db.execute("SELECT * FROM calls ORDER BY id")
        else:
            rows = db.execute("SELECT * FROM calls ORDER BY id DESC LIMIT ?", (limit,))
        for row in rows:
            item = dict(row)
            for field in ("event", "quote_event", "request"):
                if item[field] is not None:
                    item[field] = json.loads(item[field])
            yield item
    finally:
        db.close()


def printable(text):
    return "".join(c if c.isprintable() or c in "\n\t" else ascii(c)[1:-1] for c in str(text))


def main():
    parser = argparse.ArgumentParser(description="查看茉莉的 DeepSeek 调用记录")
    parser.add_argument("--id", type=int, help="输出一条完整 JSON 记录")
    count = parser.add_mutually_exclusive_group()
    count.add_argument("--limit", type=int, default=10, help="最近记录数，默认 10")
    count.add_argument("--all", action="store_true", help="按调用顺序读取全部记录")
    parser.add_argument("--json", action="store_true", help="以完整 JSON 输出")
    parser.add_argument("--db", type=Path, default=Path("/var/lib/moribot-dialogue/calls.sqlite3"))
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit 必须为正整数")
    if not args.db.is_file():
        parser.exit(1, "尚未创建对话记录库。\n")
    records = read_calls(args.db, record_id=args.id, limit=None if args.all else args.limit)
    if args.id is not None:
        record = next(records, None)
        records.close()
        if record is None:
            parser.exit(1, "找不到该记录。\n")
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return
    if args.json:
        print("[", end="")
        for index, record in enumerate(records):
            print("," if index else "", json.dumps(record, ensure_ascii=False, indent=2), sep="", end="")
        print("]")
        return
    any_records = False
    for record in records:
        any_records = True
        context = json.loads(record["request"]["messages"][-1]["content"])
        current = context["current"]
        print(printable(f'#{record["id"]}  {record["started"]}  {record["status"]}  群 {current["group_id"]}'))
        if quote := context["quote"]:
            author = quote.get("sender", {}).get("display_name") or "未知"
            print(printable(f'  引用 #{quote["message_id"]} {author}：{quote.get("text", "（原文未找到）")}'))
        name = current["sender"]["display_name"] or "昵称未上报"
        print(printable(f'  {name}：{current["text"] or "（单独 @）"}'))
        print(printable(f'  茉莉：{record["reply"] or "（暂无结果）"}\n'))
    if not any_records:
        print("尚无 DeepSeek 调用记录。")


if __name__ == "__main__":
    main()
