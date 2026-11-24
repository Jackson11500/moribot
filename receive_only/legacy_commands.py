"""Explicit legacy commands for allowlisted test conversations."""

import base64
from functools import lru_cache
from io import BytesIO
from pathlib import Path
import random
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
PUZZLES = ROOT.parent / "src" / "plugins" / "little_game" / "24点.txt"
MISSING = "数据库已丢失...茉莉酱正在寻找中"
GREETING = "主人找我有什么事呢？"
MODULE_LABELS = {
    "greeting": "问候与指南", "little_game": "小游戏", "technique": "实用资料",
    "chatting": "聊天", "someone_say": "有人说制图", "random_pic": "随机图片（缺图库）",
    "user": "签到与排行（缺资料）",
}
TEMPLATES = ("鲁迅说", "鲁迅", "年号", "宁宁", "千代", "nobeta", "追杀图", "追杀",
             "喜报", "猫娘", "气晕", "小本本")
GROUP_TEXT = {
    "小游戏": "茉莉的小游戏：\n骰子\n骰子：整数（输入需要投出的范围）\n24点",
    "实用资料": "茉莉的实用资料列表：\n蓝图档案馆\n资料导航站\n逻辑大全\n颜色列表",
    "蓝图档案馆": "Mindustry 蓝图档案馆：https://docs.qq.com/sheet/DVHNoS3lIcm1NbFFS\n"
                 "蓝图审查局：https://docs.qq.com/sheet/DVGRjTFNadXJYcHZY",
    "资料导航站": "Mindustry 资料导航站：https://docs.qq.com/sheet/DVEVob2xrcVBzQk5R",
    "有人说": "茉莉的名人名言系列！\n发送「鲁迅说：你想写的话」可以制图。\n"
             "正在找底图：年号、宁宁、千代、nobeta、追杀图、喜报、猫娘、气晕、小本本。",
}
CHAT = {
    "az": ("啊这", "别az了，你只会az吗？"),
    "啊这": ("az", "别啊这了，你只会啊这吗？"),
    "草": ("草", "艹", "茉莉知道！这是一种禾本科植物", "是什么让你这么震惊呢？"),
    "问号": ("?", "¿", "？", "(。´・ω・)ん?", "需要茉莉酱帮忙吗？"),
    "茉莉贴贴": ("贴贴！！", "贴，都可以贴~", "好啦，真是拿你没办法呢~贴~", "贴...贴贴（靠近）"),
    "变猫娘": tuple("挥动了法杖，一不小心把自己变成了[" + cat + "]"
                for cat in ("白猫", "黑猫", "猫又", "等待投喂の小猫", "火焰猫燐")),
}
ALIASES = {"游戏": "小游戏", "艹": "草", "?": "问号", "？": "问号", "贴贴茉莉": "茉莉贴贴",
           "颜色大全": "颜色列表"}
# Only these fixed filenames can be served as static material.
STATIC = {
    "逻辑大全": ("逻辑介绍.jfif", "是小撒姐姐做的哦~非常的实用呢"),
    "颜色列表": ("搞颜色.png", "Way_Zer调出来的！"),
    "吸狐狸": ("吸狐狸.jpg", ""), "救命啊": ("救命啊.jpg", ""),
}
PICTURE_CATEGORIES = frozenset(
    "图片 茉莉 狐狸 kimo kimo酱 高血压 梗图 小汤圆 shizuku 猫娘 emoji 帕秋莉 lc cloverday "
    "工业2 燐猫 火焰猫燐 carrot 萝卜 乃爱 大猫 小岛游 小屑猫 六花 小岛游六花 小恶魔 小emo "
    "小伞 多多良小伞 多多良小鼬 二次元 二刺螈 妹子 秘封 东方 车万 三色 三色绘恋 天使 "
    "白毛狐狸 BA BlueArchive ba AA AscixArt 科幻 stellaris 群星".split()
)


def image_reply(data: bytes, caption: str = "") -> list[dict]:
    # OpenQQ v0.5.0 reads at most 1 MiB of a POST response, including base64.
    if len(data) > 720 * 1024:
        with Image.open(BytesIO(data)) as large:
            large.thumbnail((900, 900))
            compressed = BytesIO()
            large.convert("RGB").save(compressed, format="JPEG", quality=80)
            data = compressed.getvalue()
    segments = [{"type": "text", "data": {"text": caption + "\n"}}] if caption else []
    segments.append({"type": "image", "data": {
        "file": "base64://" + base64.b64encode(data).decode("ascii"),
    }})
    return segments


def static_image(filename: str, caption: str = ""):
    try:
        with (ASSETS / filename).open("rb") as source:
            with Image.open(source) as img:
                img.verify()
            source.seek(0)
            return image_reply(source.read(), caption)
    except (OSError, ValueError, SyntaxError):
        return MISSING


def luxun_quote(quote: str):
    if not quote.strip():
        return "在冒号后写上想说的话哦，比如「鲁迅说：早上好」。"
    if len(quote) > 120:
        return "太长了，鲁迅说不完..."
    try:
        with Image.open(ASSETS / "luxun.jpg") as template:
            card = template.convert("RGB")
        # Use a CJK font installed on the deployment host.
        fonts = (Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
                 Path("C:/Windows/Fonts/msyh.ttc"))
        font_path = next((path for path in fonts if path.is_file()), None)
        if font_path is None:
            return MISSING
        font = ImageFont.truetype(str(font_path), card.width // 15)
        pen = ImageDraw.Draw(card)
        lines = []
        line = ""
        for char in quote:
            if char == "\n" or pen.textlength(line + char, font=font) > card.width * 0.82:
                lines.append(line)
                line = ""
            if char != "\n":
                line += char
        lines.append(line)
        line_height = font.size + 4
        if len(lines) * line_height > card.height * 0.4:
            return "太长了，鲁迅说不完..."
        bottom = int(card.height * 0.83)
        for i, line in enumerate(reversed(lines)):
            pen.text((card.width // 2, bottom - i * line_height), line, font=font,
                     anchor="mb", fill="white", stroke_width=1, stroke_fill="black")
        pen.text((card.width * 0.9, card.height * 0.94), "——鲁迅", font=font,
                 anchor="rb", fill="white", stroke_width=1, stroke_fill="black")
        encoded = BytesIO()
        card.save(encoded, format="JPEG", quality=90)
        return image_reply(encoded.getvalue())
    except (OSError, ValueError):
        return MISSING


@lru_cache(maxsize=1)
def puzzles():
    return PUZZLES.read_text(encoding="utf-8").splitlines()


def roll(name: str, argument: str | None):
    if argument is None:
        return f"使用了一个{name}，丢出了一个{random.randint(1, 6)}"
    if len(argument) > 17:
        return f"扔辣么大个{name}干什么嘛"
    if not re.fullmatch(r"-?[0-9]+", argument):
        return f"{name}只能是整数组成的懂不懂啦！"
    sides = int(argument)
    if sides == 1:
        return f"抛出了一个硬币，丢出了一个{random.randint(0, 1)}"
    if sides == 0:
        return f"使用了一个薛定谔{name}，丢出了一个{random.randint(1-10**20, 10**20-1)}"
    low, high = (1, sides) if sides > 0 else (sides, 0)
    return f"使用了一个自定义{name}（{low}~{high}），丢出了一个{random.randint(low, high)}"


def game_reply(command: str):
    if command == "小游戏":
        return GROUP_TEXT[command]
    if command == "24点":
        try:
            deck = puzzles()
        except (OSError, UnicodeError):
            return MISSING
        if not deck:
            return MISSING
        return "随机24点：\n每个数字必须恰好用一次，用 + - * / 和括号算出 24。\n" + random.choice(deck)
    dice = re.fullmatch(r"(骰子|色子)(?:[：:](.*))?", command)
    if dice:
        return roll(*dice.groups())
    if re.fullmatch(r"24点[：:][0-9]+", command):
        return MISSING


def technique_reply(command: str):
    if command in ("实用资料", "蓝图档案馆", "资料导航站"):
        return GROUP_TEXT[command]
    if command in ("逻辑大全", "颜色列表"):
        return static_image(*STATIC[command])
    if re.fullmatch(r"(?:源码[：:]|source ?=)[A-Za-z0-9_-]+", command):
        return MISSING


def chat_reply(command: str):
    if command in CHAT:
        return random.choice(CHAT[command])
    if command in ("吸狐狸", "救命啊"):
        return static_image(*STATIC[command])


def template_reply(command: str):
    if command == "有人说":
        return GROUP_TEXT[command]
    parts = re.split("[：:]", command, maxsplit=1)
    if len(parts) == 2:
        name, argument = parts
        if name in ("鲁迅说", "鲁迅"):
            return luxun_quote(argument)
        if name in TEMPLATES:
            return MISSING


def picture_reply(command: str):
    if command.startswith("随机") and command[2:] in PICTURE_CATEGORIES:
        return MISSING


def user_reply(command: str):
    if command in ("签到", "排行榜"):
        return MISSING


GROUP_HANDLERS = {
    "little_game": game_reply, "technique": technique_reply, "chatting": chat_reply,
    "someone_say": template_reply, "random_pic": picture_reply, "user": user_reply,
}


def module_names(modules: frozenset[str]) -> str:
    return "、".join(label for key, label in MODULE_LABELS.items() if key in modules) or "无"


def command_reply(text: str, *, group_modules: frozenset[str] | None):
    # None is an authorized private conversation. An empty group policy allows no commands.
    private = group_modules is None
    if private or "greeting" in group_modules:
        if text == "茉莉酱":
            return GREETING
        if text in ("茉莉酱!", "茉莉酱！"):
            if private:
                return GREETING + "\n私聊指令：你好、茉莉的命令大全、群权限（查看各测试群）。"
            return GREETING + "\n本群已开：" + module_names(group_modules) + "。\n发送「群权限」查看本群权限。"
        if text in ("茉莉的命令大全", "指令大全"):
            return static_image("legacy-help.png", "这是旧版指令图。发送「茉莉酱！」查看当前菜单。")
    if private:
        return "欢迎回来" if text == "你好" else None
    command = ALIASES.get(text, text)
    for module, handler in GROUP_HANDLERS.items():
        if module in group_modules:
            reply = handler(command)
            if reply is not None:
                return reply
    return None
