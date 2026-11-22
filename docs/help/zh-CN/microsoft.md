---
title: Microsoft Outlook和日历
area: connections
summary: 适用于Microsoft 365和Outlook.com的Outlook邮件和会议。只有在你批准后，才会发送邮件。
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: c10bf70a327b8ec0
---
## 会读取的内容

- **Outlook**：连接时读取所有邮件，之后读取最近7天的邮件以及所有新邮件。
- **Outlook日历**：读取你的会议，不会进行更改。

“其他”文件夹中的邮件和新闻邮件会先快速查看：发件人、主题和少量正文内容。遇到重要邮件时，会阅读全文，并可将其转为待办。

## 可以发送和更改的内容

- 根据待办撰写的邮件，只有在你批准后才会发送。邮件会从邮箱本身的地址发出，而不是别名地址。
- 回复会发送到所回复邮件所在的Outlook对话中。
- 回复发送后，该邮件对话中的邮件会移到Outlook的“稍后处理”文件夹几天（默认3天，除非待办另有说明），之后会回到收件箱；如果有人回复，也会提前返回。发送前，审核页面会说明这一点。

日历不会被更改。

## 同事和联系人照片

Microsoft还会被要求读取你所在组织的基本个人资料（姓名、邮箱和照片）以及你的Outlook联系人。你的Machine只会用这些资料为Graph中已有的联系人显示照片、职位和公司信息，每天最多读取200张照片。没有照片的人会在30天后重新检查。

你的组织管理员可能需要批准读取同事照片。如果未获批准，Outlook仍可连接，只是不会显示这些照片。此前已连接的账户会收到一条待办：按**重新连接**，或按**不需要**永久关闭待办。个人账户（Outlook.com、Hotmail）没有同事，因此待办只会要求读取联系人的照片。

## 连接

在托管的Machine上：

1. 打开设置页面：app.themachine.computer/setup。
2. 按**连接Microsoft**并登录。
3. 如果Microsoft要求管理员批准，请把链接（**复制链接**）发给Microsoft 365管理员。管理员批准后，组织中的所有人都可以连接。如果你是管理员，请按**我是管理员：立即批准**。

也可以在控制面板中依次打开**连接**、**邮件**，选择Outlook，然后按**使用Microsoft登录**。管理员链接就在按钮下方。

在自己的电脑上，[将电脑与账户配对](friends.md#a-machine-on-your-own-computer)后，打开**连接**，再打开**邮件**，选择Outlook，然后按**使用Microsoft登录**。邮件和日历会一起连接。完成Microsoft登录后，你会回到控制面板中的**连接**。

使用自有Microsoft Entra应用的IT团队：在此处打开**使用你自己的应用**，或运行`assistant connect outlook`。

## 移除连接

- 在托管的Machine上：在设置页面中，按账户旁边的**断开连接**。在连接页面按**断开连接 ↗**可前往该页面。
- 在自己的电脑上：打开**连接**，选择账户，再打开**详情**，然后按**断开连接**。

## 在Microsoft中卸载

Microsoft不允许我们撤销登录授权，因此还需要在Microsoft中移除：

- 工作或学校账户：myapps.microsoft.com
- 个人账户：account.live.com/consent/Manage
