---
title: Intercom
area: connections
summary: 在你的Intercom工作区查看客户对话。只有你发送后，它才会以你的名义回复。
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 5a6938dd6c220a43
---
## 它会读取哪些内容

连接时，它会读取你的Intercom工作区中最近7天的客户对话，之后也会读取新收到的对话。它还会读取登录信息对应的工作区和队友。

## 它能做什么

使用你自己的**使用Intercom登录**后，它可以在对话中以你的名义回复，但只有在你点击**发送**发送那条具体内容后才会发送。它不会分配、关闭对话、添加标签或写备注。通过你的Fleet与你共享的Intercom只能读取内容。

## Intercom待办

Intercom待办会显示客户信息，点击**阅读消息**会打开对话，并附上该对话在Intercom中的链接。每条消息下方都会标明发送者：客户在一侧，你的团队及其机器人在另一侧。即使是队友或营销活动发起的对话，也会这样显示。回复会发送到该对话中，除非你选择通过电子邮件发送。

只有分配给你或尚未分配给任何人的对话才会变成待办。队友在Intercom中接手待办后，待办会自动关闭，并提供**撤销**。对于与你共享的Intercom，你写下的对话是分配给你代为回复的队友的对话。

如果有人在Intercom中关闭了对话，待办也会自动关闭。如果待办只要求回复，而有人已经回复，且客户之后没有再发消息，待办也会自动关闭。即使你在待办出现前、The Machine读取你的回复之前就已经回复，也同样适用。备注、稍后处理或机器人的回复都不算。

如果你的Machine无法在Intercom中回复（例如，共享给你的Intercom只能读取、未启用回复功能或尚未连接），草稿会改为通过电子邮件发送。待办会说明原因，并询问你是否要**改用电子邮件发送？**要在Intercom中回复，请点击待办上的**连接你自己的Intercom**并登录。随后，待办会重新写成一条Intercom回复。你发送之前，不会有任何内容发出。

如果你自己的Intercom和与你共享的Intercom属于同一工作区，它们不会同时读取：共享的连接会暂停，其对话会转到你自己的连接中，每条只转一次。

## 连接

1. 在控制面板中，依次点击**连接**、**客户**、Intercom。或者，在托管式Machine的设置页面app.themachine.computer/setup中，点击**更多来源**、Intercom。在自己的电脑上使用时，请先将它与你的账号配对。
2. 点击**使用Intercom登录**。
3. 在Intercom中批准The Machine（由Salesflare开发）。随后会返回你刚才所在的位置。

登录另一个工作区会添加第二个Intercom账号。

Intercom始终会被视为工作内容，归属取决于其工作区名称所指的公司。

## 移除连接

- 在控制面板中，点击**连接**，打开Intercom，点击**详情**，再点击**断开连接**。它会停止读取。已经导入的内容会保留。
- 在托管式Machine上，也可以在设置页面中点击它旁边的**移除**。

## 在Intercom中卸载

在Intercom中，依次打开“设置”、“应用”、“已安装的应用”，然后移除The Machine。
