---
title: Microsoft Teams
area: connections
summary: 适用于工作或学校账号的Teams聊天、会议聊天和会议笔记。它只读取内容。
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 864f9e6e98309439
---
## 它会读取什么

Teams中的一对一聊天、群聊和会议聊天：连接时读取最近7天的内容，之后每隔几分钟读取新消息。大约一年的旧聊天记录，以及经管理员批准的频道讨论串，会稍后作为[历史记录](history.md)逐步导入，不会影响其他内容的导入。

经管理员批准后，它还会读取：

- 你所在团队中的频道讨论串。
- 你组织的会议的转录文本。
- 如果你拥有Microsoft 365 Copilot许可证，还会读取Copilot生成的会议笔记和待办。

每份转录文本或笔记都会显示在日历中对应的会议下，并标记为**来自Teams**。即使没有这些内容，会议聊天仍会保留。

机器人、应用和系统消息不会导入。

## 它能做什么

它无法在Teams中执行任何操作，只会读取内容。要回复，请点击**在Teams中打开**，打开聊天。

## 需要什么权限

Microsoft会请求允许The Machine读取你的聊天和个人资料。此操作不需要管理员批准。

读取频道、转录文本和Copilot笔记，需要你所在组织的管理员批准一次。在管理员批准之前，Teams卡片会说明暂时无法读取的内容及原因。

它仅适用于工作或学校Microsoft账号。个人账号没有可通过这种方式读取的Teams聊天。

## 连接

在托管的Machine上：

1. 在控制面板中，打开**连接**，然后为**Microsoft Teams**选择**聊天**，或为**Teams会议**选择**会议**。两者使用同一个登录方式。
2. 点击**使用Microsoft登录**并同意授权，然后返回控制面板。
3. 如需读取频道和会议笔记，请把登录页面上显示的链接发给管理员。管理员批准后，再次连接Teams。

设置过程中，设置页面上也有**连接Microsoft Teams**。

在自己的电脑上，先[将电脑与你的账号配对](friends.md#a-machine-on-your-own-computer)，然后打开**连接**，再打开**聊天**或**会议**，选择**Microsoft Teams**或**Teams会议**，并点击**使用Microsoft登录**。在这里，它会读取你的聊天和会议聊天。目前无法读取频道和会议笔记。

## 移除

在控制面板中，打开**连接**，选择Microsoft Teams，再依次点击**详情**和**断开连接**。已导入的内容会保留。

## 在Microsoft中撤销权限

打开myapps.microsoft.com并移除The Machine。如果Outlook连接的是同一个地址，也会一并断开。
