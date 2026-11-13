---
title: Gmail
area: connections
summary: 读取你的邮件，并用你的语气起草回复。只有你批准后，才会发送邮件。
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
---
## 读取哪些内容

你所有的邮件：连接时读取最近7天的邮件，之后读取所有新邮件，包括收件和发出的邮件。你发出的邮件也会计入，这样它就能学习你的写作方式和你做出的承诺。

促销、简报、更新和论坛邮件会先快速查看：发件人、主题和少量内容，一次查看多封。发现值得关注的邮件时，会完整读取，并可将其变成待办。不会有邮件未经查看就被跳过。

## 可以发送什么

可以发送待办中的邮件，但只有你批准后才会发送。**执行**会准备一份草稿；**检查并发送**会打开草稿供你编辑，在你点击**立即发送**之前，邮件不会发出。**使用Google登录**会同时请求Google授予发送权限。如果你在自己的电脑上使用自己的应用，登录权限默认为只读，除非你自行添加发送权限。

如果Gmail允许这个邮箱使用你的别名发信，检查页面中的**发件人**会显示一个小型选择器，其中一个别名会在设置的[你的地址](settings.md#your-addresses)中标记为**我的**。回复发到该别名的邮件时，会从这个别名发出；新邮件则会从你的邮箱地址发出。发送前，Gmail会再次确认：如果它没有确认这个地址，邮件就不会发送。

回复会进入所回复邮件所在的邮件会话。如果回复使用的邮箱不是收到原邮件的邮箱，待办会在发送前说明这一点。回复仍会进入对方的邮件会话。

## 连接

在托管版The Machine上：

1. 打开你的设置页面：app.themachine.computer/setup。
2. 在**邮件和日历**下，点击**连接Google**并登录。Google页面会显示The Machine的开发方Salesflare。
3. Gmail和Google Calendar会一起连接。

如果你使用Google注册，并在注册页面授权了Gmail和Calendar，它们会自动连接。只有你点击发送后，邮件才会发出。

也可以在控制面板中依次点击**连接**、**电子邮件**，选择Gmail，然后点击**使用Google登录**。完成后，你会回到控制面板。

在自己的电脑上，先[将它与你的账号配对](friends.md#a-machine-on-your-own-computer)，然后：

1. 在控制面板中打开**连接**，再打开**电子邮件**，然后选择Gmail。
2. 点击**使用Google登录**，并在打开的标签页中登录。Gmail和Google Calendar会一起连接。

如果尚未配对，或使用自己的Google OAuth客户端，请在此处打开**使用自己的应用**，或运行`assistant connect gmail`。点击**打开Google**并登录，然后粘贴Google跳转到的地址。同一地址对应的Google Calendar也会一并连接。

Google Workspace管理员可能需要先在管理控制台中允许此应用。

## 移除连接

- 在托管版The Machine上：在设置页面的邮箱地址旁点击**断开连接**。这会移除该地址对应的Gmail和Calendar连接，并让你的Machine忘记登录信息。你的其他Machine会保留各自的连接。在控制面板的连接页面点击**断开连接↗**即可前往设置页面。在那里点击**重新连接**，无需离开控制面板即可重新登录。
- 在自己的电脑上：打开**连接**，选择Gmail，点击**详情**，然后点击**断开连接**。它会停止读取邮件。已经导入的内容会保留。如果没有其他服务在使用这个Google登录信息，它就会忘记该信息。你的其他Machine会保留各自的连接。

## 在Google中卸载

在你的Google账号中，打开安全性，然后进入与第三方应用和服务的连接，移除Salesflare（使用Google登录或托管版），或移除你自己的应用。
