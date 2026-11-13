---
title: Proton Calendar和日历链接（ICS）
area: connections
summary: 从日历共享链接读取会议，包括Proton Calendar、已发布的日历，以及学校或体育日历。仅供读取。
covers: connector:proton_calendar, connector:ics
code: ics_feed.py, ical.py, machine/sources/calendar_setup.py
order: 15
---
## 读取内容

读取链接所指向日历中的事件，包括重复事件和时区：过去一周和未来一个月的事件，之后读取每项变更。这些事件会显示在日历和会议准备中。

链接只能读取，不能更改会议。它每隔至少15分钟检查一次链接。Proton表示，变更可能需要几小时才会同步到链接中。

## 连接Proton Calendar

Proton Calendar没有其他应用接入方式，因此需要使用共享链接。

1. 在网页上打开Proton Calendar，网址是calendar.proton.me。无法在手机应用中创建共享链接。
2. 依次打开“设置”、“所有设置”、“日历”，然后选择日历。
3. 在“与任何人共享”下，点击“创建链接”，然后选择“完整视图”。“有限视图”只会显示你何时忙碌。
4. 点击“复制链接”。
5. 在控制面板中打开**连接**，然后打开**日历**，选择**Proton Calendar**，粘贴链接并点击**连接**。

## 连接其他日历链接

选择**日历链接（ICS）**并粘贴链接。链接可以是以.ics结尾的https或webcal地址，例如iCloud公开日历、Outlook已发布的日历，或你孩子的学校日历。

## 保持链接私密

任何拥有链接的人都能读取日历。The Machine会像保管密码一样保管链接，不会将其写入日志或显示在屏幕上。要停止共享，请在创建链接的位置删除链接，然后在这里点击**断开连接**。

## 链接失效时

- **日历链接已失效**：链接已删除或更改。请创建新链接并重新连接。
- **无法连接到日历服务器**：系统会自动重试。
