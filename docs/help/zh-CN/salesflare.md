---
title: Salesflare CRM
area: connections
summary: 读取客户、联系人和交易，了解哪些人最重要。使用你的API密钥读取数据。
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 697e6d60b69bb1cd
---
## 读取的内容

你在Salesflare中的客户、联系人和交易，以及每个客户的动态：你未参与的同事邮件，还有带备注的会议。

## 可以更改的内容

不会更改任何内容。（在你自己的电脑上，`join_pipelines`设置可以让它把你添加到指定销售渠道中的客户。默认关闭。）

## 连接

1. 在Salesflare中，打开[设置、API密钥](https://app.salesflare.com/#/settings/apikeys)，然后创建密钥。
2. 在托管的Machine上：打开app.themachine.computer/setup中的设置页面，前往**更多来源**，打开Salesflare CRM，粘贴密钥，然后点击**连接**。
3. 在控制面板中：依次点击**连接**、**客户**和Salesflare CRM，粘贴密钥，然后点击**连接**。随后会显示读取的客户数量。

## 同步详情

在**连接**下，点击**其他来源**，Salesflare会显示同步进度：本轮读取的客户数，以及因Salesflare响应过慢而跳过的客户数。如果一轮同步运行了数小时，页面会提示同步可能卡住了。

信息卡会显示它成功打开的客户数量，以及导入的邮件和会议数量。如果Salesflare不允许你的API密钥打开任何客户，信息卡会显示**需要你协助**：请使用有权查看这些客户的用户的密钥。如果Salesflare一直超时，但每次重试最终都能成功，信息卡会提示Salesflare**有时响应缓慢**。

如果Salesflare尚未为你的团队启用API密钥的动态访问权限，信息卡会说明这一点：Salesflare支持团队启用该权限前，不会导入邮件或会议。第一天每10分钟检查一次，之后大约每小时检查一次，功能正常后会自动继续同步。

- **停止**：点击**开始**前，不会有新内容导入。之后会从上次停止的地方继续。
- **重新开始同步**：重新开始同步，并再次读取最近一周的数据。已导入的内容不会丢失。
- **API密钥**：打开Salesflare的API密钥页面，以创建新密钥。

## 移除

- 在控制面板中：点击**连接**，打开Salesflare，依次点击**详情**和**断开连接**。已导入的内容会保留。
- 在托管的Machine上，你也可以在设置页面中点击Salesflare旁边的**移除**。

## 在Salesflare中撤销访问权限

在Salesflare的设置、API密钥下删除该API密钥。
