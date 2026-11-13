---
title: Shortcut
area: connections
summary: 会改变状态的故事及其负责人和截止日期。它只读取数据。
covers: connector:shortcut
code: connectors/shortcut.py
site: Connect, More sources, Remove
---
## 读取内容

Shortcut工作区中会改变状态的故事，以及这些故事的负责人和截止日期。

## 能做什么

什么也做不了。即使Shortcut令牌允许执行更多操作，它也只读取数据。

## 连接

1. 如果使用托管版Machine：打开app.themachine.computer/setup中的设置页面，前往**更多来源**，然后打开Shortcut。如果使用自己的电脑：依次打开**连接**、**项目和代码**、Shortcut，或运行`assistant connect shortcut`。
2. 点击**获取令牌**。Shortcut会在新标签页中打开API令牌页面：创建令牌并复制。
3. 粘贴令牌，然后点击**连接**。系统会立即验证令牌，并显示连接的账号和工作区。

你有多个Shortcut工作区？令牌只能对应一个工作区，所以请先在Shortcut中切换到要连接的工作区。

## 移除连接

- 在控制面板中：打开**连接**，选择Shortcut，再依次打开**详情**和**断开连接**。已导入的内容会保留。
- 如果使用托管版Machine，也可以在设置页面中点击Shortcut旁边的**移除**。

## 在Shortcut中撤销令牌

在同一个API令牌页面中删除令牌。
