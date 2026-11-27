---
title: 桌面应用
area: getting-started
summary: Windows、Mac和Linux上的The Machine：独立窗口中的仪表盘，以及屏幕角落里的机器人。
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
桌面应用会在独立窗口中打开你的仪表盘。屏幕角落里有个小机器人：点击它即可添加待办、询问消息相关问题，或查看待你处理的内容。这是一个原型。

## 下载

每个链接始终指向最新版本：

- Windows 10或11，64位：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac，macOS 13或更新版本：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux，64位：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、适用于Ubuntu和Debian的[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)，或适用于Arch和Omarchy的[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

## Windows

打开安装程序。它只会为你安装，无需管理员权限，并且由Salesflare签名。在之前没有任何程序使用过WebView2的电脑上，准备WebView2会多花几秒钟，完成后应用会立即启动。应用会自动更新：有新版本可用时，**设置**中会显示提示。

## Mac

解压zip，将The Machine移到“应用程序”文件夹，然后从那里打开。macOS会询问一次是否打开来自互联网的应用：选择**打开**。应用经过签名和公证，并会自动更新。

## Linux

- 适用于所有发行版：运行`chmod +x`，让AppImage变为可执行文件，然后启动它。如果提示缺少FUSE，请安装`fuse3`。
- Ubuntu 22.04、Debian 12或更新版本：`sudo apt install ./the-machine-desktop-amd64.deb`。它会一并安装WebKitGTK和gtk-layer-shell。
- Arch和Omarchy：将PKGBUILD放进一个空文件夹，然后在该文件夹中运行`makepkg -si`。它会下载对应版本，根据文件中的校验和进行验证，然后安装。在Omarchy使用的Hyprland上，机器人会显示在其他窗口上方，而且不会有自己的窗口。

Linux上的应用不会自动更新。要安装新版本，请重新下载文件或更新后的PKGBUILD。

## 验证下载

每个文件都有GitHub的构建来源证明，表明它由The Machine自己的工作流基于The Machine代码构建。使用[GitHub CLI](https://cli.github.com)：`gh attestation verify <file> -R Salesflare/TheMachine`。

## 登录

首次启动时，应用窗口会打开登录页面。如果使用托管的Machine或The Machine Network上的Machine，应用会在浏览器中打开你的账号页面，然后返回应用。自托管的Machine需要填写它自己的地址，该地址必须能从Tailscale网络中的电脑访问。

如果想改用Chrome或Edge将仪表盘安装为应用，请参阅[安装应用](phone-app.md)。
