"""Mobile-sized PNG edition of the archived group digest."""

from functools import lru_cache
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from daily_report import GroupDay, MESSAGE_TYPES


PAPER, INK, MUTED = "#FBF8F1", "#193E39", "#526963"
LINE, TEAL, ORANGE = "#D5DFD6", "#398477", "#B65027"
WHITE, PEACH = "#FFFDF7", "#F7E6D6"
WIDTH, LEFT, RIGHT = 900, 44, 856


@lru_cache(maxsize=32)
def font(size, bold=False):
    candidates = [Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
                  Path("C:/Windows/Fonts/" + ("msyhbd.ttc" if bold else "msyh.ttc"))]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size, layout_engine=ImageFont.Layout.BASIC)
    raise OSError("日报需要文泉驿正黑或微软雅黑字体")


def short_name(value, available):
    name = " ".join(str(value).split())
    name = "".join(c for c in name if c.isprintable())[:80] or "未上报昵称"
    face = font(26)
    if face.getlength(name) <= available:
        return name
    while name and face.getlength(name + "…") > available:
        name = name[:-1]
    return name + "…"


def wrap_note(note):
    lines, line = [], ""
    for char in note:
        if line and font(27).getlength(line + char) > RIGHT - LEFT - 60:
            lines.append(line)
            line = ""
        line += char
    return [*lines, line]


def render_png(s: GroupDay):
    note_lines = wrap_note(s.mori_note())
    ranking_rows = max(1, min(len(s.ranking), 5))
    note_end = 352 + len(note_lines) * 39
    hourly_top = note_end + 48
    ranking_top = hourly_top + 275
    types_top = ranking_top + 70 + ranking_rows * 56
    interactions_top = types_top + 295
    height = interactions_top + 160
    sheet = Image.new("RGB", (WIDTH, height), PAPER)
    draw = ImageDraw.Draw(sheet)

    def write(x, y, text, size, color=INK, *, bold=False, anchor="lm"):
        draw.text((x, y), str(text), font=font(size, bold), fill=color, anchor=anchor)

    def section(y, title, unit):
        write(LEFT, y, title, 34, bold=True)
        write(RIGHT, y, unit, 23, MUTED, anchor="rm")

    def track(x, y, width, value, maximum, color):
        draw.rectangle((x, y, x + width - 1, y + 8), fill=LINE)
        if value:
            length = max(1, round(width * value / maximum))
            draw.rectangle((x, y, x + length - 1, y + 8), fill=color)

    # Masthead and the fox's folded-paper silhouette.
    draw.rectangle((0, 0, WIDTH, 180), fill=INK)
    write(LEFT, 39, f"{s.day:%Y.%m.%d}   /   群 {s.group}", 24, "#C7DFD4")
    write(LEFT - 2, 102, "茉莉的群聊日报", 56, WHITE, bold=True)
    partial = s.day == s.as_of.date()
    span = f"截至 {s.as_of:%H:%M}" if partial else "全天"
    write(LEFT, 151, "北京时间   ·   " + span, 22, "#C7DFD4")
    draw.polygon([(741, 45), (770, 65), (809, 65), (838, 45), (828, 106),
                  (790, 139), (751, 106)], fill="#E6A077")
    draw.polygon([(751, 97), (783, 108), (790, 134), (762, 113)], fill=WHITE)
    draw.polygon([(828, 97), (797, 108), (790, 134), (817, 113)], fill=WHITE)
    draw.line([(763, 91), (775, 96)], fill=INK, width=4)
    draw.line([(805, 96), (817, 91)], fill=INK, width=4)
    draw.polygon([(784, 124), (796, 124), (790, 132)], fill=INK)

    metrics = (("群消息 / 条", s.total), ("发言账号 / 个", len(s.ranking)), ("正文 / 字符", s.chars))
    for i, (title, value) in enumerate(metrics):
        x = LEFT + i * 278
        if i:
            draw.line((x - 20, 205, x - 20, 278), fill=LINE, width=2)
        write(x, 215, title, 24, MUTED)
        write(x, 263, f"{value:,}", 42 if value < 10000000 else 33, bold=True)

    draw.rounded_rectangle((LEFT, 306, RIGHT, note_end), radius=17, fill=PEACH)
    write(LEFT + 22, 331, "茉莉手记", 23, ORANGE, bold=True)
    for i, line in enumerate(note_lines):
        write(LEFT + 22, 372 + i * 39, line, 27)

    section(hourly_top, "几点最热闹", "每小时归档消息 / 条")
    left, step = 99, 31
    base = hourly_top + 172
    maximum = max(1, max(s.hours))
    # Whole-number ticks, including when there is a single message.
    ticks = sorted({0, maximum // 2, maximum})
    for tick in ticks:
        y = base - round(112 * tick / maximum)
        write(left - 10, y, tick, 21, MUTED, anchor="rm")
        draw.line((left, y, left + 24 * step, y), fill=LINE, width=2)
    for hour, count in enumerate(s.hours):
        x = left + hour * step
        if partial and hour > s.as_of.hour:
            draw.line((x + 6, base - 3, x + 18, base - 15), fill="#ACB8B1", width=3)
        if count:
            top = base - max(2, round(112 * count / maximum))
            draw.rectangle((x + 3, top, x + step - 4, base - 1),
                           fill=ORANGE if count == maximum else TEAL)
        if hour in (0, 4, 8, 12, 16, 20, 23):
            write(x + step // 2, base + 19, f"{hour:02d}", 21, MUTED, anchor="mm")
    legend = "橙色为发言最高小时" if s.total else "这一天暂无归档发言"
    if partial:
        legend += "   /   斜线为尚未到达的小时" if s.as_of.hour < 23 else ""
    write(LEFT, base + 55, legend, 22, MUTED)
    draw.line((LEFT, ranking_top - 31, RIGHT, ranking_top - 31), fill=LINE, width=2)

    section(ranking_top, "谁来冒过泡", "发言前五 / 条")
    for i, (uid, count) in enumerate(s.ranking[:5]):
        y = ranking_top + 57 + i * 56
        write(LEFT, y, short_name(s.names.get(uid, "未上报昵称"), 205), 26)
        write(LEFT + 220, y, f"QQ {uid}", 22, MUTED)
        track(500, y - 3, 242, count, s.ranking[0][1], TEAL)
        write(RIGHT, y, f"{count:,}", 26, anchor="rm")
    if not s.ranking:
        write(LEFT, ranking_top + 57, "只有匿名发言，咱认不出是谁。" if s.anonymous else "还没有发言账号。", 26, MUTED)
    draw.line((LEFT, types_top - 30, RIGHT, types_top - 30), fill=LINE, width=2)

    section(types_top, "消息里有什么", "占全部群消息的比例")
    for i, (kind, label) in enumerate(MESSAGE_TYPES):
        x = LEFT + (i % 2) * 425
        y = types_top + 55 + (i // 2) * 57
        count = s.types[kind]
        write(x, y, "图片" if kind == "image" else label, 25)
        pct = f"{count / s.total:.0%}" if s.total else "—"
        write(x + 382, y, f"{count} 条  ·  {pct}", 22, MUTED, anchor="rm")
        track(x, y + 19, 382, count, s.total, TEAL)
    write(LEFT, types_top + 237, "一条图文消息会同时计入文字和图片。", 22, MUTED)

    draw.rectangle((0, interactions_top - 21, WIDTH, height), fill="#E6EEE7")
    section(interactions_top + 17, "群友怎么接话", f"另有匿名消息 {s.anonymous} 条")
    for i, (title, value) in enumerate((("带引用 / 条", s.quoted), ("定向 @ / 人次", s.person_mentions),
                                        ("@ 全体 / 条", s.everyone))):
        x = LEFT + i * 278
        write(x, interactions_top + 76, value, 37, bold=True)
        write(x, interactions_top + 120, title, 23, MUTED)

    output = BytesIO()
    sheet.save(output, format="PNG", compress_level=4)
    return output.getvalue()
