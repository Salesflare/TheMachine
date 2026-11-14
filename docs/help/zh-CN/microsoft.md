---
title: Microsoft Outlook和日历
area: connections
summary: 适用于Microsoft 365和Outlook.com的Outlook邮件和会议。只有你批准后才会发送邮件。
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 41c9c0174a2a21c7
---
## 会读取哪些内容

- **Outlook**：你所有的邮件。连接时读取最近7天的邮件，之后读取所有新邮件。
- **Outlook日历**：你的会议，只读。

“其他”文件夹中的邮件和新闻简报会先快速浏览：发件人、主题和几句话。发现重要内容后，才会完整阅读，也可以将其变成待办。

## 可以发送和更改哪些内容

- 根据待办发送邮件，但只有你批准后才会发送。邮件会从邮箱自己的地址发出，不会使用别名。
- 回复会加入被回复邮件所在的Outlook会话。
- 如果你将与邮件相关的待办稍后处理，该邮件会话中的邮件会移到Outlook的“稍后处理”文件夹，并在待办重新出现时移回来。

日历不会被更改。

## 同事和联系人的照片

我们还会请求Microsoft读取你所在组织的基本个人资料（姓名、邮箱和照片）以及你的Outlook联系人。你的Machine只会将这些资料用于显示Graph中已有联系人的照片、职位和公司信息，每天最多读取200张照片。没有照片的人会在30天后再次检查。

你所在组织的管理员可能需要批准读取同事照片。如果未获批准，Outlook仍可连接，只是不会显示这些照片。此前已连接的账户会收到一个待办：按**重新连接**，或按**不需要**永久关闭此待办。个人账户（Outlook.com、Hotmail）没有同事，因此相关待办只会询问是否读取联系人的照片。

## 连接

在托管的Machine上：

1. 前往app.themachine.computer/setup打开设置页面。
2. 按**连接Microsoft**并登录。
3. 如果Microsoft要求管理员批准，请把链接发给Microsoft 365管理员（**复制链接**）。管理员批准后，组织中的所有人都可以连接。如果你是管理员，按**我是管理员：立即批准**。

也可以在控制面板中依次打开**连接**、**邮件**，选择Outlook，然后按**使用Microsoft登录**。管理员链接就在按钮下方。

在自己的电脑上，先[将电脑与你的账户配对](friends.md#a-machine-on-your-own-computer)，然后打开**连接**，再打开**邮件**，选择Outlook并按**使用Microsoft登录**。邮件和日历会一起连接。完成Microsoft登录后，你会返回控制面板中的**连接**页面。

使用自有Microsoft Entra应用的IT团队：在该页面打开**使用自己的应用**，或运行`assistant connect outlook`。

## 移除连接

- 在托管的Machine上：在设置页面的账户旁按**断开连接**。在“连接”页面按**断开连接↗**即可前往设置页面。
- 在自己的电脑上：打开**连接**，选择账户，再依次打开**详情**和**断开连接**。

## 在Microsoft中卸载

Microsoft不允许我们撤销登录，因此也要在Microsoft中移除应用：

- 工作或学校账户：myapps.microsoft.com
- 个人账户：account.live.com/consent/Manage
