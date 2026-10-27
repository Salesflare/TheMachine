---
title: Google Docs und Word
area: connections
summary: Kommentare, Erwähnungen, Änderungsvorschläge und Freigaben in deinen Google Docs oder Word-Dateien. Es liest und postet eine Antwort auf einen Kommentar nur, wenn du sie freigibst.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
---
## Was es liest

Docs nutzt die Google- oder Microsoft-Anmeldung, die du für diese Adresse schon hast. Es bringt rein:

- Dokumente, die jemand mit dir teilt.
- Kommentare und Antworten in Dokumenten, die dir gehören, und Kommentare, die dich erwähnen.
- Änderungsvorschläge in Google Docs, die dir gehören, und nachverfolgte Änderungen in Word-Dateien, die dir gehören.

Die erste Synchronisierung schaut 30 Tage zurück. Daraus wird jeweils ein Termin, verknüpft mit den Personen und Projekten in deinem [Graph](graph.md). Wenn ein Kommentar dich braucht, wird daraus eine Aufgabe.

## Was es tun kann

Wenn eine Aufgabe den Text eines Dokuments braucht, liest deine Machine genau dieses Dokument, und nur, solange sie an dieser Aufgabe arbeitet.

Es kann eine Antwort auf einen Kommentar entwerfen. Bei Google Docs wartet die Antwort bei der Aufgabe: Tippe auf **Prüfen und posten**, sieh sie dir an und dann auf **Jetzt posten**. Vorher wird nichts gepostet. Word-Dateien bieten keinen Weg, von außerhalb von Word zu antworten. Diese Antworten bleiben also Entwürfe, die du in Word kopierst.

Es bearbeitet nie ein Dokument, nimmt keine Vorschläge an, löst keine Kommentare auf und teilt keine Dateien.

## Worum es fragt

Das Lesen von Dokumenten braucht ein eigenes OK, getrennt von deiner Mail-Anmeldung. Dein Zugriff auf Gmail und Kalender bleibt, wie er ist.

- Google: Lesezugriff auf deine Drive-Dateien und Kommentare. Antworten posten braucht ein weiteres OK, das du auslassen kannst.
- Microsoft: Lesezugriff auf deine Dateien, auch auf die, die in OneDrive und SharePoint mit dir geteilt sind.

Wird dieses OK später zurückgenommen, zeigt die Docs-Karte **Wartet auf dein OK, um Dokumente zu lesen**.

## Verbinden

Auf einer gehosteten Machine erscheint Docs unter **+ Hinzufügen**, sobald deine Einrichtungsseite es anbietet.

Auf deinem eigenen Computer:

1. Verbinde zuerst Gmail oder Outlook für die Adresse.
2. Öffne **Verbindungen**, dann **+ Hinzufügen**, wähle Docs und gib diese Adresse ein. Oder führe `assistant connect docs` aus.
3. Es prüft, ob deine Anmeldung Dokumente lesen darf. Ohne dieses OK wird es nicht hinzugefügt.

## Arbeit oder privat

Docs folgt der Kennzeichnung Arbeit oder privat seiner Verbindung, wie bei Mail. Arbeitsdokumente können nach deinen [Freigaberegeln](sharing-rules.md) in den Graph deines Teams gelangen. Private nie.

## Entfernen

Im Dashboard: **Verbindungen**, Docs öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
