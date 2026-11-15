---
title: RSS 源
area: connections
summary: 你关注的 RSS 或 Atom 源中的帖子。
covers: connector:rss
code: connectors/rss.py
site: More sources
translated: efeb27dadc6163e9
---
## 读取的内容

每个连接只读取一个 RSS 或 Atom 源中的新帖子。每个源都要单独添加。

每 30 分钟读取一次源，读取间隔不会短于 15 分钟。只读取公开的 https:// 地址。

## 可以执行的操作

什么也不能。它只读取源。

## 连接

1. 在控制面板中，打开 **连接**，然后选择 **其他**，再选择 RSS 源。在托管版 Machine 上，也可以在设置页面的 **更多来源** 下找到它。在自己的电脑上，也可以运行 `assistant connect rss`。
2. 粘贴源地址。

## 移除

在控制面板中，打开 **连接**，选择这个源，再打开 **详情**，然后选择 **断开连接**。其他地方不需要卸载任何内容。
