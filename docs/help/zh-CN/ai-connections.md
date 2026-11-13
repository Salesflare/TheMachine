---
title: 连接其他AI
area: connections
summary: 让Claude、ChatGPT、Cursor、Codex或GBrain查看你的待办和Graph；授予查看和编辑权限后，它们还能进行修改，你可以撤销这些修改。
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## 其他AI能做什么

Claude、ChatGPT、Cursor、Codex、GBrain和其他AI都可以连接到你的Machine。它们可以查看你的待办、承诺、团队简报，以及Graph中的人物和公司。

授予**查看和编辑**权限后，它们还可以添加待办或邮件草稿，也可以更新Graph：保存事实、修正详细信息、字段和标签，或为某个人的摘要添加一行内容。

每项更改都会显示在**动态**中，并提供**撤销**选项。它们绝不会合并、删除或分享记录。保存的内容会标记为**AI：**，并注明AI的名称。你的Machine会把这些内容视为AI的说法，而不是你的指示。

草稿会一直保留，直到你亲自查看并按下发送。连接的AI绝不会发送任何内容，也不会代你采取行动。

## 连接一个AI

打开**设置**、**应用**。在**The Machine应用**下方，你会看到**添加到ChatGPT**和**添加到Claude**。在**也可以通过地址添加**下方，有官方应用的通用地址`https://mcp.themachine.computer/mcp`，以及**你的地址**`https://<your name>.mcp.themachine.computer/mcp`，两者旁边都有**复制**按钮。

如果你使用的是自己电脑上的Machine，请先在**获取你的地址**下方按**设置**。系统会打开你账号中的一个页面：检查页面显示的代码是否相同，确认后选择一个名称。Machine会自动完成配对，无需重启。两种连接方式都需要这一步。

随后，Machine会自动设置安全地址。这需要几分钟。

要连接Claude，按**添加到Claude**，或打开[Claude目录中的The Machine](https://claude.ai/directory/the-machine)，然后按Connect。在Team和Enterprise中，需要由所有者在Organization settings中添加。

如果要在Claude中使用地址，请改为打开Customize、Connectors，按+ Add，然后选择Add custom connector。将名称设为The Machine，粘贴地址，按Continue，然后按Add。

要连接ChatGPT，按**添加到ChatGPT**，或打开[ChatGPT中的The Machine](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4)，然后按Install plugin。在Business和Enterprise中，管理员可能需要先允许使用。

官方应用可以连接托管的Machine；自己电脑上的Machine设置好地址后，也可以通过官方应用连接。

如果要使用私有地址，或连接Network之外的Machine，请改为在ChatGPT中添加自定义MCP服务器：打开chatgpt.com/plugins，按+，然后选择Add custom MCP server。将名称设为The Machine，粘贴地址并选择OAuth。确认警告，然后按Create as a plugin。你的套餐或工作区必须允许使用自定义MCP服务器。

使用官方应用时，AI会要求你用The Machine账号登录。如果你有多台Machine，请选择要连接的那台，然后在它自己的页面上批准连接。使用私有地址时，AI会直接连接到你的Machine。

私有网络（Tailscale）中的设备上的AI，例如Claude Code或Cursor，也可以使用你的仪表板地址，再加上`/mcp`。在**设置**、**账号**页面底部按**取消这台Machine的配对**，即可将自己电脑上的Machine从账号中移除。

你的Machine会显示发起请求的AI。如果无法识别，它会显示请求的来源：只有在你刚刚亲自发起连接时，才批准请求。

选择AI可以执行的操作：**查看**或**查看和编辑**。如果同时有工作和个人账号，请选择它可以查看的范围。然后选择权限有效时长：**1天**、**7天**、**30天**或**1年**。按**连接**，或按**取消**，拒绝连接。

## 官方应用或私有地址

官方应用是最简单的方式：所有人使用同一个地址，系统会通过你的账号找到Machine。我们的云端只会转发请求，不会存储任何内容。

使用私有地址时，所有内容都会加密并一路传输到你的Machine。云端只会转发内容，无法读取。

无论使用哪种方式，都由你的Machine决定是否允许连接。只有你在Machine页面上批准的AI才能访问，并且只能使用你授予的权限。在**设置**、**应用**中，通过官方应用连接的AI会显示**官方应用**。

## AI能看到什么

每个连接只能访问自己的范围。工作范围包括你的工作账号中的待办和承诺、工作联系人、公司、项目，以及Work Fleet的团队简报。个人范围包括其他所有内容。除非你开启**消息**，否则消息正文会留在你的Machine上；不开启时，AI只能通过发件人、主题和日期查看待办的来源。

团队成员的Team Graph记录不会发送给外部AI。

## 消息

开启**消息**后，AI可以搜索和读取你的邮件、Slack、WhatsApp及其他聊天内容。你需要在连接AI的页面，或之后在**设置**、**应用**中手动开启。AI只能读取，绝不会发送、删除或标记任何内容。

AI只能读取自己范围内的消息。以下内容绝不会发出：一次性验证码和登录链接、**只有你**的看板或项目中的消息、The Machine判断为敏感的邮件往来（交易、人力资源、法律、健康、金钱相关）、你设为私密的邮件往来，以及已删除的消息。

每次读取都会显示在AI的**动态**中，包括读取的消息数量和邮件往来，但不会显示正文。你的Machine会将正文标记为数据后交给AI，因此AI不应该遵循消息中写入的指令。

开启消息后，拥有**查看和编辑**权限的AI对Graph所做的更改都需要你确认。在**动态**中，按更改旁边的**应用**或**忽略**。

## 在设置中管理

打开**设置**、**应用**，即可查看每个已连接的AI，以及它的权限、范围、到期日期和最近使用时间。你可以直接在这里开启或关闭**消息**。按**更改**可调整权限、范围或有效时长。下次请求会使用新设置。**动态**会列出每次请求，包括被拒绝的请求。按**立即关闭**可暂停连接：所有登录都会失效，但历史记录会保留。按**移除**可删除连接及其历史记录。

如果你再次登录同一个AI，新的批准会取代之前的批准。

如果AI无法自行登录，可以使用密钥。在**添加密钥**下方输入名称，选择权限和有效时长，然后按**创建密钥**。请立即复制密钥：它只会显示一次。AI会将密钥作为`Authorization: Bearer <key>`发送。

## 确保安全

每次请求都会记录，包括被拒绝的请求。连接过期或已关闭时，请求会被拒绝，直到你更改设置。你的Machine只会保存每次登录的指纹，因此仅凭数据副本无法登录。
