---
title: Zoom
area: connections
summary: The Machine会总结你主持的会议并生成文字记录。它只会读取。
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
translated: 9533caa1429fb3fc
---
## 它会读取什么

你主持的每场Zoom会议的AI Companion摘要，以及Zoom提供的文字记录：连接时读取最近7天的内容，之后读取新生成的内容。它还会读取你的Zoom姓名和邮箱，以确认会议属于谁。

使用摘要需要付费Zoom套餐、在会议期间开启AI Companion，并且未启用端到端加密。

## 它会如何处理这些内容

每份摘要都会与日历中的对应会议匹配。摘要会显示在该会议的**笔记**中，文字记录会显示在**文字记录**中，并标记为**来自Zoom**，与您添加的其他内容并列。你的The Machine会根据属于你的后续步骤创建待办。只有你主动发送时，内容才会发出。

## 它能做什么

它只会读取你自己的会议。它绝不会在Zoom中创建、修改或删除任何内容。你的Zoom登录信息会保留在你的The Machine上。

## 连接

在托管的The Machine上：

1. 打开设置页面app.themachine.computer/setup，然后前往**更多来源**。
2. 打开Zoom，选择工作或个人，然后点击**连接Zoom**。
3. 登录Zoom，并授权The Machine（由Salesflare开发）。

也可以在控制面板中选择**连接**、**会议**，再选择Zoom并点击**使用Zoom登录**。完成后，你会回到控制面板。

在自己的电脑上，先[将它与你的账户配对](friends.md#a-machine-on-your-own-computer)，然后打开**连接**，再选择**会议**，选择Zoom并点击**使用Zoom登录**。

## 移除

- 在控制面板中：选择**连接**，打开Zoom，选择**详情**，然后点击**断开连接**。它会停止读取。已经导入的内容会保留。
- 在托管的The Machine上，你也可以在设置页面点击它旁边的**移除**。

## 在Zoom中卸载

登录marketplace.zoom.us，打开“管理”，再打开“已添加的应用”，然后移除The Machine。它将无法再读取任何内容。已经导入的内容会保留在你的The Machine上，直到你将其删除：请参阅[取消并删除](cancel-and-delete.md)。
