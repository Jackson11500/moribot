---
name: moribot-receive-only
description: 在 moribot 仓库部署、恢复或排查 OpenQQ、LLBot 与 NoneBot2 的 OneBot v11 只接收实例，复用已验证的配置并记录新的故障与恢复断点。
---

# moribot 只接收部署

接手任务时先读[部署与排障记录](references/deployment.md)。从仓库根目录执行其中的 PowerShell 命令。先查本机状态和已有运行目录，再决定是否需要安装。

这个实例只接收事件。使用 `receive_only/receiver.py`，保留签名校验、空 204 响应以及全局 OneBot API 禁用。旧的 Docker Compose 和 `src/plugins` 属于原机器人。签到、复读、定时任务、好友或入群请求处理均不属于此入口。

验证改动时运行 `receive_only/check_offline.py`。实机验收用上报心跳和自然到达的消息，避免向任何会话发送测试消息。授权、扫码由用户在本机完成。分享状态只需计数和时间，凭证、登录二维码及聊天正文留在运行环境。

每次解决会再次遇到的问题，在记录中补上日期、症状、原因、实际修复和验证结果。更新已经失效的断点，并区分本机已验证的结果与尚待验证的步骤。

Linux 线上实例使用 OpenQQ。接收程序在 `receive_only/`，启动脚本和 systemd 单元在 `receive_only/linux/`。修改部署文件时按仓库根目录的 [AGENTS.md](../../../AGENTS.md) 同步本机副本、验证并提交。
