---
title: Die Desktop-App
area: getting-started
summary: The Machine unter Windows, Mac und Linux: dein Dashboard in einem eigenen Fenster und ein Roboter in einer Bildschirmecke.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
Die Desktop-App öffnet dein Dashboard in einem eigenen Fenster. In einer Bildschirmecke sitzt ein kleiner Roboter. Klick darauf, um eine Aufgabe hinzuzufügen, nach deinen Nachrichten zu fragen oder zu sehen, was für dich ansteht. Die App ist ein Prototyp.

## Herunterladen

Jeder Link führt immer zur neuesten Version:

- Windows 10 oder 11, 64-Bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac mit macOS 13 oder neuer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-Bit: das [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), die [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) für Ubuntu und Debian oder das [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) für Arch und Omarchy

## Windows

Öffne das Installationsprogramm. Es wird nur für dich installiert, ohne Administratorrechte, und ist von Salesflare signiert. Auf einem Rechner, auf dem WebView2 noch nie verwendet wurde, dauert die Einrichtung ein paar Sekunden länger. Danach startet die App sofort. Sie aktualisiert sich selbst. In den **Einstellungen** siehst du, wann eine neue Version bereitsteht.

## Mac

Entpacke die ZIP-Datei, verschiebe The Machine in den Ordner „Programme“ und öffne sie dort. macOS fragt einmal, ob eine App aus dem Internet geöffnet werden darf. Wähle **Öffnen**. Die App ist signiert und notariell beglaubigt und aktualisiert sich selbst.

## Linux

- Jede Distribution: Mach das AppImage mit `chmod +x` ausführbar und starte es. Wenn eine Meldung besagt, dass FUSE fehlt, installiere `fuse3`.
- Ubuntu 22.04, Debian 12 oder neuer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK und gtk-layer-shell sind darin enthalten.
- Arch und Omarchy: Lege das PKGBUILD in einen leeren Ordner und führe dort `makepkg -si` aus. Dadurch wird diese Version heruntergeladen, mit der Prüfsumme in der Datei abgeglichen und installiert. Unter Hyprland, wie es bei Omarchy zum Einsatz kommt, bleibt der Roboter über anderen Fenstern sichtbar, ohne ein eigenes Fenster zu haben.

Unter Linux aktualisiert sich die App nicht selbst. Für eine neuere Version lade die Datei oder das neuere PKGBUILD erneut herunter.

## Download überprüfen

Für jede Datei gibt es GitHubs Build-Provenienz. Sie zeigt, dass die Datei mit The Machines eigenem Workflow aus dem Code von The Machine erstellt wurde. Mit der [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Anmelden

Beim ersten Start öffnet sich das Anmeldefenster. Bei einer gehosteten Machine oder einer im The Machine Network öffnet sich dein Konto im Browser. Anschließend kehrt die App zurück. Bei einer selbst gehosteten Machine gibst du ihre eigene Adresse ein. Das geht von einem Rechner in deinem Tailscale-Netzwerk aus.

Wenn du das Dashboard stattdessen als App in Chrome oder Edge nutzen möchtest, lies [App installieren](phone-app.md).
