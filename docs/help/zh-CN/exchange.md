---
title: Exchange Server
area: connections
summary: 查看公司运行的Exchange Server（2013至2019版或Subscription Edition）中的会议。只读。
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## 读取的内容

连接时可读取过去一周和接下来一个月的会议，以及会议的参与者、会议室和备注；之后的每项更改也会同步。会议会显示在日历和会议准备中。

这是只读连接，不会添加、移动或删除会议。目前还不会读取Exchange Server中的邮件。

## Microsoft 365还是Exchange Server？

Exchange Server由你的公司自行运行。Microsoft 365（Exchange Online）是Microsoft的云服务，请改选**Outlook日历**。如果系统发现你的邮箱地址属于Microsoft 365，表单会提示你。

## 连接

1. 在仪表板中打开**连接**，再打开**日历**，然后选择**Exchange Server**。
2. 填写你的工作邮箱地址和Windows密码。
3. 点击**连接**。

系统会根据你的邮箱地址查找服务器（Autodiscover）。如果找不到，请打开**服务器设置**，输入IT团队提供的Outlook服务器地址，例如`mail.example.com`。如果登录名与你的邮箱地址不同，请在**用户名**下输入登录名`DOMAIN\name`。

仅通过https使用NTLM或Basic进行登录。

## 连接中断时

- **日历服务器拒绝了密码**：你的Windows密码已更改。请重新连接。
- **Microsoft 365邮箱**：你的邮箱已迁移到Microsoft 365。请断开此连接，然后连接**Outlook日历**。
- **无法连接到日历服务器**：系统会自动重试。有些服务器只能通过公司网络或VPN访问。

## 移除连接

打开**连接**，再打开日历，选择**详情**，然后点击**断开连接**。已导入的内容会保留。
