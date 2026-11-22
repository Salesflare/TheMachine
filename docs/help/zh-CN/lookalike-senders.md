---
title: 相似发件人
area: security
summary: 如果邮件来自冒充你所联系对象的地址，相关待办会标记出来，草稿也绝不会发往该地址。
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 15a6a5dafcfa807b
---
## 会识别哪些情况

有些骗局会使用看起来像你熟悉的地址发件：例如`examp1e.com`冒充`example.com`或`example-billing.com`，只差一个字母，或有两个字母互换。The Machine会将每个发件人的域名与你已经联系过的域名进行比较。

两个地址看起来相似时，你主动写过邮件、见过对方或亲自设置过的那个才是真的，即使另一个地址先联系了你。如果无法据此区分，较新的那个会被视为相似发件人。

结尾不同但名称相同的地址，例如`example.nl`和`example.com`，属于同一个组织，不算相似发件人。gmail.com这类免费邮箱不计入比较。

## 在待办中

如果待办涉及这类邮件，会直接说明情况，例如：“这不是Alex。邮件来自examp1e.com，而不是example.com。”发件人只显示纯地址，不显示头像，也不会链接到被冒充的人。

## The Machine不会做什么

- The Machine绝不会在你的Graph中为相似发件人分配角色，也不会将他们的域名设为项目所属组织。
- The Machine绝不会把他们与被冒充的人合并，即使他们在同一对话中使用同一个名字发件也不例外，也绝不会在**是同一个人？**下推荐他们。
- The Machine准备的回复会发往记录中的地址，而不是相似发件人的地址。

你的选择始终优先：你仍可以为他们分配角色、将他们合并，或向任何地址写信。
