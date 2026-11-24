---
name: moribot-receive-only
description: 在 moribot 仓库部署、恢复或排查 OpenQQ、LLBot 与 NoneBot2 的 OneBot v11 只接收实例，复用已验证的配置并记录新的故障与恢复断点。
---

# moribot 只接收部署

接手任务时先读[部署与排障记录](references/deployment.md)。从仓库根目录执行其中的 PowerShell 命令。先查本机状态和已有运行目录，再决定是否需要安装。

使用 `receive_only/receiver.py` 验签并核对私有白名单。`legacy_commands.py` 只处理本人好友私聊或本人在获准测试群发送的文字和对机器人的直接 @。当前可测指令与群聊限制见[功能清单](../../../docs/legacy-features.md)。群内文字和图片通过原事件的 HTTP 响应引用触发消息。直接 @ 先分派指令，未命中且该群启用 ai_dialogue 时才调用 DeepSeek。其他事件返回空 204。制图测试免费，用户旧档案和账本只在另有迁移任务时处理。

验证改动时运行 `receive_only/check_offline.py`。实机验收用上报心跳和自然到达的消息，避免向任何会话发送测试消息。授权、扫码由用户在本机完成。分享状态只需计数和时间，凭证、登录二维码及聊天正文留在运行环境。

每次解决会再次遇到的问题，在记录中补上日期、症状、原因、实际修复和验证结果。更新已经失效的断点，并区分本机已验证的结果与尚待验证的步骤。

Linux 线上实例使用 OpenQQ。接收程序在 `receive_only/`，启动脚本和 systemd 单元在 `receive_only/linux/`。修改部署文件时按仓库根目录的 [AGENTS.md](../../../AGENTS.md) 同步本机副本、验证并提交。
