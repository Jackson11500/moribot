---
name: moribot-receive-only
description: 在 moribot 仓库部署、恢复或排查 OpenQQ、LLBot 与 NoneBot2 的 OneBot v11 只接收实例，复用已验证的配置并记录新的故障与恢复断点。
---

# moribot 只接收部署

接手任务时先读[部署与排障记录](references/deployment.md)。从仓库根目录执行其中的 PowerShell 命令。先查本机状态和已有运行目录，再决定是否需要安装。

使用 `receive_only/receiver.py` 验签并核对私有白名单。`legacy_commands.py` 只处理本人好友私聊或本人在获准测试群发送的文字和对机器人的直接 @。当前可测指令与群聊限制见[功能清单](../../../docs/legacy-features.md)。群内文字和图片通过原事件的 HTTP 响应引用触发消息。直接 @ 先分派指令，未命中且该群启用 ai_dialogue 时才调用 DeepSeek。引用后 @ 时，从同群近期入站消息补原文。排查称呼、引用或模型回答时，通过服务器的 `moribot-dialogues` 按调用编号查看原始事件与模型输入输出。制图测试免费，用户旧档案和账本只在另有迁移任务时处理。

查看某群某天的完整聊天，用 `moribot-messages --group <群号> --date YYYY-MM-DD --jsonl`。长期归档覆盖机器人收到的全部群，回复继续使用私有权限组。默认条数只用于查看。归档范围、历史补录与查错入口见[部署记录](references/deployment.md)。

管理群发「查看指令」可列出跨群只读操作。管理权同时绑定私有配置中的 `user_id` 和 `admin_group_id`，核验时包括共享权限组的其他群和同群其他成员。

查群日报时使用 `moribot-daily`，核对数据口径和开源参考见[日报说明](../../../docs/group-daily-report.md)。

验证改动时运行 `receive_only/check_offline.py`。实机验收用上报心跳和自然到达的消息，避免向任何会话发送测试消息。授权、扫码由用户在本机完成。分享状态只需计数和时间，凭证、登录二维码及聊天正文留在运行环境。

每次解决会再次遇到的问题，在记录中补上日期、症状、原因、实际修复和验证结果。更新已经失效的断点，并区分本机已验证的结果与尚待验证的步骤。

Linux 线上实例使用 OpenQQ。接收程序在 `receive_only/`，启动脚本和 systemd 单元在 `receive_only/linux/`。修改部署文件时按仓库根目录的 [AGENTS.md](../../../AGENTS.md) 同步本机副本、验证并提交。
