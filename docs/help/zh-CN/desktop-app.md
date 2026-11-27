---
title: 桌面应用
area: getting-started
summary: 在Windows、Mac和Linux上使用The Machine：在独立窗口中查看你的仪表盘，还能在屏幕一角看到一个机器人。
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
桌面应用会在独立窗口中打开你的仪表盘。屏幕一角还会有一个小机器人，点击它即可添加待办、询问消息相关问题，或查看待你处理的内容。这是一个原型。

## 下载

每个链接始终提供最新版本：

- Windows 10或11，64位：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac，macOS 13或更高版本：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux，64位：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、适用于Ubuntu和Debian的[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)，或适用于Arch和Omarchy的[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

你的仪表盘中也有这些下载链接。在电脑上，“**设置**”>“**应用**”会列出这三种应用，你正在使用的电脑旁会标注**这台电脑**。**充分利用The Machine**待办中有**下载桌面应用**，点击后会下载适用于你电脑的版本，或打开下方的Linux安装步骤。登录你的Machine后，这条待办就会消失。手机上或桌面应用中都不会显示这些内容。

## Windows

打开安装程序即可。它只为你安装，无需管理员权限，并由Salesflare签名。如果电脑上之前没有应用使用过WebView2，首次准备WebView2会多花几秒，完成后应用就会立即启动。应用会自动更新；有新版本可用时，应用的设置中会显示提示。

## Mac

解压zip文件，将The Machine移到“应用程序”文件夹，然后从那里打开。macOS第一次会询问是否打开从互联网下载的应用：选择“打开”即可。应用已签名并经过公证，还会自动更新。

## Linux

- 适用于任何发行版：运行`chmod +x`，将AppImage设为可执行文件并启动。如果提示缺少FUSE，请安装`fuse3`。
- 适用于Ubuntu 22.04、Debian 12或更高版本：运行`sudo apt install ./the-machine-desktop-amd64.deb`。它会一并安装WebKitGTK和gtk-layer-shell。
- 适用于Arch和Omarchy：将PKGBUILD放入一个空文件夹，然后在该文件夹中运行`makepkg -si`。它会下载对应版本，与文件中的校验和进行核对，然后完成安装。在Hyprland上（Omarchy默认使用Hyprland），机器人会显示在其他窗口上方，且不会单独占用一个窗口。

如果AppImage放在你的文件夹中（例如~/Applications），它会自动更新；有新版本可用时，应用的设置中会显示提示。.deb和Arch软件包由apt和pacman管理：有更新版本时，设置中会显示提示，并提供适用于.deb或PKGBUILD的下载选项。解压到文件夹中的AppImage不会自动更新，请直接使用AppImage文件。

## 检查下载文件

每个文件都包含GitHub构建来源信息，可证明它是由The Machine自己的工作流从The Machine代码构建的。使用[GitHub CLI](https://cli.github.com)：`gh attestation verify <file> -R Salesflare/TheMachine`。

## 登录

首次打开时，窗口会显示登录页面。如果使用托管的Machine或The Machine Network上的Machine，应用会在浏览器中打开你的账号，登录后再返回应用。自托管的Machine需要填写它自己的地址，该地址需在Tailscale网络中的电脑上访问。

如果想改用Chrome或Edge将仪表盘安装为应用，请参阅[安装应用](phone-app.md)。

## 机器人

应用窗口位于最前方时，机器人会隐藏；切换到其他窗口，或最小化、关闭应用窗口后，机器人会重新出现。如果有多台显示器，机器人会显示在应用窗口所在的屏幕上，也可以拖到其他屏幕上（在Hyprland、Sway和KDE上，机器人会显示在主屏幕上）。要开启或关闭机器人：打开设置（Ctrl+comma；Mac上为Command-comma），选择“显示机器人”。
