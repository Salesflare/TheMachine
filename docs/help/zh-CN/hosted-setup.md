---
title: 设置托管版Machine
area: getting-started
summary: 登录，开启免费试用，连接邮箱并选择AI，只需几分钟。
code: onboarding.py, dashboard.html
site: Mail and Calendar, Your AI, Continue with Google, Continue with Microsoft, Turn on, Add more any time, More sources, Open your dashboard, Sources, Ask for a source, Build it, Add a passkey, Use an authenticator app instead, Add to Claude, Back
order: 1
translated: 45dda198434fcd3a
---
托管版Machine在欧盟的云端运行，只为你服务。我们会负责保持它运行并及时更新。

## 注册

1. 前往app.themachine.computer，点击**使用Google继续**或**使用Microsoft继续**，创建账号。使用Google时，同一页面会询问你是否连接Gmail和Google日历。允许连接后，邮箱就会连好，无需再经过一次Google授权页面。
2. 选择Machine的规格和地址。前{trial_days}天免费，试用结束前不会扣费。如果设置过程中没有要求添加银行卡，请在试用结束前前往账号页面添加。
3. 点击**添加通行密钥**，然后使用指纹、面容或设备PIN。如果更喜欢使用身份验证器应用，请打开**改用身份验证器应用**，扫描二维码，输入六位数代码，然后点击**开启**。请保存接下来显示的恢复码。

## 设置页面

设置过程每个页面完成一个步骤：选择套餐、设置通行密钥，然后设置**邮件和日历**和**你的AI**。页面顶部会显示当前步骤。Machine会在后台启动，无需等待。

1. **邮件和日历**：点击**连接Google**或**连接Microsoft**。系统会先使用你注册时用的账号。如果注册时已允许连接Gmail和Google日历，这一步会自动跳过，直接进入AI设置。系统会根据邮箱地址判断它是工作邮箱还是个人邮箱，你可以稍后在账号中更改。请参阅[Gmail](gmail.md)和[Microsoft](microsoft.md)。
2. **你的AI**：登录ChatGPT或Claude，或者粘贴AI服务提供商给你的密钥。使用Claude时，请粘贴Claude页面上的代码。还没有套餐？可以获取ChatGPT或Claude，也可以使用密钥：此步骤会链接到各服务提供商的密钥页面，费用由服务提供商按使用量收取。请参阅[ChatGPT](chatgpt.md)。
点击**返回**或使用浏览器的后退按钮，即可返回上一步。邮箱和AI都连接好后，你就会进入控制面板。

你的首批待办会出现在这里：Machine会先检查最新邮件，然后检查最近7天的邮件。如果没有需要你处理的内容，它会说明读过哪些邮件，以及接下来可以连接哪些服务。如果检查失败，系统会在几分钟内重试；如果一直失败，列表会显示相关提示。

设置过程中不会询问任何可选内容。完成后，你随时可以在设置页面点击**随时添加更多**，然后选择**更多来源**，例如Slack、WhatsApp、GitHub、[Telegram](telegram.md)和[Codex](hand-to-agent.md)。如果有帮助，控制面板也会推荐来源，例如在持续收到相关邮件后推荐GitHub。

Machine准备就绪后，页面顶部会显示**打开你的控制面板**。点击**添加到Claude**，即可向Claude询问邮件和待办。要接收通知，请将The Machine添加到手机主屏幕：请参阅[安装应用并开启通知](phone-app.md)。

## 申请新来源

找不到需要的来源？前往**来源**，在**申请新来源**下填写服务名称和要读取的内容，然后点击**开始构建**。你自己的AI会在你的Machine上构建并测试它。如果你选择分享，The Machine会代你将它发布到GitHub，供所有人使用。无需GitHub账号；[连接GitHub](github.md)后即可获得署名。

## 稍后继续

设置页面会一直保留在app.themachine.computer/setup。你可以随时在此添加或移除来源。在控制面板中，点击**设置**，然后选择**打开账号**。
