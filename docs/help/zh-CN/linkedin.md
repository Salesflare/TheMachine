---
title: LinkedIn
area: connections
summary: 在你的Machine自己已登录的浏览器中读取你的LinkedIn消息。只有经你批准后才会回复。
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: bc67fbc21c77a97a
---
## 读取的内容

你的LinkedIn消息。你的Machine会在自己的浏览器中以你的身份登录，并在你醒着时不时读取消息。不会将任何消息标为已读。已归档对话中的回复和消息请求也会读取，垃圾消息则不会。

## 职位和公司

The Machine还会通过你的连接列表，更新Graph中已有的LinkedIn联系人的职位和公司信息。不会打开他们的个人资料，也不会添加新人。如果某人的职位或公司有变更，他们的时间线会显示变更内容，例如“现任Acme销售主管，之前是Acme销售负责人”。

职位信息取自他们的个人简介标题，例如“Acme销售主管”或“销售与战略副总裁”，不会取自标语。The Machine会通过个人资料链接，或姓名和公司来查找联系人。如果没有公司信息可供比对，只要Graph中只有一个人使用这个全名，就足以确认身份。他们的页面也会显示你们从何时开始建立连接。

读取速度很慢：一次读取一个页面，间隔几分钟，每天读取几十个页面，而且只在白天读取。约3,000个连接需要大约四天。如果LinkedIn阻止读取，The Machine会暂停，直到第二天再继续。

## 可以发送的内容

可以回复消息，也可以向你指定的个人资料发送新消息，但必须先由你在待办中批准。在你批准之前，The Machine只会起草消息。

LinkedIn没有提供官方方式来实现这些功能。读取消息和偶尔发送一条经你批准的消息不太可能造成问题；大量发送或自动发送可能会导致账号被封。

## 连接

1. 在控制面板中打开**连接**，再打开**聊天**，然后选择LinkedIn。
2. 选择**工作**（及其公司）或**个人**，然后点击**连接**。
3. 点击**登录LinkedIn**，并在你的Machine的浏览器中登录。登录后会自动连接。

如果使用托管版Machine，也可以前往app.themachine.computer/setup打开设置页面：转到**更多来源**，打开LinkedIn，按提示登录，然后点击**连接**。如果使用自己的电脑，在终端中运行`assistant connect linkedin`也能完成相同操作。

第二个LinkedIn账号会使用独立的浏览器。如果LinkedIn让你的Machine退出登录，请参阅[已退出网站](signed-out.md)。

## 如果LinkedIn要求输入验证码

你的Machine首次登录时，LinkedIn通常会通过电子邮件发送验证码。在登录对话框的**代码**下输入验证码，然后点击**登录**。输入时，页面会保持不动。

如果LinkedIn返回起始页面，或两分钟内没有任何反应，请等待一分钟，然后点击**重试**。如果LinkedIn显示机器人验证，请在你的Machine的浏览器中完成验证。

## 移除

- 在控制面板中：打开**连接**，选择LinkedIn，再打开**详情**，然后点击**断开连接**。之后将停止读取，已读取的内容会保留。
- 如果使用托管版Machine，也可以在设置页面中点击LinkedIn旁边的**移除**。

## 在LinkedIn中让它退出登录

在LinkedIn中，打开“设置”>“登录和安全”>“你登录的位置”，然后让你的Machine浏览器的会话退出登录。
