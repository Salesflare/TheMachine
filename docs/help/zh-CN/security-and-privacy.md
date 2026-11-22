---
title: 安全与隐私
area: security
summary: 专属于你的Machine，邮件加密存储，未经你同意不会发送任何内容。简要说明和相关链接。
covers:
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: e636b2a2fbbc714d
---
## 简要说明

- 专属于你的Machine：托管版运行在欧盟云端，仅供你使用，不会与他人共享。也可以在自己的电脑上运行。
- 我们不会读取你的邮件：邮件会加密存储，我们的支持工具无法打开。
- 未经你同意不会发送任何内容：它会读取邮件并起草内容，由你决定发送什么。请参阅[执行](do-it.md)。
- 不会用于训练AI：我们没有自己的AI。你的AI服务提供商会在你的账户下，按照其条款提供服务。
- 除非你关闭，否则会分享团队心得：偶尔分享几条通用建议，不含个人信息，且发送前会经过审核。请参阅[分享心得](share-learnings.md)。
- 除非你关闭，否则会发送错误报告：发生故障时，报告会包含错误类型和代码中的位置，不会包含你的邮件、姓名或地址。请参阅[错误报告](error-reports.md)。
- 托管版Machine会统计使用次数：每天统计你执行的操作（例如打开待办或发送邮件），绝不包含内容。
- 可以带走数据，也可以删除：前往**设置** › **常规**导出所有内容，或用一个按钮删除你的Machine和备份。请参阅[取消或删除](cancel-and-delete.md)。
- 我们的访问会留下记录：每当团队成员查看你托管版Machine的报告或日志时，都会留下记录。Fleet所有者和管理员可以在**动态**中查看。请参阅[Fleet](fleet.md)。

## 安全级别

**标准**保留当前默认设置。**谨慎**不会在通知中显示文字，不保存登录信息，并且保留的数据更少。工作Fleet的管理员可以将整个Fleet设为谨慎。请参阅[安全级别](security-levels.md)。

## 登录

登录托管版控制面板需要使用通行密钥，或使用Google或Microsoft登录并输入身份验证器代码。

## 连接

每个连接的文章都会说明它会读取什么内容，以及可以发送什么内容。你可以随时断开任何连接，请参阅[连接](connections.md)。

## 帮助

帮助功能在你自己的Machine上运行，无法查看你的数据。只有每个问题的主题会发送给The Machine团队，不会发送你的原话。请参阅[咨询帮助](help-chat.md#what-the-team-sees)。

## 更多信息

- [安全](/security)：了解安全机制、工作人员可以和不可以查看的内容，以及我们如何扫描问题。
- [隐私声明](/privacy)和[数据处理条款](/dpa)。
- 发现安全问题？请参阅[安全政策](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md)。
