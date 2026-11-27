---
title: Die Desktop-App
area: getting-started
summary: The Machine unter Windows, Mac und Linux: dein Dashboard in einem eigenen Fenster und ein Roboter in einer Bildschirmecke.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
Die Desktop-App öffnet dein Dashboard in einem eigenen Fenster. In einer Bildschirmecke sitzt ein kleiner Roboter: Klick darauf, um eine Aufgabe hinzuzufügen, Fragen zu deinen Nachrichten zu stellen oder zu sehen, was für dich ansteht. Die App ist ein Prototyp.

## Herunterladen

Jeder Link führt immer zur neuesten Version:

- Windows 10 oder 11, 64-Bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac mit macOS 13 oder neuer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-Bit: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) für Ubuntu und Debian oder [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) für Arch und Omarchy

Du findest die Downloads auch in deinem Dashboard. Auf einem Computer listet **Einstellungen** unter **Apps** alle drei auf. Bei deinem steht **Dieser Computer**. Die Aufgabe **Hol mehr aus The Machine heraus** enthält **Desktop-App herunterladen**. Damit lädst du die passende Version für deinen Computer herunter oder öffnest die Linux-Anleitung weiter unten. Die Aufgabe verschwindet, sobald die App bei deiner Machine angemeldet ist. Beides wird weder auf dem Handy noch in der Desktop-App angezeigt.

## Windows

Öffne das Installationsprogramm. Es wird nur für dich installiert, ohne Administratorrechte, und ist von Salesflare signiert. Auf einem Computer, auf dem WebView2 noch nie verwendet wurde, dauert die Einrichtung ein paar Sekunden länger. Danach startet die App sofort. Die App aktualisiert sich selbst. In ihren Einstellungen steht, wenn eine neue Version verfügbar ist.

## Mac

Entpacke die ZIP-Datei, verschiebe The Machine in den Ordner „Programme“ und öffne sie dort. macOS fragt einmal, ob eine App aus dem Internet geöffnet werden soll: Wähle **Öffnen**. Die App ist signiert und notarisiert und aktualisiert sich selbst.

## Linux

- Jede Distribution: Mache die AppImage-Datei mit `chmod +x` ausführbar und starte sie. Wenn FUSE fehlt, installiere `fuse3`.
- Ubuntu 22.04, Debian 12 oder neuer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK und gtk-layer-shell sind enthalten.
- Arch und Omarchy: Lege die PKGBUILD-Datei in einen leeren Ordner und führe dort `makepkg -si` aus. Damit wird diese Version heruntergeladen, mit der Prüfsumme in der Datei abgeglichen und installiert. Unter Hyprland, wie bei Omarchy, bleibt der Roboter über anderen Fenstern, ohne ein eigenes Fenster zu haben.

Unter Linux aktualisiert sich die App nicht selbst. Für eine neuere Version lädst du die Datei oder die neuere PKGBUILD-Datei erneut herunter.

## Download überprüfen

Für jede Datei gibt es den Build-Nachweis von GitHub. Er zeigt, dass sie mit dem eigenen Workflow aus dem Code von The Machine erstellt wurde. Mit der [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Anmelden

Beim ersten Start öffnet sich das Anmeldefenster. Bei einer gehosteten Machine oder einer auf The Machine Network öffnet sich dein Konto im Browser, dann kehrst du zur App zurück. Bei einer selbst gehosteten Machine brauchst du ihre eigene Adresse. Du findest sie auf einem Computer in deinem Tailscale-Netzwerk.

Wenn du das Dashboard stattdessen als Chrome- oder Edge-App verwenden möchtest, lies [App installieren](phone-app.md).

## Der Roboter

Der Roboter wird ausgeblendet, solange das Fenster der App im Vordergrund ist. Er erscheint wieder, wenn ein anderes Fenster im Vordergrund ist oder du das Fenster minimierst oder schließt. Bei mehreren Monitoren erscheint er auf dem Monitor mit dem App-Fenster, bis du ihn woandershin ziehst (unter Hyprland, Sway und KDE auf dem Hauptmonitor). So schaltest du ihn ein oder aus: **Einstellungen** (Strg+Komma oder auf dem Mac Befehl+Komma), **Roboter anzeigen**.
