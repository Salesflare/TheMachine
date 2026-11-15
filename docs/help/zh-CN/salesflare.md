---
title: Salesflare CRM
area: connections
summary: 账户、联系人和交易信息，帮助 The Machine 了解哪些人最重要。通过你的 API 密钥读取数据。
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 3d6041d568843d96
---
## 读取的内容

Salesflare 中的账户、联系人和交易，以及每个账户的动态：你未参与的同事邮件，以及带有备注的会议。

## 可以更改的内容

不会更改任何内容。（在自己的电脑上，`join_pipelines` 设置可以让它把你添加到所选销售渠道中的账户。默认关闭。）

## 连接

1. 在 Salesflare 中，打开[设置、API 密钥](https://app.salesflare.com/#/settings/apikeys)并创建密钥。
2. 在托管的 Machine 上：打开 app.themachine.computer/setup 上的设置页面，前往**更多来源**，打开 Salesflare CRM，粘贴密钥，然后点击**连接**。
3. 在控制面板中：依次打开**连接**、**客户**和 Salesflare CRM，粘贴密钥，然后点击**连接**。随后，卡片会显示同步进度。

## 同步详情

在**连接**、**客户**中，Salesflare 会显示同步进度：本轮读取的账户数，以及因 Salesflare 响应太慢而跳过的账户数。如果一轮同步持续数小时，系统会提示同步可能卡住了。

卡片会显示成功打开的账户数，以及导入的邮件和会议数。如果你的 API 密钥无法打开任何账户，卡片会显示**需要你帮忙**：请使用有权限查看这些账户的用户的密钥。如果 Salesflare 多次超时，但每次重试都能成功，卡片会提示 Salesflare **有时响应较慢**。

如果 Salesflare 尚未为你的团队启用 API 密钥的动态访问权限，卡片会说明这一点。在 Salesflare 支持团队启用此权限之前，不会导入邮件或会议。系统第一天每 10 分钟检查一次，之后大约每小时检查一次。功能可用后，系统会自动继续同步。

- **停止**：在你点击**开始**之前，不会导入新内容。之后会从上次停止的位置继续。
- **重新启动同步**：从头开始，并重新读取最近一周的数据。已导入的内容不会丢失。
- API 密钥：打开 Salesflare 的 API 密钥页面，以便创建新密钥。

## 移除

- 在控制面板中：打开**连接**，选择 Salesflare，点击**详情**，然后点击**断开连接**。已导入的内容会保留。
- 在托管的 Machine 上，也可以在设置页面中点击旁边的**移除**。

## 在 Salesflare 中撤销访问权限

在 Salesflare 的“设置”下，打开“API 密钥”并删除该密钥。
