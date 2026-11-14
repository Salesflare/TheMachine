---
title: 让浏览器通过家里的网络连接
area: troubleshooting
summary: 通过Tailscale让托管的Machine浏览器使用家里的网络，这样网站就会接受登录。
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
translated: 9935ac3c09fa5c00
---
有些网站（例如LinkedIn、X，以及需要通过Cloudflare检查的网站）会拒绝来自云端浏览器的登录。你可以在设置页面通过Tailscale，让托管的Machine浏览器改用家里的网络。Tailscale免费，设置大约需要10分钟，大部分步骤会自动完成。

## 设置

1. 在设置页面中，找到Machine的浏览器，选择**Tailscale**，然后点击**登录Tailscale**。登录或免费注册一个账号。
2. 在家里找一台常年开机的电脑，安装Tailscale并使用同一个账号登录。不要用手机，手机会休眠。
3. 将这台电脑设为出口节点。设置页面会显示对应系统的菜单。Linux用户运行`sudo tailscale set --advertise-exit-node`。
4. 点击**在Tailscale中打开**并允许设置：Machine设置、编辑路由设置、用作出口节点、保存。在同一个菜单中，选择禁用密钥过期。

设置页面会自动勾选已完成的步骤。只有一个出口节点时，浏览器会立即开始使用它。如果有多个出口节点，选择一个，然后点击**使用此出口节点**。

## 检查

点击**测试**。页面会显示网站看到的浏览器位置，包括所在城市和互联网服务提供商。

## 家里的电脑关机时

浏览器会直接通过Machine连接网络；电脑重新开机后，浏览器会恢复通过家里的网络连接。Tailscale已退出登录？点击**重新登录**。如果未关闭密钥过期，Tailscale会在6个月后让设备退出登录。设置页面会显示日期。

## 停止使用

点击**停止使用**，即可恢复直接连接。选择**同时退出Tailscale**，也会让Machine的浏览器退出Tailscale。之后，Tailscale管理控制台会将其列为“已过期”，你可以在那里将其移除。
