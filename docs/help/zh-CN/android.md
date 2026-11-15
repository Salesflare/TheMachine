---
title: Android 通知
area: connections
summary: 通过 OpenClaw 应用读取 Android 手机上的通知。它只读取通知。
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## 读取的内容

通过 OpenClaw 应用读取 Android 手机上的通知。不会读取一次性验证码，也不会读取 WhatsApp、Telegram、Signal 和 Discord 的通知。

## 可以做什么

无法在手机上执行任何操作，只能读取通知。

## 连接

使用托管的 Machine：

1. 在手机上从 Google Play 安装 OpenClaw。
2. 在仪表板中打开 **连接**，再选择 **其他**，找到 Android 通知，然后点 **显示设置代码**。
3. 在 OpenClaw 应用中添加 Gateway 并扫描代码。然后返回仪表板，点 **批准**。
4. 按提示允许应用访问通知。然后在应用设置中开启 **转发通知事件**，这样收到通知时就会立即转发，而不必等到每 10 分钟检查一次。

在自己的电脑上，先在 OpenClaw 应用中配对手机，然后运行 `assistant connect android`。

## 移除连接

- 在仪表板中：打开 **连接**，选择 Android，再点 **详情**，然后点 **断开连接**。
- 使用托管的 Machine 时，也可以在设置页面中点它旁边的 **移除**。

## 在手机上移除

在 Android 设置中关闭 OpenClaw 应用的通知访问权限，或在 OpenClaw 应用中取消配对手机。
