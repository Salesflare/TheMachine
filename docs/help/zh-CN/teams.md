---
title: Microsoft Teams
area: connections
summary: 适用于工作或学校帐户的 Teams 聊天、会议聊天和会议记录。只有你批准后才会回复。
covers: connector:teams
code: connectors/teams.py, teams_send.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 9ca0bb08466b4d58
---
## 读取的内容

连接时读取 Teams 中你的一对一、群组和会议聊天，范围为最近 7 天；之后每隔几分钟读取新消息。约一年的较早聊天记录，以及经管理员同意后读取的频道帖子，会稍后分批作为[历史记录](history.md)导入，不会影响其他内容的同步。

经管理员同意后，还会读取：

- 你所在团队的频道帖子。
- 你组织的会议的会议转录。
- 你拥有 Microsoft 365 Copilot 许可证时，Copilot 生成的会议记录和待办事项。

每份转录或会议记录都会显示在 Calendar 中对应的会议下，并标记为**来自Teams**。即使没有这些内容，会议聊天仍会保留。

不会读取机器人、应用和系统消息。

## 可以做什么

在待办事项来源的一对一、群组或会议聊天中回复。The Machine 会起草回复；只有你审核并按下**立即发送**后，才会以你的身份在该聊天中发送。它不会发起新聊天。

它不会在频道中发帖。要回复频道帖子，请使用**在Teams中打开**打开该帖子。

## 需要哪些权限

Microsoft 会请求允许 The Machine 读取你的聊天和个人资料，并以你的身份发送聊天消息。这不需要管理员批准。

如果你在 The Machine 获得发送权限之前就连接了 Teams，Teams 卡片会提示你**重新连接**以发送回复。按下**重新连接**并再次授权。在此之前，草稿会保留，你可以在 Teams 中发送。

频道、会议转录和 Copilot 会议记录需要组织管理员批准一次。获批前，Teams 卡片会说明目前无法读取的内容及原因。

此功能仅适用于工作或学校 Microsoft 帐户。个人帐户没有可通过这种方式读取的 Teams 聊天。

## 连接

在托管版 Machine 上：

1. 在控制面板中打开**连接**，然后为 **Microsoft Teams** 选择**聊天**，或为 **Teams会议**选择**会议**。两者使用相同的登录方式。
2. 按下**使用 Microsoft 登录**并授权。之后会返回控制面板。
3. 如需启用频道和会议记录，请把登录页面显示的链接发给管理员。管理员批准后，再次连接 Teams。

设置过程中，设置页面也会显示**连接 Microsoft Teams**。

在自己的电脑上，先[将 Machine 与你的帐户配对](friends.md#a-machine-on-your-own-computer)，然后打开**连接**，再选择**聊天**或**会议**，选 **Microsoft Teams** 或 **Teams会议**，并按下**使用 Microsoft 登录**。在这里，The Machine 会读取你的聊天和会议聊天。目前无法读取频道和会议记录。

## 移除连接

在控制面板中打开**连接**，选择 Microsoft Teams，再选择**详情**，然后选择**断开连接**。已导入的内容会保留。

## 在 Microsoft 中撤销权限

打开 myapps.microsoft.com 并移除 The Machine。如果 Outlook 使用同一地址连接，也会一并断开。
