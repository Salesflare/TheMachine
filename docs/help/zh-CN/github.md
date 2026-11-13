---
title: GitHub
area: connections
summary: 查看审核请求、提及、指派和失败的CI运行。只有你确认后才会创建议题。
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## 会读取哪些内容

你的GitHub通知：审核请求、提及、指派、回复和失败的CI运行。它不会将通知标记为已读。

## 可以做什么

读取内容不会更改GitHub上的任何内容。如果待办最后一步需要在GitHub上执行操作，例如创建议题，待办会说明这一点，并且只有在你点击**确认**，或在聊天中明确要求执行完全相同的操作后，才会运行这一步。截图会通过你的Machine中的浏览器上传。如果没有连接GitHub，待办会说明将使用浏览器，并显示**连接GitHub**。

## 连接

在托管版Machine上：

1. 打开**连接**，然后选择**项目和代码**，再选择GitHub。
2. 选择**工作**或**个人**，然后点击**使用GitHub登录**。
3. 点击**打开GitHub ↗**，输入显示的代码并授权。连接会自动完成。

app.themachine.computer/setup上的设置页面也可以在**更多来源**下使用相同的登录方式。

在你自己的电脑上：

1. 打开**连接**，然后选择**项目和代码**，再选择GitHub。
2. 选择对应公司的**工作**，或选择**个人**，然后点击**连接**。
3. 如果系统提示，点击**打开GitHub ↗**，输入代码并授权。连接会自动完成。

或者运行`assistant connect github`并确认你的GitHub登录。

## 移除

- 打开**连接**，然后依次选择GitHub、**详情**和**断开连接**。它会停止读取。已导入的内容会保留。
- 在托管版Machine上，你也可以在设置页面中点击它旁边的**移除**。

## 在GitHub上卸载

在GitHub上，打开设置、应用、已授权的OAuth应用，然后撤销GitHub CLI的授权。在你自己的电脑上，运行`gh auth logout`也会退出登录。
