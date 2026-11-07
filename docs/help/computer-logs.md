---
title: Problems on your computer
area: troubleshooting
summary: Your Machine reads its computer's own logs and tells you about real problems, with the cause and a fix. A fix runs only when you tap Do it.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
---
## What it reads

On Linux with systemd, your Machine reads the log of your own user session: your own services and the crash reports of your own programs. On Omarchy it also checks Hyprland and the bar. It never reads the whole system's log and never asks for more access.

It reads which service stopped, how it ended and which program crashed. Never what a log line says, so no log text is kept or leaves your computer.

## What counts as a problem

A service that keeps restarting, one that failed several times in a day or stays down, one that ran out of memory, and a program that crashed. On Omarchy also a Hyprland or bar crash, and errors in your Hyprland settings.

A single restart or a single failed run is normal and stays quiet.

## What you get

A to-do that says what happened in plain words, why it matters and the command that shows or fixes it. Ask in its chat and The Machine looks into it. Anything it changes waits for your OK, as with Do it.

When there is a safe fix, the to-do has Do it. For a service of yours that stays down it starts it again, and on Omarchy it brings the bar back. Do it runs only that command, and the result shows in the to-do's chat. It never touches The Machine's own services or the OpenClaw Gateway.

The same problem brings at most one to-do every two weeks, and never while its to-do is still open. At most two new ones a day.

## In a terminal

`assistant doctor` lists the same problems from the last day.

## Other computers

On macOS, Windows and computers without systemd it reads nothing and says so in `assistant doctor`.

## Turn it off

Set `"computer_logs": false` in config.json and restart the service.
