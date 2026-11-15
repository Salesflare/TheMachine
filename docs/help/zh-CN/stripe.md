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

Stripe 账户中可能需要你处理的事件：付款失败、争议、取消订阅和新增的大额订阅，以及这些事件对应的客户。客户的电子邮箱会将事件关联到 [Graph](graph.md) 中的对应人员和组织。

## 可以做什么

它不会在 Stripe 中执行任何操作，也不会退款、重试付款或更改任何内容。它只申请读取权限，安装前 Stripe 会显示这一点。

## 连接

使用 Stripe 登录，操作更简单：

1. 在控制面板中依次选择 **连接**、**客户**、Stripe。或者，在托管的 Machine 设置页面 app.themachine.computer/setup 中选择 **更多来源**、Stripe。在自己的电脑上使用前，请先将 Machine 与你的账户配对。
2. 点击 **使用 Stripe 登录**。Stripe 会询问要连接哪个账户，并显示 The Machine 可以读取的内容。
3. 点击 **安装**。随后会返回原来的页面，Stripe 就连接好了。

在自己的电脑上，也可以改为粘贴受限密钥：

1. 在 Stripe 中创建受限密钥：将 Events、Customers 和 Account 的权限设为 Read，其他所有权限设为 None。
2. 在 Settings、Business details 下找到你的账户 ID（acct_...）。
3. 按上述方法打开 Stripe（或运行 `assistant connect stripe`），打开 **也可以粘贴受限密钥**，粘贴账户 ID 和密钥，然后点击 **连接**。

在自己的电脑上，如果暂时无法使用“使用 Stripe 登录”，Connections 会提示你，并直接打开此表单。

## 为团队连接一次

在 Work Fleet 中，所有者或管理员只需连接一次 Stripe，然后与团队共享：

1. 在自己的 Machine 上连接 Stripe（见上文）。Fleet 标签页的 **共享连接** 区域也有 **连接Stripe**。
2. 在 Fleet 标签页中打开 **共享 Stripe**。默认会选中所有人，取消选择不应获得访问权限的成员，然后点击 **分享**。

队友的 Machines 随后也能读取 Stripe 数据。Connections 会显示共享者，且只有 Fleet 管理员可以修改或停止共享。你的 Machine 每小时会续期一次访问权限，因此你的 Machine 关闭时，队友的 Stripe 访问也会暂停。其他人无法获得你的登录信息。详情请参阅：[Fleets](fleet.md)。

如果队友也自行连接了同一个 Stripe 账户，数据只会读取一次：共享的连接会暂停使用。

通过某项服务连接的 Stripe 不能共享，因为该服务的密钥也可以打开其他应用。请直接连接 Stripe，以便与团队共享。

## 移除连接

- 在控制面板中，依次选择 **连接**，打开 Stripe，点击 **详情**，然后点击 **断开连接**。已经导入的数据会保留。
- 在托管的 Machine 上，如果 Stripe 是通过登录连接的，会显示 **断开连接 ↗**，点击后会打开设置页面。然后点击旁边的 **移除**。
- 如果 Stripe 已与 Fleet 共享，请先在 Fleet 标签页点击 **停止共享**。

## 在 Stripe 中撤销访问权限

- 如果是通过 Stripe 登录连接的：在 Stripe 中打开 Settings、Installed apps，然后移除 The Machine。
- 如果使用受限密钥：在 Stripe 中打开 Developers、API keys，然后删除或轮换密钥。
