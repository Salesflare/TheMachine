---
title: Die Desktop-App
area: getting-started
summary: The Machine unter Windows, Mac und Linux: dein Dashboard in einem eigenen Fenster und ein Roboter in einer Bildschirmecke.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
Die Desktop-App öffnet dein Dashboard in einem eigenen Fenster. In einer Bildschirmecke steht ein kleiner Roboter. Klick darauf, um eine Aufgabe hinzuzufügen, nach deinen Nachrichten zu fragen oder zu sehen, was für dich ansteht. Die App ist ein Prototyp.

## Herunterladen

Jeder Link führt immer zur neuesten Version:

- Windows 10 oder 11, 64-Bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac mit macOS 13 oder neuer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-Bit: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) für Ubuntu und Debian oder [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) für Arch und Omarchy

Du findest sie auch auf deinem Dashboard. Am Computer listet **Einstellungen** unter **Apps** alle drei auf. Auf deinem Computer steht **Dieser Computer** daneben. Die Aufgabe **Hol mehr aus The Machine heraus** enthält **Desktop-App herunterladen**. Damit lädst du die passende Version für deinen Computer herunter oder öffnest die Linux-Anleitung weiter unten. Die Aufgabe verschwindet, sobald du dich in der App bei deiner Machine angemeldet hast. Auf dem Handy und in der Desktop-App wird sie nicht angezeigt.

## Windows

Öffne das Installationsprogramm. Es wird nur für dich installiert, ohne Administratorrechte, und ist von Salesflare signiert. Auf einem Computer, auf dem WebView2 bisher nicht verwendet wurde, dauert die Einrichtung ein paar Sekunden länger. Danach startet die App sofort. Die App aktualisiert sich selbst. In den Einstellungen steht, sobald eine neue Version bereit ist.

## Mac

Entpacke die ZIP-Datei, verschiebe The Machine in den Ordner „Programme“ und öffne die App von dort. macOS fragt einmal nach, ob eine App aus dem Internet geöffnet werden soll. Wähle „Öffnen“. Die App ist signiert und notarisiert und aktualisiert sich selbst.

## Linux

- Beliebige Distribution: Mach die AppImage-Datei mit `chmod +x` ausführbar und starte sie. Wenn FUSE fehlt, installiere `fuse3`.
- Ubuntu 22.04, Debian 12 oder neuer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK und gtk-layer-shell werden mitinstalliert.
- Arch und Omarchy: Lege die PKGBUILD in einen leeren Ordner und führe dort `makepkg -si` aus. Der Befehl lädt die Version herunter, prüft sie anhand der Prüfsumme in der Datei und installiert sie. Unter Hyprland, wie es bei Omarchy eingerichtet ist, bleibt der Roboter über anderen Fenstern, ohne ein eigenes Fenster zu haben.

Die AppImage-Datei aktualisiert sich selbst, wenn sie sich in einem deiner Ordner befindet, zum Beispiel ~/Applications. In den Einstellungen steht, sobald eine neue Version bereit ist. Das .deb-Paket und das Arch-Paket werden über apt und pacman verwaltet. In den Einstellungen steht, wenn eine neuere Version verfügbar ist, mit „Herunterladen“ für die .deb-Datei oder die PKGBUILD. Eine in einen Ordner entpackte AppImage-Datei aktualisiert sich nicht selbst. Verwende die AppImage-Datei so, wie sie ist.

## Einen Download prüfen

Für jede Datei gibt es die Build-Provenienz von GitHub. Sie zeigt, dass die Datei mit The Machine-Code und dem eigenen Workflow erstellt wurde. Mit der [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Anmelden

Beim ersten Start öffnet sich ein Fenster zur Anmeldung. Bei einer gehosteten Machine oder einer Machine im The Machine Network öffnet sich dein Konto im Browser und die App kehrt anschließend zurück. Bei einer selbst gehosteten Machine gibst du ihre Adresse ein. Du findest sie auf einem Computer in deinem Tailscale-Netzwerk.

Wenn du das Dashboard stattdessen als Chrome- oder Edge-App nutzen möchtest, lies [App installieren](phone-app.md).

## Der Roboter

Der Roboter verschwindet, solange das App-Fenster im Vordergrund ist, und erscheint wieder, wenn ein anderes Fenster im Vordergrund ist oder du das App-Fenster minimierst oder schließt. Bei mehreren Monitoren erscheint er auf dem Monitor mit dem App-Fenster, bis du ihn woandershin ziehst. Unter Hyprland, Sway und KDE erscheint er auf dem Hauptmonitor. Ein- und ausschalten kannst du ihn unter **Einstellungen** (Strg+Komma oder auf dem Mac Befehlstaste+Komma) mit **Roboter anzeigen**.
