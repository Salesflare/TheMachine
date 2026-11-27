---
title: Die Desktop-App
area: getting-started
summary: The Machine unter Windows, Mac und Linux: dein Dashboard in einem eigenen Fenster und ein Roboter in einer Bildschirmecke.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: af0a8a2994af969d
---
Die Desktop-App öffnet dein Dashboard in einem eigenen Fenster. In einer Bildschirmecke steht ein kleiner Roboter: Klick darauf, um eine Aufgabe hinzuzufügen, nach deinen Nachrichten zu fragen oder zu sehen, was für dich ansteht. Die App ist ein Prototyp.

## Herunterladen

Jeder Link führt immer zur neuesten Version:

- Windows 10 oder 11, 64-Bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac mit macOS 13 oder neuer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-Bit: das [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), das [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) für Ubuntu und Debian oder das [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) für Arch und Omarchy

Du findest alle drei auch in deinem Dashboard. Am Computer zeigt **Einstellungen** unter **Apps** alle drei an. Auf deinem Computer steht **Dieser Computer** daneben. Bei der Aufgabe **Hol mehr aus The Machine heraus** findest du **Desktop-App herunterladen**. Damit lädst du die passende Version für deinen Computer herunter oder öffnest die Linux-Anleitung weiter unten. Die Aufgabe verschwindet, sobald du dich in der App bei deiner Machine angemeldet hast. Auf dem Handy und in der Desktop-App selbst wird sie nicht angezeigt.

## Windows

Öffne das Installationsprogramm. Es wird nur für dich installiert, ohne Administratorrechte, und ist von Salesflare signiert. Wenn WebView2 auf deinem Computer bisher noch nicht verwendet wurde, dauert die Einrichtung ein paar Sekunden länger. Danach startet die App sofort. Sie aktualisiert sich selbst. In den Einstellungen siehst du, wann eine neue Version bereitsteht.

## Mac

Entpacke die ZIP-Datei, verschiebe The Machine in den Ordner „Programme“ und öffne die App dort. macOS fragt einmal, ob eine App aus dem Internet geöffnet werden soll. Wähle **Öffnen**. Die App ist signiert und notarisiert und aktualisiert sich selbst.

## Linux

- Beliebige Distribution: Mache das AppImage mit `chmod +x` ausführbar und starte es. Wenn die Meldung erscheint, dass FUSE fehlt, installiere `fuse3`.
- Ubuntu 22.04, Debian 12 oder neuer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK und gtk-layer-shell sind enthalten.
- Arch und Omarchy: Lege das PKGBUILD in einen leeren Ordner und führe dort `makepkg -si` aus. Der Befehl lädt die jeweilige Version herunter, prüft sie anhand der Prüfsumme in der Datei und installiert sie. Unter Hyprland, wie es bei Omarchy eingerichtet ist, bleibt der Roboter über anderen Fenstern, ohne ein eigenes Fenster zu haben.

Das AppImage aktualisiert sich selbst, wenn es sich in einem deiner Ordner befindet, zum Beispiel ~/Applications. In den Einstellungen siehst du, wann eine neue Version bereitsteht. Das .deb und das Arch-Paket werden über apt und pacman verwaltet. In den Einstellungen siehst du, wenn eine neuere Version verfügbar ist, mit **Herunterladen** für das .deb oder PKGBUILD. Ein in einen Ordner entpacktes AppImage aktualisiert sich nicht selbst. Verwende das AppImage so, wie es ist.

## Download überprüfen

Für jede Datei gibt es den Build-Nachweis von GitHub. Er zeigt, dass sie mit dem eigenen Workflow aus dem Code von The Machine erstellt wurde. Mit der [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Anmelden

Beim ersten Start öffnet sich ein Fenster zur Anmeldung. Bei einer gehosteten Machine oder einer auf The Machine Network öffnet sich dein Konto im Browser und die App kehrt anschließend dorthin zurück. Bei einer selbst gehosteten Machine brauchst du ihre Adresse. Du findest sie auf einem Computer in deinem Tailscale-Netzwerk.

Eine Seite deiner Machine kann die App über einen eigenen Link in den Vordergrund holen: `computer.themachine.desktop://open`. Der Link öffnet nur die App und überträgt keine Daten.

Wenn du das Dashboard stattdessen als Chrome- oder Edge-App verwenden möchtest, lies [App installieren](phone-app.md).

## Der Roboter

Der Roboter wird ausgeblendet, wenn das Fenster der App im Vordergrund ist. Er erscheint wieder, wenn ein anderes Fenster im Vordergrund ist oder du das App-Fenster minimierst oder schließt. Bei mehreren Monitoren erscheint er auf dem Monitor, auf dem sich das App-Fenster befindet, bis du ihn an eine andere Stelle ziehst. Unter Hyprland, Sway und KDE erscheint er auf dem Hauptmonitor. Zum Ein- oder Ausschalten: Einstellungen (Strg+Komma oder auf dem Mac Befehlstaste+Komma), „Roboter anzeigen“.
