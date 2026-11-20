---
title: 给另一个AI的知识
area: settings
summary: 把你的 Machine 学到的内容带到其他 AI 中，以任何 AI 都能读取的普通文件形式保存。
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: db1c7f4768a71630
---
你的 Machine 学到的一切都属于你。你可以把这些内容交给其他 AI，例如 ChatGPT 或 Claude，也可以留着自己用。

## 导出

1. 前往 **设置** › **常规** › **导出**，点击 **给另一个AI的知识** 旁边的 **导出**。
2. **消息内容** 默认关闭：导出内容只会注明每项信息的来源和时间。开启后，文件中也会包含消息内容。
3. 只有在需要包含仅自己可见的项目、私密对话和谨慎 Fleet 时，才开启 **私密且谨慎**。
4. 你也可以设置 **密码短语**（至少 10 个字符），为文件加密。
5. 点击 **下载**。文件只能下载一次。

托管版 Machine 和运行在自己电脑上的 Machine，操作方式相同。

## 文件内容

- 人员、组织和项目：每项各有一个 Markdown 页面，并说明彼此的关系。
- 事实和偏好：你的 Machine 了解的关于你和他们的信息。
- 过往事实：已失效（已结束或被替代）的信息，以及替代它的内容。你删除的事实不会包含在内。
- 规则、写作风格和签名：草稿遵循的内容。
- 技能：你的操作指南，以及已开启或已关闭的技能。
- 上下文：团队简介、摘要、承诺和未完成的待办。
- 来源：每项信息的来源，按 ID 和日期标注。

联系人和待办也会以电子表格（CSV）形式提供。文件顶部的 README 会告诉 AI 如何读取所有内容。将 zip 文件上传到 AI，作为知识文件或项目使用。

## 不会包含的内容

密码、密钥和登录信息绝不会包含在内。队友的数据、设置和照片也不会包含在内。如需迁移整个 Machine，请参阅[迁移到另一台电脑](moving.md)。

开发者请参阅：[文件格式](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md)。
