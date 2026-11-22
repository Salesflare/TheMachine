---
title: 分享规则
area: fleet
summary: 按Fleet和问题类型设置Machine可以回答什么。选择先问我、始终或从不，还可以设置是否分享姓名。
covers:
code: fleet.py, dashboard.html
order: 2
keywords: share, sharing, colleagues, teammates, team, what others see, answer for me
translated: 1ae445260f88518d
---
## 设置规则

决定你的Machine要告诉Fleet什么。在**Fleet**标签页中，打开**分享**。每种问题都有一条规则：

- **先问我**：每次有人提问，你都会看到并决定是否回答。
- **始终**：你的Machine会自动回答。
- **从不**：你的Machine会拒绝回答。
- **名称**：设置回答中是否可以提及具体的人，例如访客的姓名，或是否省略姓名。

Machine绝不会分享邮件内容或会议主题。使用**对某个人来说不一样？添加例外**，可以为某个人设置不同的规则。

规则只能在控制面板中更改，不能通过消息更改。

## 在工作Fleet中

在标准工作Fleet中，关于谁认识某人、会议背景以及谁处理共享邮件的问题，规则只有**始终**和**从不**。选择**始终**后，Machine只会根据[Team Graph](team-graph.md)已与团队分享的信息作答，也只会提及已分享信息中的人。保存为**先问我**的规则会按**始终**处理。

如果Team Graph尚未开始分享，关于谁认识某人和会议背景的问题也可以选择**先问我**。谨慎Fleet也一样。请参阅[Fleet](fleet.md#answered-by-itself-in-a-work-fleet)。

## 有人首次提问时

需要你决定的问题会以待办的形式显示，你可以选择**分享一次**、**始终分享**、**拒绝**或**绝不分享**。
