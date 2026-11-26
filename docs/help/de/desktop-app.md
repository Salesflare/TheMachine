---
title: Die Desktop-App
area: getting-started
summary: The Machine unter Windows, Mac und Linux: dein Dashboard in einem eigenen Fenster und ein Roboter in einer Bildschirmecke.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
Die Desktop-App öffnet dein Dashboard in einem eigenen Fenster. In einer Bildschirmecke steht ein kleiner Roboter: Klick darauf, um eine Aufgabe hinzuzufügen, Fragen zu deinen Nachrichten zu stellen oder zu sehen, was für dich ansteht. Die App ist ein Prototyp.

## Herunterladen

Jeder Link führt immer zur neuesten Version:

- Windows 10 oder 11, 64-Bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac mit macOS 13 oder neuer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-Bit: das [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), die [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) für Ubuntu und Debian oder die [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) für Arch und Omarchy

## Windows

Öffne den Installer. Er installiert die App nur für dich, ohne Administratorrechte, und ist von Salesflare signiert. Auf einem Computer, auf dem WebView2 noch nie verwendet wurde, dauert die Einrichtung ein paar Sekunden länger. Danach startet die App sofort. Sie aktualisiert sich selbst. In den **Einstellungen** steht, wann eine neue Version bereit ist.

## Mac

Entpacke die ZIP-Datei, verschiebe The Machine in den Ordner „Programme“ und öffne sie von dort. macOS fragt einmal, ob eine App aus dem Internet geöffnet werden soll: Wähle **Öffnen**. Die App ist signiert und notariell beglaubigt und aktualisiert sich selbst.

## Linux

- Für jede Distribution: Mach das AppImage mit `chmod +x` ausführbar und starte es. Wenn die Meldung erscheint, dass FUSE fehlt, installiere `fuse2` auf Arch oder `libfuse2t64` auf Ubuntu 24.04.
- Ubuntu 22.04, Debian 12 oder neuer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK und gtk-layer-shell sind enthalten.
- Arch und Omarchy: Lege die PKGBUILD in einen leeren Ordner und führe dort `makepkg -si` aus. Der Befehl lädt diese Version herunter, prüft sie anhand der Prüfsumme in der Datei und installiert sie. Unter Hyprland, wie bei Omarchy, bleibt der Roboter über anderen Fenstern, ohne ein eigenes Fenster zu haben.

Unter Linux aktualisiert sich die App nicht selbst. Für eine neuere Version lädst du die Datei oder die neuere PKGBUILD erneut herunter.

## Anmelden

Beim ersten Start öffnet sich das Anmeldefenster. Bei einer gehosteten Machine oder einer Machine im The Machine Network öffnet sich dein Konto im Browser, und die App kehrt zurück. Für eine selbst gehostete Machine brauchst du ihre eigene Adresse auf einem Computer in deinem Tailscale-Netzwerk.

Wenn du das Dashboard stattdessen als Chrome- oder Edge-App nutzen möchtest, lies [App installieren](phone-app.md).
