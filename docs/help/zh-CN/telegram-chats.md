---
title: Telegram聊天
area: connections
summary: 像使用自己账号的设备一样读取你的Telegram聊天和小群组。只有你批准后才会回复。
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## 读取哪些内容

读取你自己Telegram账号中的私聊和最多50人的群组，就像Telegram Desktop一样。连接后会读取最近7天的消息，之后读取新收到的消息。

不会读取频道、机器人、已保存的消息或Telegram自己的服务消息。已静音和归档的聊天也会跳过。

不会影响你的已读和在线状态：不会将任何消息标记为已读，你的手机仍会把新消息显示为新消息。

这与[Telegram](telegram.md)是分开的。在那里，你自己的机器人会把待办发给你。

## 可以发送哪些内容

可以向已有聊天发送一条文字消息，但只有你在待办中批准后才会发送。消息会一条一条发出，中间会有间隔。

如果待办是通过邮件收到的，但你平时在Telegram上和对方聊天，可以在待办的聊天中说明。The Machine会找到你和对方已有的聊天，并将草稿切换到Telegram，供你检查和发送。它不会新建聊天。

## 连接

1. 在控制面板中打开**连接**，再打开**聊天**，然后选择Telegram聊天。
2. 选择**用另一台设备上的Telegram扫描二维码**。
3. 在手机上打开Telegram，依次进入设置、设备，选择**关联桌面设备**，然后扫描二维码。
4. 如果你的账号设置了云密码，请按提示输入。密码会发送给Telegram，不会被保存。

在手机上，表单会优先显示**获取发送到手机号的验证码**，因为你无法在同一个屏幕上扫描二维码。表单会说明Telegram将验证码发送到了哪里：你另一台设备上的Telegram应用、短信或登录邮箱。没有收到验证码？点击**重新发送验证码**。

在自己的电脑上，你还需要一个自己的Telegram应用ID。前往[my.telegram.org](https://my.telegram.org)，在API开发工具中创建应用ID，然后在表单中填写api_id和api_hash。

也可以在终端中运行`assistant connect telegram`，然后扫描终端中显示的二维码。

## 连接中断时

- **已退出Telegram**：Telegram结束了此设备的登录，或者你在手机上将它退出。前往**连接**，点击**重新连接**。
- **Telegram不再接受此应用ID**：Telegram不再接受此The Machine使用的应用ID。在你点击**重新连接**并添加自己的应用ID之前，不会读取或发送任何内容。

Telegram可能会限制或结束来自The Machine等应用的登录。

## 图片

对于Graph中没有头像的人，The Machine会通过读取聊天时使用的同一登录，向Telegram请求其头像。每天最多请求50个，而且只针对出现在可读取聊天中的人。不会向他们发送任何内容。如果有人不让你查看头像，The Machine就不会为其添加头像。

## 移除

打开**连接**，进入Telegram聊天，选择**详情**，然后点击**断开连接**。你的Machine会退出Telegram，并删除为Telegram保存的内容。

或者在手机上结束会话：在Telegram中打开设置、设备，点按The Machine，然后结束会话。
