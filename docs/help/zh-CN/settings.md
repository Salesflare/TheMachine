---
title: 设置
area: settings
summary: 了解各项设置的位置，从浅色模式到安全和账号。
covers: settings:general
code: dashboard.html
order: 1
translated: 012a9e1fdd9e1752
---
点击顶部的齿轮图标，打开**设置**。其中包含以下标签页：

- **账号**：顶部有**你的地址**（会被视为你的地址）和**退出登录**。托管版Machine还会显示你的套餐、账单、Fleet、好友、登录信息和数据，**取消套餐**和**删除账号**位于最底部。在你自己的电脑上运行、并已配对Network的Machine中，会显示你的Fleet、用户名、好友和登录信息，每项都附有链接，可打开账号中的对应部分（并在那里登录），**删除账号**位于底部。尚未配对时，顶部会显示**加入Network**。请参阅[套餐和账单](plans-and-billing.md)。
- **常规**：语言和地区、此设备、语音输入、你的Machine使用的浏览器、Fleet、导出和导入，以及Machine运行的版本。没有“账号”标签页时，末尾会显示**加入Network**。
- **安全**：**标准**或**谨慎**。请参阅[安全级别](security-levels.md)。开启**支持访问权限**后，这里也会显示该选项，请参阅[获取支持](get-support.md#support-access)。
- **动态**：The Machine为你做过的所有事，最新的排在最前面。请参阅[动态](activity.md)。
- **通知**：哪些内容会发送到哪里，以及你的工作时间。请参阅[通知](notifications.md)和[工作时间](work-hours.md)。
- **写作**：签名和你的写作风格。请参阅[写作](writing.md)。
- **技能**：你的Machine会遵循的操作指南。请参阅[技能](skills.md)。
- **应用**：The Machine的手机和电脑应用，以及你连接的Claude、ChatGPT等AI和它们各自可以执行的操作。在电脑上，这里会列出适用于Windows、Mac和Linux的桌面应用，每个应用旁都有**下载**按钮，并标记出**这台电脑**上正在使用的应用。请参阅[手机应用](mobile-app.md)、[桌面应用](desktop-app.md)和[连接其他AI](ai-connections.md)。
- **模型**：为你阅读和起草内容的AI，以及它的限制。请参阅[模型](model.md)。这里还包含**Codex和Claude Code**，请参阅[转交给Claude Code或Codex](hand-to-agent.md)。下方还有**按含义搜索**。

没有内容可显示的标签页会隐藏。

## 常规

- **语言和地区**：**地区**决定日期、时间和数字的显示方式（Oct 24或24 Oct）。**时间格式**可选择12小时制（2:05 PM）或24小时制（14:05）。待办、Telegram、摘要和Fleet消息都会采用这些设置。托管版Machine会使用你注册时选择的时区。
- **语言**：English、Nederlands、Français、Deutsch、Español、Italiano、Português (Brasil)、简体中文、日本語、한국어或Русский。默认使用浏览器的语言。选择语言后，控制面板、帮助、通知、Telegram、每周回顾，以及你的Machine撰写的待办都会立即切换语言。之前的文字保持原样。队友会用自己的语言收到Fleet和Family问题，发给其他人的草稿则会使用对应对话的语言。
- **此设备**：仅适用于当前浏览器或手机的**安装应用**、**通知**（含**发送测试**）和**浅色模式**。请参阅[安装应用并开启通知](phone-app.md)。使用[Omarchy](omarchy.md)时，还会显示**Omarchy主题**。
- **语音输入**：设置说出的话如何转换成文字，以及实时交谈时使用的声音。请参阅[语音输入](voice-input.md)和[实时语音对话](talk-live.md)。
- **打开Machine的浏览器 ↗**：你的Machine用于访问LinkedIn等网站的浏览器。
- **Fleet规则**：请参阅[分享规则](sharing-rules.md)。
- **导出**：
  - **全部**：将你的Machine知道的所有内容导出到一个加密文件中，方便迁移或保存；也可以使用**导入**导入文件。请参阅[迁移到另一台电脑](moving.md)。
  - **给另一个AI的知识**：将你的Machine学到的内容导出为任何AI都能读取的文件。请参阅[给另一个AI的知识](knowledge-export.md)。

## 版本

你的Machine当前运行的版本。更新会自动安装。托管版Machine有新版本可用时，点击**立即更新**即可马上安装。安装需要几分钟，你的数据会保留。

在你自己的电脑上，Linux会通过每日定时任务安装每个经过签名的新版本。请参阅[在自己的电脑上运行](self-hosted-setup.md)。

## 按含义搜索

在**设置**中的**模型**下。它可以根据邮件、消息和笔记的内容含义进行查找，而不只是匹配文字。托管版Machine会在Machine本机上使用一个小型AI完成搜索，不会将任何内容发送到其他地方。内存达到8 GB时，此功能默认开启。内存为4 GB时，可通过开关开启。它大约会占用半个GB内存，因此繁忙的Machine可能会变慢。关闭后，待办准备流程仍会按文字查找相关消息。

在你自己的电脑上，它是`embeddings`中的`config.json`模块。修改后请重启Machine。

## 在这台Machine上

如果你的Machine运行在自己的电脑上，以下操作会在终端中完成：

- 设置文件`config.json`：所有设置都集中在一处。修改后请重启Machine。
- `assistant connect`：添加数据源，例如`assistant connect gmail`或`assistant connect outlook`。
- `assistant telegram on`或`off`：Telegram上的消息。请参阅[Telegram](telegram.md)。
- `assistant doctor`：检查所有内容，并为每个问题输出修复方法。

## 你的地址

这里会列出Machine找到的所有你的地址：你的账号、Gmail或Outlook别名、日历、Slack和Intercom个人资料。来自这些地址的邮件和会议都会被视为与你有关。对于不属于你的地址，点击**移除**。

info@或Google Group这类共享地址不会自动被视为你的地址。Machine不确定归属的地址会显示在**可能是你的**下。请选择一项：

- **只有我来回复**：将其视为你的地址。发到这里的邮件可能会成为你的待办。
- **团队负责：其他人也会回复**：这不是你的地址。只发送到该地址的邮件不会为你生成待办或草稿，但仍会补充到Graph中。
- **不是我的**：不将其视为你的地址。

根据现在由谁回复来选择。像support@这样的团队收件箱属于团队。像partnerships@这样只有你回复的地址则属于你。等其他人也开始回复时，再切换设置。

之后可以点击对应行中的**更改**来切换设置。你自己的登录地址始终属于你。

### 你公司的域名

你自己的地址所属的域名会被视为你公司的域名。你还会使用其他域名吗？例如，除了acme.com还使用acme.co？在**你公司的域名**下输入该域名，然后点击**添加**。

这些域名下的人员会被视为同事，而不是客户：他们的对话不会进入Team Graph，也不会为其创建组织。点击**移除**即可删除域名。不能添加gmail.com等免费邮箱域名。

如果Gmail确认你可以使用自己的某个别名发送邮件，该别名也可以作为草稿的**发件人**。请参阅[Gmail](gmail.md#what-it-can-send)。
