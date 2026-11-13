---
title: Salesforce
area: connections
summary: 查看Salesforce中的交易、待办和人物与项目活动。开启后，还能在Salesforce中更新联系人信息。
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
---
## 可以读取的内容

新交易，以及阶段变更或金额变动的交易。未完成的待办、通话记录、已完成并附有备注的其他待办，以及附有说明的会议。连接时会读取过去7天的数据，之后每15分钟读取一次新数据。

每笔交易都会在你的Graph中成为一个项目，交易中的联系人也会显示在对应的人物页面上，作为其帐户下的Salesforce联系人。

## 可以更改的内容

除非你开启**更新联系人信息**，否则不会更改任何内容。你的Salesforce登录信息会保存在你的Machine上。

## 连接

在托管的Machine上：

1. 打开设置页面app.themachine.computer/setup，然后进入**更多来源**。
2. 打开Salesforce，然后点击**连接Salesforce**。
3. 登录Salesforce，并授权The Machine（由Salesflare开发）。

或者在控制面板中：依次点击**连接**、**客户**，选择Salesforce，然后点击**使用Salesforce登录**。

你的Salesforce用户需要拥有API访问权限，大多数版本都包含此权限。

## 更新联系人信息

如果你的Machine发现某位Salesforce联系人的信息有更新，就可以更新该联系人：职位、电话，以及LinkedIn链接（如果你的组织在联系人中设有LinkedIn字段）。

1. 在**连接**中打开Salesforce，然后点击**查看将要更改的内容**。
2. 检查列表，然后点击**开启**或**暂不**。

更新规则：

- 只使用本人提供的信息，例如LinkedIn或Slack个人资料中的信息，或你在其页面上填写的信息。绝不猜测。
- 只有当信息比Salesforce中该联系人的最后修改时间更新时，才会更新。Salesforce中的修改优先。
- 只更新有差异的字段，且绝不填写空值。绝不更改电子邮件地址或帐户。
- 每次更改都会作为一条带日期的记录显示在人物页面上。

点击**关闭**即可停止更新。Fleet共享的连接只会读取数据。

## 移除连接

- 在控制面板中：点击**连接**，打开Salesforce，依次点击**详情**和**断开连接**。已导入的内容会保留。
- 在托管的Machine上，你也可以在设置页面中点击旁边的**移除**。

## 在Salesforce中撤销授权

在Salesforce中打开个人设置，然后进入Connected Apps OAuth Usage；也可以请管理员帮你撤销The Machine的授权。撤销后，The Machine将无法再读取或更改任何内容。
