---
title: Mistral
area: connections
summary: 使用Mistral的API密钥，让你的Machine运行Mistral模型。Le Chat Pro包含API额度。
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key, Keys, Remove
translated: 5d782f28fb69efef
---
## 适用场景

Mistral是一家欧洲AI服务商。添加Mistral API密钥后，你的Machine就能使用Mistral模型来阅读和起草内容。The Machine本身不提供AI服务：请求会直接发送给Mistral，并由你的账户承担，且受Mistral的条款约束。

## 获取密钥

Mistral不支持登录其他应用，因此需要使用API密钥。在[Mistral控制台](https://console.mistral.ai/)中打开API密钥页面，然后创建一个密钥。Le Chat Pro每月包含API额度；额度用完后，Mistral会按使用量收费。

## 连接

如果使用托管的Machine，请打开设置页面，前往“你的AI”，然后打开**其他AI服务**。选择Mistral作为服务商，粘贴密钥，然后点击**保存密钥**。你的Machine会先用密钥发送一个极小的请求进行测试。如果密钥有误，页面会立即显示错误，而且不会保存密钥。

Mistral Large会成为主模型。你也可以使用Mistral Small，它价格更低，可用于聊天或作为备用模型。

如果是在自己的电脑上使用，请参阅[模型指南](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md)。

## 使用情况

**设置**中的**模型**会显示“正在使用你的Mistral API密钥”。API密钥没有使用量限制，因此后台工作不会因此暂停。请参阅[模型](model.md)。

## 移除

在设置页面的“你的AI”下方，在**密钥**中找到Mistral，然后点击旁边的**移除**。密钥会从你的Machine中删除。如果Mistral正在运行主模型，另一个已连接的模型会接替它。要取消密钥本身，请在Mistral控制台中删除它。
