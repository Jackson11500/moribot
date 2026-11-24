"""Read-only queries for an authorized group or the owner's archive console."""

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


MENU = ("查看指令\n日报 / 昨日日报 / 日报 YYYY-MM-DD\n运行状态 / 群权限 / 消息统计\n"
        "最近消息（5 条，可加 #编号 查看更早的消息）\n查记录 #编号 [页码]")
ADMIN_MENU = (MENU + "\n\n管理群专用\n群列表　列出已归档的群\n群 <群号> 日报 / 昨日日报 / 日报 YYYY-MM-DD"
              "\n群 <群号> 最近消息 / 消息统计 / 查记录 #编号\n查记录 #编号　跨群或本人私聊查原文"
              "\n我的私聊　本人好友会话最近消息\n模型记录 / 模型回复 #调用编号 [页码]　查看 DeepSeek 问答"
              "\n列表有后续页时，末行给出下一条指令。")
DATE_HELP = "请输入「日报 YYYY-MM-DD」，日期可选今天或更早。"
RECORD_HELP = "请输入「查记录 #编号 [页码]」，编号可在日报或最近消息中找到。"


@dataclass(frozen=True)
class GroupQuery:
    kind: str
    value: str = ""
    group_id: int | None = None

    @property
    def admin_only(self):
        return self.group_id is not None or self.kind in {"groups", "private", "calls", "call", "admin_help"}


def number(value):
    if re.fullmatch(r"[1-9][0-9]{0,18}", value):
        n = int(value)
        if n <= 2**63 - 1:
            return n
    return None


def parse_query(text):
    text = text.strip()
    group = None
    if re.match(r"^群(?:\s|[0-9])", text):
        head = re.fullmatch(r"群\s*([0-9]+)\s+(.+)", text)
        if not head or (group := number(head[1])) is None:
            return GroupQuery("admin_help")
        text = head[2].strip()
    simple = {"本群查询": "menu", "查询帮助": "menu", "查看指令": "menu", "查询指令": "menu",
              "指令列表": "menu", "菜单": "menu", "帮助": "menu", "日报": "today", "本群日报": "today",
              "今日日报": "today", "昨日日报": "yesterday", "运行状态": "status",
              "消息统计": "stats"}
    kind, value = simple.get(text), ""
    if kind is None:
        match = re.fullmatch(r"(日报|查记录|群列表|已归档群|最近消息|我的私聊|模型记录|模型回复)(?:[\s：:]+(.*)|(#.*))?", text)
        if not match:
            return GroupQuery("admin_help") if group is not None else None
        kind = {"日报": "date", "查记录": "record", "群列表": "groups", "已归档群": "groups",
                "最近消息": "recent", "我的私聊": "private", "模型记录": "calls", "模型回复": "call"}[match[1]]
        value = (match[2] or match[3] or "").strip()
    if group is not None and kind not in {"today", "yesterday", "date", "stats", "recent", "record"}:
        return GroupQuery("admin_help")
    return GroupQuery(kind, value, group)


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


def paged_detail(text, page, command):
    size = 1400
    pages = max(1, (len(text) + size - 1) // size)
    if page > pages:
        return f"这条记录共 {pages} 页。"
    body = text[(page - 1) * size:page * size]
    return body + (f"\n下一页：{command} {page + 1}" if page < pages else "")


def model_query(db, kind, bot, owner, item, page):
    scope = """json_extract(event,'$.self_id')=? AND (json_extract(event,'$.message_type')='group'
        OR (json_extract(event,'$.message_type')='private' AND json_extract(event,'$.user_id')=?))"""
    cols = "id,started,status,event,quote_event,reply"
    if kind == "call":
        rows = db.execute(f"SELECT {cols} FROM calls WHERE {scope} AND id=?", (bot, owner, item))
    else:
        before = " AND id<?" if item else ""
        rows = db.execute(f"SELECT {cols} FROM calls WHERE {scope}{before} ORDER BY id DESC LIMIT 6",
                          (bot, owner, item) if item else (bot, owner))
    lines = []
    for idx, started, state, raw, quote, reply in rows:
        if len(lines) == 5:
            lines.append(f"更早：模型记录 #{last_id}")
            break
        event = json.loads(raw)
        place = "群 " + str(event["group_id"]) if event.get("group_id") else "本人私聊"
        when = datetime.fromisoformat(started).astimezone(LOCAL_TIME).strftime("%m-%d %H:%M")
        header = f"调用 #{idx} · {place} · {when} · {state}"
        question = preview(event["message"])
        if kind == "call":
            text = header + f"\n提问人 QQ {event['user_id']}\n提问：{question}"
            if quote:
                source = json.loads(quote)
                text += f"\n引用（QQ {source['user_id']}）：{preview(source['message'])}"
            text += "\n茉莉：" + (reply or "暂无回复")
            return paged_detail(text, page, f"模型回复 #{idx}")
        lines.append(f"{header}\n{question[:80]}")
        last_id = idx
    return ("模型记录\n" + "\n".join(lines)) if lines else "没有匹配的模型调用。"


def read_query(query, path, bot, group, row_id, ai_ready, *, admin_owner=None):
    if query.admin_only and admin_owner is None:
        return "此查询仅限管理群。"
    if query.kind == "admin_help":
        return ADMIN_MENU
    if query.kind == "menu":
        return ADMIN_MENU if admin_owner is not None else MENU
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
    item, page = None, 1
    if query.kind in {"call", "record"}:
        parts = query.value.removeprefix("#").split()
        if not (1 <= len(parts) <= 2 and (item := number(parts[0])) and
                (len(parts) == 1 or (page := number(parts[1])))):
            return RECORD_HELP if query.kind == "record" else "请输入「模型回复 #调用编号 [页码]」。"
    elif query.value and query.kind in {"groups", "private", "calls", "recent"}:
        item = number(query.value.removeprefix("#"))
        if item is None:
            return "续查请使用列表末行给出的编号。"
    database = path.with_name("calls.sqlite3") if query.kind in {"call", "calls"} else path
    deadline = monotonic() + 2.6
    with closing(sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True, timeout=0.25)) as db:
        db.set_progress_handler(lambda: int(monotonic() >= deadline), 1000)
        db.execute("BEGIN")
        if query.kind in {"call", "calls"}:
            return model_query(db, query.kind, bot, admin_owner, item, page)
        if query.kind == "groups":
            groups = db.execute("""SELECT chat,COUNT(*) FROM messages WHERE kind='group' AND bot=? AND chat>?
                GROUP BY chat ORDER BY chat LIMIT 21""", (bot, item or 0)).fetchall()
            lines = [f"群 {g}　{count} 条" for g, count in groups[:20]]
            if len(groups) > 20:
                lines.append(f"下一页：群列表 {groups[19][0]}")
            return "已归档群\n" + ("\n".join(lines) or "暂无更多群。")
        start = int(datetime.combine(day, time.min, LOCAL_TIME).timestamp())
        end = min(start + 86400, int(now.timestamp()) + 1)
        target = query.group_id or group
        place = f"群 {target}" if query.group_id is not None else "本群"
        scope = "kind=? AND chat=? AND bot=?"
        params = ("group", target, bot)
        if query.kind in ("today", "yesterday", "date"):
            raw = report(db, target, day, start, end, now, bot_id=bot)
            lines = [unescape(line.removeprefix("## ").removeprefix("# ").replace("**", ""))
                     for line in raw.splitlines()]
            return "\n".join(line[:340] + ("…" if len(line) > 340 else "") for line in lines)[:3500]
        if query.kind == "stats":
            total, = db.execute(f"SELECT COUNT(*) FROM messages WHERE {scope}", params).fetchone()
            today, = db.execute(f"SELECT COUNT(*) FROM messages WHERE {scope} AND sent_at>=? AND sent_at<?",
                                (*params, start, end)).fetchone()
            suffix = "含本条查询。" if target == group else ""
            return f"{place}消息统计（北京时间）\n今日归档 {today} 条，累计归档 {total} 条。{suffix}"
        if query.kind in {"recent", "private"}:
            prefix = f"群 {target} " if query.group_id is not None else ""
            command = prefix + "最近消息"
            if query.kind == "private":
                params, place, command = ("private", admin_owner, bot), "本人私聊", "我的私聊"
            rows = db.execute(f"SELECT id,sent_at,sender,event FROM messages WHERE {scope} AND id<? ORDER BY id DESC LIMIT 6",
                              (*params, min(item or row_id, row_id))).fetchall()
            lines = [record_line(row, 100) for row in rows[:5]]
            if len(rows) > 5:
                lines.append(f"更早：{command} #{rows[4][0]}")
            return place + "最近消息\n" + ("\n".join(lines) or "暂时没有更早的记录。")
        if admin_owner is not None and query.group_id is None:
            scope = "bot=? AND (kind='group' OR (kind='private' AND chat=?))"
            params, place = (bot, admin_owner), "档案中"
        row = db.execute(f"SELECT kind,chat,sent_at,sender,event,quick_reply FROM messages WHERE {scope} AND id=?",
                         (*params, item)).fetchone()
        if not row:
            return place + "没有这个归档编号。"
        kind, chat, stamp, uid, raw, quick = row
        event = json.loads(raw)
        sender = event.get("sender") or {}
        name = sender.get("card") or sender.get("nickname") or "未上报昵称"
        where = f"群 {chat}" if kind == "group" else "本人私聊"
        when = datetime.fromtimestamp(stamp, LOCAL_TIME).strftime("%Y-%m-%d %H:%M:%S")
        text = f"归档 #{item} · {where} · {when}\n{name}（QQ {uid}）\n{preview(event['message'])}"
        if quick and admin_owner is not None:
            text += "\n茉莉快速回复：" + preview(json.loads(quick)["reply"])
        prefix = f"群 {target} " if query.group_id is not None else ""
        return paged_detail(text, page, f"{prefix}查记录 #{item}")


async def run_query(query, path, bot, group, row_id, ai_ready, *, admin_owner=None):
    try:
        return await asyncio.wait_for(asyncio.to_thread(read_query, query, path, bot, group, row_id, ai_ready,
                                                       admin_owner=admin_owner), 3.3)
    except (TimeoutError, sqlite3.Error):
        return "这次没能读完本群记录，稍后再试一下吧。"
