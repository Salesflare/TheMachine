---
title: 给另一个AI的知识
area: settings
summary: 把The Machine学到的内容带给其他AI，导出为任何AI都能读取的文件。
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
The Machine学到的一切都归你所有。你可以把这些内容交给ChatGPT或Claude等其他AI，也可以留着自己用。

## 导出

1. 依次前往**设置** › **常规** › **导出**，然后点击**给另一个AI的知识**旁边的**导出**。
2. **消息内容**默认关闭：只导出每项内容的来源和时间。开启后会一并导出消息内容。
3. 只有需要加入仅你可见的项目、私人聊天串和谨慎Fleet时，才开启**私密且谨慎**。
4. 你也可以设置**密码短语**（至少10个字符），为文件加密。
5. 点击**下载**。文件只能下载一次。

托管的The Machine和安装在自己电脑上的The Machine，导出方式相同。

## 导出内容

- 人员、组织和项目：每项内容各有一个Markdown页面，并说明它们之间的关系。
- 事实和偏好：The Machine对你和相关人员的了解。
- 过去的事实：不再成立的内容（已结束、搁置或替换），以及替换它的内容。你删除的事实不会导出。
- 规则、写作风格和签名：草稿所遵循的内容。
- 技能：已启用和已停用的操作指南。
- 上下文：团队简介、摘要、承诺和未完成的待办。
- 来源：每项内容的来源，按ID和日期记录。

联系人和待办也会以电子表格（CSV）的形式导出。文件顶部的README会告诉AI如何读取所有内容。将ZIP文件上传给AI，作为知识文件或项目即可。

## 不会导出的内容

密码、密钥和登录信息绝不会导出。团队成员的数据、设置和照片也不会导出。要迁移整个The Machine，请参阅[迁移到另一台电脑](moving.md)。

开发者可查看：[文件格式](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md)。
