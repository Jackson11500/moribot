"""Exercise the real HTTP receiver on a temporary port without starting LLBot."""

import base64
import hashlib
import hmac
from io import BytesIO
import json
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
from legacy_commands import ASSETS, GREETING, MISSING, MODULE_LABELS, PUZZLES


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
            (Path(directory) / "greeting-access.json").write_text(json.dumps(
                {"bot_id": 10000, "user_id": 30000,
                 "profiles": {"test": list(MODULE_LABELS), "games": ["greeting", "little_game"]},
                 "groups": {"20000": "test", "20002": "games"}}
            ), encoding="ascii")
        code = (
            "from pathlib import Path; import receiver, sys; "
            "receiver.RUNTIME = Path(sys.argv[1]); receiver.PORT = int(sys.argv[2]); "
            "receiver.start()"
        )
        process = subprocess.Popen(
            [sys.executable, "-c", code, directory, str(port)], cwd=Path(__file__).parent
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
            group = dict(private, message_type="group", sub_type="normal", group_id=20000)
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
                        return operation["reply"]
                    elif reply.status == 204:
                        assert reply.read() == b""

            post(private, 403, signing_key="wrong-key")
            post(group, 403, signing_key="wrong-key")
            for denied in (
                dict(private, user_id=30001, sender={"user_id": 30001}),
                dict(group, user_id=30001, sender={"user_id": 30001, "role": "owner"}),
                dict(second_group, user_id=30001, sender={"user_id": 30001, "role": "owner"}),
                dict(group, group_id=20001),
                dict(group, self_id=10001),
                dict(group, user_id=10000, sender={"user_id": 10000}),
                dict(group, sub_type="anonymous"),
                dict(private, sub_type="group"),
                dict(group, message=[{"type": "at", "data": {"qq": "10000"}}, *group["message"]]),
                dict(private, message="茉莉酱！！"),
                dict(private, post_type="message_sent"),
            ):
                post(denied)
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
            assert final["command_responses"] == (8 + len(replies) if greeting_enabled else 0)
            print("PASS: scoped text, image rendering, missing assets, and duplicate delivery")
        finally:
            process.terminate()
            process.wait(timeout=5)


if __name__ == "__main__":
    from receiver import GreetingAccess

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "access.json"
        base_config = {"bot_id": 10000, "user_id": 30000}
        path.write_text(json.dumps(dict(base_config, group_id=20000)), encoding="ascii")
        assert GreetingAccess.load(path).groups == {20000: "test"}
        path.write_text(json.dumps(dict(base_config, group_ids=[20000, 20002])), encoding="ascii")
        old = GreetingAccess.load(path)
        assert old.groups == {20000: "test", 20002: "test"} and old.profiles["test"] == MODULE_LABELS.keys()
        for fields in ({"group_ids": []}, {"group_ids": "20000"}, {"group_ids": [20000, True]},
                       {"group_ids": [20000, -1]}, {"group_id": 20000, "group_ids": [20002]},
                       {"groups": {"20000": "unknown"}, "profiles": {}},
                       {"groups": {"20000": "bad"}, "profiles": {"bad": ["typo"]}}):
            path.write_text(json.dumps({**base_config, **fields}), encoding="ascii")
            assert GreetingAccess.load(path) is None
    check()
    check(greeting_enabled=True)
