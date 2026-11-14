---
title: Google Meet
area: connections
summary: 你组织的Meet会议转录稿和Gemini笔记。只读取内容。
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
translated: cea7230915b5a536
---
## 它会读取什么

你组织的Google Meet会议转录稿和Gemini笔记。Meet生成这些内容后，它会读取你连接时最近7天内的内容，以及之后新增的内容。Meet会保留这些内容30天。

只有在会议期间开启了转录或Gemini笔记，Meet才会生成这些内容。

每份内容都会关联到Calendar中的对应会议：Gemini笔记显示在Notes下，转录稿显示在Transcript下，并标记为**来自Google Meet**。你自己添加的内容会保留。

## 它能做什么

它不会在Meet、Docs或Drive中执行任何操作，只会读取内容，也不会自行开启转录。

## 它需要哪些权限

它需要单独授权，与邮件权限分开。Google会请求允许The Machine：

- 查看你的Google Meet会议、转录稿和Gemini笔记。
- 查看你的Google Docs，以读取Gemini笔记文档。

它不会请求访问你的Drive。Gmail和Calendar的访问权限保持不变。

## 连接

你不需要连接Gmail。连接方法如下：

- 托管版Machine：在控制面板中打开**连接**、**会议**，选择**Google Meet**，然后点击**使用Google登录**。授予上述权限后，你会返回控制面板。
- 在自己的电脑上使用已关联账号：步骤相同。登录页面会在新标签页中打开。

如果没有授予Meet权限，就不会添加它。你不需要粘贴任何内容，也不需要续期。

如果之后撤销权限，**连接**中的Google Meet会提示你重新登录。

## 移除连接

在控制面板中打开**连接**，选择Google Meet，点击**详情**，然后点击**断开连接**。它已经导入的内容会保留。

## 在Google中撤销权限

打开myaccount.google.com/permissions，移除The Machine对Google Meet的访问权限。Gmail和Calendar仍可正常使用。
