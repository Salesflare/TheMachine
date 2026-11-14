---
title: Telegram
area: connections
summary: 通过自己的机器人在Telegram接收待办，按钮与仪表板上的相同。此功能为可选。
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## 功能

在Telegram中通过自己的机器人，在你的[工作时间](work-hours.md)内接收待办。每条待办都附有仪表板上的按钮：**执行**、**稍后处理**、**要求修改**、**标记为已完成**、**不需要**，以及用于发送预先拟好消息的**发送**。如果你想让The Machine读取你的Telegram聊天，请参阅[Telegram聊天](telegram-chats.md)。

此功能为可选：手机应用也会以通知形式发送相同的待办。

## 可以发送什么

机器人只会向你发送消息。向其他人发送消息仍需你在待办中批准。

## 连接机器人

在托管的Machine上：

1. 在Telegram中给@BotFather发消息，并发送/newbot。复制它提供给你的令牌。
2. 在设置页面的**随时添加更多**下，打开Telegram，粘贴令牌，然后点击**添加我的机器人**。

你可以随时添加机器人。

在自己的电脑上，安装程序会询问你是否要添加机器人；你也可以使用自己的Telegram用户ID运行`assistant telegram on`。

## 移除机器人

- 在托管的Machine上：在设置页面点击**断开Telegram连接**。你的机器人及其令牌会从The Machine中移除。
- 在自己的电脑上：`assistant telegram off`。添加`--remove-bot`，即可同时忘记这个机器人。

## 在Telegram中删除机器人

给@BotFather发消息，发送/deletebot，然后选择你的机器人。
