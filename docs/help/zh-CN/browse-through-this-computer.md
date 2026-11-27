---
title: 通过桌面应用浏览网页
area: troubleshooting
summary: 让托管的Machine通过桌面应用所在的电脑访问网站，这样网站看到的就是你自己的网络。
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
translated: 6da69c78d7e60574
---
有些网站（例如LinkedIn）会拒绝来自云端浏览器的登录。登录[桌面应用](desktop-app.md)后，托管的Machine就能通过这台电脑访问网站。这样，网站看到的就是你家里或办公室的网络，而不是数据中心。

## 开启此功能

你的Machine支持此功能后，默认就会开启。在桌面应用的**设置**中，开关名称是**让我的Machine通过这台电脑浏览网页**。关闭后，你的Machine浏览器会立即恢复直接访问网站。

你的Machine浏览器通过这台电脑访问网站时，机器人卡片以及菜单栏或任务栏中的应用图标会显示**你的Machine正在通过这台电脑浏览网页**。

## 流量会经过哪里

只有你的Machine浏览器访问网站时会经过这台电脑，范围仅限公共互联网地址的80和443端口。应用不会连接到这台电脑本身、你的家庭或办公室网络，也不会连接到其他私有地址；它不会在你的电脑上开放任何端口。流量上限为下载4 MB/s、上传1 MB/s，每天2 GB。

## 电脑关机时

你的Machine浏览器会直接从你的Machine访问网站。桌面应用再次运行后，流量就会重新通过这台电脑。
