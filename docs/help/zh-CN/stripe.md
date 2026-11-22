---
title: Stripe
area: connections
summary: 失败的付款、争议、取消订阅和新增的大额订阅。它只读取数据。
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 6e7ca235dc502297
---
## 读取的内容

Stripe账户中可能需要你处理的事件：付款失败、争议、取消订阅和新增的大额订阅，以及这些事件对应的客户。客户的电子邮箱会将事件关联到[Graph](graph.md)中的对应人员和组织。

## 可以做什么

它不会在Stripe中执行任何操作，也不会退款、重试付款或更改任何内容。它只申请读取权限，安装前Stripe会显示这一点。

## 连接

使用Stripe登录，操作更简单：

1. 在控制面板中依次选择**连接**、**客户**、Stripe。或者，在托管的Machine设置页面app.themachine.computer/setup中选择**更多来源**、Stripe。在自己的电脑上使用前，请先将Machine与你的账户配对。
2. 点击**使用Stripe登录**。Stripe会询问要连接哪个账户，并显示The Machine可以读取的内容。
3. 点击**安装**。随后会返回原来的页面，Stripe就连接好了。

在自己的电脑上，也可以改为粘贴受限密钥：

1. 在Stripe中创建受限密钥：将Events、Customers和Account的权限设为Read，其他所有权限设为None。
2. 在Settings、Business details下找到你的账户ID（acct_...）。
3. 按上述方法打开Stripe（或运行`assistant connect stripe`），打开**也可以粘贴受限密钥**，粘贴账户ID和密钥，然后点击**连接**。

在自己的电脑上，如果暂时无法使用“使用Stripe登录”，**连接**中会提示你，并直接打开此表单。

## 为团队连接一次

在工作Fleet中，所有者或管理员只需连接一次Stripe，然后与团队共享：

1. 在自己的Machine上连接Stripe（见上文）。Fleet标签页的**共享连接**区域也有**连接Stripe**。
2. 在Fleet标签页中打开**共享Stripe**。默认会选中所有人，取消选择不应获得访问权限的成员，然后点击**分享**。

队友的Machine随后也能读取Stripe数据。**连接**中会显示共享者，且只有Fleet管理员可以修改或停止共享。你的Machine每小时会续期一次访问权限，因此你的Machine关闭时，队友的Stripe访问也会暂停。其他人无法获得你的登录信息。详情请参阅：[Fleet](fleet.md)。

如果队友也自行连接了同一个Stripe账户，数据只会读取一次：共享的连接会暂停使用。

通过某项服务连接的Stripe不能共享，因为该服务的密钥也可以打开其他应用。请直接连接Stripe，以便与团队共享。

## 移除连接

- 在控制面板中，依次选择**连接**，打开Stripe，点击**详情**，然后点击**断开连接**。已经导入的数据会保留。
- 在托管的Machine上，如果Stripe是通过登录连接的，会显示**断开连接 ↗**，点击后会打开设置页面。然后点击旁边的**移除**。
- 如果Stripe已与Fleet共享，请先在Fleet标签页点击**停止共享**。

## 在Stripe中撤销访问权限

- 如果是通过Stripe登录连接的：在Stripe中打开Settings、Installed apps，然后移除The Machine。
- 如果使用受限密钥：在Stripe中打开Developers、API keys，然后删除或轮换密钥。
