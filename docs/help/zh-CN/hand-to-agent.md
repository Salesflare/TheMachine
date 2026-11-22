---
title: 转交给Claude Code或Codex
area: cards
summary: 把编码待办发送给Claude Code或Codex，结果会返回到待办中。
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 22e1b9b950988a58
---
## 转交待办

1. 在待办中打开**…**，然后选择**转交…**，再选**Codex**或**Claude Code**。这里只会显示已完成设置的工具。
2. 检查摘要和它能访问的内容，需要的话添加备注，然后点击**转交**。点击**查看完整任务**可以查看完整说明。

待办会显示任务正在处理，完成后显示结果，并提供**它做了什么**和**显示更改**。点击**要求修改**可以告诉它要改什么。点击**…**中的**转交…**可以重新开始。点击**隐藏**可以收起结果。转交一个卡住的待办后，任务运行期间会显示**正在处理…**，而不是**卡住**。

任务不会代你发送任何内容。如果任务需要你完成发布或部署步骤，点击待办中的**执行**即可运行该步骤。它写好的回复会保留为草稿，由你自行发送。

## 在Codex应用中

- 点击**在Codex中打开**，即可在Codex应用中打开该任务的对话。任务完成后，此选项才会出现。
- **要求修改**会在同一个Codex对话中继续，待办也会跟进对话内容。
- 任务在30分钟没有进展后，或运行满6小时后会停止。重启不会让任务停止。

## 设置

在**设置**的**模型**中，找到**Codex和Claude Code**：

- **Codex**：选择任务的运行位置。在你的Machine或你的电脑上运行时，这里无需填写其他内容；点击**更改**可打开设置页面。
- **Codex云端**：填写Codex提供的环境ID，也可以选择一个**分支**作为起点。
- **Claude Code**：填写Claude Code会话的链接。

Claude会通过The Machine连接器发回结果。在claude.ai中选择“设置”>“连接器”>“添加自定义连接器”，并填写会话下方显示的地址。只需添加一次。

## Codex的运行位置

如果使用托管的Machine，请在设置页面的**随时添加更多**>**Codex**中选择：

- **在你的Machine上**（默认）：点击**连接Codex**，然后输入OpenAI显示的验证码。它使用与你的模型相同的ChatGPT套餐，任务会在你的Machine上运行。无需使用终端。如果登录的是同一个ChatGPT账号，你的Machine还可以查看并使用你的用量限额重置情况。
- **其他方式**>**在我的电脑上**：任务会在你的电脑上运行，并使用已登录Codex的账号。任务会加密传输，且只会传输到这台电脑。在这台电脑上安装The Machine，在账号页面完成配对，运行`codex login`，并保持The Machine运行。结果会返回到待办中。电脑关机时，任务会等待。
- **其他方式**>**Codex云端**：任务会在OpenAI云端运行。点击**连接Codex**。它使用与你的模型相同的ChatGPT套餐，OpenAI还会要求你输入一个Codex验证码。然后在“设置”中填写Codex云端环境。

也可以从控制面板登录：**连接**>**项目与代码**>**Codex**>**获取验证码**。自托管的Machine会自行完成相同的登录流程。

托管的Machine连接GitHub或Codex后，“设置”中就会显示**Codex和Claude Code**。开发者可以查看[代理指南](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md)。
