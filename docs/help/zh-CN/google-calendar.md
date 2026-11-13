---
title: Google日历
area: connections
summary: 查看会议，提前做好准备并跟进。只有你点按后才会有更改。
covers: connector:calendar
code: onboarding.py, google_api.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google
order: 11
---
## 它会读取什么

过去7天到未来30天的日程，包括重复事件。日程会显示在[日历](calendar.md)标签页中，帮助你处理与会议相关的待办。

## 它能做什么

它不会自行执行任何操作。它不会回复邀请，也只会邀请你亲自列出的人。

如果登录时授予了日历写入权限，你可以在自己的日历或你有权编辑的共享日历中添加、更改或删除不含受邀人的事件。每次更改都需要你点按确认：在[日历](calendar.md)中，或在提供此选项的待办中。通过**连接Google**登录时，只能读取日历。

你也可以通过[日历](calendar.md)中的表单，在自己的日历上邀请他人。按钮会显示受邀人数，点按后Google会发送邀请。待办不会邀请任何人。

## 连接

在托管版The Machine上，它会与Gmail一起连接：前往设置页面，在**邮件和日历**下点按**连接Google**。

在自己的电脑上，完成[与账号配对](friends.md#a-machine-on-your-own-computer)后，打开**连接**，然后打开**日历**，选择Google日历，再点按**通过Google登录**。它会与Gmail一起连接。

使用自己的应用时，运行`assistant connect calendar`，或在那里打开**使用自己的应用**。系统会询问要读取哪个日历。

## 移除连接

- 在托管版The Machine上：前往设置页面，点按地址旁边的**断开连接**。这会移除该地址对应的Gmail和日历连接。
- 在自己的电脑上：打开**连接**，选择日历，再点按**详情**，然后点按**断开连接**。

## 在Google中卸载

在Google账号中打开“安全性”，然后打开“你与第三方应用和服务的连接”，并移除该应用。另请参阅[Gmail](gmail.md)。
