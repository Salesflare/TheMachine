---
title: LinkedIn
area: connections
summary: Deine LinkedIn-Nachrichten, gelesen im eigenen angemeldeten Browser deiner Machine. Antworten werden erst nach deiner Freigabe gesendet.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: bc67fbc21c77a97a
---
## Was gelesen wird

Deine LinkedIn-Nachrichten. Deine Machine liest sie in ihrem eigenen Browser, in dem sie als du angemeldet ist, ab und zu während des Tages. Sie markiert nichts als gelesen. Auch Antworten in archivierten Unterhaltungen und Nachrichtenanfragen werden gelesen. Spam bleibt außen vor.

## Titel und Unternehmen

Deine Machine hält auch die Titel und Unternehmen deiner LinkedIn-Verbindungen aktuell, sofern diese Personen bereits in deinem Graph sind. Dafür nutzt sie deine Kontaktliste. Sie öffnet keine Profile und fügt keine neuen Personen hinzu. Wenn sich der Titel oder das Unternehmen einer Person ändert, wird das in ihrem Verlauf angezeigt, zum Beispiel: „Jetzt Head of Sales bei Acme, zuvor Sales Lead bei Acme“.

Der Titel stammt aus der Profilüberschrift, zum Beispiel „Head of Sales bei Acme“ oder „VP Sales and Strategy“, niemals aus einem Slogan. Deine Machine findet Personen über den Link zu ihrem Profil oder anhand ihres Namens und Unternehmens. Wenn es kein Unternehmen zum Abgleichen gibt, reicht ein vollständiger Name, den nur eine Person in deinem Graph hat. Auf der jeweiligen Seite siehst du auch, seit wann ihr verbunden seid.

Deine Machine liest sehr langsam: eine Seite nach der anderen, mit mehreren Minuten Abstand und nur einige Dutzend Seiten pro Tag, ausschließlich tagsüber. Bei etwa 3.000 Verbindungen dauert es ungefähr vier Tage. Wenn LinkedIn sich querstellt, wartet deine Machine bis zum nächsten Tag.

## Was gesendet werden kann

Eine Antwort auf eine Nachricht oder eine neue Nachricht an ein Profil, das du nennst. Gesendet wird nur, wenn du die Aufgabe freigibst. Bis dahin wird nur ein Entwurf erstellt.

LinkedIn bietet keine offizielle Möglichkeit dafür. Das Lesen und gelegentliche Senden einer von dir freigegebenen Nachricht führen sehr wahrscheinlich zu keinen Problemen. Massenhaftes oder automatisiertes Senden kann dazu führen, dass ein Konto gesperrt wird.

## Verbinden

1. Öffne im Dashboard **Verbindungen** und dann **Chat**. Wähle LinkedIn aus.
2. Wähle **Arbeit** (mit dem Unternehmen) oder **Privat** und drücke **Verbinden**.
3. Drücke **Bei LinkedIn anmelden** und melde dich im Browser deiner Machine an. Sobald du angemeldet bist, wird die Verbindung automatisch hergestellt.

Auf einer gehosteten Machine kannst du auch die Einrichtungsseite unter app.themachine.computer/setup verwenden: Gehe zu **Weitere Quellen**, öffne LinkedIn und melde dich an, wenn du dazu aufgefordert wirst. Drücke anschließend **Verbinden**. Auf deinem eigenen Computer erledigt `assistant connect linkedin` dasselbe im Terminal.

Für ein zweites LinkedIn-Konto wird ein eigener Browser verwendet. Wenn LinkedIn deine Machine abmeldet, lies den Artikel [Von einer Website abgemeldet](signed-out.md).

## Wenn LinkedIn einen Code anfordert

Wenn deine Machine sich zum ersten Mal anmeldet, schickt LinkedIn häufig einen Code per E-Mail. Gib ihn im Anmeldedialog unter **Code** ein und drücke **Anmelden**. Während du den Code eingibst, bleibt die Seite geöffnet.

Wenn LinkedIn wieder zum Anfang zurückkehrt oder nach zwei Minuten nichts passiert, warte eine Minute und drücke **Erneut versuchen**. Wenn LinkedIn eine Roboterprüfung anzeigt, schließe sie im Browser deiner Machine ab.

## Verbindung entfernen

- Im Dashboard: Öffne **Verbindungen**, wähle LinkedIn und dann **Details** und drücke **Trennen**. Deine Machine liest dann keine Nachrichten mehr. Bereits übernommene Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du auf der Einrichtungsseite auch neben LinkedIn auf **Entfernen** drücken.

## Bei LinkedIn abmelden

Öffne bei LinkedIn **Einstellungen**, **Anmelden und Sicherheit** und **Wo du angemeldet bist**. Melde dort die Sitzung des Browsers deiner Machine ab.
