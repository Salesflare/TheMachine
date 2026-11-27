---
title: 桌面应用
area: getting-started
summary: The Machine可在Windows、Mac和Linux上使用：在独立窗口中打开你的仪表板，屏幕角落里还有一个机器人。
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: af0a8a2994af969d
---
桌面应用会在独立窗口中打开你的仪表板。屏幕角落里有一个小机器人，点击它即可添加待办、询问消息相关问题，或查看待你处理的事项。这还是一个原型。

## 下载

每个链接始终提供最新版本：

- Windows 10或11，64位：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac，macOS 13或更高版本：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux，64位：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、适用于Ubuntu和Debian的[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)，或适用于Arch和Omarchy的[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

你的仪表板里也有这些下载链接。在电脑上，进入“**设置**”>“**应用**”，可以看到这三个版本，你正在使用的电脑旁会显示“**这台电脑**”。“**充分利用The Machine**”待办中有“**下载桌面应用**”，点击后会下载适用于你电脑的版本，或打开下方的Linux安装步骤。应用登录到你的Machine后，这项待办就会消失。手机上或桌面应用内都不会显示这些内容。

## Windows

打开安装程序即可。它只为你安装，不需要管理员权限，并由Salesflare签名。如果电脑之前没有使用过WebView2，还需要几秒钟来安装它，完成后应用会立即启动。应用会自动更新，进入“**设置**”即可查看新版本何时备好。

## Mac

解压zip文件，将The Machine移到“应用程序”文件夹，然后在那里打开。macOS首次会询问是否打开来自互联网的应用，选择“**打开**”即可。应用已签名并经过公证，而且会自动更新。

## Linux

- 适用于任何发行版：运行`chmod +x`，让AppImage变为可执行文件，然后启动它。如果提示缺少FUSE，请安装`fuse3`。
- 适用于Ubuntu 22.04、Debian 12或更高版本：`sudo apt install ./the-machine-desktop-amd64.deb`。其中包含WebKitGTK和gtk-layer-shell。
- 适用于Arch和Omarchy：将PKGBUILD放入一个空文件夹，然后在该文件夹中运行`makepkg -si`。它会下载对应版本，根据文件中的校验和进行检查，然后安装。在Omarchy使用的Hyprland上，机器人会显示在其他窗口上方，且不会占用自己的窗口。

如果AppImage放在你的文件夹中，例如~/Applications，它会自动更新。进入“**设置**”即可查看新版本何时备好。.deb和Arch软件包由apt和pacman管理：进入“**设置**”可查看是否有更新版本，并点击“**下载**”获取对应的.deb或PKGBUILD。解压到文件夹中的AppImage不会自动更新，请直接使用AppImage文件。

## 检查下载文件

每个文件都有GitHub的构建溯源信息，可证明它是由The Machine自己的工作流根据The Machine的代码构建的。使用[GitHub CLI](https://cli.github.com)：`gh attestation verify <file> -R Salesflare/TheMachine`。

## 登录

首次启动时，窗口会打开登录页面。对于托管的Machine或The Machine Network上的Machine，应用会在浏览器中打开你的账号页面，然后返回应用。自托管的Machine需要填写自己的地址，该地址需在你的Tailscale网络中的电脑上访问。

你Machine上的页面可以通过专属链接将应用调到前台：`computer.themachine.desktop://open`。该链接只会打开应用，不会携带任何内容。

如果想改用Chrome或Edge将仪表板作为应用使用，请参阅[安装应用](phone-app.md)。

## 机器人

应用窗口位于前台时，机器人会隐藏；切换到其他窗口，或最小化、关闭应用窗口后，机器人会重新出现。如果你有多个显示器，机器人会出现在应用窗口所在的显示器上，直到你将它拖到其他位置（在Hyprland、Sway和KDE上，它会显示在主显示器上）。如需关闭或开启机器人：点击“**设置**”（Ctrl+逗号，Mac上按Command+逗号），然后选择“**显示机器人**”。
