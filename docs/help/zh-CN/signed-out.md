---
title: 网站已将你登出
area: troubleshooting
summary: LinkedIn 或 X 将你的 Machine 登出了。重新登录一次，或保存登录信息以便下次使用。
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: da165847c9a9d091
---
LinkedIn 和 X 等网站会在你的 Machine 自带的浏览器中打开。有时，网站会让它退出登录。

## 重新登录

**连接**和待办事项顶部会显示已退出登录。点击**在此登录**，然后在控制面板的小窗口中登录。

勾选**保存以备下次使用**，下次遇到这种情况时，只需点一下就能重新登录。密码会加密保存在你的 Machine 上，AI 永远看不到。

## 密码和验证码

请自行输入密码。两步验证的验证码也需要你自己输入。

已保存的登录方式位于**连接**下的**登录方式**。点击**忘记**即可移除一项。

## 如果网站拒绝登录或要求进行机器人验证

LinkedIn、X 以及使用 Cloudflare 验证的网站，通常会拒绝来自云端浏览器的登录。在托管的 Machine 上，登录页面会显示**通过家中网络登录**。点击后会打开设置页面，你可以通过 Tailscale 或自己的代理，让 Machine 的浏览器通过家中网络访问互联网。然后再次登录。

如果是在自己的电脑上，则不需要这样做，因为电脑上的浏览器已经在家中网络里。
