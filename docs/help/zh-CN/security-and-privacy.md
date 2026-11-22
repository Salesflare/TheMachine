---
title: 安全与隐私
area: security
summary: 你的专属Machine，邮件加密存储，未经你确认不会发送任何内容。简要说明和相关链接。
covers:
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: a6595c0cdc308f55
---
## 简要说明

- 你的专属Machine：托管版运行在欧盟云端，仅供你使用，不与他人共享。你也可以在自己的电脑上运行。
- 我们不会阅读你的邮件：邮件会加密存储，我们的支持工具也无法打开。
- 未经你确认，不会发送任何内容：它会读取邮件并起草内容，由你决定发送什么。查看[执行](do-it.md)。
- 不会用于训练AI：我们没有自己的AI。你的服务提供商会在你的账号和其条款下运行。
- 默认会与团队分享心得，除非你关闭此功能：我们偶尔会分享几条通用建议，不含个人信息，发送前会审核。查看[分享心得](share-learnings.md)。
- 默认会发送错误报告，除非你关闭此功能：发生故障时，报告会包含错误类型和代码中的位置，不会包含你的消息、姓名或地址。查看[错误报告](error-reports.md)。
- 托管版Machine会统计使用情况：每天统计你执行的操作（例如打开待办或发送邮件），但不会记录操作内容；还会统计仪表板的加载速度（仅记录加载时间，并区分手机或电脑、应用或浏览器）。
- 你可以导出数据，也可以删除数据：在**设置**>**常规**中导出所有内容，或点击一个按钮删除你的Machine及其备份。查看[取消或删除](cancel-and-delete.md)。
- 我们的访问会留有记录：每次团队成员查看托管版Machine的报告或日志时，都会记录。Fleet所有者和管理员可以在**动态**中查看。查看[Fleet](fleet.md)。

## 安全级别

**标准**保留当前默认设置。**谨慎**会隐藏通知中的文本、不保存登录信息，并保留更少的数据。工作Fleet的管理员可以将Fleet设为谨慎。查看[安全级别](security-levels.md)。

## 登录

登录托管版仪表板需要使用通行密钥，或使用Google或Microsoft账号登录并输入验证器代码。

## 连接

每篇连接说明都会介绍它会读取哪些内容，以及可以发送哪些内容。你可以随时断开任意连接，查看[连接](connections.md)。

## 帮助

帮助功能在你自己的Machine上运行，无法查看你的数据。每个问题只有主题会发送给The Machine团队，不会发送你的原话。查看[向帮助提问](help-chat.md#what-the-team-sees)。

## 更多

- [安全](/security)：了解系统如何构建、员工能或不能查看哪些内容，以及我们如何扫描安全问题。
- [隐私声明](/privacy)和[数据处理条款](/dpa)。
- 发现安全问题？请查看[安全政策](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md)。
