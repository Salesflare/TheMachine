---
title: 在自己的电脑上运行
area: getting-started
summary: 在Linux、macOS或Windows上安装这款开源应用。免费使用，模型和数据都由你掌控。
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
在自己的电脑上免费运行The Machine。它采用开源协议（AGPL），你的数据也会留在自己手中。安装需要使用终端，连接账号则不需要。

## 运行要求

- 安装OpenClaw 2026.11.2或更高版本。The Machine基于这款开源智能体运行，安装程序会提示你安装它。
- Python 3.12或更高版本，以及Node.js 24（24.22.1或更高版本）或26.12.1或更高版本，不能使用25。
- Tailscale，用来在手机上访问你的控制面板。
- 普通用户账号，不能是root账号。

## 安装

在Linux或macOS上（macOS版本仍处于Beta阶段）：

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

在Windows上（Beta版），应用会在WSL2中运行。在PowerShell中运行`irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`。它会安装配置WSL2和Ubuntu，并准备好应用所需的一切，然后运行`./install.sh`。

安装程序会找到你的账号，逐个连接，并在启用任何功能前显示上周的预览。

## 安装后

- 连接邮箱：在**待办**顶部，点击**Gmail**（或**Outlook**），再点击**配对这台Machine**，将它与账号配对。如果没有账号，下面会显示**使用自己的应用**。
- 然后点击**使用Google登录**（使用Outlook时，点击**使用Microsoft登录**）。邮箱和日历会一起连接。
- 连接其他来源：点击**连接**，再选择来源类型。要使用自己的Google客户端或Entra应用，请在终端中运行`assistant connect`。
- 运行`assistant doctor`检查所有问题。它会为每个问题提供修复方法。
- 安装程序会安装最新的签名版本，后续更新也会以签名版本的形式发布。
- 与账号配对后，登录手机应用即可打开它。取消配对会移除该关联。

完整指南请查看代码仓库：[入门指南](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md)。
