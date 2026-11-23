---
title: 设置
area: settings
summary: 查找各项设置的位置，从浅色模式到安全和账号。
covers: settings:general
code: dashboard.html
order: 1
translated: 31820c6221312d35
---
点击顶部的齿轮打开**设置**。其中的标签页包括：

- **账号**：顶部有**你的地址**（哪些地址会被视为你的地址）和**退出登录**。托管版Machine还会显示你的套餐、账单、Fleet、好友、登录和数据，**取消套餐**和**删除账号**在最底部。与Network配对的自有电脑上的Machine会显示你的Fleet、用户名、好友和登录，每项都附有链接，可打开账号的对应部分（在那里登录）；**删除账号**在底部。尚未配对时，顶部会显示**加入Network**。请参阅[套餐和账单](plans-and-billing.md)。
- **常规**：语言和地区、此设备、语音输入、你的Machine的浏览器、Fleet、导出和导入，以及当前运行的版本。没有“账号”标签页时，**加入Network**会显示在最后。
- **安全**：标准或谨慎。请参阅[安全级别](security-levels.md)。启用时还会显示**支持访问权限**：请参阅[获取支持](get-support.md#support-access)。
- **动态**：The Machine为你做过的所有事，按时间从新到旧排列。请参阅[动态](activity.md)。
- **通知**：哪些内容会发送到哪里，以及你的工作时间。请参阅[通知](notifications.md)和[工作时间](work-hours.md)。
- **写作**：签名和你的写作风格。请参阅[写作](writing.md)。
- **技能**：你的Machine会遵循的操作指南。请参阅[技能](skills.md)。
- **应用**：The Machine的手机和电脑应用，以及你连接的Claude、ChatGPT和其他AI，还有它们各自可以执行的操作。请参阅[手机应用](mobile-app.md)和[连接其他AI](ai-connections.md)。
- **模型**：为你阅读和起草内容的AI，以及它的限制。请参阅[模型](model.md)。这里还有**Codex和Claude Code**：请参阅[转交给Claude Code或Codex](hand-to-agent.md)。下方还有**按含义搜索**。

没有内容可显示的标签页会隐藏。

## 常规

- **语言和地区**：**地区**决定日期、时间和数字的显示方式（Oct 24或24 Oct）。**时间格式**可选择12小时制（2:05 PM）或24小时制（14:05）。待办、Telegram、摘要和Fleet消息都会采用这两项设置。托管版Machine会使用你注册时选择的时区。
- **语言**：English、Nederlands、Français、Deutsch、Español、Italiano、Português (Brasil)、简体中文、日本語、한국어或Русский。默认使用浏览器的语言。更改语言后，控制面板、帮助、通知、Telegram、每周回顾以及你的Machine撰写的待办会立即切换。旧文本保持原样。队友会用自己的语言收到Fleet和Family相关问题，发给其他人的草稿则会保持对话所用的语言。
- **此设备**：仅适用于当前浏览器或手机的**安装应用**、**通知**（含**发送测试**）和**浅色模式**。请参阅[安装应用并开启通知](phone-app.md)。使用[Omarchy](omarchy.md)时，还会显示**Omarchy主题**。
- **语音输入**：设置语音转文字的方式，以及实时对话的语音。请参阅[语音输入](voice-input.md)和[实时对话](talk-live.md)。
- **打开Machine的浏览器 ↗**：你的Machine访问LinkedIn等网站时使用的浏览器。
- **Fleet规则**：请参阅[分享规则](sharing-rules.md)。
- **导出**：
  - **全部**：将你的Machine掌握的所有内容导出到一个加密文件，方便迁移或留存；也可用**导入**导入文件。请参阅[迁移到另一台电脑](moving.md)。
  - **给另一个AI的知识**：将你的Machine学到的内容导出为任何AI都能读取的文件。请参阅[给另一个AI的知识](knowledge-export.md)。

## 版本

你的Machine当前运行的版本。更新会自动安装。托管版Machine有新版本可用时，点击**立即更新**即可安装。安装需要几分钟，你的数据会保留。

在自有电脑上，Linux会通过每日定时任务安装每个经过签名的新版本。请参阅[在自己的电脑上运行](self-hosted-setup.md)。

## 按含义搜索

在**设置**的**模型**中。它能根据内容主题而不只是文字本身查找邮件、消息和笔记。托管版Machine会在Machine本机上用一个小型AI进行搜索，不会向外发送任何内容。内存达到8 GB时，此功能会自动开启。内存为4 GB时，可用开关开启。它会占用约半GB内存，因此繁忙的Machine可能会变慢。关闭后，待办的准备过程仍会按关键词查找相关消息。

在自有电脑上，它是`embeddings`中`config.json`的配置块。更改后请重启Machine。

## 在这台Machine上

如果你的Machine在自有电脑上运行，有些操作会在电脑的终端中完成：

- 设置文件`config.json`：所有设置都集中在这里。更改后请重启Machine。
- `assistant connect`：添加来源，例如`assistant connect gmail`或`assistant connect outlook`。
- `assistant telegram on`或`off`：Telegram消息。请参阅[Telegram](telegram.md)。
- `assistant doctor`：检查所有内容，并为每个问题显示修复方法。

## 你的地址

Machine找到的所有你的地址：你的账号、Gmail或Outlook别名、日历、Slack和Intercom个人资料。来自这些地址的邮件和会议都会被视为与你有关。不是你的地址，请点击**移除**。

info@或Google群组这样的共享地址不会自动被视为你的地址。Machine无法确定的地址会列在**可能是你的**下。请选择一项：

- **只有我来回复**：该地址会被视为你的地址。发到这里的邮件可能会成为你的待办。
- **团队负责：其他人也会回复**：该地址不属于你。仅发送到该地址的邮件不会为你生成待办或草稿，但仍会补充到Graph中。
- **不是我的**：该地址不会被视为你的地址。

根据现在由谁回复来选择。support@这样的团队收件箱属于团队。partnerships@这样的地址如果只有你回复，就属于你。其他人也开始回复后，再切换设置。

点击地址所在行的**更改**，之后可随时切换。你自己的登录地址始终属于你。

### 你公司的域名

你自己的地址所属的域名会被视为你公司的域名。如果你还会使用其他域名，例如除了acme.com还使用acme.co，请在**你公司的域名**下输入，然后点击**添加**。

这些域名下的人会被视为同事，而不是客户：他们的对话不会出现在Team Graph中，也不会为其创建组织。点击**移除**即可删除域名。不能添加gmail.com等免费邮箱域名。

如果Gmail确认你可以使用自己的别名发信，该别名也可以作为草稿的**发件人**。请参阅[Gmail](gmail.md#what-it-can-send)。
