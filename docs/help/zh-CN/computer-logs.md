---
title: 电脑上的问题
area: troubleshooting
summary: 你的 Machine 会读取电脑自身的日志，告诉你实际存在的问题、原因和解决办法。只有点击 **执行** 才会运行修复。
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: b18e5f4989d6baff
---
## 读取哪些内容

在使用 systemd 的 Linux 上，你的 Machine 会读取你自己的用户会话日志，包括你自己的服务和程序崩溃报告。在 Omarchy 上，它还会检查 Hyprland 和栏。它不会读取整个系统的日志，也不会要求更多权限。

它会读取哪个服务停止了、服务如何结束，以及哪个程序崩溃了，但不会读取日志行的具体内容。因此，日志文本不会被保存，也不会离开你的电脑。

## 哪些情况算问题

反复重启的服务、一天内多次失败或持续停止的服务、内存耗尽的服务，以及崩溃的程序。在 Omarchy 上，还包括 Hyprland 或栏崩溃，以及 Hyprland 设置中的错误。

单次重启或单次运行失败都很正常，不会通知你。服务失败几次后又恢复正常，也不会通知你。未启用且没有其他服务或计时器会启动的服务，即使失败了，也不会通知你。

由测试或代理驱动的浏览器（无头模式、Playwright、Puppeteer、CI）不会触发通知。服务正在停止或重启时随之停止的程序也不会触发通知。开发运行也不会触发通知，包括编码代理运行的程序、测试，以及从临时目录或缓存目录运行的程序。反复崩溃的程序只会生成一个待办，其中会说明发生的次数和时间。

脚本会按自身名称标记，例如 backup.py，而不是 python3 或 node。

## 你会看到什么

一个待办会用通俗的语言说明发生了什么、为什么重要，以及你可以怎么做。用于说明原因的命令位于 **查看更多** 中。在聊天中询问，The Machine 就会进一步调查。任何更改都会等你确认后才执行，包括点击 **执行**。

有安全的修复方法时，待办中会显示 **执行**。如果你的某项服务持续停止，它会重新启动该服务；在 Omarchy 上，它还会恢复栏的运行。点击 **执行** 只会运行对应的命令，结果会显示在该待办的聊天中。它绝不会影响 The Machine 自身的服务或 OpenClaw 网关。

同一问题每两周最多生成一个待办，且待办仍未处理时不会生成新的待办。每天最多生成两个新待办。服务停止时生成的待办，会在服务重新运行或问题解决后自动关闭。

## 在终端中

`assistant doctor` 会列出过去一天内的同类问题。

## 其他电脑

在 macOS、Windows 和未安装 systemd 的电脑上，它不会读取任何内容，并会在 `assistant doctor` 中说明原因。

对于托管的 Machine，服务器由我们负责维护运行。服务器的问题会发送给 The Machine 团队，不会作为待办发送给你。

## 关闭此功能

在 config.json 中设置 `"computer_logs": false`，然后重启服务。
