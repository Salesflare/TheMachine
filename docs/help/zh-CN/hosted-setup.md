---
title: 设置托管版The Machine
area: getting-started
summary: 登录、开始免费试用、连接邮箱并选择AI，只需几分钟。
code: onboarding.py, dashboard.html
site: Mail and Calendar, Your AI, Continue with Google, Continue with Microsoft, Turn on, Add more any time, More sources, Open your dashboard, Sources, Ask for a source, Build it, Add a passkey, Use an authenticator app instead, Add to Claude, First to-dos, Back
order: 1
translated: 0be6044113aaaa39
---
托管版The Machine在欧盟的云端运行，只供你使用。我们会让它持续运行并保持更新。

## 注册

1. 在app.themachine.computer上，点击**继续使用Google**或**继续使用Microsoft**，即可创建账户。使用Google时，同一页面会请求访问你的Gmail和日历。允许访问后，邮箱就会连接好，无需再打开另一个Google页面。
2. 选择The Machine的规格和地址。前{trial_days}天免费，到期前不会扣费。如果设置过程中没有要求你提供付款卡，请在此之前前往账户页面添加。
3. 点击**添加通行密钥**，然后使用指纹、面容或设备PIN码。如果你更想使用身份验证器应用，请打开**改用身份验证器应用**，扫描二维码，输入六位数代码，然后点击**开启**。请保存接下来显示的恢复代码。

## 设置页面

设置流程每个页面只有一个步骤：套餐、通行密钥，然后是**邮箱和日历**、**你的AI**和**第一批待办**。页面顶部会显示当前步骤。The Machine会在后台启动，你不用等待。

1. **邮箱和日历**：点击**连接Google**或**连接Microsoft**。系统会先使用你注册时的账户。如果你注册时已允许访问Gmail和日历，设置流程会跳过这一步，进入AI设置。系统会根据邮箱地址判断这是工作账户还是个人账户；之后可在账户页面更改。请参阅[Gmail](gmail.md)和[Microsoft](microsoft.md)。
2. **你的AI**：登录ChatGPT或Claude，或者粘贴AI服务提供商提供的密钥。使用Claude时，请粘贴Claude页面上的代码。如果你没有套餐，可以开通ChatGPT或Claude，或者使用密钥：此步骤会链接到各服务提供商的密钥页面，费用由服务提供商按使用量收取。请参阅[ChatGPT](chatgpt.md)。
3. **第一批待办**：The Machine会先检查最新邮件，然后检查最近7天的邮件。如果没有需要你处理的内容，它会告诉你已读取的内容，以及接下来可以连接什么。如果检查失败，会在几分钟内重试；如果一直失败，列表会显示相关提示。

点击**返回**或浏览器的后退按钮，即可回到上一步。邮箱和AI都设置好后，你就会进入控制面板。

设置过程中不会询问任何可选内容。之后，你随时可以在设置页面点击**随时添加更多**，再选择**更多来源**，例如Slack、WhatsApp、GitHub、[Telegram](telegram.md)和[Codex](hand-to-agent.md)。有帮助时，控制面板也会推荐来源，例如GitHub邮件不断到达时，会推荐连接GitHub。

The Machine准备好后，页面顶部会显示**打开你的控制面板**。点击**添加到Claude**，即可向Claude询问邮件和待办。要接收通知，请将The Machine添加到手机主屏幕：请参阅[安装应用并开启通知](phone-app.md)。

## 请求添加来源

找不到需要的来源？在**来源**页面的**请求添加来源**下，写明服务名称和要读取的内容，然后点击**构建**。你的AI会在The Machine上构建并测试来源。如果你选择分享，The Machine会帮你在GitHub上向所有人提供该来源。无需GitHub账户；[连接GitHub](github.md)即可获得署名。

## 稍后再回来

你的设置页面会保留在app.themachine.computer/setup。你可以随时在此添加或移除来源。在控制面板中，点击**设置**，再选择**打开账户**。
