---
title: 移动应用
area: getting-started
summary: 在 iPhone 和 Android 上使用 The Machine 应用：接收待办通知，还能从任何应用分享内容到 The Machine。
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 0d4d41134db91fcc
---
移动应用会打开你自己的控制面板，登录状态与你在网页上的相同。iPhone 和 iPad 用户可从 [App Store](https://apps.apple.com/app/id6829875215) 获取，Android 用户可从 [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) 获取。

待办列表顶部的 **充分利用The Machine** 待办会推荐安装应用。在手机浏览器中，点按 **获取** 会打开应用商店。手机设置为显示桌面网站时，会显示两个应用商店的链接。在电脑上会显示二维码，供手机扫描，也会显示两个应用商店的链接。

在任何手机上打开 [themachine.computer/app](https://themachine.computer/app)，都会进入对应的应用商店。在手机上，**设置**中的**应用**会在顶部显示对应的应用商店；在电脑上则会显示两个应用商店。在电脑上，**电脑**可以将控制面板安装为应用：请参阅[安装应用](phone-app.md)。

## 连接应用

托管版 The Machine 会让应用使用你的账户登录。对于自托管的 The Machine，请在电脑上打开**设置**中的**应用**。应用商店链接下方的**不在Network上？**会显示一个代码。安装应用后，用手机摄像头扫描代码，或者在应用中输入代码下方显示的地址。应用会在连接前征求你的同意，你的 The Machine 仍会使用自己的登录方式。

## 通知

应用首次打开时会询问是否允许发送通知。点按通知即可查看相关内容：待办会在列表中高亮显示；早间简报会打开**日历**中的今天；团队简报会打开待办；Fleet 问题会打开对应待办。待办的文本不会经过 Apple、Google 或 The Machine 的服务，它们只会传递一条固定提示，例如「有待办需要你处理」。

之后，应用会向你的 The Machine 请求待办标题和下一步，例如「回复 Sam」，并附上「发送给 Sam：周二 10:00 可以」。早间简报会显示等待处理的事项和首场会议时间，团队简报会显示首批事项，Fleet 更新会显示发生了什么。如果应用无法连接到你的 The Machine，就会保留固定提示。在 Android 上，提示会显示等待处理的待办数量，例如「有 2 个待办需要你处理」。

通知提供**稍后处理**（推迟到明天）和**标记为已完成**；对于尚未开始的待办，还会提供**执行**。解锁手机后即可使用这些操作，无需打开应用。发送内容和最后的步骤始终会打开应用。每个待办只会有一条通知：「正在准备」会变为「已备好」；待办在此处或其他地方完成或推迟后，通知就会消失。

你确认的步骤执行成功后，通知会显示**已完成**以及执行结果，直到你在待办中点按**知道了**。在 iPhone 上，可以等到下次打开应用时再处理。

如果在**设置**的**安全**中关闭**通知中的文本**，通知就会保留固定提示。锁屏设置为隐藏通知内容时也一样。如果没有可显示的内容，通知会显示「点按以打开」。如果通知送达时手机无法连接到你的 The Machine，手机重新联网后就会显示详细内容。

通知遵循与网页推送相同的规则：你在[通知](notifications.md)中为每种类型选择的设置、你的[工作时间](work-hours.md)，以及使用控制面板时不显示通知。

每部安装了应用的手机都会作为**装有应用的手机**显示在**设置**的**通知**中。点按**移除**即可停止向这部手机发送通知。自托管的 The Machine 需要 The Machine Network 才能发送通知；应用本身不依赖通知也能使用。

## 分享到 The Machine

在任何应用中点按「分享」，然后选择 The Machine。应用会打开**新建待办**，并填入你分享的文本、链接或文件。检查内容，按需添加日期，然后添加待办。只有在你确认后，内容才会添加。

只分享文件也可以，例如发票或信件。你的 The Machine 会读取 PDF 中的文本并填写待办内容，包括事项、下一步和日期。文件会直接发送到你的 The Machine，并保存在那里。

在 Android 上，安装为应用的控制面板也能接收分享：在分享菜单中用同样的方式选择它。

应用中不会显示套餐和账单信息。**设置**中仍会保留**打开账户**，方便你删除账户。
