---
title: Omarchy
area: settings
summary: 在Omarchy上，控制面板会跟随Omarchy主题，并随主题切换。
covers: omarchy
code: machine/omarchy.py, dashboard/settings-omarchy.js
order: 7
keywords: omarchy, theme, colors, hyprland, arch, linux, desktop
translated: 44bd9921ac59483e
---
## 跟随Omarchy主题

当你的Machine在安装了[Omarchy](https://omarchy.org)的电脑上运行时，控制面板会像Omarchy自带的应用一样，跟随Omarchy主题。它会采用当前主题的配色，无论是浅色还是深色，并在几秒内随主题切换，无需重新加载。

默认情况下，该电脑上的浏览器或桌面应用会开启此功能，其他电脑上则会关闭，直到你手动开启。你可以在**设置**、**常规**、**此设备**中的**Omarchy主题**里开启或关闭此功能，选择会一直保留。开启后，**浅色模式**会隐藏，因为显示效果由主题决定。

## 读取的内容

此功能只会读取Omarchy为当前主题写入的颜色文件。它不会更改Omarchy自身的任何设置；没有安装Omarchy的电脑上也不会显示此设置。

将控制面板安装为应用后，它就会和其他应用一起显示在Omarchy启动器中。请参阅[安装应用并开启通知](phone-app.md)。
