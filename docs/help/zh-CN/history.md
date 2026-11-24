---
title: 历史记录
area: connections
summary: 可搜索、阅读约一年前的旧邮件、会议记录，以及WhatsApp、Slack和Teams消息，了解身边的人。绝不创建待办。
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 2b5e84c61892c8e4
---
## 会保留哪些内容

你的Machine会导入约一年前的旧邮件、会议记录，以及WhatsApp、Slack和Teams消息。搜索可以找到这些内容，也可以按含义搜索；对话中会显示这些内容，[日历](calendar.md)会显示过去的会议。

**连接**中的每个连接都会说明能追溯到多早，例如**历史记录：追溯至**2025年11月。

## 对你的Graph有什么帮助

你的[Graph](graph.md)会记录这些信息：你和他人的关系有多近、上次联系是什么时候、谁认识谁，以及相关的人和组织。个人或组织的时间线也会显示这些信息，让你随时查看最近联系时间。Fleet中“谁认识某人”的回答会参考工作账号中的这些信息，遵循与新邮件相同的[共享规则](sharing-rules.md)。

## 绝不会做什么

这些历史记录绝不会创建待办或承诺，不会算作新内容，不会启动检查，也不会添加到项目中。个人历史会一直保持私密，就像个人邮件一样。

除按含义搜索外，你的AI模型只会在以下三种情况下读取这些记录：

- 搜索找到的内容，例如你提问时找到的内容，或处理待办时找到的内容
- 包含预订详情的邮件，用于[旅行和活动](calendar.md#trips-and-events)
- [会议前准备](calendar.md#ready-for-your-meetings)：之前会议的笔记，以及与你要见面的人有关的几条旧消息

## 什么时候运行

它会在首次查看消息后开始运行。每个连接都要等首周数据同步完成后才会开始，包括之后添加的连接。它会在后台缓慢运行；检查或同步正在运行、服务要求降低速度，或你的Machine空间不足时，会暂停。新消息始终优先处理。

邮箱历史记录导入完成后，你的Machine会再次读取保留的邮件，查找预订和票务详情，这样旧预订也会显示在[旅行和活动](calendar.md#trips-and-events)中。读取速度同样缓慢，也会因相同原因暂停。

它使用每个连接已有的访问权限，无需额外批准。

## 追溯范围

约一年。在你自己的电脑上，可以通过设置文件中的`history_days`更改此范围（0表示关闭，最多730天）。Telegram和其他来源不会导入更早的历史记录。

LinkedIn和X消息会追溯90天，读取速度非常慢：每小时少量读取几次，只在白天进行；如果网站限制访问，就会暂停一天，以保障账号安全（`social_history_days`，0表示关闭）。
