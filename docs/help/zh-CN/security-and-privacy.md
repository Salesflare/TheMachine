---
title: 安全与隐私
area: security
summary: 你的专属 Machine，邮件经过加密存储，未经你确认不会发送任何内容。简要说明，附相关链接。
covers: 
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: 237400429e8be40b
---
## 简要说明

- 你的专属 Machine：托管版运行在欧盟云端，只供你使用，不会与他人共享。你也可以在自己的电脑上运行。
- 我们不会读取你的邮件：邮件经过加密存储，我们的支持工具也无法打开。
- 未经你确认，不会发送任何内容：它会读取邮件并起草内容，由你决定发送什么。查看[执行](do-it.md)。
- 不会用于训练 AI：我们没有自己的 AI。你的服务提供商会在你的账号下，根据其条款提供服务。
- 只有得到你的确认，才会与团队分享心得：它偶尔会询问是否发送几条通用建议，不会包含个人信息。查看[分享心得](share-learnings.md)。
- 除非你关闭错误报告：发生问题时，报告会包含错误类型和代码中的位置，不会包含你的消息、姓名或地址。查看[错误报告](error-reports.md)。
- 托管版 Machine 的使用次数：每天统计你执行的操作，例如打开待办或发送邮件，但不会记录内容。
- 随时带走或删除数据：在**设置** › **常规**中导出所有内容，也可以用一个按钮删除你的 Machine 及其备份。查看[取消或删除](cancel-and-delete.md)。
- 我们的访问行为会记录：每当团队成员查看你的托管版 Machine 的报告或日志时，都会留下记录。Fleet所有者和管理员可以在**动态**中查看。查看[Fleets](fleet.md)。

## 安全级别

**标准**会保留当前默认设置。**谨慎**不会在通知中显示文本，不会保存登录信息，并且保留的数据更少。工作 Fleet 的管理员可以将 Fleet 设为谨慎。查看[安全级别](security-levels.md)。

## 登录

登录托管版控制面板需要使用 Google 或 Microsoft账号，并通过身份验证器代码或通行密钥验证。

## 连接

每个连接的说明文章都会介绍它可以读取和发送哪些内容。你可以随时断开任何连接：查看[连接](connections.md)。

## 帮助

帮助功能在你自己的 Machine 上运行，无法查看你的数据。每个问题的主题会发送给 The Machine 团队，但不会发送你的原话。查看[咨询帮助](help-chat.md#what-the-team-sees)。

## 更多信息

- [安全](/security)：了解产品的构建方式、我们的员工可以和不可以查看哪些内容，以及我们如何扫描问题。
- [隐私声明](/privacy)和[数据处理条款](/dpa)。
- 发现安全问题？请查看[安全政策](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md)。
