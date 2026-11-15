---
title: 相似发件人
area: security
summary: 来自仿冒你往来对象的地址的邮件，会在对应待办中标记，草稿绝不会发给该地址。
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## 会识别哪些情况

有些诈骗邮件会使用看起来和你认识的地址相似的发件人地址：`examp1e.com` 会冒充 `example.com`、`example-billing.com`，或只差一个字母。The Machine 会将每位发件人的域名与你已有往来的域名进行比较。如果新地址只是看起来像某个已知地址，就会被视为相似地址。

如果只是后缀不同，但名称相同，例如 `example.nl` 和 `example.com`，那是同一家机构，不是相似地址。gmail.com 这类免费邮箱不计入。

## 在待办中

关于此类邮件的待办会直接说明情况，例如：“这不是 Alex 发的。邮件来自 examp1e.com，而不是 example.com。”发件人会显示为纯地址，不会显示头像，也不会链接到被冒充的人。

## The Machine 不会做什么

- 绝不会让相似发件人在你的 Graph 中获得角色。
- 绝不会将相似发件人与被冒充的人合并，也不会在 **是同一个人？** 下推荐合并。
- 准备好的回复会发送到记录中的地址，而不是相似地址。

你的选择始终优先：你仍然可以为他们指定角色、将他们合并，或向任何地址发送邮件。
