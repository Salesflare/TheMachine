---
title: Slack
area: connections
summary: 你加入的频道和私信。只有你批准后才会发送私信。
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
---
## 它会读取什么

你加入的对话：频道、私密频道、私信和群组消息。连接时会读取最近7天的消息，之后读取所有新消息。它不会自行加入频道或打开对话。安静的频道大约每天读取一次；待办需要最新消息时，The Machine会立即读取。

大约一年的旧消息会在之后逐步作为[历史记录](history.md)导入。

联系人显示为姓名，应用显示为应用名称，不会显示Slack ID。Slack账号已停用的人会显示为以前的Slack用户。

## 它可以发送什么

以你的身份向一个人发送私信，但只有你在待办中批准后才会发送。回复待办来源的Slack消息时，回复会发到该消息所在私信或频道的话题串中；草稿会显示**在话题串中**。它不会在频道中发布新消息。

## 连接

1. 依次点击**连接**、**聊天**、**Slack**和**使用Slack登录**，然后在Slack中允许连接。在自己的电脑上使用前，请先将它与themachine.computer上的账号配对。
2. 新消息和私信会优先导入。Slack允许应用每分钟读取大约一个对话，因此旧消息会在几小时内逐步导入。

也可以使用Maton API密钥：登录maton.ai，在那里连接Slack，然后从Home复制Maton API密钥。接着打开Slack下方的**或使用Maton API密钥**并粘贴密钥，或者在自己的电脑上运行`assistant connect slack`。通过Maton连接的Slack会继续正常工作。

## 移除连接

- 在控制面板中：点击**连接**，打开Slack，点击**详情**，然后点击**断开连接**。已经导入的内容会保留。
- 如果使用托管版Machine，也可以在设置页面中点击Slack旁边的**移除**。

## 在Slack中卸载

使用Slack登录：在Slack中打开工作区的“管理应用”页面，然后移除The Machine。通过Maton连接：在Maton中移除Slack连接，并删除你提供的Maton API密钥。Slack管理员也可以在工作区的“管理应用”中移除任一应用。
