# 部署与排障记录

## 群权限组与查询（2026-11-24）

当前私有配置以 `groups` 将群号映射到权限组名称，以 `profiles` 将名称映射到功能模块列表。`bot_id` 和 `user_id` 继续绑定机器人和唯一调用者。例如 `"groups": {"20000": "games"}, "profiles": {"games": ["greeting", "little_game"]}` 表示合成测试群只可执行问候和小游戏。真实授权关系保存在服务器的 `.runtime/greeting-access.json`。增加同策略的群只需追加一条绑定，再重启接收服务。要给某群单独设权限，可增加一个权限组并更改该群的绑定。

已部署的模块键沿用旧功能名：`greeting`（问候、指南）、`little_game`、`technique`、`chatting`、`someone_say`、`random_pic`、`user`。缺少素材或账本的功能仍使用原有提示。未启用的模块直接忽略其命令，包括别名和缺图分支。群权限查询始终只对已授权本人开放。私聊 `群权限` 列出所有授权群，群内查询只列本群；`群组状态` 是同一指令的别名。

此前的 `group_id` / `group_ids` 配置仍能按其原有测试功能读取。正式配置已将两个获准群绑定到同一 `test` 权限组。使用合成数据验证了两个群绑定不同策略时的实际分派、菜单、跨群信息隔离，以及未知策略或模块拒绝加载。Windows 和 Linux 的隔离测试均通过，线上接收服务已重启并核对实际策略。

## 追加测试群（2026-11-24）

接收端的私有配置文件 `receive_only/.runtime/greeting-access.json` 使用 `bot_id`、`user_id` 和 `group_ids`。追加群时保留前两个身份字段，将新群加到现有正整数列表里。旧配置的单个 `group_id` 仍可读取。新旧群字段同时出现、列表为空或任一号码无效时，接收端关闭回复。

在服务器原子替换私有配置，保留 root 所有、接收服务组可读的 0640 权限，仅重启 `moribot-receiver`。本次用合成签名事件在 Windows 和 Linux 验证了两个群与好友私聊均可由本人触发、其他用户及第三个群被忽略。上线后用服务账号核对实际生效的名单和服务健康状态。真实群号仅存私有配置。

## 白名单指令和背景图恢复（2026-11-24）

`茉莉酱！` 显示当前菜单，`茉莉的命令大全` 返回带历史版本说明的原图。白名单用户可在测试群试 `24点`、`骰子：20`、`鲁迅说：早上好`。制图由用户选定免费测试，旧账本未接入。已识别但缺图或缺资料的命令按原文回“数据库已丢失...茉莉酱正在寻找中”。完整列表见[功能清单](../../../../docs/legacy-features.md)。

旧插件把图片路径写死在 Windows 外部目录。查 Git 的全部可达历史时，从 `f071155e:resources/img/other/luxun.jpg` 找回鲁迅底图，从 `a045c4b:src/plugins/greeting/命令说明.png` 找回旧指南。两张图经目视检查。制图使用 Pillow，在内存中独立排字、编码 JPEG，Linux 用系统的文泉驿正黑。OpenQQ v0.5.0 的快速操作响应上限为 1 MiB，大图转为缩小的 JPEG 后再编码为 base64。

部署时保持仓库相对布局。接收端额外需要 `receive_only/legacy_commands.py`、`receive_only/assets/` 下两张图、`src/plugins/little_game/24点.txt` 和更新后的 Python 依赖。重启接收服务前，在临时目录运行其 `check_offline.py`。Windows 的受限环境中子进程可能显示启动但回环访问失败，同一隔离测试在宿主回环可通过。SSH 正常而 SCP 提示 Connection closed 时，本次使用 `scp -O` 经相同 SSH 别名传输成功。

两端离线验收已覆盖开关、白名单、重复投递、中文排字、图库原图、无素材文案和群专用命令。另在本机用上游 v0.5.0 的实际 HTTP 上报模块向模拟发送器投递六个事件，仅出现三次动作，即好友私聊 PNG、测试群 JPEG 和测试群缺图文字。正式部署逐一比对七个文件的 SHA-256，只重启了接收服务。回环状态 `command_responses` 是当前进程返回的全部指令回复数，`greeting_responses` 是精确问候的子集。QQ 客户端送达需由授权本人触发确认。

## 测试会话的单条问候（2026-11-24）

线上仅为私有白名单恢复了纯文字口令 `茉莉酱`。发送者必须是配置的同一用户，地点是该用户与专用号的好友私聊，或指定测试群的普通群消息。回复内容为“主人找我有什么事呢？”。其他发送者、其他群、临时私聊、非文字指令和不同机器人都无法获得这条回复。

接收端从 `receive_only/.runtime/greeting-access.json` 读入三个正整数键 `bot_id`、`user_id` 和 `group_id`。线上使用 root 所有、接收服务组可读的 0640 文件。缺失或无效时退回只接收。修改配置后仅重启 `moribot-receiver`。真实号码和登录信息仅存运行环境。

OpenQQ v0.5.0 会处理签名 HTTP POST 的响应体。通过授权校验的口令返回 JSON 快速回复，OpenQQ 从原始事件选择目的地。其他有效上报仍返回空 204。没有为此启用标准 HTTP 动作端口、WebSocket、通用 NoneBot 出站 API 或历史插件。

Windows 与 Linux 都已通过隔离的 `check_offline.py`。本机另用 v0.5.0 的上报模块连接隔离接收端，向模拟发送器投递 6 条合成事件，验证仅有授权私聊和授权测试群各一次文字发送。线上已核对代码、私有配置权限、接收服务和现有 QQ 登录会话。回环 `/status` 的 `greeting_enabled` 表示配置生效，`greeting_responses` 只统计本次进程发出的快速回复指令；最终送达以 QQ 会话为准。

## 本机代码与 Linux 部署对应关系（2026-11-24）

| 本机仓库 | 服务器 |
|---|---|
| `receive_only/receiver.py`、`check_offline.py`、`requirements.txt` | `/opt/moribot-openqq/receive_only/` 下的同名文件 |
| `receive_only/linux/session.sh` | `/opt/moribot-openqq/session.sh` |
| `receive_only/linux/systemd/` 下的服务单元和两个 `.service.d/` 目录 | `/etc/systemd/system/` 下的同名文件和目录 |

以上八个文件已逐一比对 SHA-256。本机离线检查通过，未签名上报返回 401，已签名的模拟消息返回空 204 并计数一次。两个 systemd 覆盖文件使用本次已确认的专用号资料目录。更换资料目录时同步检查 `BindPaths` 和 `ConditionPathExists` 指向同一份资料。

## SSH 免密登录与一次性私聊测试（2026-11-24）

在这台 Windows 电脑上用 `ssh moribot-openqq` 登录部署主机。主机别名写在用户的 `~/.ssh/config` 中，使用专用 Ed25519 密钥并启用 `IdentitiesOnly`、`BatchMode` 和严格主机密钥校验。已通过仅允许公钥认证的实际 SSH 登录验证。新终端可以直接复用此别名。

本机登录页连不上时，先检查现有隧道。如果 16080 未监听，在本机运行以下命令并保持该进程运行，再打开 [noVNC 登录页](http://127.0.0.1:16080/vnc.html?autoconnect=true&resize=scale)。

```powershell
ssh -NT -o ExitOnForwardFailure=yes -L 127.0.0.1:16080:/run/moribot-openqq/novnc.sock moribot-openqq
```

恢复隧道后已验证网页 HTTP 200 并看到了服务器虚拟桌面。桌面只显示壁纸时，读取生效资料目录中的 `runtime/status.json`。本次阶段为 `session_ready`，资料目录有 `confirmed` 标记，WebUI 的 `get_login_info` 返回账号与运行时 `self_id` 一致，直接复用了已登录的会话。

用户指定的一次私聊测试已完成。通过服务器回环 WebUI 的 `/api/action` 提交一次 `send_private_msg`，OpenQQ 返回 `status=ok`、`retcode=0`、`message_id=1462`。提交前已移除本次临时管理凭证文件，以防重复发送。此项已办结。常驻接收端沿用原配置。

Windows 生成密钥时，本次 PowerShell 的 `--%` 把空口令传成了两个引号。表现是服务器接受公钥，客户端在批处理模式仍然登录失败。用保留空参数的原生参数传递修正了本次生成的私钥，并核对公钥一致。后续验证可执行 `ssh -o PreferredAuthentications=publickey moribot-openqq id -un`，成功返回 `root`。

## 一次性测试的前期排障（2026-11-23）

当时 OpenQQ 重启后处于 `hook_installed`，尚未提交私聊。短暂启用的标准 OneBot HTTP 测试端口已关闭。WebUI 管理凭证与 OneBot accessToken 独立。此前通过筛选 Node 进程的 stderr，在服务私有目录临时取得本次运行正常签发的管理凭证。在虚拟桌面启动器外层截取 stderr 没有取得管理地址。测试最终结果见上节。

## 专用号已恢复只接收（2026-11-23）

用户明确确认新会话是机器人专用号。已核对当前资料目录的登录阶段为 session_ready、签名上报目标和接收端密钥一致，OneBot HTTP 动作接口、正反向 WebSocket 与自身消息上报均关闭。已在该资料目录创建 confirmed 标记，moribot-receiver 的启动条件通过，状态为 active/running。接收服务仅监听 127.0.0.1:18765。北京时间 16:30:11 观察到正式接收端的消息计数从 0 增至 1，完成专用号真实入站验收。验收期间未发送测试消息。

## 误登账号后重新扫码（2026-11-23）

用户确认第一次服务器扫码选错了账号。已停止两个服务，保留原资料，在 moribot-openqq 服务的挂载命名空间中将全新的 home 和 runtime 绑定到原路径。生效配置在 /etc/systemd/system/moribot-openqq.service.d/90-scan-profile.conf，真实的新目录位于 /var/lib/moribot-qq-profiles 下。读取当前 status.json 应使用该配置指向的新 runtime。新窗口已显示“手机QQ扫码登录”，阶段为 hook_installed。

moribot-receiver.service.d/90-scan-confirmation.conf 的 ConditionPathExists 指向本次专用资料目录下的 confirmed 标记。用户确认专用号前，接收端保持 inactive，包括系统重启后。用户确认后先检查新 runtime 的 phase 为 session_ready，再创建条件指定的空标记，启动 moribot-receiver 并查看回环 /status。凭自然入站计数验收，省略账号和正文。旧资料保留在原处，当前 OpenQQ 会话使用新资料。

再次收到二维码过期反馈时，在 QQ 登录框中切到“账号登录”，再选“扫码登录”重新取码。仅刷新 noVNC 网页会重连现有画面。此次操作后已见 QQ 主窗口，并从当前资料目录验证 phase 为 session_ready。此时接收端仍为 inactive；新旧状态文件及常见账号目录未能完成账号比对，恢复接收前以用户所确认的账号为准。

## OpenQQ Linux 原生部署（2026-11-23）

已在目标 Ubuntu 24.04 x86-64 上完成原生部署。v0.5.0 的 GitHub Release 提供预编译 Linux x64 包，后续恢复应先复用此实例。OpenQQ 发行包已按 GitHub 资产 SHA-256 验证，Node.js v22.23.5 按官方 SHASUMS 验证，腾讯 Linux QQ 3.2.35-54395 amd64 已对照发行包的 SHA-256 核验。OpenQQ doctor 报 supported 和 native.ready 均为 true。[OpenQQ v0.5.0 发行包](https://github.com/feijx3/OpenQQ/releases/tag/v0.5.0) · [Linux QQ 包校验信息](https://github.com/flathub/com.qq.QQ/blob/master/com.qq.QQ.yaml)

- 程序、独立运行时、下载缓存和配置位于 /opt/moribot-openqq，初次安装目录合计约 1.1 GiB。服务账号 moribot-qq 的主目录 /var/lib/moribot-openqq 保存独立 QQ 登录资料，实测登录前约 2.9 MiB。QQ 数据目录为该主目录下的 .config/QQ。Windows 主号资料没有迁移。
- systemd 单元 moribot-openqq 和 moribot-receiver 均已启用开机启动。用 systemctl is-active moribot-openqq moribot-receiver 核查服务，用 curl -fsS http://127.0.0.1:18765/status 查看接收计数。OpenQQ 阶段文件为 /opt/moribot-openqq/vendor/openqq/openqq-v0.5.0-linux-x64/.runtime/status.json。仅提取 phase 字段，不打印账号、原始聊天和令牌。
- OneBot 只启用向回环接收端的签名 HTTP POST；WebSocket、反向 WebSocket、HTTP 动作接口和自身消息上报均关闭。只接收端的全局 API 调用禁用逻辑已部署，业务 Bot 目录初始为空。真实接收端启动后计数为 0，独立模拟测试验证无签名 401、有签名空 204 且消息计数加 1。不向 QQ 发送验收消息。
- 登录用的 noVNC 网页和 VNC 后端走权限受限的 Unix 套接字。客户端用下列转发命令（替换 SSH 目标），在同一台电脑用浏览器打开 http://127.0.0.1:16080/vnc.html?autoconnect=true&resize=scale。已实际通过本地隧道验证网页 HTTP 200 和 WebSocket 内 RFB 003.008 握手。只把登录入口交给用户，由用户用专用号扫码确认。初验阶段 hook_installed，已看到 QQ 窗口；真实专用号入站待登录后核实。首次启动曾有 Fluxbox 壁纸提示遮挡窗口，已关闭该提示并处理壁纸组件。
- 服务器仅在 127.0.0.1 监听接收端 18765 和 OpenQQ 内置管理界面 17860。管理界面无需转发。VNC 和 noVNC 无公网 TCP 监听。服务器系统自带 websockify 缺少 --unix-listen，/opt/moribot-openqq/novnc-venv 的 0.13.0 支持该选项。不要在部署记录内保存 SSH 密码、上报密钥或二维码。

```sh
ssh -NT -o ExitOnForwardFailure=yes -L 127.0.0.1:16080:/run/moribot-openqq/novnc.sock root@<服务器地址>
```

## 目标 Linux 主机部署前核查（2026-11-23）

通过 SSH 只读核查目标主机。Ubuntu 24.04.4 LTS x86-64，8 个逻辑核，内存可用约 61 GiB，系统分区 ext4 共 99 GiB、可用 61 GiB。Python 为 3.12.3。资源满足前述单账号预算。未安装 Docker，本机 APT 索引可查到 docker.io 和 docker-compose-v2。

从该主机请求 GitHub 项目页、Debian 软件源、npm、PyPI 和腾讯 QQ 版本清单均得到 HTTP 200。Docker Hub 的 registry-1.docker.io 两次探测分别超时和网络不可达。Amazon ECR Public 返回了所需 Node 22 bookworm-slim 的 linux/amd64 镜像清单，但同一映射下的 docker/dockerfile:1 前端返回 404。仅查了元数据，未拉镜像层、安装软件、构建容器或登录 QQ。

按当前网络条件，建议在可访问 Docker Hub 的 Linux/amd64 环境用上游 Dockerfile 构建，另将只接收入口及依赖打成接收端镜像；将两者通过 docker save 和 docker load 迁移至目标主机。目标端用已加载的准确标签启动并跳过构建与拉取。正式部署前重新核对磁盘与仓库连通性。账号仍由用户在服务器的独立配置目录中用专用号登录。

## Linux 服务器磁盘预算（2026-11-23）

OpenQQ v0.5.0、一个专用 QQ 号、NoneBot2 仅接收、在 Linux x86-64 主机本地构建。以下为部署前估算，尚未实测 Linux 镜像。现有服务器建议留 20 GB 可用空间；新购独立 VPS 建议 40 GB 系统盘。多个图片活跃群需要按缓存留存时间另算。

- 运行镜像与接收端环境合计按 2–4 GB 估算。Flathub 的打包清单记录 Linux QQ 3.2.35-54395 amd64 的压缩包为 188,287,504 字节。上游镜像还安装了 Node、图形库、FFmpeg 和 noVNC。[QQ 包清单](https://github.com/flathub/com.qq.QQ/blob/master/com.qq.QQ.yaml) · [OpenQQ Dockerfile](https://github.com/feijx3/OpenQQ/blob/v0.5.0/Dockerfile)
- 首次本机构建或升级时，镜像、临时文件、构建缓存和可能共存的旧镜像，合计按 6–10 GB 做预算（含运行镜像）。QQ 账号数据、媒体和日志另留 5–10 GB 起步。
- 上线后从上游 Compose 目录用 `du -sh ./docker-data/qq` 跟踪 QQ 持久化目录，另用 `docker system df` 检查镜像与构建缓存，用 `df -h .` 查看所在分区剩余空间。首次同步结束后对比一周的目录大小，按日均净增长和计划保留天数调整。[上游 Compose](https://github.com/feijx3/OpenQQ/blob/v0.5.0/compose.yaml)

## 账号选择与 Linux 迁移（2026-11-23）

Windows 上已在桌面 QQ 退出后启动过 OpenQQ：阶段为 `session_ready`，正式接收端从 0 计到 80 条消息。用户确认当时登录的是主号。该计数可能包括首次同步。本次随即停止了这个 OpenQQ 实例，确认 WebUI 端口已关闭，保留了 QQ 客户端；专用号尚未验收。后续需要测试专用号时，先确认客户端实际登录身份再开启正式上报。只核对身份与计数，不记录 QQ 号或聊天内容。

OpenQQ 使用同机 QQ 客户端的当前会话。OneBot 上报签名只用于接收端鉴权，不能用于选择 QQ 账号。在独立 Linux 服务器上，v0.5.0 的 Docker 方案运行官方 Linux QQ NT，首次可通过 SSH 转发访问 noVNC 登录窗口，由用户用专用号确认登录。上游 Compose 将登录态保存在服务器的 `./docker-data/qq`；使用新的专用数据目录可以与 Windows 主号会话隔离，失效后需重新验证。此次未部署 Linux。[Docker 部署说明](https://github.com/feijx3/OpenQQ/blob/v0.5.0/docs/docker.md) · [上游 Compose](https://github.com/feijx3/OpenQQ/blob/v0.5.0/compose.yaml)

## OpenQQ 本机测试部署（2026-11-23）

Windows 发行包已安装在 `receive_only/.runtime/openqq/openqq-v0.5.0-win-x64/`，工作区为 `D:\github\moribot`。入口为 `openqq.cmd`，实际配置为 `config/openqq.json`。保留的原始 ZIP 位于 `receive_only/.runtime/openqq-v0.5.0-win-x64.zip`，SHA-256 为 `55626197e3f0f57438e8043a709b76b0c5725aee99720af769044bdb48a12d9d`。原来的 `.runtime/windows/` 是 LLBot。两个协议端共用的接收服务位于 `http://127.0.0.1:18765/status`。

- `openqq.cmd doctor` 检测到 Node.js 22.20.0、QQNT 9.9.37-54395，并报告版本匹配和组件就绪。首次配置用 `receive_only/configure_openqq.py`，仅开启发往本机 NoneBot2 的签名 HTTP POST。业务 Bot 目录为空；没有启动旧插件。配置与本机密钥由 Git 忽略。
- 使用 `receive_only/check_offline.py` 已验证空 204 和无签名 401。另用 v0.5.0 标签的真实 HTTP 上报模块向一次性本机接收端投递模拟群消息，观测到上报成功、消息计数 1、动作计数 0。正式接收端仍是 0 条真实消息。
- Windows 受限执行环境及其中的 doctor 没看到桌面 QQ；在与实际启动相同的宿主环境中检查，发现用户已有 QQ 会话。OpenQQ 发行包要求完全退出已有 QQ 再启动。此次保留了用户的会话，尚未启动 OpenQQ 的 QQ 登录或验证真实入站。恢复前先重新检查，不依赖旧 PID 或历史进程数量。
- 用户正常退出桌面 QQ 后，在宿主环境确认接收服务可访问并从便携目录运行 `openqq.cmd`，由用户在 QQ 窗口选择账号。v0.5.0 的 HTTP POST 分支会跳过 meta_event；等待一条自然到达的群聊或私聊来验证端到端接收，空闲时计数为 0 不能用于判断登录是否成功。[上游发行包](https://github.com/feijx3/OpenQQ/releases/tag/v0.5.0) · [传输源码](https://github.com/feijx3/OpenQQ/blob/v0.5.0/src/network.mjs#L394-L397)

## 2026-11-23 的恢复点

Windows x64，Python 3.12，LLBot 8.3.2，NoneBot2 2.5.0，OneBot 适配器 2.4.6。已校验上游 Windows 包、启动本机接收服务，并通过独立的模拟群消息检查。首次实机启动停在 LLBot 项目授权，尚未生成 QQ 登录二维码或收到真实事件。后续先重新查询本机状态。

```powershell
Invoke-RestMethod -NoProxy http://127.0.0.1:18765/status
Test-Path .\receive_only\.runtime\windows\LuckyLillia.exe
(Get-Item .\receive_only\.runtime\windows\bin\llbot\data\auth_token.txt -ErrorAction SilentlyContinue).Length
```

若服务可访问，复用该进程。状态中的 `events` 包含心跳，`messages` 仅统计消息事件，两者在进程重启后清零。`last_event_utc` 是本机接收时间。计数增加可用于区分仅上线和已收到真实消息。

## 新用户接入选择（2026-11-23）

用户在 LLBot 授权入口发现新用户登录已暂停。本机此前也在项目授权检查处停止。仅有接收端通过验证。新用户恢复工作时，先看以下备选；已有有效授权或上游恢复时才继续下面的 LLBot 登录步骤。

- **保留个人 QQ 号**。NapukettoQQ 在 11 月 21 日发布了 `milestone-0.6`。上游列出 Windows x64、Node.js 24+ 和 QQ 扫码；本机 PATH 的 Node.js 为 22.20。文档中没有 LLBot 项目授权步骤，尚未实机验证新账号登录和真实消息。支持单独配置 OneBot v11 的 `httpPostUrls`，部署时只启用向本机推送事件的连接。[上游项目](https://github.com/NapukettoDev/NapukettoQQ) · [里程碑](https://github.com/NapukettoDev/NapukettoQQ/releases/tag/milestone-0.6) · [协议文档](https://github.com/NapukettoDev/NapukettoQQ/blob/milestone-0.6/docs/protocols/onebot11.md)
- **接收端兼容问题**。该里程碑的 HTTP 上报设置 `X-Self-ID` 和可选的 Bearer token；HTTP 客户端序列化 JSON 时没有添加 `X-Signature`。已在本地用合成请求直接验证当前 NoneBot 适配器的签名检查返回 401，全程无网络请求。若选此路线，可在本机单设仅接收 POST 的入口，校验独立 Bearer 后，按原始请求体计算 HMAC，再交给当前接收端。保留原有签名检查与空 204，并先离线测试正确和错误 token。该兼容入口尚未实现。[传输代码](https://github.com/NapukettoDev/NapukettoQQ/blob/milestone-0.6/packages/adapter/src/onebot11/transport.ts) · [HTTP 客户端](https://github.com/NapukettoDev/NapukettoQQ/blob/milestone-0.6/packages/network/src/http-client.ts)
- **目标群可添加官方机器人**。使用 `nonebot-adapter-qq` 对接腾讯提供的机器人身份。群主逐群开启“获取群内全部消息”，主动发言保持关闭。群内成员以 OpenID 标识。接收端要适配 QQ 官方事件，旧 OneBot 载荷和个人号的会话范围不适用。本次仅调研。[NoneBot QQ 适配器](https://github.com/nonebot/adapter-qq) · [群权限说明](https://docs.maibot.chat/manual/adapters/qq-official)

## 其他 OneBot 11 协议端（2026-11-23）

以下是公开发行情况和离线核对结果。尚未用个人 QQ 登录这些候选。历史结论按已核对的版本使用。

| 项目 | 验证结果与下次选择依据 |
|---|---|
| OpenQQ v0.5.0 | 11 月 22 日发布 Windows x64 包。上游测试构建含 9.9.37-54395，本机 QQNT 的 versions 目录也有此构建。上报带 X-Self-ID，可用 secret 生成 HMAC-SHA1 的 X-Signature，空 204 表示成功且不执行快捷操作。按文档构造模拟请求，本机适配器验签成功、解析为群消息、拒绝被改动的正文。个人号只接收优先验证此项，单开 HTTP 上报，保持业务 Bot 关闭。上游不重投失败事件。[发布包](https://github.com/feijx3/OpenQQ/releases/tag/v0.5.0) · [接入约定](https://github.com/feijx3/OpenQQ/blob/v0.5.0/docs/connect.md) |
| NegiQhook | Windows 个人号。上游记录 QQNT 9.9.36-53644 与 NoneBot2 OneBot v11 的实机验证。HTTP 上报源码确认有 X-Self-ID 和可选 HMAC-SHA1 的 X-Signature。核查日 GitHub Releases 为空，上游文档给出源码构建流程。[项目与测试环境](https://github.com/negichan/NegiQhook) · [上报实现](https://github.com/negichan/NegiQhook/blob/main/qqproto/protocols/onebot11/network/http-post.js) |
| icqq-onebot（Rust） | v0.6.15 有 Linux x64 包（6.21 MB，压缩体积），可直接运行，使用专用个人 QQ 登录，需要另有与协议版本匹配的登录签名服务。上游文档说明其消息 ID 为 base64url 字符串。已在本项目虚拟环境离线构造群消息，对照验证 OneBot 适配器 2.4.6 的 GroupMessageEvent 接受整数 ID，在传入非数字字符串时于 message_id 报 int_parsing。只收消息也需要适配，不能直接复用原上报入口。尚未验证专用号登录。[发行包](https://github.com/icqqjs/icqq-onebot/releases/tag/v0.6.15) · [登录条件](https://icqqjs.zhin.dev/rust/guide/quickstart) · [消息 ID 说明](https://icqqjs.zhin.dev/rust/guide/message-id) |
| Gensokyo-NewQQ | 将 QQ 官方机器人事件转为 OneBot v11，使用独立机器人身份。官方平台权限和群主授权决定全量群消息。配置文档提及 post_secret，但 Release015-Hotfix 中 Processor.go 的 sendPostRequest 只设置 Content-Type 和 X-Self-ID，未写 X-Signature。该版本直接上报无法通过此仓库的签名校验；也需核对网关内置指令的行为。[网关文档](https://gsk.mizuki.top/guide/overview) · [版本源码](https://github.com/Te-River/Gensokyo-NewQQ/blob/Release015-Hotfix/Processor/Processor.go#L426-L449) |

## LLBot 恢复登录（已有授权或重新开放时）

LLBot CLI 在出现二维码之前检查 `receive_only/.runtime/windows/bin/llbot/data/auth_token.txt`。首次启动报 “没有 Auth Token”。已为用户创建空文件；由用户从授权站取得凭证并在本机填写。用文件长度确认是否已填写，不要输出文件内容。[LLBot 授权站](https://auth.luckylillia.com/)

当授权文件准备好且上一次 LLBot 已退出，再从独立目录启动 CLI，用目标 QQ 账号扫码。首次尝试使用该版本提供的 headless 模式。这一步之后的实机效果仍需验证。

```powershell
Push-Location .\receive_only\.runtime\windows
try { .\LuckyLillia.exe --headless } finally { Pop-Location }
```

出现心跳时，等待下一条自然到达的群聊或私聊。比较前后的 `messages`，保持测试群和私聊静默。若项目授权失败，保留实际错误；检查授权站返回的状态即可，避免循环重启。

## 仅在缺失时重建

1. 用可写的 Python 3.12 创建仓库根目录 `.venv`，然后安装 `receive_only/requirements.txt`。原 `pyproject.toml` 配的是早期 NoneBot 和旧插件。
2. 获取 LLBot 8.3.2 的 `LuckyLillia-CLI-win-x64.zip`。本机已校验的包位于 `receive_only/.runtime/LLBot-verified.zip`，SHA-256 为 `3b29f2bdaafbbb1e0e494e42d81da7566aeb16114e9eb42a5d168c59dbcadcb7`。解压到 `receive_only/.runtime/windows/`，其中应直接包含 `LuckyLillia.exe` 和 `bin/llbot/`。[上游发行页](https://github.com/LuckyLilliaDev/LuckyLilliaBot/releases/tag/v8.3.2)
3. 在 LLBot 停止时运行下列命令。配置脚本只修改独立便携目录的默认配置和已有账号配置。保留现有签名密钥。后续恢复健康的实例时可跳过重新配置。

```powershell
.\.venv\Scripts\python.exe -m pip install -r receive_only/requirements.txt
.\.venv\Scripts\python.exe receive_only/configure.py
.\.venv\Scripts\python.exe receive_only/check_offline.py
```

当状态端点不可访问且端口空闲时，启动接收端。前台运行可在本机查看新入站事件；后台无须重定向聊天正文。随后按“恢复登录”操作。

```powershell
.\.venv\Scripts\python.exe receive_only/receiver.py
```

## 已解决的问题

| 症状 | 原因和验证过的做法 |
|---|---|
| 按 NoneBot 接入教程配置后协议不一致 | LLBot 官网的 NoneBot 教程示例选的是 Milky。本实例只启用 OneBot v11 的 `http-post`，指向 `http://127.0.0.1:18765/onebot/v11/http`，关闭 WebUI、Milky、Satori 和双向连接。[上游配置](https://luckylillia.com/guide/config) |
| 上报提示签名缺失 | 这个版本的 HTTP POST 用连接的 `token` 对原始请求体做 HMAC-SHA1，放在 `X-Signature`。NoneBot 对应参数是 `onebot_v11_secret`。独立脚本统一配置两端，本机模拟验证为无签名 401、有签名且有效 204 空响应。[上报实现](https://github.com/LuckyLilliaDev/LuckyLilliaBot/blob/v8.3.2/src/onebot11/connect/http.ts) |
| 希望确认旧命令绝不会触发 | 离线检查启动独立进程，使用一次性密钥和端口投递模拟“签到”，断言仅计数一次且响应体为空。真实接收服务的计数不受影响。只接收适配器连引用消息的自动查询也会拒绝。 |
| GitHub 整包下载中断 | 普通下载曾得到残缺 ZIP。改用 GitHub 官方 release asset API，按字节范围下载，核对每段 Content-Range，再校验整个文件的 SHA-256。已有校验通过的整包时直接复用。 |
| pip 报 No usable temporary directory，换临时目录仍然失败 | 当时 PATH 首选的 Python 来自 deepseek-harness，在安装进程里连仓库临时文件都无法创建。改用 Codex 附带的 Python 3.12 重建同一虚拟环境后，安装和 `pip check` 均成功。 |
| 接收进程已启动，本机探针报 WinError 10013 | 当时的受限执行环境阻止了回环 TCP。使用获准访问本机回环的环境运行同一离线检查后通过。先区分权限错误和端口未监听，再决定是否重装。 |

`receive_only/.runtime/` 与 `.venv/` 已被 Git 忽略。记录问题时保存版本、错误和验证结果，省略 QQ 账号、签名密钥、项目授权、二维码及真实聊天内容。
