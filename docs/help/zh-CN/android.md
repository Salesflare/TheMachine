---
title: Android通知
area: connections
summary: 通过OpenClaw应用读取Android手机上的通知。它只读取通知。
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## 读取的内容

通过OpenClaw应用读取Android手机上的通知。不会读取一次性验证码，也不会读取WhatsApp、Telegram、Signal和Discord的通知。

## 可以做什么

无法在手机上执行任何操作，只能读取通知。

## 连接

使用托管的Machine：

1. 在手机上从Google Play安装OpenClaw。
2. 在控制面板中打开**连接**，再选择**其他**，找到Android通知，然后点**显示设置码**。
3. 在OpenClaw应用中添加Gateway并扫描代码。然后返回控制面板，点**批准**。
4. 按提示允许应用访问通知。然后在应用设置中开启**Forward Notification Events**，这样收到通知时就会立即转发，而不必等到每10分钟检查一次。

在自己的电脑上，先在OpenClaw应用中配对手机，然后运行`assistant connect android`。

## 移除连接

- 在控制面板中：打开**连接**，选择Android，再点**详情**，然后点**断开连接**。
- 使用托管的Machine时，也可以在设置页面中点它旁边的**移除**。

## 在手机上移除

在Android设置中关闭OpenClaw应用的通知访问权限，或在OpenClaw应用中取消配对手机。
