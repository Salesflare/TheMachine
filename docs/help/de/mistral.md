---
title: Mistral
area: connections
summary: Lass deine Machine mit den Modellen von Mistral laufen, mit einem API-Schlüssel von Mistral. Le Chat Pro enthält API-Guthaben.
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key
---
## Wofür es ist

Mistral ist ein europäischer KI-Anbieter. Mit einem API-Schlüssel von Mistral liest deine Machine und schreibt Entwürfe mit den Modellen von Mistral. The Machine hat keine eigene KI: Die Anfragen gehen direkt an Mistral, unter deinem Konto und deren Bedingungen.

## Einen Schlüssel holen

Mistral hat keine Anmeldung für andere Apps, deshalb läuft es mit einem API-Schlüssel. Öffne in der [Mistral-Konsole](https://console.mistral.ai/) API keys und erstelle einen. Le Chat Pro enthält jeden Monat API-Guthaben; danach rechnet Mistral nach Nutzung ab.

## Verbinden

Öffne auf einer gehosteten Machine deine Einrichtungsseite, gehe zu Deine KI und öffne **Andere KI-Dienste**. Wähle Mistral als Anbieter, füge den Schlüssel ein und tippe auf **Schlüssel speichern**. Deine Machine probiert den Schlüssel zuerst mit einer winzigen Anfrage. Ein falscher Schlüssel zeigt sich sofort, und nichts wird gespeichert.

Mistral Large wird das Hauptmodell. Mistral Small ist auch da, als günstigere Wahl für Chats oder als Ersatz.

Auf deinem eigenen Computer: siehe den [Modell-Leitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).

## Nutzung

**Einstellungen**, **Modell** zeigt "Nutzt deinen Mistral-API-Schlüssel". Ein API-Schlüssel hat keine Nutzungslimits, deshalb pausiert Hintergrundarbeit nie dafür. Siehe [Modell](model.md).

## Entfernen

Wähle auf deiner Einrichtungsseite ein anderes Hauptmodell. Um den Schlüssel zu stoppen, lösche ihn in der Mistral-Konsole.
