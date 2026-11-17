---
title: 网站已退出登录
area: troubleshooting
summary: LinkedIn 或 X 让你的 Machine 退出了登录。你可以重新登录，也可以保存登录信息以便下次使用。
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js
order: 2
translated: 060f7ca4f870ad0a
---
你的 Machine 会通过自己的浏览器访问 LinkedIn 和 X 等网站。有时，网站会让它退出登录。

## 重新登录

**连接**和待办事项顶部会显示已退出登录。点击**在此登录**，然后在控制面板的小窗口中登录。

勾选**保存以备下次使用**，下次遇到这种情况时，只需点一下就能重新登录。密码会加密保存在你的 Machine 上，AI 永远不会看到密码。如果同一网站有多个账号，**另存为**可以为当前账号命名（工作、个人）。如果待办事项没有注明使用哪个账号，系统会询问你。

## 密码和验证码

请自行输入密码。两步验证代码也需要你自己输入。

已保存的登录信息位于**连接**中的**登录方式**。点击**忘记**即可删除一项。点击**导入**即可从密码管理器导入登录信息。

## 如果网站拒绝登录或要求进行人机验证

LinkedIn、X 以及使用 Cloudflare 验证的网站，通常会拒绝来自云端浏览器的登录。在托管的 Machine 上，登录界面会显示**通过家中网络登录**。点击后会打开设置页面，你可以让 Machine 的浏览器通过 Tailscale 使用家中网络，或通过你自己的代理访问互联网。然后重新登录。

如果使用自己的电脑，则无需这样做：电脑的浏览器已经连接到家中网络。
