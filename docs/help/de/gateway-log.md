---
title: Zustand deiner Machine
area: connections
summary: Das eigene Log deiner Machine, damit sie eigene Probleme erkennt. Es liest nur.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
---
## Was es liest

Das eigene Log deiner Machine: fehlgeschlagene Durchläufe, abgelehnte Übergaben, Telegram-Nachrichten, die nicht rausgingen, und Fehler von The Machine selbst. Eine Aufgabe sagt dir, wenn etwas repariert werden muss.

## Korrekturen, die eine Aktualisierung beiseitegelegt hat

Wenn The Machine sich aktualisiert und eine ihrer eigenen Korrekturen nicht mehr zur neuen Version passt, legt die Aktualisierung diese Korrektur beiseite und macht weiter, damit deine Machine nie auf einer alten Version bleibt. Eine Aufgabe, **Eine beiseitegelegte Korrektur neu machen**, nennt die Korrektur. Bitte darum, sie auf der neuen Version neu zu machen, oder schließ die Aufgabe.

## Deine eigenen Dateien, die eine Aktualisierung behalten hat

Wenn eine neue Version eine Datei mit demselben Namen mitbringt wie eine, die du selbst hinzugefügt hast, benennt die Aktualisierung deine um, statt sie zu überschreiben, und macht weiter. Eine Aufgabe sagt, wie viele sie behalten hat, und nennt jeden alten und neuen Namen. Schließ sie, wenn du sie geprüft hast.

## Was es tun kann

Nichts. Es liest nur das Log auf deiner eigenen Machine.

## Verbinden

- Auf einer gehosteten Machine steht es auf deiner Einrichtungsseite unter **Weitere Quellen**, als Zustand deiner Machine. Eins pro Machine.
- Auf deinem eigenen Computer: Führe `assistant connect gateway` aus.

## Entfernen

- Im Dashboard: **Verbindungen**, öffnen, **Details**, dann **Trennen**.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

Woanders gibt es nichts zu deinstallieren.
