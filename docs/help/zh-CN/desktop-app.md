---
title: 桌面应用
area: getting-started
summary: 在Windows、Mac和Linux上使用The Machine：在独立窗口中查看仪表板，还能让小机器人待在屏幕角落。
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
桌面应用会在独立窗口中打开你的仪表板。屏幕角落里会有一个小机器人：点击它即可添加待办、询问消息相关的问题，或查看待你处理的事项。目前这还是一个原型。

## 下载

每个链接始终提供最新版本：

- Windows 10或11，64位：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac，macOS 13或更高版本：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux，64位：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、适用于Ubuntu和Debian的[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)，或适用于Arch和Omarchy的[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

## Windows

打开安装程序即可。它只为你安装，无需管理员权限，并由Salesflare签名。如果电脑之前没有使用过WebView2，准备WebView2还需要几秒钟，之后应用会立即启动。应用会自动更新；有新版本时，**“设置”**中会显示提示。

## Mac

解压zip文件，将The Machine移到“应用程序”文件夹并在那里打开。macOS首次会询问是否打开来自互联网的应用：选择“打开”。应用已签名并经过公证，也会自动更新。

## Linux

- 任何发行版：运行`chmod +x`，为AppImage添加可执行权限，然后启动它。如果提示缺少FUSE，请在Arch上安装`fuse2`，或在Ubuntu 24.04上安装`libfuse2t64`。
- Ubuntu 22.04、Debian 12或更高版本：运行`sudo apt install ./the-machine-desktop-amd64.deb`。它会同时安装WebKitGTK和gtk-layer-shell。
- Arch和Omarchy：将PKGBUILD放入空文件夹，然后在该文件夹中运行`makepkg -si`。它会下载对应版本，根据文件中的校验和进行检查，然后安装。在Omarchy使用的Hyprland上，机器人会显示在其他窗口上方，且不会占用自己的窗口。

Linux版应用不会自动更新。要安装新版本，请重新下载文件或更新后的PKGBUILD。

## 登录

首次启动时，应用窗口会打开登录页面。如果使用托管版Machine或The Machine Network上的Machine，应用会在浏览器中打开你的账号页面，完成后再返回应用。自托管Machine需要填写其地址，这个地址可从Tailscale网络中的电脑访问。

如果想改用Chrome或Edge将仪表板作为应用使用，请参阅[安装应用](phone-app.md)。
