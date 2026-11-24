"""Read-only QQ commands scoped to the authenticated event's group."""

import asyncio
from contextlib import closing
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from html import unescape
import json
import re
import sqlite3
import subprocess
from time import monotonic

from daily_report import report
from message_archive import LOCAL_TIME, preview


MENU = ("本群查询\n日报 / 昨日日报 / 日报 YYYY-MM-DD\n运行状态 / 消息统计\n"
        "最近消息（最近 5 条） / 查记录 #编号")
DATE_HELP = "请输入「日报 YYYY-MM-DD」，日期可选今天或更早。"
RECORD_HELP = "请输入「查记录 #编号」，编号可在本群日报或最近消息中找到。"


@dataclass(frozen=True)
class GroupQuery:
    kind: str
    value: str = ""


def parse_query(text):
    text = text.strip()
    simple = {"本群查询": "menu", "查询帮助": "menu", "日报": "today", "本群日报": "today",
              "今日日报": "today", "昨日日报": "yesterday", "运行状态": "status",
              "消息统计": "stats", "最近消息": "recent"}
    if text in simple:
        return GroupQuery(simple[text])
    match = re.fullmatch(r"(日报|查记录)(?:[\s：:]+(.*)|(#.*))?", text)
    if match:
        return GroupQuery("date" if match[1] == "日报" else "record", (match[2] or match[3] or "").strip())
    return None


def service_states():
    try:
        states = subprocess.run(["systemctl", "is-active", "moribot-openqq.service", "moribot-daily.timer"],
                                capture_output=True, text=True, timeout=0.7).stdout.splitlines()
    except (OSError, subprocess.TimeoutExpired):
        states = []
    labels = {"active": "运行中", "inactive": "未运行", "failed": "故障", "activating": "启动中"}
    return [labels.get(state, "未知") for state in (states + ["", ""])[:2]]


def record_line(row, length):
    row_id, stamp, uid, raw = row
    event = json.loads(raw)
    sender = event.get("sender") or {}
    name = (sender.get("card") or sender.get("nickname") or "未上报昵称")[:48]
    content = " ".join(preview(event["message"]).split())
    when = datetime.fromtimestamp(stamp, LOCAL_TIME).strftime("%m-%d %H:%M")
    return f"#{row_id} {when} {name}（{uid}）\n{content[:length]}" + ("…" if len(content) > length else "")


def read_query(query, path, bot, group, row_id, ai_ready):
    if query.kind == "menu":
        return MENU
    if query.kind == "status":
        qq, timer = service_states()
        return (f"运行状态\nOpenQQ：{qq}\n接收器：已收到本条上报\n本群归档：本条已入库"
                f"\nDeepSeek：{'已配置' if ai_ready else '未就绪'}\n每日 00:10 日报定时器：{timer}（北京时间）")
    now = datetime.now(LOCAL_TIME)
    day = now.date()
    if query.kind == "yesterday":
        day -= timedelta(days=1)
    elif query.kind == "date":
        try:
            day = date.fromisoformat(query.value)
        except ValueError:
            return DATE_HELP
        if day > now.date() or query.value != day.isoformat():
            return DATE_HELP
    deadline = monotonic() + 2.6
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=0.25)) as db:
        db.set_progress_handler(lambda: int(monotonic() >= deadline), 1000)
        db.execute("BEGIN")
        start = int(datetime.combine(day, time.min, LOCAL_TIME).timestamp())
        end = min(start + 86400, int(now.timestamp()) + 1)
        scope = "kind='group' AND chat=? AND bot=?"
        if query.kind in ("today", "yesterday", "date"):
            raw = report(db, group, day, start, end, now, bot_id=bot)
            lines = [unescape(line.removeprefix("## ").removeprefix("# ").replace("**", ""))
                     for line in raw.splitlines()]
            return "\n".join(line[:340] + ("…" if len(line) > 340 else "") for line in lines)[:3500]
        if query.kind == "stats":
            total, = db.execute(f"SELECT COUNT(*) FROM messages WHERE {scope}", (group, bot)).fetchone()
            today, = db.execute(f"SELECT COUNT(*) FROM messages WHERE {scope} AND sent_at>=? AND sent_at<?",
                                (group, bot, start, end)).fetchone()
            return f"本群消息统计（北京时间）\n今日归档 {today} 条，累计归档 {total} 条。含本条查询。"
        select = f"SELECT id,sent_at,sender,event FROM messages WHERE {scope}"
        if query.kind == "recent":
            rows = db.execute(select + " AND id<? ORDER BY sent_at DESC,id DESC LIMIT 5", (group, bot, row_id))
            return "本群最近消息\n" + ("\n".join(record_line(row, 100) for row in rows) or "暂时没有更早的记录。")
        value = query.value.removeprefix("#").strip()
        if not re.fullmatch(r"[0-9]{1,19}", value) or not 0 < int(value) <= 2**63 - 1:
            return RECORD_HELP
        row = db.execute(select + " AND id=?", (group, bot, int(value))).fetchone()
        return record_line(row, 1400) if row else "本群没有这个归档编号。"


async def run_query(query, path, bot, group, row_id, ai_ready):
    try:
        return await asyncio.wait_for(asyncio.to_thread(read_query, query, path, bot, group, row_id, ai_ready), 3.3)
    except (TimeoutError, sqlite3.Error):
        return "这次没能读完本群记录，稍后再试一下吧。"
