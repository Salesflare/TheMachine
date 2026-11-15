---
title: Android通知
area: connections
summary: 通过OpenClaw应用获取Android手机上的通知。它只读取通知。
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 344d64dafc75a0a9
---
## 它会读取什么

通过OpenClaw应用获取Android手机上的通知。不会读取一次性验证码，也不会读取WhatsApp、Telegram、Signal和Discord的通知。

## 它能做什么

它无法操作手机，只会读取通知。

## 连接

在托管的Machine上：

1. 在手机上从Google Play安装OpenClaw。
2. 在控制面板中打开**连接**，然后选择**其他**，再选Android手机并点击**显示设置码**。
3. 在OpenClaw应用中添加Gateway并扫描设置码。然后回到控制面板，点击**批准**。
4. 应用询问时，允许访问通知。然后在应用的设置中开启“转发通知事件”，这样通知一到就会转发，而不只是每10分钟检查一次。

在自己的电脑上，先在OpenClaw应用中配对手机，然后运行`assistant connect android`。

## 移除连接

- 在控制面板中：打开**连接**，选择Android，点击**详情**，然后选择**断开连接**。
- 在托管的Machine上，也可以在设置页面中点击它旁边的**移除**。

## 在手机上移除

在Android设置中关闭OpenClaw应用的通知访问权限，或在OpenClaw应用中取消配对手机。
