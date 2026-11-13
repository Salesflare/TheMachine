---
title: 历史记录
area: connections
summary: 约一年的旧邮件、会议，以及WhatsApp、Slack和Teams消息，可供搜索、阅读和了解相关联系人。绝不会变成待办。
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
---
## 保存的内容

The Machine会导入约一年的旧邮件、会议，以及WhatsApp、Slack和Teams消息。你可以搜索这些内容，也可以按含义搜索；对话串会显示这些内容，[日历](calendar.md)会显示过去的会议。

**连接**中的每个连接都会说明数据可追溯到多久以前，例如**历史记录：追溯至**2025年11月。

## 添加到Graph的内容

你的[Graph](graph.md)会统计这些信息：你和他人有多亲近、上次交谈的时间、谁认识谁，以及相关的人和组织。个人或组织的时间线也会显示这些信息，因此始终能看到上次联系的时间。你的Fleet会根据工作账户中的这些信息回答“谁认识某人”，并遵循与新邮件相同的[共享规则](sharing-rules.md)。

## 绝不会做的事

它绝不会创建待办或承诺，也不会将内容计为新消息、启动检查或添加到项目中。个人历史记录会像个人邮件一样保持私密。除了按含义搜索时，不会有AI模型读取这些内容。

## 运行时间

首次查看消息后，历史记录导入就会开始。对于每个连接，只有在首次使用满一周后才会开始导入，之后添加的连接也一样。导入会在后台慢慢进行；检查或同步运行、服务要求降低速度，或The Machine空间不足时，导入会暂停。新消息始终优先处理。

导入会使用每个连接已有的访问权限，无需额外批准。

## 追溯范围

约一年。在你自己的电脑上，可以修改设置文件中的`history_days`来调整范围（0表示关闭，最多730）。Telegram和其他来源不会导入更早的历史记录。

LinkedIn和X消息会追溯90天，读取速度非常慢：每小时少量读取，只在白天读取；如果网站限制访问，则会暂停一天，以确保账户安全（`social_history_days`，0表示关闭）。
