---
title: 桌面应用
area: getting-started
summary: 在Windows、Mac和Linux上使用The Machine：在独立窗口中查看控制面板，还能在屏幕角落看到一个小机器人。
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
桌面应用会在独立窗口中打开控制面板。屏幕角落里还有一个小机器人：点击它可以添加待办、询问消息相关的问题，或查看待你处理的事项。这还是一个原型。

## 下载

每个链接始终提供最新版本：

- Windows 10或11，64位：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac，macOS 13或更新版本：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux，64位：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、适用于Ubuntu和Debian的[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)，或适用于Arch和Omarchy的[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

控制面板中也能找到这些下载。在电脑上，打开**设置**，再点**应用**，即可看到全部三个版本；当前电脑对应的版本会标有**这台电脑**。**充分利用The Machine**待办中有一项**下载桌面应用**，会下载适用于当前电脑的版本，或打开下方的Linux安装步骤。桌面应用登录你的Machine后，这项待办就会消失。手机上和桌面应用内都不会显示这些内容。

## Windows

打开安装程序即可。它只为你安装，不需要管理员权限，并由Salesflare签名。如果电脑之前没有应用使用过WebView2，首次安装时会多花几秒准备好WebView2，完成后应用会立即启动。应用会自动更新：有新版本可用时，可以在设置中看到提示。

## Mac

解压zip文件，将The Machine移到“应用程序”文件夹，然后从那里打开。macOS首次询问是否打开来自互联网的应用时，选择“打开”。应用经过签名和公证，并会自动更新。

## Linux

- 适用于任何发行版：运行`chmod +x`，将AppImage设为可执行文件后启动。如果提示缺少FUSE，请安装`fuse3`。
- 适用于Ubuntu 22.04、Debian 12或更新版本：运行`sudo apt install ./the-machine-desktop-amd64.deb`。它会一并安装WebKitGTK和gtk-layer-shell。
- 适用于Arch和Omarchy：将PKGBUILD放进一个空文件夹，然后在该文件夹中运行`makepkg -si`。它会下载对应版本，根据文件中的校验和验证下载内容，然后安装。在Omarchy使用的Hyprland上，小机器人会显示在其他窗口上方，且不会占用独立窗口。

Linux上的应用不会自动更新。要安装新版本，请重新下载文件或更新后的PKGBUILD。

## 验证下载

每个文件都有GitHub构建来源证明，表明它由The Machine自己的工作流根据The Machine的代码构建。使用[GitHub CLI](https://cli.github.com)：`gh attestation verify <file> -R Salesflare/TheMachine`。

## 登录

首次打开时，应用窗口会显示登录页面。如果使用托管的Machine或The Machine Network上的Machine，应用会在浏览器中打开你的账号页面，然后返回应用。自托管的Machine需要输入它自己的地址，可在Tailscale网络中的电脑上找到。

如果想改用Chrome或Edge将控制面板安装为应用，请参阅[安装应用](phone-app.md)。

## 小机器人

应用窗口在最前面时，小机器人会隐藏；切换到其他窗口、最小化应用或关闭窗口后，它会重新出现。如果有多个显示器，小机器人会出现在应用窗口所在的显示器上，直到你把它拖到别处为止（在Hyprland、Sway和KDE上，它会显示在主显示器上）。要关闭或开启小机器人，请打开**设置**（Ctrl+comma，Mac上为Command-comma），然后选择**显示机器人**。
