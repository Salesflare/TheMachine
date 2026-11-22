---
title: 连接其他AI
area: connections
summary: 让Claude、ChatGPT、Cursor、Codex或GBrain查看你的待办和Graph，还能通过**查看和编辑**进行修改，并且可以撤销。
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: a8637260c99df309
---
## 其他AI可以做什么

Claude、ChatGPT、Cursor、Codex、GBrain和其他AI可以连接到你的Machine。它们可以查看你的待办、承诺、团队简报，以及Graph中的人物和公司。

有了**查看和编辑**权限，它们还可以添加待办或邮件草稿，以及更新Graph：保存事实、修正详细信息、字段和标签，或为某人的摘要添加一行内容。

每项更改都会显示在**动态**中，并提供**撤销**。它们不会合并、删除或分享记录。它们保存的内容会标记为**AI：**，并注明AI名称。你的Machine会将其视为AI的说法，而不是你的指令。

草稿会一直保留，直到你阅读并亲自点击“发送”。连接的AI不会发送任何内容，也不会替你执行操作。

## 连接一个AI

打开**设置**>**应用**。在**The Machine应用**下方，可以看到**添加到ChatGPT**和**添加到Claude**。在**也可以通过地址添加**下方，有官方应用适用于所有Machine的统一地址`https://mcp.themachine.computer/mcp`，以及**你的地址**`https://<your name>.mcp.themachine.computer/mcp`，每项旁边都有**复制**。

如果Machine运行在你自己的电脑上，请先点击**获取你的地址**下方的**设置**。系统会打开你账号中的一个页面：确认显示的是相同的设置码，然后确认并选择名称。你的Machine会自动配对，无需重启。两种连接方式都需要完成这一步。

之后，你的Machine会自动设置安全地址。这需要几分钟。

连接Claude时，点击**添加到Claude**，或打开[Claude目录中的The Machine](https://claude.ai/directory/the-machine)，然后点击Connect。使用Team和Enterprise时，需要由所有者在Organization settings中添加。

如果要在Claude中使用地址，请打开Customize、Connectors，点击+ Add，再点击Add custom connector。名称填写The Machine，粘贴地址，点击Continue，然后点击Add。

连接ChatGPT时，点击**添加到ChatGPT**，或打开[ChatGPT中的The Machine](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4)，然后点击Install plugin。使用Business和Enterprise时，管理员可能需要先允许使用。

官方应用可以连接托管的Machine，也可以连接已设置地址的本地Machine。

如果要使用你的私人地址，或连接未加入Network的Machine，请改为在ChatGPT中添加自定义MCP服务器：打开chatgpt.com/plugins，点击+，然后点击Add custom MCP server。名称填写The Machine，粘贴地址并选择OAuth。确认警告，然后点击Create as a plugin。你的套餐或工作区必须允许使用自定义MCP服务器。

使用官方应用时，AI会要求你使用The Machine账号登录。如果你有多个Machine，请选择要连接的Machine，然后在该Machine自己的页面上批准连接。使用私人地址时，AI会直接连接到你的Machine。

在私人网络（Tailscale）设备上运行的AI，例如Claude Code或Cursor，也可以使用你的控制面板地址，并在后面加上`/mcp`。在**设置**>**账号**底部点击**取消这台Machine的配对**，即可解除本地Machine与账号的关联。

你的Machine会显示发起连接的AI。如果无法识别，它会显示请求来源。只有在你刚刚亲自发起连接时才继续。

选择AI可以执行的操作：**查看**或**查看和编辑**。如果同时有Work和Personal账号，还要选择它可以访问的范围。然后选择访问时长：**1天**、**7天**、**30天**或**1年**。点击**连接**，或点击**取消**，不授予权限并返回。

## 使用官方应用还是私人地址

官方应用是最简单的方式：所有人使用同一个地址，你的账号会自动找到你的Machine。我们的云服务只转发请求，不会存储请求内容。

使用私人地址时，数据会全程加密，直达你的Machine。云服务只负责转发，无法读取数据。

无论使用哪种方式，都由你的Machine决定是否允许连接。只有在页面上获得你批准的AI才能访问，并且只能使用你选择的权限。在**设置**>**应用**中，通过官方应用连接的AI会显示**官方应用**。

## AI可以看到什么

每个连接只能访问指定范围内的内容。Work包括工作账号中的待办和承诺、工作联系人、公司、项目，以及工作Fleet的团队简报。Personal包括其他所有内容。除非你开启**消息**，否则消息正文会留在你的Machine上；关闭时，AI只能通过发件人、主题和日期查看待办的来源。

团队成员的Team Graph记录不会发送给外部AI。

## 消息

**消息**允许AI搜索和阅读你的邮件、Slack、WhatsApp及其他聊天内容。此功能默认关闭，你可以在连接AI的页面上开启，也可以之后前往**设置**>**应用**开启。AI只能阅读，不会发送、删除或标记任何内容。

AI只能读取其访问范围内的消息。有些内容绝不会发送出去：一次性验证码和登录链接、**只有你**看板或项目中的消息、The Machine判定为敏感的对话（商机、人力资源、法律、健康、金钱）、你设为私密的对话，以及已删除的消息。

每次读取都会显示在**动态**中，包括读取的消息数量和对话，但不会显示正文。你的Machine会将正文标记为数据后交给AI，因此AI不应遵循消息中写下的指令。

开启消息后，拥有**查看和编辑**权限的AI对Graph所做的更改都需要你确认。在**动态**中点击相应更改上的**应用**或**忽略**。

## 在设置中管理

打开**设置**>**应用**，即可查看每个曾连接过的AI，以及它的权限、访问范围、到期日期和最近使用时间。可以直接在此处开启或关闭**消息**。点击**更改**可以修改权限、访问范围或有效时长。下次调用时会使用新设置。**动态**会列出所有调用，包括被拒绝的调用。点击**立即关闭**可暂停连接：所有登录都会失效，但历史记录会保留。点击**移除**可删除连接及其历史记录。

再次登录同一个AI时，新授权会取代之前的授权。

无法自行登录的AI可以使用密钥。在**添加密钥**下方为密钥命名，选择权限和有效时长，然后点击**创建密钥**。请立即复制密钥，因为它只会显示一次。AI会将密钥作为`Authorization: Bearer <key>`发送。

## 安全须知

所有调用都会记录，包括被拒绝的调用。连接过期或已关闭时，调用会被拒绝，直到你更改设置。你的Machine只保存每次登录的指纹，因此即使复制这些数据，也无法借此登录。
