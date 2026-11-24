#!/usr/bin/env python3
"""Build private group digests from the read-only OneBot message archive."""

import argparse
from collections import Counter, deque
from contextlib import closing
from datetime import date, datetime, time, timedelta
from html import escape
import json
from pathlib import Path
import re
import sqlite3
import tempfile

from message_archive import DEFAULT_DB, LOCAL_TIME


CQ = re.compile(r"\[CQ:([\w-]+)((?:,[^\]]*)?)\]")
URL = re.compile(r"""https?://[^\s<>"'\[\]，。！？、；（）【】《》]+""", re.I)


def unescape_cq(value):
    return value.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&")


def segments(value):
    if isinstance(value, list):
        yield from value
    elif isinstance(value, str):
        end = 0
        for match in CQ.finditer(value):
            if match.start() > end:
                yield {"type": "text", "data": {"text": unescape_cq(value[end:match.start()])}}
            fields = {}
            for item in match[2].split(",")[1:]:
                key, _, val = item.partition("=")
                fields[key] = unescape_cq(val.replace("&#44;", ","))
            yield {"type": match[1], "data": fields}
            end = match.end()
        if end < len(value):
            yield {"type": "text", "data": {"text": unescape_cq(value[end:])}}


def label(value):
    plain = " ".join(str(value).split())
    plain = "".join(c for c in plain if c.isprintable())
    return re.sub(r"([\\`*_{}\[\]()#+!|~])", r"\\\1", escape(plain, quote=False))


def excerpt(parts):
    content = "".join(p.get("data", {}).get("text", "") if p["type"] == "text"
                      else "[" + p["type"] + "]" for p in parts)
    return label(content[:90]) + ("…" if len(content) > 90 else "")


def report(db, group, day, start, end, as_of):
    total = anonymous = chars = person_mentions = everyone = quoted = 0
    hours = [0] * 24
    members, types, links, citations = Counter(), Counter(), Counter(), Counter()
    names, link_sources, first_quote = {}, {}, {}
    window, recent_people = deque(), Counter()
    peak_people, peak_end = 0, None
    rows = db.execute("""SELECT id,bot,sender,sent_at,event FROM messages
        WHERE kind='group' AND chat=? AND sent_at>=? AND sent_at<? AND post_type='message' AND sender<>bot
        ORDER BY sent_at,id""", (group, start, end))
    for row_id, bot, sender, stamp, raw in rows:
        event = json.loads(raw)
        total += 1
        hours[datetime.fromtimestamp(stamp, LOCAL_TIME).hour] += 1
        while window and window[0][0] <= stamp - 600:
            _, old_sender = window.popleft()
            recent_people[old_sender] -= 1
            if not recent_people[old_sender]:
                del recent_people[old_sender]
        if event.get("sub_type") == "anonymous" or event.get("anonymous"):
            anonymous += 1
        else:
            members[sender] += 1
            author = event.get("sender") or {}
            display = author.get("card") or author.get("nickname")
            if display:
                names[sender] = display
            window.append((stamp, sender))
            recent_people[sender] += 1
            if len(recent_people) > peak_people:
                peak_people, peak_end = len(recent_people), stamp

        seen_types, targets, references, urls = set(), set(), set(), set()
        for part in segments(event.get("message")):
            kind, data = part["type"], part.get("data", {})
            seen_types.add(kind)
            if kind == "text":
                text = data.get("text", "")
                chars += len(text)
                urls.update(m.group().rstrip(".,;!?") for m in URL.finditer(text))
            elif kind == "at" and data.get("qq") is not None:
                targets.add(str(data["qq"]))
            elif kind == "reply" and data.get("id") is not None:
                references.add(str(data["id"]))
        types.update(seen_types)
        person_mentions += sum(t.isascii() and t.isdecimal() for t in targets)
        everyone += int("all" in targets)
        quoted += bool(references)
        for target in references:
            key = (bot, target)
            citations[key] += 1
            first_quote.setdefault(key, (stamp, row_id))
        for url in urls:
            links[url] += 1
            link_sources.setdefault(url, row_id)

    lines = [f"# 群 {group} · {day} 信息日报", "",
             f"统计依据为已归档群消息。生成于北京时间 {as_of:%Y-%m-%d %H:%M}。", "",
             f"群消息 **{total} 条**，可识别发言账号 **{len(members)} 个**，匿名消息 {anonymous} 条，正文 {chars} 字符。"]
    if not total:
        lines.append("这一天暂无符合条件的归档消息。")
        return "\n".join(lines) + "\n"
    high = max(hours)
    peaks = "、".join(f"{h:02d} 时" for h, n in enumerate(hours) if n == high)
    lines += ["", "## 活跃时段", "", f"发言高峰为 {peaks}，每小时 {high} 条。"]
    if peak_end is not None:
        until = datetime.fromtimestamp(peak_end, LOCAL_TIME)
        lines.append(f"10 分钟内最多有 {peak_people} 个账号发言，首次达到峰值是在 {until:%H:%M:%S}。")
    lines += ["", "小时分布（北京时间，仅列有消息的时段）", "",
              " · ".join(f"{h:02d} 时 {n} 条" for h, n in enumerate(hours) if n),
              "", "## 发言排行", ""]
    for uid, n in sorted(members.items(), key=lambda pair: (-pair[1], pair[0]))[:10]:
        display = label(names.get(uid, "未上报名片或昵称"))
        lines.append(f"- {display}（QQ {uid}）　{n} 条，占全部群消息 {n / total:.1%}")
    if not members:
        lines.append("当日仅有匿名发言。")
    lines += ["", "## 消息与互动", "",
              " · ".join(f"{title} {types[kind]} 条" for kind, title in
                         (("text", "含文字"), ("image", "含图"), ("face", "含 QQ 表情"),
                          ("record", "含语音"), ("video", "含视频"), ("file", "含文件"))),
              "", f"引用消息 {quoted} 条，定向 @ {person_mentions} 人次，@全体 {everyone} 条。",
              "", "## 被引用的消息", ""]
    for (bot, target), n in sorted(citations.items(), key=lambda pair: (-pair[1], first_quote[pair[0]]))[:5]:
        stamp, first_id = first_quote[(bot, target)]
        originals = db.execute("""SELECT id,event FROM messages WHERE bot=? AND kind='group' AND chat=?
            AND message_id=? AND sent_at<=? AND id<>? LIMIT 2""", (bot, group, target, stamp, first_id)).fetchall()
        if len(originals) == 1:
            original_id, raw = originals[0]
            quote = excerpt(segments(json.loads(raw).get("message")))
            lines.append(f"- {n} 条消息引用 · 原文归档 #{original_id} · {quote}")
        else:
            lines.append(f"- {n} 条消息引用 · 消息号 {label(target)} · 原文无法唯一定位，可查引用方归档 #{first_id}")
    if not citations:
        lines.append("当天没有带引用的消息。")
    lines += ["", "## 群内分享的链接", ""]
    for url, n in sorted(links.items(), key=lambda pair: (-pair[1], link_sources[pair[0]], pair[0]))[:5]:
        lines.append(f"- <{url}> · {n} 条消息分享 · 首见归档 #{link_sources[url]}")
    if not links:
        lines.append("当天文字消息中未发现 HTTP 或 HTTPS 链接。")
    return "\n".join(lines) + "\n"


def save_report(folder, day, group, content):
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    tmp = tempfile.NamedTemporaryFile(dir=folder, delete=False)
    staging = Path(tmp.name)
    try:
        with tmp:
            tmp.write(content.encode("utf-8"))
        staging.replace(folder / f"{day}-{group}.md")
    finally:
        staging.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="从本机群消息档案生成北京时间日报")
    parser.add_argument("--group", type=int, help="群号，默认读取当天有群消息记录的全部群")
    which = parser.add_mutually_exclusive_group()
    which.add_argument("--date", type=date.fromisoformat, help="YYYY-MM-DD，默认今日截至目前")
    which.add_argument("--yesterday", action="store_true", help="上一北京时间自然日")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--save", type=Path, metavar="DIR", help="逐群写入私有目录，默认输出到终端")
    args = parser.parse_args()
    as_of = datetime.now(LOCAL_TIME)
    day = args.date or (as_of.date() - timedelta(days=int(args.yesterday)))
    midnight = datetime.combine(day, time.min, LOCAL_TIME)
    start = int(midnight.timestamp())
    end = min(start + 86400, int(as_of.timestamp()) + 1)
    if day > as_of.date():
        parser.error("请选择今天或以前的日期")
    with closing(sqlite3.connect(args.db.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        db.execute("BEGIN")
        groups = [args.group] if args.group is not None else [r[0] for r in db.execute(
            """SELECT DISTINCT chat FROM messages WHERE kind='group' AND sent_at>=? AND sent_at<?
               ORDER BY chat""", (start, end))]
        for group in groups:
            content = report(db, group, day, start, end, as_of)
            if args.save:
                save_report(args.save, day, group, content)
            else:
                print(content)
        if args.save:
            print(f"{day} 已生成 {len(groups)} 份群日报。")
        elif not groups:
            print(f"{day} 暂无群消息归档。")


if __name__ == "__main__":
    main()
