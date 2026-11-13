---
title: 共享规则
area: fleet
summary: 每个Fleet、每类问题都有对应规则，决定The Machine可以回答什么。可选先问我、始终、从不或仅限名称。
covers: 
code: fleet.py, dashboard.html
order: 2
keywords: share, sharing, colleagues, teammates, team, what others see, answer for me
---
## 设置规则

决定The Machine可以告诉Fleet什么。在**Fleet**标签页中，打开**分享**。每类问题都有一条规则：

- **先问我**：每次有问题时，你都会看到并决定。
- **始终**：The Machine会自行回答。
- **从不**：The Machine会拒绝回答。
- **名称**：决定回答能否透露是谁，例如访客的姓名，还是要隐去姓名。

The Machine绝不会分享电子邮件内容或会议主题。**对某个人来说不一样？添加例外**可为某个人设置规则。

规则只能在控制面板中更改，不能通过消息更改。

## 在Work Fleet中

在Standard Work Fleet中，对于谁认识某人、会议背景以及谁负责处理共享邮件，只能选择**始终**或**从不**。选择**始终**时，回答只会包含[团队Graph](team-graph.md)已与团队共享的内容，也只会提及已共享的人员。如果保存的规则是**先问我**，则会按**始终**处理。

在团队Graph尚未开始共享时，对于谁认识某人和会议背景，仍可选择**先问我**；Careful Fleet也一样。请参阅[Fleets](fleet.md#answered-by-itself-in-a-work-fleet)。

## 有人首次提问时

需要你处理的问题会作为待办发给你，你可以选择**分享一次**、**始终共享**、**拒绝**或**绝不分享**。
