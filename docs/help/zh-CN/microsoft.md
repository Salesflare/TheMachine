---
title: Microsoft Outlook和日历
area: connections
summary: 适用于Microsoft 365和Outlook.com的Outlook邮件和会议。只有在你批准后才会发送邮件。
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 7229063d9365735d
---
## 可读取的内容

- **Outlook**：所有邮件。连接时读取最近7天的邮件，之后读取所有新邮件。
- **Outlook日历**：你的会议，只读。

“其他”文件夹中的邮件和新闻邮件会先快速查看：发件人、主题和几句话。发现重要内容后，会完整读取，并可将其转为待办。

## 可发送和更改的内容

- 根据待办发送邮件，但只有在你批准后才会发送。邮件会从邮箱本身的地址发出，而不是别名地址。
- 回复会进入被回复邮件所在的Outlook对话。
- 回复发出后，该对话中的邮件会移至Outlook的“稍后处理”文件夹几天（默认3天，除非待办另有说明），之后返回收件箱；如果有人回复，也会提前返回。邮件不会在截止日期之后继续留在该文件夹中。发送前，审核页面会说明这一点。

日历不会有任何更改。

## 同事和联系人的照片

Microsoft还会被要求读取你所在组织的基本个人资料（姓名、邮箱和照片）以及你的Outlook联系人。你的Machine只会将这些资料用于显示Graph中已有人员的照片、职位和公司信息，每天最多读取200张照片。没有照片的人会在30天后再次检查。

你所在组织的管理员可能需要批准读取同事照片。如果未获批准，Outlook仍会连接，只是不会显示这些照片。之前已连接的账号会收到一个待办：点击**重新连接**，或点击**不需要**将其永久关闭。个人账号（Outlook.com、Hotmail）没有同事，因此待办只会要求读取联系人的照片。

## 连接

在托管的Machine上：

1. 打开设置页面：app.themachine.computer/setup。
2. 点击**连接Microsoft**并登录。
3. 如果Microsoft要求管理员批准，请将链接（**复制链接**）发给你的Microsoft 365管理员。管理员批准后，组织中的所有人都可以连接。如果你是管理员，点击**我是管理员：立即批准**。

也可以在控制面板中点击**连接**、**邮件**，选择Outlook，然后点击**使用Microsoft登录**。管理员链接就在按钮下方。

在自己的电脑上，先[将它与你的账号配对](friends.md#a-machine-on-your-own-computer)，然后打开**连接**，再点击**邮件**，选择Outlook并点击**使用Microsoft登录**。邮件和日历会一并连接。完成Microsoft登录后，你会返回控制面板中的**连接**页面。

如果IT团队使用自己的Microsoft Entra应用，请在此处打开**使用你自己的应用**，或运行`assistant connect outlook`。

## 移除连接

- 在托管的Machine上：在设置页面点击账号旁的**断开连接**。在“连接”页面点击**断开连接 ↗**也会带你前往该页面。
- 在自己的电脑上：点击**连接**，打开账号，选择**详情**，然后点击**断开连接**。

## 在Microsoft中卸载

Microsoft不允许我们撤销登录授权，因此还需要在Microsoft中移除：

- 工作或学校账号：myapps.microsoft.com
- 个人账号：account.live.com/consent/Manage
