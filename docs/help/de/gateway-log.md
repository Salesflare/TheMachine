---
title: Zustand deiner Machine
area: connections
summary: Das eigene Protokoll deiner Machine, damit sie Probleme selbst erkennt. Es wird nur gelesen.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 7d66ff6a6a5d5b1d
---
## Was sie liest

Das eigene Protokoll deiner Machine: fehlgeschlagene Abläufe, abgelehnte Übergaben, Telegram-Nachrichten, die nicht gesendet wurden, und eigene Fehler von The Machine. Eine Aufgabe zeigt dir, wenn etwas repariert werden muss. Auf deinem eigenen Computer gehört dazu **Die letzte Aktualisierung fertig installieren**: Ein Teil eines Updates braucht nachts einen kurzen Neustart, und das hat ein paar Nächte lang nicht geklappt. Frag im Chat der Aufgabe, dann schließt The Machine die Installation ab. Die Aufgabe schließt sich selbst, sobald dieser Teil installiert ist.

## Korrekturen, die ein Update beiseitegelegt hat

Wenn The Machine ein Update ausführt und eine eigene Korrektur nicht mehr zur neuen Version passt, legt das Update diese Korrektur beiseite und läuft weiter. So bleibt deine Machine nie auf einer alten Version. Eine Aufgabe namens **Eine vom Update beiseitegelegte Korrektur erneut anwenden** nennt die Korrektur.

Mit **Neu machen** lässt du deine Machine die Korrektur in der neuen Version erneut erstellen, wie bei jeder eigenen Korrektur: Du siehst die Änderung und tippst auf **Korrektur zusammenführen**. Sobald sie zusammengeführt ist, wird die alte Kopie gelöscht. Oder schließe die Aufgabe.

## Eigene Dateien, die ein Update behalten hat

Wenn eine neue Version eine Datei mit demselben Namen enthält wie eine Datei, die du selbst hinzugefügt hast, benennt das Update deine Datei um, statt sie zu überschreiben, und läuft weiter. Eine Aufgabe zeigt dir, wie viele Dateien behalten wurden, und listet jeweils den alten und den neuen Namen auf. Schließe sie, sobald du die Namen überprüft hast.

## Was sie tun kann

Nichts. Sie liest nur das Protokoll auf deiner eigenen Machine.

## Verbinden

- Auf einer gehosteten Machine findest du sie auf deiner Einrichtungsseite unter **Weitere Quellen** als „Zustand deiner Machine“. Einmal pro Machine.
- Auf deinem eigenen Computer: **Verbindungen**, **Andere**, „Zustand deiner Machine“. Oder führe `assistant connect gateway` aus.

## Entfernen

- Im Dashboard: **Verbindungen**, öffne den Eintrag und wähle **Details** und dann **Trennen**.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

An anderer Stelle musst du nichts deinstallieren.
