---
title: LinkedIn
area: connections
summary: 在 The Machine 自己登录的浏览器中读取你的 LinkedIn 消息。只有你批准后才会回复。
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
---
## 会读取哪些内容

你的 LinkedIn 消息。The Machine 会以你的身份登录自己的浏览器，并在你清醒时不时读取消息。它不会将任何消息标记为已读。已归档对话中的回复和消息请求也会收到，垃圾消息除外。

## 职位和公司

它还会根据你的 Connections 列表，更新 Graph 中已有联系人的职位和公司信息。它不会打开对方的个人资料，也不会添加新联系人。有人更换职位或公司时，他们的时间线会显示相关变化，例如“现任 Acme 销售主管，曾任 Acme 销售负责人”。

职位信息来自对方的个人简介标题，例如“Acme销售主管”或“销售与战略副总裁”，不会采用宣传口号。它会通过个人资料链接，或姓名和公司来识别对方。如果没有公司信息可供比对，只要 Graph 中只有一个人使用该全名，就足以识别。对方的页面还会显示你们从何时开始建立联系。

它读取得很慢：一次读取一个页面，每次间隔几分钟，每天只读取几十个页面，而且只在白天读取。大约3,000个联系人需要四天左右。如果 LinkedIn进行限制，它会停止读取，直到第二天。

## 可以发送哪些内容

可以回复消息，也可以向你指定的个人资料发送新消息，但必须先由你在待办中批准。在你批准前，它只会起草内容。

LinkedIn没有提供官方方式来实现这些操作。读取消息和偶尔发送一条你批准的消息，极不可能造成问题；批量或自动发送则可能导致账号被封禁。

## 连接

使用托管版 The Machine：

1. 打开设置页面 app.themachine.computer/setup，然后进入**更多来源**。
2. 打开 LinkedIn，按提示在 The Machine 的浏览器中登录 LinkedIn，然后点击**连接**。

在自己的电脑上使用：

1. 在控制面板中打开**连接**，再打开**聊天**，然后选择 LinkedIn。
2. 选择**工作**（及其公司）或**个人**，然后点击**连接**。
3. 点击**登录 LinkedIn**，并在 The Machine 的浏览器中登录。登录后会自动连接。

或者运行`assistant connect linkedin`。

第二个 LinkedIn 账号会使用自己的浏览器。如果 LinkedIn 将 The Machine 登出，请参阅[网站已登出](signed-out.md)。

## 如果 LinkedIn 要求输入验证码

The Machine 首次登录时，LinkedIn 通常会通过电子邮件发送验证码。在登录对话框的**验证码**栏中输入验证码，然后点击**登录**。输入时页面会保持不变。

如果 LinkedIn 返回起始页面，或两分钟内没有任何反应，请等待一分钟，然后点击**重试**。如果 LinkedIn 显示机器人验证，请在 The Machine 的浏览器中完成验证。

## 移除连接

- 在控制面板中：打开**连接**，选择 LinkedIn，再依次打开**详情**和**断开连接**。它会停止读取。已读取的内容会保留。
- 使用托管版 The Machine 时，也可以在设置页面点击它旁边的**移除**。

## 在 LinkedIn 中将其登出

在 LinkedIn 中依次打开 Settings、Sign in and security、Where you're signed in，然后将 The Machine 浏览器对应的会话登出。
