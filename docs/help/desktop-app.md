---
title: The desktop app
area: getting-started
summary: The Machine on Windows, Mac and Linux: your dashboard in a window of its own, and a robot in a corner of the screen.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
---
The desktop app opens your dashboard in a window of its own. A small robot stands in a corner of the screen: click it to add a to-do, ask about your messages, or see what is for you. It is a prototype.

## Download it

Each link always has the newest version:

- Windows 10 or 11, 64-bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac with macOS 13 or newer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-bit: the [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), the [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) for Ubuntu and Debian, or the [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) for Arch and Omarchy

## Windows

Open the installer. It installs for you alone, without an administrator, and is signed by Salesflare. On a computer where nothing used WebView2 before, it takes a few seconds more to get that ready, so the app starts at once after it. The app updates itself: its Settings say when a new version is ready.

## Mac

Unpack the zip, move The Machine to Applications and open it there. macOS asks once whether to open an app from the internet: choose Open. It is signed and notarized, and updates itself.

## Linux

- Any distribution: make the AppImage executable with `chmod +x` and start it. If it says FUSE is missing, install `fuse3`.
- Ubuntu 22.04, Debian 12 or newer: `sudo apt install ./the-machine-desktop-amd64.deb`. It brings WebKitGTK and gtk-layer-shell with it.
- Arch and Omarchy: put the PKGBUILD in an empty folder and run `makepkg -si` there. It downloads that version, checks it against the checksum in the file, and installs it. On Hyprland, as Omarchy has it, the robot stays above other windows without a window of its own.

On Linux the app doesn't update itself. For a newer version, download the file again, or the newer PKGBUILD.

## Check a download

Every file has GitHub's build provenance, which shows it was built from The Machine's code by its own workflow. With the [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Sign in

The first time, its window opens to sign in. For a hosted Machine or one on The Machine Network, it opens your account in your browser and comes back. A self-hosted Machine takes its own address, from a computer on your Tailscale network.

To have the dashboard as an app of Chrome or Edge instead, see [Install the app](phone-app.md).
