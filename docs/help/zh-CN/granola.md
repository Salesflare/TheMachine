---
title: Granola
area: connections
summary: 你在Granola中参加的会议笔记和文字记录。它只读取。
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## 它会读取什么

你参加的会议在Granola中的笔记和文字记录：连接时读取最近7天的内容，之后有新内容时也会读取。尚未写完的笔记会在Granola完成后导入。

每条内容都会关联到日历中的对应会议，优先匹配Granola命名的会议，否则匹配时间相同的会议。Granola的笔记会放在“笔记”下，文字记录会放在“文字记录”下，并标记为**来自Granola**。你自己添加的内容会保留。

会议结束后，The Machine会读取这些内容，找出其中的承诺、决定事项或仍待完成的事项，例如“我会发送演示文稿”，并且只为明确的后续行动创建待办。会议中的参与者会通过电子邮件地址关联到你的[Graph](graph.md)。

## 它可以做什么

它不会在Granola中执行任何操作。它只读取，绝不会修改、分享或删除笔记。

## 它需要什么

Granola的个人API密钥。Granola的Business和Enterprise套餐提供API密钥。该密钥可以读取你自己的笔记，以及与你分享的笔记，与你在Granola中看到的内容一致。

## 连接

1. 在Granola桌面应用中，依次选择**设置**、**连接器**、**API密钥**。创建一个具有个人笔记访问权限的密钥，并复制它。
2. 在控制面板中，依次选择**连接**、**会议**、Granola。或者，在托管版Machine的设置页面app.themachine.computer/setup中，选择**更多来源**、Granola。在自己的电脑上，`assistant connect granola`也会提示你输入密钥。
3. 粘贴密钥，选择**工作**或**个人**，然后点击**连接**。

系统会立即验证密钥。如果Granola之后拒绝该密钥，你可以在**连接**中打开Granola并输入新密钥。

## 移除

- 在控制面板中，依次选择**连接**、打开Granola、**详情**，然后选择**断开连接**。已导入的内容会保留。
- 在托管版Machine上，也可以在设置页面中点击Granola旁边的**移除**。

## 在Granola中撤销密钥

在Granola桌面应用中，依次选择**设置**、**连接器**、**API密钥**，然后删除密钥。
