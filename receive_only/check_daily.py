"""Exercise the CLI using a synthetic archive, with no network or QQ connection."""

from datetime import datetime
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image

from daily_report import collect_day
from message_archive import LOCAL_TIME, MessageArchive


def main():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        path = root / "messages.sqlite3"
        archive = MessageArchive(path, root / "missing.sqlite3", None)
        start = int(datetime(2025, 6, 2, tzinfo=LOCAL_TIME).timestamp())

        def add(number, offset, author, msg, group=20000, **extra):
            event = dict(self_id=10000, group_id=group, user_id=author, message_id=number,
                         message_type="group", post_type="message", sub_type="normal", time=start + offset,
                         sender={"nickname": "同名"}, message=msg)
            event.update(extra)
            return archive.record(event, group)[0]

        try:
            old = add(81, -1, 30000, "上日原文")
            add(81, -1, 30000, "别群同号", group=20001)
            evidence = add(1, 0, 30000, "地图 https://example.org/map https://example.org/map")
            add(1, 0, 30000, "地图 https://example.org/map https://example.org/map")
            archive.quick_reply(evidence, {"reply": "机器人快速回复"})
            add(2, 1, 30001, "[CQ:reply,id=81][CQ:at,qq=30000][CQ:at,qq=30000]确认。")
            add(3, 600, 30002, [{"type": "image", "data": {"file": "fake"}},
                                 {"type": "image", "data": {"file": "fake2"}},
                                 {"type": "text", "data": {"text": "https://example.org/map"}}])
            add(4, 1000, 30000, "[CQ:at,qq=all][CQ:reply,id=999]集合", sender={"card": "新名片"})
            add(5, 3600, 30003, "匿名发言", sub_type="anonymous")
            add(6, 4000, 10000, "茉莉自己发的", post_type="message_sent")
            add(7, 86400, 30011, "次日数据")
            add(8, 1200, 30012, "好友私聊", message_type="private", sub_type="friend")
            cutoff = datetime.fromtimestamp(start + 1500, LOCAL_TIME)
            partial = collect_day(archive.db, 20000, cutoff.date(), start, int(cutoff.timestamp()) + 1, cutoff, bot_id=10000)
            assert partial.hours == [4] + [0] * 23 and partial.peak_hours == [0]
            assert partial.ranking == [(30000, 2), (30001, 1), (30002, 1)]
            assert partial.peak_people == 2 and "4 条" in partial.mori_note() and "2 个账号" in partial.mori_note()
            other_bot = add(9, 7200, 30012, "跨机器人统计测试", self_id=10001)
            assert other_bot and collect_day(archive.db, 20000, cutoff.date(), start, start + 86400,
                                             cutoff, bot_id=10000).total == 5
            other = collect_day(archive.db, 20000, cutoff.date(), start, start + 86400, cutoff, bot_id=10001)
            assert other.total == 1 and "2 点" in other.mori_note()
            add(10, 10800, 30012, "并列时段", self_id=10001)
            tied = collect_day(archive.db, 20000, cutoff.date(), start, start + 86400, cutoff, bot_id=10001)
            assert tied.peak_hours == [2, 3] and "2 点和 3 点各有 1 条" in tied.mori_note()
            # Remove just these two synthetic rows before testing the all-bot CLI.
            with archive.db:
                archive.db.execute("DELETE FROM messages WHERE bot=10001")
        finally:
            archive.db.close()
        cli = [sys.executable, "-X", "utf8", str(Path(__file__).with_name("daily_report.py")),
               "--db", str(path), "--date", "2025-06-02"]
        text = subprocess.check_output(cli, encoding="utf-8")
        for fragment in ("**5 条**", "**3 个**", "匿名消息 1 条", "新名片（QQ 30000）　2 条",
                         "含图 1 条", "最多有 2 个账号", "00 时，每小时 4 条", "引用消息 2 条",
                         "定向 @ 1 人次，@全体 1 条", f"原文归档 #{old} · 上日原文",
                         "原文无法唯一定位", f"<https://example.org/map> · 2 条消息分享 · 首见归档 #{evidence}"):
            assert fragment in text, fragment
        assert all(x not in text for x in ("机器人快速回复", "QQ 10000", "QQ 30012", "QQ 30011", "别群同号"))
        assert "暂无符合条件" in subprocess.check_output([*cli, "--group", "20999"], encoding="utf-8")
        saved = root / "reports"
        for _ in range(2):
            subprocess.run([*cli, "--save", str(saved)], check=True, stdout=subprocess.DEVNULL)
        assert sorted(p.name for p in saved.iterdir()) == ["2025-06-02-20000.md", "2025-06-02-20000.png"]
        assert "原文归档" in (saved / "2025-06-02-20000.md").read_text(encoding="utf-8")
        with Image.open(saved / "2025-06-02-20000.png") as chart:
            assert chart.format == "PNG" and chart.width == 900 and chart.height > chart.width
            chart.verify()
        viewer = Path(__file__).with_name("message_archive.py")
        detail = subprocess.check_output([sys.executable, "-X", "utf8", str(viewer), "--db", str(path),
                                          "--id", str(old), "--jsonl"], encoding="utf-8")
        assert len(detail.splitlines()) == 1 and "上日原文" in detail
        print("PASS: local day, stable accounts, multi-segment counts, exact peak window, scoped evidence, and repeatable files")


if __name__ == "__main__":
    main()
