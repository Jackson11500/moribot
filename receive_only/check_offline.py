"""Exercise the real HTTP receiver on a temporary port without starting LLBot."""

import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import hashlib
import hmac
from io import BytesIO
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener

from PIL import Image, ImageChops
import httpx
import deepseek_dialogue
import dialogue_context
from deepseek_dialogue import MODEL, UNAVAILABLE
from dialogue_context import RecentMessages
from dialogue_log import DialogueLog, read_calls
from legacy_commands import ASSETS, GREETING, MISSING, MODULE_LABELS, PUZZLES
from message_archive import LOCAL_TIME, MessageArchive


async def fake_model(request):
    assert str(request.url) == "https://api.deepseek.com/chat/completions"
    assert request.headers["authorization"] == "Bearer offline-test"
    body = json.loads(request.content)
    system, user = body["messages"]
    assert body["model"] == MODEL and system["role"] == "system" and "用茉莉的口吻接话" in system["content"]
    assert user["role"] == "user"
    context = json.loads(user["content"])
    if context["current"]["text"] == "模拟失败":
        return httpx.Response(503)
    await asyncio.sleep(0.15)
    return httpx.Response(200, json={"choices": [{
        "message": {"content": "模拟对白 [CQ:at,qq=all]"}, "finish_reason": "stop",
    }]})


async def check_model_timeout():
    from unittest.mock import patch
    with tempfile.TemporaryDirectory() as tmp, patch.object(deepseek_dialogue, "MODEL_TIMEOUT", 0.01):
        path = Path(tmp) / "calls.sqlite3"
        model = deepseek_dialogue.DeepSeekDialogue("offline-test", "用茉莉的口吻接话", DialogueLog(path),
                                                  httpx.MockTransport(fake_model))
        try:
            context = {"current": {"text": "模拟慢回复"}, "quote": None}
            assert await model.answer(context, {}, None) == UNAVAILABLE and model.failures == 1
            row, = read_calls(path)
            assert row["status"] == "timeout" and row["http_status"] is None and row["reply"] == UNAVAILABLE
        finally:
            await model.client.aclose()
            await model.close_journal()


def check(greeting_enabled=False):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    client = build_opener(ProxyHandler({}))

    def status():
        with client.open(base + "/status", timeout=2) as response:
            return json.load(response)

    with tempfile.TemporaryDirectory() as directory:
        key = secrets.token_hex(32)
        (Path(directory) / "post-secret").write_text(key, encoding="ascii")
        if greeting_enabled:
            (Path(directory) / "deepseek-key").write_text("offline-test", encoding="ascii")
            (Path(directory) / "greeting-access.json").write_text(json.dumps(
                {"bot_id": 10000, "user_id": 30000,
                 "profiles": {"test": list(MODULE_LABELS), "games": ["greeting", "little_game"],
                              "ai_only": ["ai_dialogue"]},
                 "groups": {"20000": "test", "20002": "games", "20003": "ai_only"}}
            ), encoding="ascii")
        code = (
            "from pathlib import Path; import receiver, sys; "
            "receiver.RUNTIME = Path(sys.argv[1]); receiver.PORT = int(sys.argv[2]); "
            "from check_offline import fake_model, stop_on_eof; import httpx, threading; "
            "threading.Thread(target=stop_on_eof, daemon=True).start(); "
            "receiver.start(model_transport=httpx.MockTransport(fake_model))"
        )
        process = subprocess.Popen(
            [sys.executable, "-c", code, directory, str(port)], cwd=Path(__file__).parent,
            stdin=subprocess.PIPE,
            env={**os.environ, "STATE_DIRECTORY": str(Path(directory) / "dialogue")},
        )
        try:
            for _ in range(100):
                if process.poll() is not None:
                    raise RuntimeError("Receiver exited before the check")
                try:
                    if status()["events"] == 0:
                        break
                except URLError:
                    time.sleep(0.1)
            else:
                raise RuntimeError("Receiver did not become ready")

            event = {
                "time": int(time.time()), "self_id": 10000, "post_type": "message",
                "message_type": "group", "sub_type": "normal", "group_id": 20000,
                "message_id": 1, "user_id": 30000, "sender": {"user_id": 30000},
                "message": [{"type": "text", "data": {"text": "普通消息"}}],
                "raw_message": "普通消息", "font": 0,
            }
            body = json.dumps(event).encode()
            request = Request(base + "/onebot/v11/http", data=body, headers={
                "Content-Type": "application/json", "X-Self-ID": "10000",
            })
            try:
                client.open(request, timeout=2).close()
            except HTTPError as exc:
                assert exc.code == 401
            else:
                raise AssertionError("Unsigned event accepted")
            signature = hmac.new(key.encode(), body, hashlib.sha1).hexdigest()
            request.add_header("X-Signature", "sha1=" + signature)
            with client.open(request, timeout=2) as response:
                assert (response.status, response.read()) == (204, b"")
            for _ in range(40):
                counts = status()
                if counts["events"] == counts["messages"] == 1:
                    break
                time.sleep(0.05)
            else:
                raise AssertionError(counts)
            print("PASS: unsigned event rejected; signed message counted; empty HTTP 204")

            private = dict(event, message_type="private", sub_type="friend",
                           raw_message="茉莉酱", message=[{"type": "text", "data": {"text": "茉莉酱"}}])
            del private["group_id"]
            group = dict(private, message_type="group", sub_type="normal", group_id=20000, message_id=2)
            second_group = dict(group, group_id=20002)

            def post(payload, expected_code=204, *, header_id="10000", signing_key=key):
                data = json.dumps(payload).encode()
                digest = hmac.new(signing_key.encode(), data, hashlib.sha1).hexdigest()
                req = Request(base + "/onebot/v11/http", data=data, headers={
                    "Content-Type": "application/json", "X-Self-ID": header_id,
                    "X-Signature": "sha1=" + digest,
                })
                try:
                    reply = client.open(req, timeout=2)
                except HTTPError as exc:
                    reply = exc
                with reply:
                    assert reply.status == expected_code, (reply.status, expected_code)
                    if reply.status == 200:
                        operation = json.load(reply)
                        assert set(operation) == {"reply", "at_sender", "auto_escape"}
                        assert operation["at_sender"] is False and operation["auto_escape"] is True
                        result = operation["reply"]
                        if payload["message_type"] == "group":
                            assert result[0] == {"type": "reply", "data": {"id": str(payload["message_id"])}}
                            assert all(s["type"] in ("text", "image") for s in result[1:])
                            body = result[1:]
                            if len(body) == 1 and body[0]["type"] == "text":
                                return body[0]["data"]["text"]
                            return body
                        if isinstance(result, list):
                            assert all(s["type"] in ("text", "image") for s in result)
                        return result
                    elif reply.status == 204:
                        assert reply.read() == b""

            post(private, 403, signing_key="wrong-key")
            post(group, 403, signing_key="wrong-key")
            for index, denied in enumerate((
                dict(private, user_id=30001, sender={"user_id": 30001}),
                dict(group, user_id=30001, sender={"user_id": 30001, "role": "owner"}),
                dict(second_group, user_id=30001, sender={"user_id": 30001, "role": "owner"}),
                dict(group, group_id=20001),
                dict(group, self_id=10001),
                dict(group, user_id=10000, sender={"user_id": 10000}),
                dict(group, sub_type="anonymous"),
                dict(private, sub_type="group"),
                dict(private, message="茉莉酱！！"),
                dict(private, post_type="message_sent"),
            )):
                post(dict(denied, message_id=-20 - index))
            post(group, header_id="10001")
            for allowed in (private, group, second_group):
                reply = post(allowed, 200 if greeting_enabled else 204)
                assert reply == (GREETING if greeting_enabled else None)
                post(allowed)  # The same event must never request two replies.

            serial = 10
            def command(event, text, accepted=True):
                nonlocal serial
                serial += 1
                payload = dict(event, message_id=serial, raw_message=text,
                               message=[{"type": "text", "data": {"text": text}}])
                result = post(payload, 200 if accepted and greeting_enabled else 204)
                post(payload)
                return result

            def at(qq):
                return {"type": "at", "data": {"qq": qq}}

            def words(text):
                return {"type": "text", "data": {"text": text}}

            # An ordinary group outside every reply profile is still fully archived.
            day = datetime(2025, 6, 2, tzinfo=LOCAL_TIME)
            other = dict(group, group_id=20100, user_id=30100, sender={"nickname": "合成群友", "user_id": 30100},
                         message_id=801, time=int(day.timestamp()), raw_message="正文",
                         message=[words("正文"), {"type": "image", "data": {"file": "example.jpg"}}])
            post(other)
            post(other)
            post(dict(other, message_id=802, time=int(day.timestamp()) - 1))
            post(dict(other, message_id=803, time=int((day + timedelta(days=1)).timestamp())))
            post(dict(other, message_id=804, post_type="message_sent", user_id=10000, sender={"user_id": 10000}))
            post(dict(other, group_id=20101))
            post(dict(other, message_id=805), 403, signing_key="invalid")
            post(dict(other, message_id=806), header_id="10001")
            post(dict(other, message_id=807, self_id=10001))

            archive_file = Path(directory) / "dialogue/messages.sqlite3"
            archive_cli = [sys.executable, "-X", "utf8", str(Path(__file__).with_name("message_archive.py")),
                           "--db", str(archive_file)]
            def archive_rows(*args):
                out = subprocess.check_output([*archive_cli, *args, "--jsonl"], encoding="utf-8")
                return [json.loads(line) for line in out.splitlines()]
            daily = archive_rows("--group", "20100", "--date", "2025-06-02")
            assert [r["event"]["message_id"] for r in daily] == [801, 804]
            assert daily[0]["event"] == other and all(r["quick_reply"] is None for r in daily)
            assert len(archive_rows("--group", "20100", "--all")) == 4
            assert archive_rows("--group", "20101")[0]["event"]["group_id"] == 20101

            def mention(event, parts, accepted=False):
                nonlocal serial
                serial += 1
                payload = dict(event, message_id=serial, message=parts, raw_message="ignored")
                result = post(payload, 200 if accepted and greeting_enabled else 204)
                post(payload)
                return result

            bot_at = at("10000")
            addressed = [bot_at, words("　小游戏")]
            front = mention(group, addressed, True)
            end = mention(second_group, [words("游戏 "), at(10000), words(" ")], True)
            bare = mention(group, [bot_at], True)
            for parts in ([at("all"), words("游戏")], [at("30001"), words("游戏")],
                          [bot_at, at("30001"), words("游戏")], [bot_at, bot_at, words("游戏")],
                          [words("游"), bot_at, words("戏")], [words("@茉莉 游戏")],
                          [words("[CQ:at,qq=10000]游戏")],
                          [bot_at, {"type": "image", "data": {"file": "test.jpg"}}]):
                mention(group, parts)
            mention(private, addressed)
            mention(second_group, [bot_at])
            mention(second_group, [bot_at, words(" 鲁迅：测试")])
            mention(dict(group, group_id=20001), addressed)
            mention(dict(group, user_id=30001, sender={"user_id": 30001}), addressed)
            if greeting_enabled:
                assert front == end and "骰子" in front
                assert bare == "模拟对白 [CQ:at,qq=all]"
            ai_only = dict(group, group_id=20003)
            mention(ai_only, addressed)
            mention(ai_only, [bot_at, words(" 茉莉酱")])
            mention(ai_only, [bot_at, words(" 鲁迅：测试")])
            mention(second_group, [bot_at, words(" 今天真累")])
            command(group, "今天真累", False)
            mention(dict(group, group_id=20001), [bot_at, words(" 今天真累")])
            mention(dict(group, user_id=30001, sender={"user_id": 30001}), [bot_at, words(" 今天真累")])
            if greeting_enabled:
                serial += 1
                payload = dict(group, message_id=serial, message=[bot_at, words(" 今天真累")])
                with ThreadPoolExecutor(max_workers=1) as pool:
                    future = pool.submit(post, payload, 200)
                    for _ in range(100):
                        if status()["ai_requests"] == 2:
                            break
                        time.sleep(0.01)
                    post(payload)
                    assert future.result() == "模拟对白 [CQ:at,qq=all]"
                assert mention(group, [bot_at, words(" 模拟失败")], True) == UNAVAILABLE

            # Identical message IDs in another group cannot supply this group's quotation.
            original = dict(group, message_id=700, user_id=30004, message=[words("周六\n下午三点")],
                            raw_message="周六\n下午三点", sender={"nickname": "小禾", "user_id": 30004},
                            extra_test_field="完整上报")
            post(original)
            post(dict(original, group_id=20003, message=[words("他群同号消息")]))
            quoted = {"type": "reply", "data": {"id": "700"}}
            speaker = dict(group, sender={"user_id": 30000, "nickname": "栗子", "card": "阿栗", "role": "member"})
            question = [quoted, at("30004"), words(" "), bot_at, words(" 我记成周日了？")]
            mention(speaker, question, True)
            mention(group, [quoted, bot_at, words(" 游戏")], True)
            mention(group, [quoted, words("没叫茉莉")])
            mention(group, [quoted, at("30099"), bot_at, words("错误目标")])
            mention(group, [quoted, quoted, bot_at, words("两个引用")])
            mention(group, [{"type": "reply", "data": {"id": "99999"}}, bot_at, words(" 原话呢")], True)
            if greeting_enabled:
                path = Path(directory) / "dialogue/calls.sqlite3"
                records = list(read_calls(path))
                assert len(records) == 5
                missing, found, failure = records[:3]
                assert found["event"]["message"] == question and found["quote_event"] == original
                ctx = json.loads(found["request"]["messages"][-1]["content"])
                assert ctx["current"]["sender"] == {"user_id": 30000, "nickname": "栗子", "group_card": "阿栗",
                                                    "display_name": "阿栗", "role": "member"}
                assert ctx["current"]["text"] == "我记成周日了？" and ctx["current"]["group_id"] == 20000
                assert ctx["quote"]["text"] == "周六\n下午三点" and ctx["quote"]["sender"]["display_name"] == "小禾"
                assert ctx["quote"]["status"] == "resolved" and ctx["quote"]["message_id"] == 700
                assert json.loads(missing["request"]["messages"][-1]["content"])["quote"]["status"] == "unavailable"
                assert missing["quote_event"] is None and found["finished"] and found["status"] == "ok"
                assert json.loads(found["response_body"])["choices"][0]["message"]["content"] == found["reply"]
                assert failure["http_status"] == 503 and failure["status"] == "error" and failure["reply"] == UNAVAILABLE
                assert "offline-test" not in json.dumps(records)
                viewer = subprocess.check_output([sys.executable, "-X", "utf8", str(Path(__file__).with_name("dialogue_log.py")),
                                                  "--db", str(path), "--id", str(found["id"])], encoding="utf-8")
                assert json.loads(viewer) == found
                listing = subprocess.check_output([sys.executable, "-X", "utf8", str(Path(__file__).with_name("dialogue_log.py")),
                                                   "--db", str(path), "--limit", "2"], encoding="utf-8")
                assert "小禾：周六\n下午三点" in listing and "阿栗：我记成周日了？" in listing
                all_calls = subprocess.check_output([sys.executable, "-X", "utf8", str(Path(__file__).with_name("dialogue_log.py")),
                                                    "--db", str(path), "--all", "--json"], encoding="utf-8")
                assert json.loads(all_calls) == list(reversed(records))

            for text in ("24点", "鲁迅说：测试", "颜色大全", "签到"):
                command(private, text, False)
                command(dict(group, group_id=20001), text, False)
                command(dict(group, user_id=30001, sender={"user_id": 30001}), text, False)
            for text in ("传信：目标：测试", "群组状态设置：chatting：1", "数据备份",
                         "签到了吗", "随机../../", "源码：../", "提到了小游戏"):
                command(group, text, False)

            replies = {text: command(group, text) for text in (
                "茉莉酱！", "游戏", "骰子：6", "色子：-3", "骰子：", "骰子：1",
                "24点", "实用资料", "蓝图档案馆", "贴贴茉莉", "有人说",
                "茉莉的命令大全", "鲁迅说：早上好", "鲁迅:第二张", "鲁迅：",
                "年号：新春", "签到", "随机茉莉", "24点：1", "源码：mono", "颜色大全",
            )}
            private_menu = command(private, "茉莉酱!")
            second_menu = command(second_group, "游戏")
            private_permissions = command(private, "群权限")
            group_permissions = command(second_group, "群组状态")
            limited_menu = command(second_group, "茉莉酱！")
            for text in ("贴贴茉莉", "颜色大全", "实用资料", "鲁迅:测试", "有人说", "随机茉莉", "签到"):
                command(second_group, text, False)
            command(dict(group, group_id=20001), "群权限", False)
            command(dict(second_group, user_id=30001, sender={"user_id": 30001}), "群权限", False)
            if greeting_enabled:
                assert second_menu == replies["游戏"]
                assert "群权限" in private_menu and "测试群" in private_menu
                assert "20000" in private_permissions and "20002" in private_permissions
                assert "games" in group_permissions and "20000" not in group_permissions
                assert "小游戏" in limited_menu and "制图" not in limited_menu
                assert "骰子" in replies["游戏"] and "颜色列表" in replies["实用资料"]
                assert "https://docs.qq.com/" in replies["蓝图档案馆"]
                assert 1 <= int(replies["骰子：6"].split("丢出了一个")[1]) <= 6
                assert -3 <= int(replies["色子：-3"].split("丢出了一个")[1]) <= 0
                assert "整数" in replies["骰子："] and "硬币" in replies["骰子：1"]
                assert replies["24点"].splitlines()[-1] in PUZZLES.read_text().splitlines()
                assert "早上好" in replies["鲁迅："]
                for text in ("年号：新春", "签到", "随机茉莉", "24点：1", "源码：mono"):
                    assert replies[text] == MISSING
                def get_image(text):
                    segment = replies[text][-1]
                    assert segment["type"] == "image"
                    file = segment["data"]["file"]
                    assert file.startswith("base64://")
                    return base64.b64decode(file[9:], validate=True)
                assert get_image("茉莉的命令大全") == (ASSETS / "legacy-help.png").read_bytes()
                with Image.open(BytesIO(get_image("鲁迅说：早上好"))) as first, \
                     Image.open(BytesIO(get_image("鲁迅:第二张"))) as second:
                    assert first.format == "JPEG" and first.size == (480, 480)
                    diff = ImageChops.difference(first, second)
                    assert diff.getbbox() and diff.getbbox()[1] > first.height // 2
            final = status()
            assert final["greeting_enabled"] is greeting_enabled
            assert final["greeting_responses"] == (3 if greeting_enabled else 0)
            assert final["command_responses"] == (16 + len(replies) if greeting_enabled else 0)
            assert final["ai_ready"] is greeting_enabled
            assert final["ai_requests"] == (5 if greeting_enabled else 0)
            assert final["ai_failures"] == (1 if greeting_enabled else 0)
            assert final["archive_errors"] == 0
            all_rows = archive_rows("--all")
            assert len(archive_rows()) == 20 < len(all_rows)
            private_rows = [r for r in all_rows if r["event"]["message_type"] == "private"]
            assert all(r["event"]["user_id"] == 30000 for r in private_rows)
            if greeting_enabled:
                assert any(r["quick_reply"] and r["quick_reply"]["reply"] == GREETING for r in private_rows)
                found = next(r for r in all_rows if r["event"]["message"] == question)
                assert found["reply_at"] and found["quick_reply"]["reply"][1]["data"]["text"] == "模拟对白 [CQ:at,qq=all]"
            else:
                assert not private_rows and all(r["quick_reply"] is None for r in all_rows)
            if greeting_enabled:
                local = next(r for r in all_rows if r["event"].get("group_id") == 20000
                             and r["event"]["message_id"] == 700)
                foreign = next(r for r in all_rows if r["event"].get("group_id") == 20003
                               and r["event"]["message_id"] == 700)
                assert "昨日日报" in command(group, "本群查询")
                assert "本条已入库" in command(group, "运行状态")
                assert "累计归档" in command(group, "消息统计")
                assert "本群最近消息" in command(group, "最近消息")
                assert "周六" in command(group, f"查记录 #{local['id']}")
                assert "本群没有" in command(group, f"查记录 #{foreign['id']}")
                assert "本群没有" in command(group, f"查记录 #{private_rows[0]['id']}")
                assert "北京时间" in mention(group, [bot_at, words(" 日报")], True)
                assert "信息日报" in command(group, "昨日日报")
                assert "暂无符合条件" in command(group, "日报 2025-06-02")
                assert "请输入" in command(group, "日报 2025-02-30")
                assert "请输入" in command(group, "查记录 #9999999999999999999")
                for denied in (private, second_group, dict(group, group_id=20001),
                               dict(group, user_id=30004, sender={"user_id": 30004})):
                    command(denied, "最近消息", False)
                mention(dict(group, group_id=20003), [bot_at, words(" 运行状态")])
                assert status()["ai_requests"] == final["ai_requests"]
                print("PASS: scoped group queries, event-bound records, command priority and duplicates")
            print("PASS: durable group capture, self reports, scoped private history, date export and deduplication")
            print("PASS: scoped text, image rendering, missing assets, and duplicate delivery")
        finally:
            process.stdin.close()
            process.wait(timeout=10)


def stop_on_eof():
    # Stop the actual test server, including when a Windows venv launcher wraps it.
    import _thread
    sys.stdin.buffer.read()
    _thread.interrupt_main()


def check_archive_reopen(access):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "messages.sqlite3"
        calls = Path(directory) / "calls.sqlite3"
        journal = DialogueLog(calls)
        event = {"self_id": 10000, "group_id": 21000, "message_id": 1, "user_id": 31900,
                 "time": 10, "post_type": "message", "message_type": "group", "message": "旧问题"}
        quote = dict(event, message_id=2, message="旧引用")
        journal.begin(event, quote, {})
        journal.begin(event, quote, {})
        journal.db.close()
        archive = MessageArchive(path, calls, access)
        try:
            for n in range(3, 303):
                archive.record(dict(event, message_id=n), 21000)
            row_id, replied = archive.record(event, 21000)
            assert not replied
            archive.quick_reply(row_id, {"reply": "测试"})
        finally:
            archive.db.close()
        reopened = MessageArchive(path, calls, access)
        try:
            assert reopened.record(event, 21000) == (row_id, True)
            assert reopened.db.execute("SELECT COUNT(*) FROM messages").fetchone() == (302,)
            assert reopened.db.execute("SELECT COUNT(*) FROM messages WHERE source='model_journal'").fetchone() == (2,)
        finally:
            reopened.db.close()


if __name__ == "__main__":
    from receiver import GreetingAccess
    from unittest.mock import patch

    asyncio.run(check_model_timeout())
    recent = RecentMessages()
    with patch.object(dialogue_context, "monotonic", return_value=0):
        for n in range(257):
            recent.remember({"group_id": 20000, "message_id": n, "message": "示例"})
        assert recent.get(20000, "0") is None and recent.get(20000, "1") is not None
    with patch.object(dialogue_context, "monotonic", return_value=1800):
        assert recent.get(20000, "1") is None

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "access.json"
        base_config = {"bot_id": 10000, "user_id": 30000}
        path.write_text(json.dumps(dict(base_config, group_id=20000)), encoding="ascii")
        assert GreetingAccess.load(path).groups == {20000: "test"}
        path.write_text(json.dumps(dict(base_config, group_ids=[20000, 20002])), encoding="ascii")
        old = GreetingAccess.load(path)
        check_archive_reopen(old)
        assert old.groups == {20000: "test", 20002: "test"}
        assert old.profiles["test"] == MODULE_LABELS.keys() - {"ai_dialogue", "group_reports"}
        for fields in ({"group_ids": []}, {"group_ids": "20000"}, {"group_ids": [20000, True]},
                       {"group_ids": [20000, -1]}, {"group_id": 20000, "group_ids": [20002]},
                       {"groups": {"20000": "unknown"}, "profiles": {}},
                       {"groups": {"20000": "bad"}, "profiles": {"bad": ["typo"]}}):
            path.write_text(json.dumps({**base_config, **fields}), encoding="ascii")
            assert GreetingAccess.load(path) is None
    check()
    check(greeting_enabled=True)
