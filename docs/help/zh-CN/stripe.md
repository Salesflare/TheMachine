---
title: Stripe
area: connections
summary: 付款失败、争议、取消和大额新订阅。只能读取。
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 99a14108376ddcc1
---
## 它会读取什么

Stripe账号中可能需要你处理的事件：付款失败、争议、取消和大额新订阅，以及对应的客户。客户的邮箱会将事件关联到[Graph](graph.md)中的该客户及其组织。

## 它能做什么

它不会在Stripe中执行任何操作。它不会退款、重试付款或更改任何内容。它只申请读取权限，Stripe会在你安装前显示这一点。

## 连接

使用Stripe账号登录，操作很简单：

1. 在控制面板中依次打开：**连接**、**客户**、Stripe。或者，在托管版The Machine的设置页面app.themachine.computer/setup中，打开**更多来源**，然后选择Stripe。在自己的电脑上使用时，请先将它与你的账号配对。
2. 按**使用Stripe登录**。Stripe会询问你要使用哪个账号，并显示The Machine可以读取的内容。
3. 按**安装**。你会回到原来的页面，Stripe也已连接。

你也可以粘贴受限密钥：

1. 在Stripe中创建受限密钥：为Events、Customers和Account授予读取权限，其他所有项目都设为无权限。
2. 在设置、企业详情中找到你的账号ID（acct_...）。
3. 如上所述打开Stripe（或运行`assistant connect stripe`），打开**或者粘贴受限密钥**，粘贴账号ID和密钥，然后按**连接**。

在自己的电脑上，如果暂时无法使用“使用Stripe登录”，连接页面会说明原因，并直接打开此表单。

## 为团队连接一次

在Work Fleet中，所有者或管理员只需连接一次Stripe，然后与团队共享：

1. 在自己的The Machine上连接Stripe（见上文）。Fleet标签页中的**共享连接**框也有**连接Stripe**。
2. 在Fleet标签页中打开**共享Stripe**。默认勾选所有人；取消勾选不应获得访问权限的成员，然后按**共享**。

之后，队友的The Machine也能读取Stripe。连接页面会显示共享者，只有Fleet管理员可以更改或停止共享。你的The Machine每小时会续期队友的访问权限，因此它关闭时，队友对Stripe的访问也会暂停。没人能获得你的登录信息。详情请见：[Fleets](fleet.md)。

如果队友也自行连接了同一个Stripe账号，数据只会读取一次：共享的连接会暂不使用。

如果Stripe是通过某个服务连接的，而且该服务的一个密钥也能访问其他应用，就无法共享。请改为直接为团队连接Stripe。

## 移除连接

- 在控制面板中依次打开**连接**、Stripe、**详情**，然后按**断开连接**。已经导入的内容会保留。
- 在托管版The Machine上，也可以在设置页面中按它旁边的**移除**。
- 如果已与Fleet共享，请先在Fleet标签页中按**停止共享**。

## 在Stripe中撤销访问权限

- 如果你使用Stripe登录：在Stripe中打开设置、已安装的应用，然后移除The Machine。
- 如果你使用受限密钥：在Stripe中打开开发者、API密钥，然后删除或轮换密钥。
