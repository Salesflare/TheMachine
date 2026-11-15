---
title: ChatGPT
area: connections
summary: 使用ChatGPT登录，即可按你的ChatGPT套餐运行The Machine，并导入ChatGPT技能。
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## 用途

使用ChatGPT登录后，The Machine会使用你的ChatGPT套餐来读取和撰写内容。The Machine本身没有AI：请求会直接发送给OpenAI，并遵循你的账户条款和OpenAI的条款。

## 登录

如果使用托管版The Machine，请在设置页面点击**使用ChatGPT登录**，然后在ChatGPT中输入页面显示的代码。之后退出了登录？点击**重新连接ChatGPT**。

如果OpenAI拒绝了代码，请打开[ChatGPT安全设置](https://chatgpt.com/settings/security)，滚动到页面底部，然后打开“为Codex、Excel、PowerPoint和Word启用设备代码登录”。接着重新输入代码。

没有看到这个开关？如果你使用的是工作账户（Business、Enterprise或Edu），请让ChatGPT管理员在[权限和角色](https://chatgpt.com/admin/permissions)下的“Codex和本地工作”中启用它。

在自己的电脑上，在终端中运行`openclaw models auth login`。

## 使用限制

ChatGPT套餐有5小时和每周使用限制。**设置**中的**模型**会显示每项限制的已用额度和重置时间。后台任务会在达到限制前很久就暂停，以便为你自己的聊天留出额度。达到限制后，控制面板顶部会显示重置时间。详见[模型](model.md)。

## 导入ChatGPT技能

在**设置**中，进入**技能**，点击**导入**，选择**来自ChatGPT**，然后点击**查找我的技能**。导入的只有技能说明。详见[技能](skills.md)。

## 移除

在设置页面选择其他模型（如果是在自己的电脑上使用，请按相同方式登录其他服务商）。如需在OpenAI一侧撤销访问权限，请在ChatGPT安全设置中退出该会话。
