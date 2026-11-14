---
title: Beobachtete Webseiten
area: connections
summary: Eine Webseite, die du beobachtest. Eine Aufgabe nur, wenn sich dort etwas Wichtiges ändert.
covers: connector:web_page
code: connectors/web_page.py
---
## Was es liest

Den Text einer öffentlichen Webseite pro Verbindung, alle paar Stunden und höchstens einmal pro Stunde. Menüs, Fußzeilen, Cookie-Hinweise und Werbung lässt sie weg. Wenn sich der Text geändert hat, schaut The Machine, was sich geändert hat, und erstellt nur dann eine Aufgabe, wenn es wichtig ist, etwa ein neuer Preis oder eine geänderte Richtlinie. Daten, Zähler und kleine Umformulierungen ergeben nie eine Aufgabe. Eine unveränderte Seite kostet nichts.

Sie fragt zuerst die robots.txt der Website und lässt die Seite in Ruhe, wenn die Website Nein sagt. Seiten hinter einer Anmeldung oder solche, die nur mit JavaScript gebaut sind, lassen sich nicht beobachten.

## Was es tun kann

Nichts. Es liest nur die Seite.

## Verbinden

1. Öffne im Dashboard **Verbindungen**, dann **Andere**, und wähle Webseite. Oder führe `assistant connect web_page` aus.
2. Füge die Adresse der Seite ein.

Oder frag in deinem Chat: „Beobachte diese Seite auf Preisänderungen“ mit ihrer Adresse. Frag, welche Seiten du beobachtest, oder bitte darum, eine nicht mehr zu beobachten.

## Entfernen

Im Dashboard: **Verbindungen**, die Seite öffnen, **Details**, dann **Trennen**. Oder bitte deinen Chat, sie nicht mehr zu beobachten.
