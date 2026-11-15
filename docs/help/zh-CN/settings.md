---
title: 设置
area: settings
summary: 了解各项设置的位置，从浅色模式到安全和账号设置。
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
点击顶部的齿轮图标打开**设置**。其中包含这些标签页：

- **账号**：顶部显示**你的地址**（被视为你的地址）和**退出登录**。托管版The Machine还会显示你的套餐、发票、Fleet、好友、登录信息和数据，页面最底部有**取消套餐**和**删除账号**。在自己的电脑上运行并已连接Network的Machine：显示你的Fleet、用户名、好友和登录信息，每项都有一个链接，可打开账号中的对应页面（在那里登录）；页面底部有**删除账号**。尚未连接Network：页面顶部会显示**加入Network**。参阅[套餐和账单](plans-and-billing.md)。
- **常规**：语言和地区、此设备、语音输入、你的Machine使用的浏览器、Fleet、导出和导入，以及当前运行的版本。如果没有账号标签页，**加入Network**会显示在最后。
- **安全**：标准或谨慎。参阅[安全级别](security-levels.md)。此外还有**支持访问权限**，开启时可以使用。参阅[获取支持](get-support.md#support-access)。
- **动态**：The Machine为你完成的所有操作，最新的排在最前面。参阅[动态](activity.md)。
- **通知**：通知会发到哪里，以及你的工作时间。参阅[通知](notifications.md)和[工作时间](work-hours.md)。
- **正在撰写**：签名和写作风格。参阅[写作](writing.md)。
- **技能**：The Machine会遵循的操作指南。参阅[技能](skills.md)。
- **应用**：The Machine的手机和电脑应用，接着是你连接的Claude、ChatGPT和其他AI，以及它们各自能执行的操作。参阅[手机应用](mobile-app.md)和[连接其他AI](ai-connections.md)。
- **模型**：为你阅读和撰写内容的AI，以及它的限制。参阅[模型](model.md)。此外还有**Codex和Claude Code**，参阅[交给Claude Code或Codex处理](hand-to-agent.md)。还有下方的**按含义搜索**。

没有内容可显示的标签页会隐藏。

## 常规

- **语言和地区**：**地区**决定日期、时间和数字的显示格式（Oct 24或24 Oct）。**时间格式**可选择12小时制（2:05 PM）或24小时制（14:05）。待办、Telegram、摘要和Fleet消息都会使用这两项设置。托管版The Machine会使用你注册时选择的时区。
- **语言**：可选English、Nederlands、Français、Deutsch、Español、Italiano、Português (Brasil)、简体中文、日本語、한국어或Русский。默认使用浏览器的语言。切换语言后，控制面板、帮助中心、通知、Telegram、每周回顾，以及The Machine撰写的待办会立即切换。旧文本保持原样。队友收到的Fleet和家庭问题会使用各自的语言；写给其他人的草稿则会使用对应对话的语言。
- **此设备**：仅对当前浏览器或手机生效的**安装应用**、**通知**（可**发送测试**）和**浅色模式**。参阅[安装应用并开启通知](phone-app.md)。使用[Omarchy](omarchy.md)时，还可以设置**Omarchy主题**。
- **语音输入**：设置语音转文字的方式，以及实时通话的声音。参阅[语音输入](voice-input.md)和[实时通话](talk-live.md)。
- **打开The Machine的浏览器 ↗**：The Machine用于访问LinkedIn等网站的浏览器。
- **Fleet 规则**：参阅[共享规则](sharing-rules.md)。
- **导出**：
  - **全部**：将The Machine掌握的所有内容放进一个加密文件，方便迁移或保存；也可以用**导入**导入文件。参阅[迁移到另一台电脑](moving.md)。
  - **给另一个AI的知识**：将The Machine学到的内容导出为任何AI都能读取的文件。参阅[给另一个AI的知识](knowledge-export.md)。

## 版本

The Machine当前运行的版本。更新会自动安装。托管版The Machine有新版本可用时，点击**立即更新**即可马上安装。安装需要几分钟，你的数据会保留。

在自己的电脑上运行时，Linux会通过每日定时任务安装每个经过签名的新版本。参阅[在自己的电脑上运行](self-hosted-setup.md)。

## 按含义搜索

在**设置**的**模型**中。搜索邮件、消息和笔记时，会根据内容主题查找，而不只是匹配其中的词语。托管版The Machine会在本机上用一个小型AI进行搜索，不会向任何地方发送数据。内存达到8 GB时，此功能会自动开启。内存为4 GB时，可以用开关开启。它会占用约半个GB的内存，因此The Machine繁忙时可能会变慢。

在自己的电脑上运行时，它是`embeddings`中`config.json`的区块。更改后请重启Machine。

## 在这台Machine上

如果The Machine在自己的电脑上运行，以下操作会在终端中完成：

- 设置文件`config.json`：所有设置都集中在这里。更改后请重启Machine。
- `assistant connect`：添加来源，例如`assistant connect gmail`或`assistant connect outlook`。
- `assistant telegram on`或`off`：Telegram消息。参阅[Telegram](telegram.md)。
- `assistant doctor`：检查所有内容，并为每个问题打印修复方法。

## 你的地址

The Machine找到的所有你的地址：你的账号、Gmail或Outlook别名、日历、Slack和Intercom个人资料。来自其中任一地址的邮件和会议都会被视为与你有关。不是你的地址，可以点击**移除**。

共享地址（例如info@或Google群组）不会自动被视为你的地址。The Machine不确定归属的地址会列在**可能是你的**下。请选择一项：

- **只有我来回复**：此地址会被视为你的地址。发到这里的邮件可以变成你的待办。
- **团队负责：其他人也会回复**：此地址不属于你。只发到这里的邮件不会为你生成待办或草稿，但仍会补充到Graph中。
- **不是我的**：此地址不会被视为你的地址。

根据现在由谁回复来选择。像support@这样的团队收件箱属于团队。像partnerships@这样只有你回复的地址属于你。如果之后也有其他人回复，就更改设置。

以后可以点击该地址所在行的**更改**来切换设置。你自己的登录地址始终属于你。

### 你公司的域名

你自己的地址所用的域名会被视为你公司的域名。如果你还使用其他域名，例如除了acme.com还使用acme.co，请在**你公司的域名**下输入，然后点击**添加**。

这些域名下的人会被视为同事，而不是客户：相关对话不会显示在Team Graph中，也不会为其创建组织。点击**移除**即可删除域名。不能添加gmail.com等免费邮箱域名。

如果Gmail确认你可以使用自己的Gmail别名发信，该别名也可以作为草稿的**来自**地址。参阅[Gmail](gmail.md#what-it-can-send)。
