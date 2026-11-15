---
title: Intercom
area: connections
summary: 你在Intercom工作区中的客户对话。只有你发送后，它才会以你的身份回复。
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 2cbee87e6d24c0a9
---
## 它会读取什么

你在Intercom工作区中的客户对话：连接时读取最近7天的对话，之后读取新收到的对话。它还会读取登录账号所属的工作区和队友。

## 它能做什么

使用你自己的**使用Intercom登录**后，它可以在对话中以你的身份回复，但只有你点击该条内容旁的**发送**后才会发送。它绝不会分配、关闭或添加标签，也不会写备注。通过你的Fleet与你共享的Intercom只会读取内容。

## Intercom生成的待办

Intercom生成的待办会显示客户信息。点击**阅读消息**会打开对话，并附上该对话在Intercom中的链接。回复会发送到该对话中，除非你要求通过邮件发送。

只有分配给你的对话，或尚未分配给任何人的对话，才会生成待办。队友在Intercom中接手对话后，对应待办会自动关闭，并显示**撤销**。在与你共享的Intercom中，分配给你所使用身份对应队友的对话才算是你的对话。

如果团队成员在Intercom中关闭了对话，待办也会自动关闭。如果待办只要求回复，而有人已回复且客户之后没有再发消息，待办也会自动关闭。即使你在待办出现前、The Machine读取到你的回复前就已回复，也会算作已回复。备注、稍后处理或机器人回复都不算。

如果你的Machine无法在Intercom中回复（与你共享的Intercom仅供读取、未启用回复功能，或尚未连接），草稿就会改为通过邮件发送。待办会说明原因，并询问**改为通过邮件发送？**要在Intercom中回复，请点击待办中的**连接你自己的Intercom**并登录。随后，待办会重新生成，作为Intercom中的回复。你发送之前，内容不会发出。

如果你自己的Intercom和与你共享的Intercom属于同一工作区，两者不会同时读取：共享的连接会暂停读取，对话会转到你自己的连接中，每条只转一次。

## 连接

1. 在控制面板中依次点击：**连接**、**客户**、Intercom。或者，在托管版Machine的设置页面app.themachine.computer/setup中依次点击：**更多来源**、Intercom。在自己的电脑上使用时，请先将Machine与你的账号配对。
2. 点击**使用Intercom登录**。
3. 在Intercom中授权The Machine（由Salesflare开发）。之后你会返回原页面。

登录其他工作区会添加第二个Intercom账号。

Intercom始终会被视为工作用途，归属以其工作区名称为准。

## 移除连接

- 在控制面板中依次点击：**连接**，打开Intercom，点击**详情**，然后点击**断开连接**。此后它会停止读取，已导入的内容会保留。
- 在托管版Machine的设置页面中，也可以点击Intercom旁边的**移除**。

## 在Intercom中卸载

在Intercom中依次打开设置、应用、已安装的应用，然后移除The Machine。
