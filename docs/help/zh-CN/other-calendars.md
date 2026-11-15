---
title: iCloud和其他日历（CalDAV）
area: connections
summary: 同步iCloud日历或任何CalDAV日历中的会议，例如Fastmail、Nextcloud或Zoho。仅供读取。
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
translated: 0ff916ed2bb877e1
---
## 可读取的内容

你的会议及其参与者、会议室和备注：连接时读取过去一周和未来一个月的内容，之后同步每次更改。它们会显示在日历和会议准备中，就像Google或Outlook会议一样。系统会读取该账号中的所有日历，也可以只读取你指定的日历。

此连接仅供读取：不会添加、移动或删除会议。

## 连接iCloud日历

1. 前往[appleid.apple.com](https://appleid.apple.com)，在**登录与安全**下创建专用密码。你为iCloud Mail创建的专用密码也可以使用。
2. 在控制面板中打开**连接**，然后打开**日历**，选择**iCloud日历**。
3. 输入你的Apple ID和专用密码，然后点击**连接**。

## 连接其他日历

1. 打开**连接**，然后打开**日历**，选择**其他日历**。
2. 输入你的邮箱地址和密码。许多服务提供商要求在此处使用应用专用密码，你可以在账号设置中创建。
3. 点击**连接**。

系统会自动查找Fastmail、Yahoo、Zoho以及会公布服务器地址的服务器。找不到你的服务器？打开**服务器设置**，输入它的CalDAV地址，例如`nextcloud.example.com/remote.php/dav`。启用**仅此日历**后，系统只会读取指定名称的日历。

要连接Google或Microsoft日历？请选择**Google日历**或**Outlook日历**。

## 连接停止时

- **日历服务器拒绝了密码**：你更改了密码，或者应用专用密码已被移除。请使用新密码重新连接。
- **无法连接到日历服务器**：系统会自动重试。如果持续失败，请检查服务器设置中的地址。

## 移除连接

打开**连接**，选择日历，再依次点击**详情**和**断开连接**。已同步的内容会保留。也请在服务提供商处移除应用专用密码。
