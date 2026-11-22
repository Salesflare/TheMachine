---
title: Salesforce
area: connections
summary: 在联系人和项目中查看Salesforce的商机、任务和活动。如果开启此功能，还可以在Salesforce中更新联系人详情。
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## 读取的内容

新商机，以及阶段或金额发生变化的商机。未完成的任务、通话，以及标记为已完成并附有备注的其他任务，还有附有说明的会议。连接时读取过去7天的数据，此后每15分钟读取新数据。

每个商机都会在你的Graph中成为一个项目，相关联系人会显示在对应人员的页面上，作为其账户下的Salesforce联系人。

## 可以更改的内容

在开启**更新联系人详情**之前，不会更改任何内容。你的Salesforce登录信息会保留在你的Machine上。

## 连接

在托管的Machine上：

1. 打开app.themachine.computer/setup上的设置页面，然后前往**更多来源**。
2. 打开Salesforce，然后点击**连接Salesforce**。
3. 登录Salesforce，并授权由Salesflare制作的The Machine。

也可以在控制面板中依次点击**连接**、**客户**，选择Salesforce，然后点击**使用Salesforce登录**。如果在自己的电脑上使用，请先将它与你的账户配对。

你的Salesforce用户需要拥有API访问权限，大多数版本都包含此权限。

## 更新联系人详情

如果你的Machine掌握了某位Salesforce联系人的更新详情，就可以在Salesforce中更新该联系人：职位、电话，以及LinkedIn链接（前提是你的组织在联系人中设有LinkedIn字段）。

1. 在**连接**中打开Salesforce，然后点击**显示可能的更改**。
2. 检查列表，然后点击**开启**或**暂不**。

更新规则：

- 只使用联系人本人提供的信息，例如其LinkedIn或Slack个人资料中的信息，或你在其页面上填写的信息。绝不猜测。
- 只有当信息比Salesforce中该联系人的上次更改时间更新时才会更新。在Salesforce中进行的编辑优先。
- 只更新有差异的字段，绝不填入空白内容。不会更改电子邮件地址或账户。
- 每次更改都会作为一条带日期的记录显示在该人员的页面上。

点击**关闭**即可停止更新。Fleet共享的连接只会读取数据。

## 移除

- 在控制面板中，依次点击**连接**，打开Salesforce，选择**详情**，然后点击**断开连接**。已导入的内容会保留。
- 在托管的Machine上，点击**断开连接 ↗**会打开设置页面，然后点击Salesforce旁边的**移除**。

## 在Salesforce中撤销访问权限

在Salesforce中打开个人设置，然后选择Connected Apps OAuth Usage，或联系管理员，并撤销The Machine的访问权限。之后The Machine将无法读取或更改任何内容。
