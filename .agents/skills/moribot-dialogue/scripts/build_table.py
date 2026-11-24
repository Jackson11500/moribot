"""Rebuild the dialogue reference from the repository's authored replies."""

import ast
from collections import Counter
from html import escape
from pathlib import Path
import re
import sys


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]


def load_bank(name):
    source = REPO / "src/plugins/chatting" / name
    tree = ast.parse(source.read_text(encoding="utf-8"))
    assignment, = (node for node in tree.body if isinstance(node, ast.Assign)
                   and isinstance(node.value, ast.Dict))
    return ast.literal_eval(assignment.value)


def cell(text):
    text = re.sub(r"([\\|`*_~\[\]])", r"\\\1", escape(text, quote=False))
    return text.replace("\n", "<br>")


def main():
    sys.path.insert(0, str(REPO / "receive_only"))
    from legacy_commands import ALIASES, CHAT, GREETING

    normal = load_bank("chatdir2.py")
    extended = load_bank("chatdir.py")
    keys = list(dict.fromkeys([*normal, *extended]))
    unique_pairs = sum(len(set(normal.get(k, ())) | set(extended.get(k, ()))) for k in keys)
    lines = [
        "# 茉莉对话表", "",
        "## 当前可在 QQ 触发的文字互动", "",
        "表中每行是一个触发方式；同一格的多行是随机候选。群内调用仍受发送者和群模块权限约束。", "",
        "| 触发 | 会话与模块 | 文字候选 |", "|---|---|---|",
        f"| 茉莉酱 | 好友私聊或群内问候 | {GREETING} |",
        "| 你好 | 好友私聊 | 欢迎回来 |",
        "| 直接 @ 机器人，未命中指令 | 群内已开智能对话 | DeepSeek 按风格稿生成，引用本条原消息 |",
        "| 单独 @，且该群仅开聊天、未开智能对话 | 群内聊天 | 是...在找我吗？ |",
    ]
    for key, replies in CHAT.items():
        names = [key, *(alias for alias, target in ALIASES.items() if target == key)]
        lines.append(f"| {'、'.join(names)} | 群内聊天 | {'<br>'.join(cell(s) for s in replies)} |")
    lines += [
        "", "群里的「吸狐狸」「救命啊」是找固定图片的触发词。缺素材时回复统一提示，"
        "这类运维提示不作为人物口吻样本。[当前指令源码](../../../../receive_only/legacy_commands.py)",
        "", "## 其他历史互动", "",
        "| 触发方式 | 代表性回复或行为 | 原来的回复形式 |", "|---|---|---|",
        "| 戳一戳机器人 | 摸起来舒服吗 | 群通知触发，随机文字 |",
        "| 真正 @ 机器人，旧词库没有命中 | 是...在找我吗？ | 随机文字或素材图 |",
        "| 发现 bug | 这是特性！ | 群关键词，文字或梗图 |",
        "| 戴森球工厂、塑钢带工厂 | 戴森球计划要火！ | 群关键词，文字或梗图 |",
        "| 连续复读 | 打断施法！ | 群内连续重复，打断或跟读 |",
        "| 变猫娘并 @ 某人 | 使用了猫娘变化大法，把目标变成随机品种 | 群消息中读取目标，文字配 @ |",
        "", "这一组是历史行为示例；当前调用范围见上表。"
        "[聊天与戳一戳](../../../../src/plugins/chatting/__init__.py) · "
        "[Mindustry](../../../../src/plugins/mdt_relate/__init__.py) · "
        "[复读](../../../../src/plugins/repeater.py) · [变身](../../../../src/plugins/changing/__init__.py)",
        "", "## 旧版定向聊天词库", "",
        f"模式 2（普通）有 {len(normal)} 个词、{sum(map(len, normal.values())):,} 个候选项。"
        f"模式 3（扩展）有 {len(extended)} 个词、{sum(map(len, extended.values())):,} 个候选项。"
        f"合并后为 {len(keys)} 个触发词、{unique_pairs:,} 个不同的“触发词＋回复”组合。",
        "", "旧群处理器在定向消息全文命中触发词时，从相应列表随机抽一项。"
        "表中次数是该候选在源码列表里出现的次数，0 表示该模式没有这句。"
        "它们是作者写的候选，并非聊天记录或使用频率。线上触发以第一张表为准。"
        "可在本文内搜索「累了」「饿」「贴贴」等小节。",
        "", "[普通词库](../../../../src/plugins/chatting/chatdir2.py) · "
        "[扩展词库](../../../../src/plugins/chatting/chatdir.py) · "
        "[旧触发器](../../../../src/plugins/chatting/__init__.py)",
    ]
    for key in keys:
        n, e = Counter(normal.get(key, ())), Counter(extended.get(key, ()))
        lines += ["", f"### {cell(key)}", "", "| 原文候选 | 模式 2 次数 | 模式 3 次数 |", "|---|---:|---:|"]
        for text in dict.fromkeys([*n, *e]):
            lines.append(f"| {cell(text)} | {n[text]} | {e[text]} |")
    out = SKILL / "references/dialogue-table.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(keys)} keys, {unique_pairs} distinct trigger/reply pairs")


if __name__ == "__main__":
    main()
