---
title: 网站已将你退出登录
area: troubleshooting
summary: LinkedIn或X将你的Machine退出了登录。重新登录一次，或保存登录信息以便下次使用。
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
---
LinkedIn和X等网站会在你的Machine自带的浏览器中打开。有时，网站会将它退出登录。

## 重新登录

**连接**和待办列表顶部会提示你已退出登录。点击**重新登录**，然后在控制面板的小窗口中登录。

勾选**保存以备下次使用**，下次遇到这种情况时，只需点一下就能重新登录。密码会加密保存在你的Machine上，AI永远看不到。

## 密码和验证码

请自行输入密码。两步验证码也需要你来输入。

已保存的登录信息位于**连接**中的**登录方式**下。点击**忘记**即可删除一项。

## 如果网站拒绝登录或要求进行机器人验证

LinkedIn、X以及使用Cloudflare验证的网站，通常会拒绝来自云端浏览器的登录。在托管的Machine上，这时会显示**通过家中网络登录**。点击后会打开设置页面，你可以通过Tailscale或自己的代理，让Machine的浏览器使用家中网络连接互联网。然后重新登录。

如果使用自己的电脑，则不需要这样做：它的浏览器已经连接到家中网络。
