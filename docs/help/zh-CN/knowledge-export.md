---
title: 给另一个AI的知识
area: settings
summary: 把你的Machine学到的内容带到其他AI中，以任何AI都能读取的普通文件形式保存。
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: db1c7f4768a71630
---
你的Machine学到的一切都属于你。你可以把这些内容交给其他AI，例如ChatGPT或Claude，也可以留着自己用。

## 导出

1. 前往**设置** › **常规** › **导出**，点击**给另一个AI的知识**旁边的**导出**。
2. **消息内容**默认关闭：导出内容只会注明每项信息的来源和时间。开启后，文件中也会包含消息内容。
3. 只有在需要包含仅自己可见的项目、私密对话和谨慎Fleet时，才开启**私密且谨慎**。
4. 你也可以设置**密码短语**（至少10个字符），为文件加密。
5. 点击**下载**。文件只能下载一次。

托管版Machine和运行在自己电脑上的Machine，操作方式相同。

## 文件内容

- 人员、组织和项目：每项各有一个Markdown页面，并说明彼此的关系。
- 事实和偏好：你的Machine了解的关于你和他们的信息。
- 过往事实：已失效（已结束或被替代）的信息，以及替代它的内容。你删除的事实不会包含在内。
- 规则、写作风格和签名：草稿遵循的内容。
- 技能：你的操作指南，以及已开启或已关闭的技能。
- 上下文：团队简介、摘要、承诺和未完成的待办。
- 来源：每项信息的来源，按ID和日期标注。

联系人和待办也会以电子表格（CSV）形式提供。文件顶部的README会告诉AI如何读取所有内容。将zip文件上传到AI，作为知识文件或项目使用。

## 不会包含的内容

密码、密钥和登录信息绝不会包含在内。队友的数据、设置和照片也不会包含在内。如需迁移整个Machine，请参阅[迁移到另一台电脑](moving.md)。

开发者请参阅：[文件格式](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md)。
