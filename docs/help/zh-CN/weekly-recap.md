---
title: 每周回顾
area: weekly
summary: 每周回顾一次你的Machine的工作情况：待办、承诺、人员和项目，以及它发现的情况。默认开启。
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 223b143a6efd5692
---
## 内容

- 需要你处理：别人对你的承诺中已逾期的事项，以及你自己的逾期承诺和未来两周内到期的承诺。
- 下周安排：你的会议（准备就绪后会附上链接）、即将截止的待办，以及别人承诺下周完成的事项。
- 变化情况：与前一周相比，有多少待办值得处理；**执行**首次就正确的频率；它在你的写作方式和筛选条件上做了哪些调整；以及有多少草稿按原样发出。
- 提供给The Machine团队：如有等待你分享的心得。请参阅[与团队分享心得](share-learnings.md)。
- 人员和项目：哪些项目正在升温或降温，谁是新加入的，谁最近没有动静。
- 背后情况：本周检查了多少个信号，还有多少个仍在等待处理。
- 在[Telegram](telegram.md)上，以下情况会分别通过单独的消息征求你的选择：某个繁忙来源没有产生结果（**停止检查**或**继续检查**），以及某项待办被推迟了不止一次（**不需要**、**执行**或**保留**）。点击前不会有任何变化。

## 时间和接收方式

默认每周一次，在你所在时区的周五 16:00之后发送。你会在[Telegram](telegram.md)收到，也可以在[手机应用](phone-app.md)和控制面板应用中收到标题为“你的本周”的通知。如果在“设置 › 通知”中为**早间摘要**启用了邮件，也会通过邮件发送。使用[谨慎模式](security-levels.md)，或关闭**通知中的文本**后，就不会通过邮件发送。

## 关闭每周回顾

默认开启。你可以在“设置 › 通知”中关闭**每周回顾**开关。关闭后，它会保持关闭状态。你也可以在自己的电脑上，在config.json中设置`weekly_recap`：将`enabled`设为false，并将`chosen`设为true；还可以选择设置`weekday`（1到7，周五为5）和`at`（"16:00"）。请参阅[配置指南](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md)。
