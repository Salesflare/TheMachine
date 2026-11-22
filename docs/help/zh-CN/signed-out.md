---
title: 已退出网站
area: troubleshooting
summary: LinkedIn或X让你的Machine退出了登录。重新登录一次，或保存登录信息以便下次使用。
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js, dashboard/connections-login-import.js
order: 2
translated: 9a9b91270954c031
---
LinkedIn和X等网站会在你的Machine自带的浏览器中打开。有时，网站会让它退出登录。

## 重新登录

**连接**和待办顶部会显示已退出登录。点击**在此登录**，然后在控制面板的小窗口中登录。

勾选**保存以备下次使用**，下次遇到这种情况时就能点一下重新登录。密码会加密保存在你的Machine上，AI不会看到密码。如果同一个网站有多个账号，**另存为**可以为这个账号命名（工作、个人），如果待办里没有说明要用哪个账号，对话框会询问你。

## 密码和验证码

请自己输入密码。两步验证的验证码也需要你自己输入。

已保存的登录信息位于**连接**中的**登录方式**。点击**忘记**即可移除一项。点击**导入**可以从密码管理器导入登录信息，方式是在Machine的浏览器中打开密码管理器自带的导出页面，或导入导出文件。

## 如果网站拒绝登录或要求机器人验证

LinkedIn、X以及使用Cloudflare验证的网站，通常会拒绝来自云端浏览器的登录。在托管的Machine上，登录界面会显示**通过家中网络登录**。点击后会打开设置页面，你可以让Machine的浏览器通过Tailscale使用家中网络，或通过自己的代理连接互联网。然后重新登录。

在自己的电脑上不需要这样做，因为电脑的浏览器已经在家中网络上。
