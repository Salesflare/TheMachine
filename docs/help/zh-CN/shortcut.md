---
title: Shortcut
area: connections
summary: 状态发生变化的事项及其负责人和截止日期。The Machine只能读取数据。
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
translated: 68419e11fabc157c
---
## 读取的内容

Shortcut工作区中状态发生变化的事项，以及这些事项的负责人和截止日期。

## 可以执行的操作

无法在Shortcut中执行任何操作。The Machine只能读取数据。

## 连接

1. 在控制面板中依次选择：**连接**、**项目与代码**、Shortcut。也可以在托管版Machine的设置页面app.themachine.computer/setup中选择：**更多来源**、Shortcut。在自己的电脑上使用时，请先将它与你的账号配对。
2. 点击**使用Shortcut登录**，并允许读取权限。它只会向Shortcut请求读取权限。
3. 返回The Machine后，The Machine会立即检查登录状态，并显示连接的账号和工作区。

如果你有多个Shortcut工作区，请先在Shortcut中切换到要连接的工作区。要连接其他工作区，请再次添加Shortcut。

## 改用粘贴令牌

在**或粘贴API令牌**下方，点击**获取你的令牌**。Shortcut会在新标签页中打开API令牌页面：创建并复制令牌，然后粘贴并点击**连接**。在自己的电脑上使用时，`assistant connect shortcut`也会提示你输入令牌。令牌可以完全访问你的账号，但The Machine只会用它读取数据。

## 移除连接

- 在控制面板中选择**连接**，打开Shortcut，点击**详情**，然后点击**断开连接**。已导入的内容会保留。
- 在托管版Machine的设置页面中，也可以点击Shortcut旁边的**移除**。

## 在Shortcut中撤销访问权限

如果使用的是粘贴的令牌，请在API令牌页面将其删除。如果使用登录方式，在此处断开连接后，读取操作就会停止。
