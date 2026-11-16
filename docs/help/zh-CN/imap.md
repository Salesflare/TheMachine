---
title: 其他邮箱（IMAP）
area: connections
summary: 通过 IMAP 收取任意服务商的邮件，例如 iCloud、Yahoo、Fastmail、Telenet，或你自己的域名邮箱。
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
translated: a21e9d52d723f351
---
## 会读取哪些内容

你的收件箱和已发送文件夹：连接时读取最近 7 天的邮件，之后读取所有新邮件。你发送的邮件也会计入，因此它能了解你的写作方式和你做出的承诺。不会读取其他文件夹。

除了 The Machine 发送的邮件副本会存入已发送文件夹，你的邮箱不会有任何更改。邮件不会被标记为已读。

## 可以做什么

只有在你按下**发送**后，它才会通过服务商的邮件服务器（SMTP）发送邮件，并使用同一个密码。邮件副本会存入已发送文件夹。回复会保留在原邮件会话中。签名会使用你在设置中设置的签名；如果没有设置，则使用你已发送邮件末尾的签名。

## 连接邮箱

1. 在控制台中打开**连接**，再打开**邮件**，然后选择**其他邮箱**。
2. 输入你的邮箱地址和密码。
3. 按下**连接**。

许多服务商要求邮件应用使用专用应用密码，而不是你的常用密码。请在服务商的账户设置中创建应用密码：

- iCloud：在 account.apple.com 创建专用应用密码。
- Yahoo：前往 Account security，选择 Generate app password。
- Fastmail：前往 Settings、Privacy and security、App passwords。
- Telenet：使用你的 Telenet 邮件常用密码。
- 启用了双重验证的 Zoho Mail：在 Zoho 账户的 Security 中创建专用应用密码。
- Proton Mail：在同一台电脑上运行 Proton Mail Bridge，并使用 Bridge 显示的密码。只有在同一台电脑上使用 The Machine 时才能连接。The Machine 会显示 Bridge 证书的指纹，并且只信任该证书。

大多数服务商的服务器设置会自动填写。找不到你的服务商？打开**服务器设置**，输入服务商提供给邮件应用使用的信息：IMAP 和 SMTP 服务器、端口及安全协议（SSL/TLS 或 STARTTLS）。The Machine 始终使用 TLS 连接。

如果使用 Gmail 或 Microsoft 邮件，包括自有域名邮箱，请改选**Gmail**或**Outlook**。这两种方式无需密码即可登录。在服务器设置中填写这些服务商的服务器信息，也会引导你使用相应的登录方式：Microsoft 不再接受邮件应用使用密码登录。

输入 Microsoft 365 邮箱地址后，表单会识别出来，并显示**使用 Microsoft 登录**，替代密码输入框。选择后会打开 Outlook 登录页面。如果几秒内仍未识别到，密码表单会继续显示。

## 停止连接时

- **邮件服务器拒绝了密码**：你更改了密码，或应用密码已被移除。请使用新密码重新连接。
- **发送邮件时，邮件服务器拒绝了密码**：邮件未发送。请重新连接；如果仍被拒绝，请检查服务器设置中的 SMTP 服务器。在此之前，它只会读取邮件。
- **无法连接到邮件服务器**：系统会自动重试。如果持续失败，请检查服务器设置中的服务器名称。
- **邮件服务器的证书对应的是**另一个名称：共享主机通常会使用自己的服务器名称响应。请在服务器设置中输入显示的名称。The Machine 不会跳过证书检查。

## 移除邮箱

打开**连接**，选择账户，再点按**详情**，然后选择**断开连接**。断开后将停止读取邮件，已导入的内容会保留。也请在服务商处移除应用密码。
