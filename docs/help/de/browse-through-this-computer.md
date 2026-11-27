---
title: Über deinen Computer surfen
area: troubleshooting
summary: Lass den Browser deiner gehosteten Machine über den Computer laufen, auf dem die Desktop-App läuft. So sehen Websites deine eigene Internetverbindung.
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
translated: 6da69c78d7e60574
---
Manche Websites wie LinkedIn akzeptieren keine Anmeldungen über einen Browser in der Cloud. Wenn du in der [Desktop-App](desktop-app.md) angemeldet bist, kann der Browser deiner gehosteten Machine stattdessen über diesen Computer ins Internet gehen. Websites sehen dann deine Internetverbindung zu Hause oder im Büro statt die eines Rechenzentrums.

## Aktivieren

Die Funktion ist standardmäßig aktiviert, sobald deine Machine sie hat. In den Einstellungen der Desktop-App heißt der Schalter **Meine Machine über diesen Computer surfen lassen**. Wenn du ihn ausschaltest, geht der Browser deiner Machine sofort wieder direkt ins Internet.

Während der Browser deiner Machine die Funktion nutzt, zeigen die Roboteranzeige und das App-Symbol in der Menüleiste oder Taskleiste **Deine Machine surft über diesen Computer** an.

## Was darüber läuft

Nur der Browser deiner Machine greift damit auf Websites zu: über die Ports 80 und 443 unter öffentlichen Internetadressen. Die App stellt selbst keine Verbindung zu diesem Computer, deinem Heim- oder Büronetzwerk oder anderen privaten Adressen her und öffnet keine Ports auf deinem Computer. Es gelten die Limits von 4 MB/s im Download, 1 MB/s im Upload und 2 GB pro Tag.

## Wenn der Computer ausgeschaltet ist

Der Browser deiner Machine geht direkt über deine Machine ins Internet. Sobald die App wieder läuft, geht der Datenverkehr wieder über den Computer.
