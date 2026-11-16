---
title: 手机应用
area: getting-started
summary: 在 iPhone 和 Android 上使用 The Machine 应用：接收待办通知，也可以从任何应用分享内容到 The Machine。
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: f622bdc266f69965
---
手机应用会打开你自己的控制面板，登录状态与网页版相同。iPhone 和 iPad 用户可前往 [App Store](https://apps.apple.com/app/id6829875215)，Android 用户可前往 [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) 下载应用。

待办列表顶部的 **充分利用The Machine** 待办会推荐你安装应用。在手机浏览器中，点按 **获取** 会打开应用商店。如果手机设置为显示桌面版网站，则会显示两个商店的链接。在电脑上会显示二维码，你可以用手机扫描，也会显示两个商店的链接。

在任何手机上打开 [themachine.computer/app](https://themachine.computer/app)，都会进入对应的应用商店。在电脑上，**设置** 中的 **应用** 会在顶部显示两个商店；在手机上则只显示对应的应用商店。在电脑上，**电脑** 会将控制面板安装为应用，详情请参阅[安装应用](phone-app.md)。

## 连接应用

在托管的 Machine 上，应用会使用你的账户登录。在自托管的 Machine 上，请在电脑上打开 **设置** 中的 **应用**：商店链接下方的 **不在Network上？** 会显示一个代码。安装应用后，用手机摄像头扫描代码，或者在应用中输入代码下方显示的地址。应用会先征求你的同意再连接，你的 Machine 仍会要求你正常登录。

在 **连接** 中点按某项服务下的 **使用其登录**（Shortcut、Notion、Slack、Zoom 等），会打开手机的登录页面。完成登录后会返回应用，新连接也会自动显示在 **连接** 中。

## 通知

应用首次打开时会询问是否允许发送通知。点按通知即可打开相关内容：待办会在列表中高亮显示；早间通知会打开今天的 **日历**；团队简报会打开待办；Fleet 问题会打开对应的待办。待办的文本不会经过 Apple、Google 或 The Machine 的服务，它们只会传递固定提示，例如“有一项待办需要你处理”。

随后，应用会向你自己的 Machine 请求待办标题和下一步，例如“回复 Sam”，以及“发送给 Sam：周二 10:00 可以”。早间通知会显示待办事项和第一场会议的时间，团队简报会显示开头几项，Fleet 更新会显示发生了什么。如果无法连接到你的 Machine，就会保留固定提示。在 Android 上，通知还会显示待办数量，例如“有 2 项待办需要你处理”。

通知提供 **稍后处理**（推迟到明天）和 **标记为已完成**，对于尚未开始的待办，还会提供 **执行**。解锁手机后即可使用这些操作，无需打开应用。发送内容和最后步骤始终会打开应用。每项待办只会有一条通知：“正在准备”会变成“已备好”；待办完成或稍后处理后，无论是在这里还是其他地方处理，通知都会消失。

你确认的步骤完成后，通知会显示 **已完成** 和处理结果，直到你在待办中点按 **知道了**。在 iPhone 上，这条通知可以一直保留到你下次打开应用。

在 **设置** 中的 **安全** 里关闭 **通知中的文本** 后，通知会保留固定提示。锁屏设置为隐藏通知内容时也是如此。如果没有内容可以显示，通知会提示“点按以打开”。如果通知到达时手机无法连接到你的 Machine，手机恢复联网后就会显示通知详情。

通知遵循与网页版推送相同的规则：包括你在[通知](notifications.md)中按类型选择的设置、你的[工作时间](work-hours.md)，以及使用控制面板时不会收到通知。

每台装有应用的手机都会以 **装有应用的手机** 显示在 **设置** 中的 **通知** 里。点按 **移除** 可停止向该手机发送通知。自托管的 Machine 需要 The Machine Network 才能发送通知；没有通知时，应用仍可使用。

## 分享到 The Machine

在任何应用中点按“分享”，然后选择 The Machine。打开的 **新建待办** 中会包含你分享的文本、链接或文件。检查内容，按需添加日期，然后添加待办。只有你确认后，内容才会添加。

只分享一个文件也可以，例如发票或信件。你的 Machine 会读取 PDF 中的文本并填写待办内容，包括文件是什么、下一步要做什么以及日期。文件会直接发送到你的 Machine 并保存在那里。

在 Android 上，安装为应用的控制面板也可以接收分享内容，只需像平常一样在分享面板中选择它。

应用中不会显示套餐和账单信息。**设置** 中仍有 **打开账户**，可供你删除账户。
