---
title: Slack
area: connections
summary: 你加入的频道和私信。只有你批准后，才会发送私信。
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
translated: 23f9e98f4680d23c
---
## 它会读取什么

你参与的对话：频道、私人频道、私信和群组消息。连接时会读取最近 7 天的消息，之后读取所有新消息。它不会自行加入频道或打开对话。安静的频道大约每天读取一次；待办需要查看最新消息时，The Machine 会立即读取。

之后会分批导入大约一年前的旧消息，详见[历史记录](history.md)。

联系人会显示姓名，应用会显示应用名称，不会显示 Slack ID。Slack 账号已注销的人会显示为 Slack 前用户。

## 它可以发送什么

只有在你批准待办后，才会以你的身份向一个人发送私信。回复待办来源的 Slack 消息时，会发到该消息所在的私信或频道讨论串中；草稿会显示 **在讨论串中**。它不会在频道中发布新消息。

## 它会保留什么

读取的内容会保存在你的 Machine 上，直到你删除这些内容或 Machine。托管服务不会保留你的消息副本或 Slack 登录信息，也不会使用你的 Slack 数据训练 AI 模型。The Machine 使用 AI，可能会出错，因此每条消息都会先让你查看，再发送。

## 连接

1. 依次选择 **连接**、**聊天**、**Slack**，然后选择 **使用 Slack 登录**，并在 Slack 中授权。如果使用自己的电脑，请先在 themachine.computer 上将它与你的账号配对。
2. 新消息和私信会优先导入。Slack 限制应用每分钟读取一段对话，因此旧消息会在几小时内逐步补齐。

也可以使用 Maton API 密钥：登录 maton.ai，在那里连接 Slack，然后从首页复制 Maton API 密钥。接着打开 Slack 下方的 **也可以使用Maton API密钥** 并粘贴密钥，或者在自己的电脑上运行 `assistant connect slack`。通过 Maton 连接的 Slack 会照常运行。

## 移除

- 在控制面板中：选择 **连接**，打开 Slack，选择 **详情**，然后选择 **断开连接**。已导入的内容会保留。
- 如果使用托管的 Machine，也可以在设置页面中选择它旁边的 **移除**。

## 在 Slack 中卸载

使用 Slack 登录：在 Slack 中打开工作区的「管理应用」页面，然后移除 The Machine。它会立即停止读取，并要求你重新登录；已导入的内容会保留。通过 Maton 连接：在 Maton 中移除 Slack 连接，并删除你提供的 Maton API 密钥。Slack 管理员也可以在工作区的「管理应用」中移除任一应用。
