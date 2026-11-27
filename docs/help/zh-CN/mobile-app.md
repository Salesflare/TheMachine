---
title: 手机应用
area: getting-started
summary: 在iPhone和Android上使用The Machine应用：接收待办通知，也可以从任何应用分享内容到The Machine。
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: aaf34f864dadf180
---
手机应用会打开你自己的控制面板，登录状态与网页版相同。iPhone和iPad用户可在[App Store](https://apps.apple.com/app/id6829875215)下载，Android用户可在[Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app)下载。

待办列表顶部的**充分利用The Machine**待办会推荐这个应用。在手机浏览器中，点击**获取**会打开应用商店。如果手机设置为显示桌面网站，则会显示两个应用商店的链接。在电脑上会显示二维码，可用手机扫描，也会显示两个应用商店的链接。

在任何手机上打开[themachine.computer/app](https://themachine.computer/app)，都会进入对应的应用商店。在电脑上，前往“设置”>“应用”，页面顶部会显示两个应用商店；在手机上则只显示对应的应用商店。在电脑上还会显示适用于Windows、Mac和Linux的桌面应用，详见[桌面应用](desktop-app.md)。

## 连接应用

托管版Machine会使用你的账号登录应用。对于自托管的Machine，请在电脑上打开“设置”>“应用”。在应用商店链接下方，**不在Network上？**会显示一个代码。安装应用后，用手机摄像头扫描代码，或在应用中输入代码下方显示的地址。应用会在连接前征求同意，你的Machine仍会要求你使用自己的登录方式登录。

在**连接**下点击某项服务旁的**使用……登录**（Shortcut、Notion、Slack、Zoom等），会打开手机的登录页面。完成登录后，你会回到应用，新的连接也会自动显示在**连接**中。

应用无法连接到你的Machine时，会告知你并自动重试。在Mac上，如果应用窗口从睡眠状态恢复后显示空白，应用也会自动重新打开页面；你正在输入的聊天消息也会恢复。在Mac或连接了键盘的iPad上，按Cmd+R可重新加载页面。

## 通知

应用首次打开时会询问是否允许发送通知。点击通知即可打开相关内容：待办会在列表中高亮显示；早间通知会打开今天的**日历**；团队简报会打开待办；Fleet问题会打开对应待办。待办内容不会经过Apple、Google或The Machine的服务传输：这些服务只会传递固定文本，例如“有待办需要你处理”。

随后，应用会向你自己的Machine请求待办标题和下一步操作，例如“回复Sam”，下一步是“发送给Sam：周二10:00可以”。早间通知会显示待处理事项和第一场会议的时间，团队简报会显示前几项内容，Fleet更新会显示发生了什么。无法连接到你的Machine时，通知会保留固定文本。在Android上，通知会显示待处理事项的数量，例如“有2项待办需要你处理”。

通知中有**稍后处理**（延至明天）和**标记为已完成**选项；尚未开始的待办还有**执行**选项。解锁手机后即可使用这些选项，无需打开应用。发送和最后步骤始终会打开应用。每项待办只会有一条通知：“正在准备”会变为“已备好”；待办完成或稍后处理后，无论在哪完成或处理，通知都会消失。

你确认的步骤完成后，通知会显示**已完成**和处理结果，直到你在待办页面点击**知道了**。在iPhone上，可以等到下次打开应用时再处理。

在“设置”>“安全”中关闭**通知中的文本**后，通知会保留固定文本。锁屏设置为隐藏通知内容时也一样。如果通知没有可显示的内容，就会显示“点击打开”。通知到达时，如果手机无法连接到你的Machine，等手机重新联网后就会显示详情。

通知遵循与网页版推送相同的规则：根据你在[通知](notifications.md)中为各类通知所做的选择、你的[工作时间](work-hours.md)，以及你正在使用控制面板时不发送通知。

每部装有应用的手机都会以**装有应用的手机**的形式显示在“设置”>“通知”中。点击**移除**即可停止向该手机发送通知。自托管的Machine需要连接The Machine Network才能发送通知；不连接也可以使用应用。

## 分享到The Machine

在任何应用中点击“分享”，然后选择The Machine。系统会打开**新建待办**，其中包含你分享的文字、链接或文件。检查内容，按需添加日期，然后添加待办。只有你确认添加后，内容才会保存。

只分享文件也可以，例如发票或信件。你的Machine会读取PDF中的文字，并填写待办内容：文件是什么、下一步该做什么，以及日期。文件会直接发送到你的Machine，并保存在那里。

在Android上，将控制面板安装为应用后，也可以接收分享内容：在分享菜单中选择控制面板即可。

应用中不会显示套餐和账单信息。“设置”中的**打开账号**选项仍然可用，可用于删除账号。
