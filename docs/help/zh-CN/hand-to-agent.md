---
title: 转交给Claude Code或Codex
area: cards
summary: 把编程待办发送给Claude Code或Codex，结果会显示在待办中。
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
---
## 转交待办

1. 在待办中打开**…**，然后选择**转交…**，再选**Codex**或**Claude Code**。这里只会显示你已设置好的工具。
2. 检查摘要和将提供给工具的内容，你也可以添加备注，然后点击**转交**。点击**查看完整任务**可查看完整说明。

待办会显示任务正在运行，完成后会显示结果，以及**执行内容**和**显示更改**。点击**要求修改**可告诉工具要改什么。点击**…**中的**转交…**可重新开始。点击**隐藏**可收起结果。转交一个卡住的待办后，任务运行期间会显示**正在运行…**，而不是**已卡住**。

任务不会替你发送任何内容。如果任务需要你完成发布或部署步骤，点击待办中的**执行**即可运行该步骤。任务写好的回复会保留为草稿，由你自行发送。

## 在Codex应用中

- 任务完成后，点击**在Codex中打开**，即可在Codex应用中打开该任务的对话。
- 点击**要求修改**，可在同一个Codex对话中继续处理，待办也会同步更新。
- 如果任务30分钟没有进展，或总运行时间达到6小时，就会停止。重启不会让它停止。

## 设置

在**设置**的**模型**中，找到**Codex和Claude Code**：

- **Codex**：选择运行位置。在你的Machine或你的电脑上运行，无需在此处进行其他设置；点击**更改**可打开设置页面。
- **Codex云端**：填写Codex提供的环境ID，也可以选择要从哪个**分支**开始。
- **Claude Code**：填写Claude Code会话链接。

Claude会通过The Machine连接器返回结果。在claude.ai中选择Settings、Connectors、Add custom connector，然后填写会话下方显示的地址，只需添加一次。

## Codex的运行位置

如果使用托管版Machine，请在设置页面的**随时添加更多**下选择**Codex**：

- **在你的Machine上**（默认）：点击**连接Codex**，然后输入它在OpenAI页面显示的代码。它和你的模型使用同一个ChatGPT套餐，任务会在你的Machine上运行。无需使用终端。
- **其他方式**，**在我的电脑上**：任务会在你的电脑上运行，使用已在该电脑上登录的Codex。任务会加密传输，且仅适用于这台电脑。在电脑上安装The Machine，在账户页面完成配对，运行`codex login`，并让The Machine保持运行。结果会返回到待办中。电脑关机时，任务会等待。
- **其他方式**，**Codex云端**：任务会在OpenAI云端运行。点击**连接Codex**。它和你的模型使用同一个ChatGPT套餐，OpenAI还会要求你输入另一个代码，用于Codex。然后在设置中填写Codex云端环境。

你也可以从控制面板登录：**连接**、**项目和代码**、**Codex**、**获取代码**。自托管的Machine会自行完成同样的登录。

托管版Machine连接GitHub或Codex后，设置中会显示**Codex和Claude Code**。开发者请查看[代理指南](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md)。
