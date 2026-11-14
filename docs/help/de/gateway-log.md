---
title: Zustand deiner Machine
area: connections
summary: Das eigene Protokoll deiner Machine, damit sie Probleme selbst erkennt. Sie liest nur.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 3a06400a28396465
---
## Was sie liest

Das eigene Protokoll deiner Machine: fehlgeschlagene Ausführungen, abgelehnte Übergaben, Telegram-Nachrichten, die nicht gesendet wurden, und eigene Fehler von The Machine. Eine Aufgabe sagt dir, wenn etwas behoben werden muss. Auf deinem eigenen Computer gehört dazu **Die letzte Aktualisierung fertig installieren**: Ein Teil eines Updates erfordert nachts einen kurzen Neustart, und in einigen Nächten war das nicht möglich. Frag The Machine im Chat danach, und sie schließt die Installation ab. Die Aufgabe wird automatisch geschlossen, sobald dieser Teil installiert ist.

## Korrekturen, die ein Update zurückgestellt hat

Wenn The Machine ein Update installiert und eine ihrer eigenen Korrekturen nicht mehr zur neuen Version passt, stellt das Update diese Korrektur zurück und fährt fort. So bleibt deine Machine immer auf dem neuesten Stand. Eine Aufgabe, **Eine beiseitegelegte Korrektur neu machen**, nennt die Korrektur.

Mit **Neu machen** lässt du deine Machine die Korrektur in der neuen Version erneut erstellen, wie bei jeder eigenen Korrektur: Du siehst die Änderung und tippst auf **Korrektur zusammenführen**. Sobald sie zusammengeführt ist, wird die alte Kopie verworfen. Oder schließ die Aufgabe.

## Eigene Dateien, die ein Update beibehalten hat

Wenn eine neue Version eine Datei mit demselben Namen enthält wie eine Datei, die du selbst hinzugefügt hast, benennt das Update deine Datei um, statt sie zu überschreiben, und fährt fort. Eine Aufgabe sagt dir, wie viele Dateien beibehalten wurden, und listet jeweils den alten und den neuen Namen auf. Schließ die Aufgabe, sobald du die Namen überprüft hast.

## Was sie tun kann

Nichts. Sie liest nur das Protokoll auf deiner eigenen Machine.

## Verbinde sie

- Auf einer gehosteten Machine findest du sie auf deiner Einrichtungsseite unter **Weitere Quellen** als Machine health. Eine pro Machine.
- Auf deinem eigenen Computer: Führe `assistant connect gateway` aus.

## Entferne sie

- Im Dashboard: **Verbindungen** öffnen, **Details** und dann **Trennen** auswählen.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

Du musst sie nirgendwo sonst deinstallieren.
