---
title: Exchange Server
area: connections
summary: 公司运行的 Exchange Server（2013 至 2019 或订阅版）中的会议。只读。
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: f2b98c9bd4f08dba
---
## 会读取哪些内容

连接时会同步过去一周和接下来一个月的会议，以及与会者、会议室和备注；之后同步每次更改。会议会显示在日历和会议准备中。

它是只读的，不会添加、移动或删除会议。暂不读取 Exchange Server 中的邮件。

## Microsoft 365 还是 Exchange Server？

Exchange Server 由公司运行。Microsoft 365（Exchange Online）是 Microsoft 的云服务，请改选 **Outlook日历**。

先输入邮箱地址。如果邮箱属于 Microsoft 365，表单会显示这一点，并显示 **使用 Microsoft 登录**，而不是密码输入框。点击后会打开 Outlook日历登录页面，无需密码。如果几秒后仍未检测到，或者公司运行自己的服务器，密码表单会保留。

## 连接

1. 在控制面板中，打开 **连接**，然后选择 **日历**，再选 **Exchange Server**。
2. 填写工作邮箱地址和 Windows 密码。
3. 点击 **连接**。

系统会根据邮箱地址查找服务器（Autodiscover）。如果找不到，请打开 **服务器设置**，填写 IT 团队提供的 Outlook 服务器地址，例如 `mail.example.com`。如果登录名与邮箱地址不同，请在 **用户名** 下填写 `DOMAIN\name`。

仅通过 https 使用 NTLM 或 Basic 登录。

## 无法连接时

- **日历服务器拒绝了密码**：Windows 密码已更改。请重新连接。
- **Microsoft 365 邮箱**：邮箱已迁移到 Microsoft 365。请断开此连接，再连接 **Outlook日历**。
- **无法连接到日历服务器**：系统会自动重试。有些服务器只能通过公司网络或 VPN 访问。

## 移除

打开 **连接**，选择日历，然后依次点击 **详情**和 **断开连接**。已同步的内容会保留。
