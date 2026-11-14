---
title: 电脑上的问题
area: troubleshooting
summary: 你的Machine会读取电脑自己的日志，告诉你实际发生的问题、原因和解决方法。只有你点按“执行”后，才会运行修复操作。
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: 1a191d8433bfba2a
---
## 读取哪些内容

在使用systemd的Linux上，你的Machine会读取你自己的用户会话日志：你自己的服务，以及你自己运行的程序的崩溃报告。在Omarchy上，它还会检查Hyprland和状态栏。它不会读取整个系统的日志，也不会要求更多权限。

它会读取哪个服务停止了、服务如何结束，以及哪个程序崩溃了。它不会读取日志行的内容，因此不会保留或将任何日志文本传出你的电脑。

## 哪些情况算问题

包括反复重启的服务、一天内多次失败或持续停止的服务、内存耗尽的服务，以及崩溃的程序。在Omarchy上，还包括Hyprland或状态栏崩溃，以及Hyprland设置中的错误。

单次重启或单次运行失败很常见，不会打扰你。服务偶尔失败几次后又恢复正常，也不会打扰你。

由测试和代理驱动的浏览器（无头模式、Playwright、Puppeteer、CI）不会触发提醒。服务正在停止或重启时停止的程序也不会触发提醒。开发运行也不会触发提醒，包括编程代理运行的程序、测试，以及从临时文件夹或缓存文件夹运行的程序。反复崩溃的程序会生成一条待办，说明崩溃的次数和时间。

脚本会显示自己的名称，例如backup.py，而不是python3或node。

## 你会看到什么

一条待办会用通俗易懂的文字说明发生了什么、为什么重要，以及你可以怎么做。点击“显示更多”可查看原因相关的命令。在待办的聊天中提问，The Machine就会进行调查。任何更改都要等你确认后才会进行，就像点按“执行”一样。

有安全的修复方法时，待办会显示“执行”。如果你自己的服务持续停止，它会重新启动服务；在Omarchy上，它会恢复状态栏。“执行”只会运行该命令，结果会显示在待办的聊天中。它绝不会操作The Machine自己的服务或OpenClaw Gateway。

同一个问题每两周最多生成一条待办，并且只会在对应待办关闭后生成。每天最多生成两条新待办。

## 在终端中

`assistant doctor`会列出过去一天内相同的问题。

## 其他电脑

在macOS、Windows和没有systemd的电脑上，它不会读取任何内容，并会在`assistant doctor`中说明。

托管版Machine的服务器由我们负责保持运行：服务器的问题会反馈给The Machine团队，不会作为待办发给你。

## 关闭此功能

在config.json中设置`"computer_logs": false`，然后重启服务。
