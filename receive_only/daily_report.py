#!/usr/bin/env python3
"""Build private group digests from the read-only OneBot message archive."""

import argparse
from collections import Counter, deque
from contextlib import closing
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from html import escape
import json
from pathlib import Path
import re
import sqlite3
import tempfile

from message_archive import DEFAULT_DB, LOCAL_TIME
from report_topics import CONTROL, FALLBACK_NAME, STORE, clean, display, saved_metadata


CQ = re.compile(r"\[CQ:([\w-]+)((?:,[^\]]*)?)\]")
URL = re.compile(r"""https?://[^\s<>"'\[\]，。！？、；（）【】《》]+""", re.I)
MESSAGE_TYPES = (("text", "文字"), ("image", "图"), ("face", "QQ 表情"),
                 ("record", "语音"), ("video", "视频"), ("file", "文件"))


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


@dataclass
class GroupDay:
    group: int
    day: date
    as_of: datetime
    total: int
    anonymous: int
    chars: int
    hours: list[int]
    ranking: list[tuple[int, int]]
    names: dict
    types: Counter
    quoted: int
    person_mentions: int
    everyone: int
    peak_people: int
    peak_end: int | None
    quote_lines: list[str]
    link_lines: list[str]
    group_name: str = FALLBACK_NAME
    texts: list = field(default_factory=list)
    analysis: dict | None = None
    analysis_note: str = ""

    def person(self, uid):
        return "匿名群友" if uid is None else self.names.get(uid, "群友")

    def analysis_sections(self):
        a = self.analysis
        if not a:
            note = self.analysis_note or ("这天还没有可分析的聊天文字。" if not self.texts else "在群里查询这天的日报，咱就来整理话题。")
            return [("话题与关键词", note)]
        sections = [("讨论关键词", "　".join(f"{w}（{n}条）" for w,n in a["keywords"]) or "可用文字里还没找到代表词。")]
        for t in a["topics"]:
            sections.append((f"{t['title']} · {t['status']}", t["finding"] + "\n参与者（据所引发言）　" + "、".join(t["people"])))
        if not a["topics"]:
            sections.append(("讨论进展", "咱看过这些发言了，还没有可归纳的话题。"))
        sections.append(("分析范围", f"本次分析于 {a['as_of']} 取样，选读 {a['sampled']} / {a['total']} 条有效文字。词后为提到它的消息条数。"))
        if self.analysis_note:
            sections.append(("更新进度", self.analysis_note))
        return sections

    @property
    def peak_hours(self):
        high = max(self.hours)
        return [h for h, n in enumerate(self.hours) if n and n == high]

    def mori_note(self):
        if not self.total:
            return "咱翻了翻，这一天的群聊档案还是空的。"
        if self.total == 1:
            return f"翻到啦，{self.peak_hours[0]} 点那一条，就是咱这天收下的全部消息。"
        high = max(self.hours)
        peaks = self.peak_hours
        if len(peaks) == 1:
            first = f"{peaks[0]} 点那一栏最高，咱数到了 {high} 条。"
        elif len(peaks) == 2:
            first = f"{peaks[0]} 点和 {peaks[1]} 点各有 {high} 条，咱给它们并排画了个第一。"
        else:
            first = f"咱数了两遍，有 {len(peaks)} 个时段并列第一，每小时都是 {high} 条。"
        if self.peak_people >= 2:
            until = datetime.fromtimestamp(self.peak_end, LOCAL_TIME)
            return first + f"再看 {until:%H:%M}，往前十分钟就有 {self.peak_people} 个账号冒过泡啦。"
        if self.types["image"]:
            return first + f"咱还翻到 {self.types['image']} 条带图的消息。"
        return first


def collect_day(db, group, day, start, end, as_of, *, bot_id=None):
    total = anonymous = chars = person_mentions = everyone = quoted = 0
    hours = [0] * 24
    members, types, citations = Counter(), Counter(), Counter()
    links = set()
    names, first_quote = {}, {}
    window, recent_people = deque(), Counter()
    texts, group_name = [], ""
    peak_people, peak_end = 0, None
    query = """SELECT id,bot,sender,sent_at,event FROM messages
        WHERE kind='group' AND chat=? AND sent_at>=? AND sent_at<? AND post_type='message' AND sender<>bot"""
    params = [group, start, end]
    if bot_id is not None:
        query += " AND bot=?"
        params.append(bot_id)
    rows = db.execute(query + " ORDER BY sent_at,id", params)
    for row_id, bot, sender, stamp, raw in rows:
        event = json.loads(raw)
        if event.get("group_name"):
            group_name = display(event["group_name"], "")
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
            who = display(author.get("card"), "") or display(author.get("nickname"), "")
            if who:
                names[sender] = who
            window.append((stamp, sender))
            recent_people[sender] += 1
            if len(recent_people) > peak_people:
                peak_people, peak_end = len(recent_people), stamp

        seen_types, targets, references, urls = set(), set(), set(), set()
        words = []
        for part in segments(event.get("message")):
            kind, data = part["type"], part.get("data", {})
            seen_types.add(kind)
            if kind == "text":
                text = data.get("text", "")
                chars += len(text)
                words.append(text)
                urls.update(m.group().rstrip(".,;!?") for m in URL.finditer(text))
            elif kind == "at" and data.get("qq") is not None:
                targets.add(str(data["qq"]))
            elif kind == "reply" and data.get("id") is not None:
                references.add(str(data["id"]))
        plain = "".join(words).strip()
        if plain and not CONTROL.match(plain):
            safe = clean(plain)
            if safe:
                uid = None if event.get("sub_type") == "anonymous" or event.get("anonymous") else sender
                texts.append((row_id, uid, safe))
        types.update(seen_types)
        person_mentions += sum(t.isascii() and t.isdecimal() for t in targets)
        everyone += int("all" in targets)
        quoted += bool(references)
        for target in references:
            key = (bot, target)
            citations[key] += 1
            first_quote.setdefault(key, (stamp, row_id))
        links.update(urls)

    quote_lines = []
    for (bot, target), n in sorted(citations.items(), key=lambda pair: (-pair[1], first_quote[pair[0]]))[:5]:
        stamp, first_id = first_quote[(bot, target)]
        originals = db.execute("""SELECT id,event FROM messages WHERE bot=? AND kind='group' AND chat=?
            AND message_id=? AND sent_at<=? AND id<>? LIMIT 2""", (bot, group, target, stamp, first_id)).fetchall()
        if len(originals) == 1:
            _, raw = originals[0]
            quote = excerpt(segments(json.loads(raw).get("message")))
            quote_lines.append(f"- {n} 条消息引用 · {clean(quote) or '原文仅含媒体或联系方式'}")
        else:
            quote_lines.append(f"- {n} 条消息引用 · 原文无法唯一定位")
    link_lines = [f"共分享 {len(links)} 个不同链接。"] if links else []
    # Resolve display collisions locally without publishing the account used for aggregation.
    by_name = Counter(names.get(uid, "群友") for uid in members)
    seen_names = Counter()
    for uid in sorted(members):
        name = names.get(uid, "群友")
        seen_names[name] += 1
        names[uid] = f"{name}（{seen_names[name]}）" if by_name[name] > 1 else name
    return GroupDay(group, day, as_of, total, anonymous, chars, hours,
                    sorted(members.items(), key=lambda pair: (-pair[1], pair[0])), names, types,
                    quoted, person_mentions, everyone, peak_people, peak_end, quote_lines, link_lines,
                    group_name or FALLBACK_NAME, texts)


def prepare(stats, path, bot, analyzer=None, *, wait=.25):
    name, previous = saved_metadata(path.with_name(STORE), bot, stats.group, stats.day)
    stats.group_name = name or stats.group_name
    if previous:
        stats.analysis = json.loads(previous[2])
    if analyzer is not None:
        analyzer.attach(stats, bot, previous, wait)


def markdown(s):
    lines = [f"# {label(s.group_name)} · {s.day} 信息日报", "",
             f"统计依据为已归档群消息。生成于北京时间 {s.as_of:%Y-%m-%d %H:%M}。", "",
             f"群消息 **{s.total} 条**，可识别发言账号 **{len(s.ranking)} 个**，匿名消息 {s.anonymous} 条，正文 {s.chars} 字符。",
             "", f"茉莉手记　{s.mori_note()}"]
    for title, body in s.analysis_sections():
        lines += ["", "## " + title, "", body]
    if not s.total:
        return "\n".join([*lines, "这一天暂无符合条件的归档消息。"]) + "\n"
    peaks = "、".join(f"{h:02d} 时" for h in s.peak_hours)
    lines += ["", "## 活跃时段", "", f"发言高峰为 {peaks}，每小时 {max(s.hours)} 条。"]
    if s.peak_end is not None:
        until = datetime.fromtimestamp(s.peak_end, LOCAL_TIME)
        lines.append(f"10 分钟内最多有 {s.peak_people} 个账号发言，首次达到峰值是在 {until:%H:%M:%S}。")
    lines += ["", "小时分布（北京时间，仅列有消息的时段）", "",
              " · ".join(f"{h:02d} 时 {n} 条" for h, n in enumerate(s.hours) if n),
              "", "## 发言排行", ""]
    for uid, n in s.ranking[:10]:
        lines.append(f"- {label(s.person(uid))}　{n} 条，占全部群消息 {n / s.total:.1%}")
    if not s.ranking:
        lines.append("当日仅有匿名发言。")
    lines += ["", "## 消息与互动", "",
              " · ".join(f"含{' ' if kind == 'face' else ''}{title} {s.types[kind]} 条" for kind, title in MESSAGE_TYPES),
              "", f"引用消息 {s.quoted} 条，定向 @ {s.person_mentions} 人次，@全体 {s.everyone} 条。",
              "", "## 被引用的消息", "", *(s.quote_lines or ["当天没有带引用的消息。"]),
              "", "## 群内分享的链接", "", *(s.link_lines or ["当天文字消息中未发现 HTTP 或 HTTPS 链接。"])]
    return "\n".join(lines) + "\n"


def save_report(folder, name, content):
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    tmp = tempfile.NamedTemporaryFile(dir=folder, delete=False)
    staging = Path(tmp.name)
    try:
        with tmp:
            tmp.write(content)
        staging.replace(folder / name)
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
    if args.save:
        args.save.mkdir(mode=0o700, parents=True, exist_ok=True)
    with closing(sqlite3.connect(args.db.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        db.execute("BEGIN")
        if args.group is None:
            groups = db.execute("""SELECT DISTINCT bot,chat FROM messages WHERE kind='group' AND sent_at>=?
                                AND sent_at<? ORDER BY chat,bot""", (start,end)).fetchall()
        else:
            groups = db.execute("SELECT DISTINCT bot,chat FROM messages WHERE kind='group' AND chat=?",
                                (args.group,)).fetchall() or [(None, args.group)]
        for bot, group in groups:
            stats = collect_day(db, group, day, start, end, as_of, bot_id=bot)
            prepare(stats, args.db, bot)
            if args.save:
                from daily_chart import render_png
                png = render_png(stats)
                folder = args.save / f"{bot}-{group}"
                filename = re.sub(r'[<>:"/\\|?*]', "_", stats.group_name)
                save_report(folder, f"{day}-{filename}.png", png)
                save_report(folder, f"{day}-{filename}.md", markdown(stats).encode("utf-8"))
            else:
                print(markdown(stats))
        if args.save:
            print(f"{day} 已生成 {len(groups)} 份群日报。")
        elif not groups:
            print(f"{day} 暂无群消息归档。")


if __name__ == "__main__":
    main()
