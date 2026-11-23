---
title: Stripe
area: connections
summary: 失败付款、争议、取消和大额新订阅。只能读取信息。
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 85e6e07cca1a8e8d
---
## 它会读取哪些信息

你Stripe账号中可能需要你处理的事件：失败付款、争议、取消和大额新订阅，以及相关客户的信息。客户的邮箱地址可将事件关联到[Graph](graph.md)中的对应人员和组织。

失败付款事件会说明付款用途（首次付款、续费）以及Stripe何时会再次尝试付款。事件不会说明银行卡被拒的原因，因为Stripe不会提供这项信息。要查看原因，请在Stripe中打开该事件。

## 它能做什么

它不会在Stripe中执行任何操作，也不会退款、重试付款或更改任何信息。它只申请读取权限，安装前Stripe会显示这一点。

## 连接

使用Stripe登录，这是最简单的方式：

1. 在控制面板中依次点击**连接**、**客户**和Stripe。或者，在托管版Machine的设置页面app.themachine.computer/setup中，点击**更多来源**，再选择Stripe。在你自己的电脑上，请先将Machine与你的账号配对。
2. 点击**使用Stripe登录**。Stripe会询问你要使用哪个账号，并显示The Machine可以读取哪些信息。
3. 点击**安装**。你会返回原来的页面，Stripe也就连接好了。

在你自己的电脑上，也可以粘贴受限密钥：

1. 在Stripe中创建受限密钥，并为Events、Customers和Account设置Read权限，其他所有项目设置为None。
2. 在“设置”>“商家详情”中找到账号ID（acct_...）。
3. 按上述步骤打开Stripe（或运行`assistant connect stripe`），打开**也可以粘贴受限密钥**，粘贴账号ID和密钥，然后点击**连接**。

在你自己的电脑上，如果暂时无法使用Stripe登录，“连接”会提示你，并直接打开这个表单。

## 为团队连接一次

在工作Fleet中，所有者或管理员只需连接一次Stripe，然后与团队共享：

1. 在你自己的Machine上连接Stripe（见上文）。Fleet标签页的**共享连接**框中也有**连接Stripe**。
2. 在Fleet标签页中打开**分享Stripe**。默认会勾选所有人，取消勾选不应获得访问权限的成员，然后点击**分享**。

之后，队友的Machine也可以读取Stripe信息。“连接”会显示分享者，只有Fleet管理员可以更改或停止共享。你的Machine每小时会续期队友的访问权限，因此你的Machine关闭期间，他们将无法访问Stripe。没人会获得你的登录信息。详情请见：[Fleet](fleet.md)。

如果队友也自行连接了同一个Stripe账号，信息只会读取一次：共享的连接会暂停使用。

通过某项服务连接的Stripe无法共享，因为该服务的一个密钥可能也能访问其他应用。请改为直接为团队连接Stripe。

## 移除连接

- 在控制面板中点击**连接**，打开Stripe，点击**详情**，再点击**断开连接**。已导入的信息会保留。
- 在托管版Machine上，通过登录方式连接的Stripe会显示**断开连接 ↗**。点击后会打开设置页面，再点击Stripe旁边的**移除**。
- 如果Stripe是与Fleet共享的，请先在Fleet标签页点击**停止分享**。

## 在Stripe中撤销访问权限

- 如果使用Stripe登录：在Stripe中打开“设置”>“已安装的应用”，然后移除The Machine。
- 如果使用受限密钥：在Stripe中打开“开发者”>“API密钥”，然后删除或轮换密钥。
