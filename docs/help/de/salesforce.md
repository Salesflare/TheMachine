---
title: Salesforce
area: connections
summary: Deals, Aufgaben und Aktivitäten aus Salesforce zu deinen Personen und Projekten. Wenn du das einschaltest, kann The Machine dort Kontaktdaten aktuell halten.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## Was The Machine liest

Neue Deals sowie Deals, die in eine andere Phase wechseln oder deren Betrag sich ändert. Deine offenen Aufgaben, Anrufe und andere als erledigt protokollierte Aufgaben samt Notizen sowie Meetings mit einer Beschreibung. Die letzten 7 Tage beim Verbinden und danach alle 15 Minuten neue Einträge.

Jeder Deal wird zu einem Projekt in deinem Graph. Die zugehörigen Kontakte erscheinen bei den jeweiligen Personen als Salesforce-Kontakt in deren Account.

## Was The Machine ändern kann

Nichts, bis du **Kontaktdaten aktualisieren** einschaltest. Deine Salesforce-Anmeldedaten bleiben auf deiner Machine.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und gehe zu **Weitere Quellen**.
2. Öffne Salesforce und klicke auf **Salesforce verbinden**.
3. Melde dich bei Salesforce an und erlaube The Machine (von Salesflare entwickelt) den Zugriff.

Oder im Dashboard: **Verbindungen**, **Kunden**, wähle Salesforce und klicke auf **Mit Salesforce anmelden**. Auf deinem eigenen Computer musst du ihn zuerst mit deinem Konto koppeln.

Dein Salesforce-Benutzerkonto braucht API-Zugriff. Dieser ist in den meisten Editionen enthalten.

## Kontaktdaten aktualisieren

Wenn deine Machine neuere Angaben zu einem deiner Salesforce-Kontakte kennt, kann sie den Kontakt dort aktualisieren: Berufsbezeichnung, Telefonnummer und den LinkedIn-Link, falls deine Organisation ein LinkedIn-Feld für Kontakte eingerichtet hat.

1. Öffne unter **Verbindungen** Salesforce und klicke auf **Zeigen, was sich ändern würde**.
2. Prüfe die Liste und klicke dann auf **Einschalten** oder **Nicht jetzt**.

Dabei gilt:

- Nur Angaben, die die Person selbst gemacht hat, zum Beispiel in ihrem LinkedIn- oder Slack-Profil, oder die du auf ihrer Seite eingetragen hast. Nie Vermutungen.
- Nur wenn die Angabe neuer ist als die letzte Änderung des Kontakts in Salesforce. Änderungen dort haben Vorrang.
- Nur Felder, deren Werte abweichen, und nie leere Werte. Die E-Mail-Adresse und der Account werden nie geändert.
- Jede Änderung wird als datierte Zeile auf der Seite der Person angezeigt.

Klicke auf **Ausschalten**, um die Funktion zu stoppen. Eine Verbindung, die deine Fleet teilt, liest nur Daten.

## Verbindung entfernen

- Im Dashboard: Öffne unter **Verbindungen** Salesforce, klicke auf **Details** und dann auf **Trennen**. Bereits importierte Daten bleiben erhalten.
- Auf einer gehosteten Machine öffnet **Trennen ↗** dort deine Einrichtungsseite. Klicke daneben auf **Entfernen**.

## Zugriff in Salesforce widerrufen

Öffne in Salesforce deine persönlichen Einstellungen und dann „Connected Apps OAuth Usage“, oder bitte deine Administration darum, und widerrufe den Zugriff für The Machine. Sie kann dann nichts mehr lesen oder ändern.
