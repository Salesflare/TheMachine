---
title: 仿冒发件人
area: security
summary: 如果邮件来自仿冒联系人的地址，该邮件的待办会标明这一点，草稿也绝不会发给这个地址。
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## 检测内容

有些诈骗邮件来自看起来像你熟悉的地址，例如 `examp1e.com` 和 `example.com`、`example-billing.com` 很像，或者只差一个字母。The Machine 会将每个发件人的域名与您已有往来的域名进行比较。如果新地址只是看起来像一个已知地址，就会被视为仿冒地址。

同一个名称搭配不同后缀，例如 `example.nl` 和 `example.com`，属于同一个组织，不算仿冒地址。gmail.com 之类的免费邮箱永远不会被视为仿冒地址。

## 在待办中

关于这类邮件的待办会明确说明情况，例如：“这不是 Alex。邮件来自 examp1e.com，而不是 example.com。”发件人会显示为纯地址，不带照片，也不会链接到被仿冒的人。

## The Machine 不会做什么

- 绝不会在你的 Graph 中为仿冒发件人分配角色。
- 绝不会将他们与被仿冒的人合并，也绝不会在**是同一个人？**下推荐他们。
- 准备好的回复会发送到记录中的地址，而不是仿冒地址。

你的选择始终优先：你仍然可以为他们分配角色、将他们合并，或向任何地址发送邮件。
