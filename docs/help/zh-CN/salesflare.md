---
title: Salesflare CRM
area: connections
summary: 读取Salesflare中的账号、联系人和商机，了解哪些人最重要。使用你的API密钥读取数据。
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 8051c61777603a7e
---
## 读取的内容

你在Salesflare中的账号、联系人和商机，以及每个账号的动态：你未参与的同事邮件，以及带有备注的会议。

## 可以更改的内容

什么也不会更改。（在你自己的电脑上，`join_pipelines`设置可以让它将你添加到指定销售流程中的账号。默认关闭。）

## 连接

1. 在Salesflare中，打开[设置，API密钥](https://app.salesflare.com/#/settings/apikeys)，创建密钥。
2. 使用托管版Machine：打开app.themachine.computer/setup上的设置页面，前往**更多来源**，打开Salesflare CRM，粘贴密钥，然后点击**连接**。
3. 在控制面板中：依次点击**连接**、**客户**和Salesflare CRM，粘贴密钥，然后点击**连接**。卡片会显示同步进度。

## 同步详情

在**连接**>**客户**下，Salesflare会显示同步进度：本轮检查的账号、因Salesflare响应过慢而跳过的账号，以及你的API密钥无法打开的账号（**无法访问**）。如果一轮同步运行数小时，会提示同步可能卡住了。

卡片会统计本周读取的账号，以及导入的邮件和会议数量。

少数账号无法访问，不需要处理，其他数据仍会照常导入。如果你的API密钥无法打开任何账号，卡片会显示**需要你帮忙**：请使用有权查看这些账号的用户所持有的密钥。新密钥会从头开始重新读取最近一周的数据。如果Salesflare经常超时，但每次重试都能成功，卡片会提示Salesflare**有时响应缓慢**。

如果Salesflare尚未为你的团队启用API密钥的动态访问权限，卡片会显示提示。在Salesflare支持团队启用该权限之前，不会导入邮件或会议。第一天每10分钟检查一次，之后大约每小时检查一次；功能恢复后会自动继续同步。

- **停止**：点击**开始**之前，不会有新内容导入。恢复后会从中断处继续。
- **重新启动同步**：从头开始重新读取最近一周的数据。已导入的内容不会丢失。
- **API密钥**：打开Salesflare的API密钥页面，以便创建新密钥。

## 移除

- 在控制面板中：点击**连接**，打开Salesflare，点击**详情**，然后点击**断开连接**。已导入的内容会保留。
- 使用托管版Machine时，也可以在设置页面中点击它旁边的**移除**。

## 在Salesflare中撤销访问权限

在Salesflare的“设置”>“API密钥”中删除该API密钥。
