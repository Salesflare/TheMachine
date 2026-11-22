---
title: 手机应用
area: getting-started
summary: 在iPhone和Android上通过应用使用The Machine：接收待办通知，也可以从任何应用分享内容到The Machine。
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 672364a90f92ef8f
---
手机应用会打开你的专属控制面板，登录状态与网页版相同。iPhone和iPad用户可从[App Store](https://apps.apple.com/app/id6829875215)下载，Android用户可从[Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app)下载。

待办列表顶部的**充分利用The Machine**待办会推荐手机应用。在手机浏览器中，点击**获取**会打开应用商店。如果手机设置为显示桌面版网站，则会显示两个应用商店的链接。在电脑上会显示一个二维码，可用手机扫描，也会显示两个应用商店的链接。

在任何手机上打开[themachine.computer/app](https://themachine.computer/app)，都会进入对应的应用商店。在电脑上，**设置**中的**应用**会在顶部显示两个应用商店；在手机上则只显示对应的应用商店。在电脑上，点击**电脑**可将控制面板安装为应用，详情请见[安装应用](phone-app.md)。

## 连接应用

托管版Machine会使用你的账户登录应用。对于自托管的Machine，请在电脑上打开**设置**中的**应用**：应用商店下方的**不在Network上？**会显示一个代码。安装应用后，用手机相机扫描代码，或在应用中输入代码下方显示的地址。应用会先征求你的同意再连接，你的Machine仍会使用自己的登录方式。

在**连接**中点击某项服务（Shortcut、Notion、Slack、Zoom等）的登录按钮，例如**使用Slack登录**，会打开手机的登录界面。登录完成后会返回应用，新的连接也会自动显示在**连接**中。

应用无法连接到你的Machine时，会提示你并自动重试。在Mac或带键盘的iPad上，按Cmd+R可重新加载页面。

## 通知

应用首次打开时会询问是否允许发送通知。点击通知即可打开相关内容：待办会在列表中高亮显示；早间通知会打开当天的**日历**；团队简报会打开待办；Fleet问题会打开对应的待办。待办内容不会经过Apple、Google或The Machine的服务传输，这些服务只会传递一条固定通知，例如“有一项待办需要你处理”。

随后，应用会向你的Machine请求待办标题和下一步内容，例如“回复Sam”，以及“发送给Sam：周二 10:00可以”。早间通知会显示待处理事项和首场会议的时间，团队简报会显示首批事项，Fleet更新会显示发生的情况。应用无法连接到你的Machine时，会保留固定通知内容。在Android上，通知还会显示待处理事项数量，例如“有2项待办需要你处理”。

通知上有**稍后处理**（推迟到明天）和**标记为已完成**，尚未开始的待办还会显示**执行**。解锁手机后即可使用这些操作，无需打开应用。发送内容和执行最后步骤时，始终会打开应用。每项待办只会有一条通知：“正在准备”会变为“已备好”；待办完成或稍后处理后，无论在哪完成，通知都会消失。

你确认的步骤完成后，通知会显示**已完成**和处理结果，直到你在待办中点击**知道了**。在iPhone上，可以等到下次打开应用时再处理。

在**设置**的**安全**中关闭**通知中的文本**后，通知只会保留固定内容。锁屏设置为隐藏通知内容时也一样。如果没有可显示的内容，通知会显示“轻点以打开”。如果通知到达时手机无法连接到你的Machine，恢复连接后便会显示详细内容。

通知遵循与网页版推送相同的规则：你在[通知](notifications.md)中为各类通知选择的设置、你的[工作时间](work-hours.md)，以及使用控制面板期间不发送通知。

每台装有应用的手机都会显示在**设置**的**通知**中，标为**装有应用的手机**。点击**移除**即可停止向该手机发送通知。自托管的Machine需要The Machine Network才能发送通知；没有通知时，应用仍可使用。

## 分享到The Machine

在任何应用中，点击“分享”并选择The Machine。系统会打开一个**新建待办**，其中已填入你分享的文本、链接或文件。检查内容，可按需添加日期，然后添加待办。只有你确认后，内容才会添加。

只分享一个文件也可以，例如发票或信件。你的Machine会读取PDF中的文本并填写待办内容：文件是什么、下一步要做什么，以及日期。文件会直接发送到你的Machine并保存在那里。

在Android上，安装为应用的控制面板也能接收分享内容：在分享菜单中选择它即可，操作方式相同。

应用中不会显示套餐和账单信息。**设置**中仍有**打开账户**，可用于删除账户。
