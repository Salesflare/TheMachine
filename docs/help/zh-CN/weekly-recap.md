---
title: 每周回顾
area: weekly
summary: 每周了解一次 The Machine 的表现：待办、承诺、联系人和项目，以及它注意到的情况。默认开启。
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
---
## 包含哪些内容

- 你和 The Machine 共度的一周，以及值得处理的待办数量与前一周相比如何。
- 待办：新增、已完成、已忽略和已推迟的待办，以及你回复得有多快。
- 承诺：你已兑现和待兑现的承诺，以及别人已兑现或仍在等待的承诺。
- 如果有心得等待你分享给 The Machine 团队，也会列出来。请参阅[与团队分享心得](share-learnings.md)。
- 联系人和项目，例如哪些人最近没什么动静。
- 我注意到的情况：草稿未经修改或经过修改后发出、几分钟内忽略的待办，以及被推迟不止一次的待办。
- 背后情况：本周检查了多少个信号，还有多少个仍在等待处理。
- 回顾结束后，每项选择会单独发一条消息：一个繁忙但没有结果的信息来源（**停止检查**或**继续检查**），以及被推迟不止一次的待办（**不需要**、**执行**或**保留**）。点按前不会有任何更改。

## 何时以及在哪里

默认情况下，每周五在你所在时区的16:00之后发送。你可以在[Telegram](telegram.md)中查看，也可以在[手机应用](phone-app.md)和仪表盘应用中收到标题为“你的一周”的通知。如果在“设置”›“通知”中为**早间摘要**开启了电子邮件，也会通过电子邮件发送。使用[谨慎](security-levels.md)级别时，不会通过电子邮件发送。

## 关闭每周回顾

默认开启。你可以在“设置”›“通知”中关闭**每周回顾**开关。关闭后，它会一直保持关闭状态。在自己的电脑上，你也可以在config.json中设置`weekly_recap`：将`enabled`设为 false，并将`chosen`设为 true；还可以设置`weekday`（1到7，周五为5）和`at`（"16:00"）。请参阅[配置指南](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md)。
