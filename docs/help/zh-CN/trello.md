---
title: Trello
area: connections
summary: 单个Trello看板上的卡片变更、评论和动态。仅可读取。
covers: connector:trello
code: connectors/trello.py
site: Sign in with Trello, Connect, More sources, Remove
translated: 7fc2a596ef58bd93
---
## 读取的内容

每个连接对应一个Trello看板，读取卡片变更、评论和动态。它不会将看板标记为已查看。

## 能做什么

它无法在Trello中执行任何操作，只能读取。

## 连接

1. 在控制面板中依次选择：**连接**、**项目和代码**、Trello。或者，在托管版Machine的设置页面app.themachine.computer/setup中选择：**更多来源**、Trello。在自己的电脑上使用时，请先将它与你的账号配对。
2. 点击**使用Trello登录**并授予读取权限。Trello会显示该应用由Salesflare开发。
3. 选择要关注的看板，然后点击**连接**。如需连接另一个看板，请再次添加Trello。

## 移除

- 在控制面板中选择**连接**，打开看板，依次点击**详情**、**断开连接**。已导入的内容会保留。
- 使用托管版Machine时，也可以在设置页面中点击Trello旁边的**移除**。

## 在Trello中撤销授权

在Trello账号设置的Applications下撤销The Machine的授权。
