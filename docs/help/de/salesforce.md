---
title: Salesforce
area: connections
summary: Deals, Aufgaben und Aktivität aus Salesforce bei deinen Personen und Projekten. Wenn du es einschaltest, hält es Kontaktdaten dort aktuell.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: e2394748e0a676b1
---
## Was es liest

Neue Deals, und Deals, die in eine andere Phase wechseln oder deren Betrag sich ändert. Deine offenen Aufgaben, Anrufe und andere Aufgaben, die mit Notizen als erledigt eingetragen sind, und Meetings mit einer Beschreibung. Die letzten 7 Tage beim Verbinden, danach alle 15 Minuten neue.

Jeder Deal wird ein Projekt in deinem Graph, und die Kontakte darauf erscheinen bei ihren Personen, als Salesforce-Kontakt bei ihrem Account.

## Was es ändern kann

Nichts, bis du **Kontaktdaten aktualisieren** einschaltest. Deine Salesforce-Anmeldung bleibt auf deiner Machine.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und geh zu **Weitere Quellen**.
2. Öffne Salesforce und tippe auf **Salesforce verbinden**.
3. Melde dich bei Salesforce an und erlaube The Machine. Es kommt von Salesflare.

Oder im Dashboard: **Verbindungen**, **Kunden**, wähle Salesforce und tippe auf **Mit Salesforce anmelden**.

Dein Salesforce-Benutzer braucht API-Zugriff, den die meisten Editionen haben.

## Kontaktdaten aktualisieren

Wenn deine Machine neuere Daten zu einem deiner Salesforce-Kontakte kennt, kann sie den Kontakt dort aktualisieren: Jobtitel, Telefon und den LinkedIn-Link, wenn deine Org ein LinkedIn-Feld bei Kontakten hat.

1. Öffne in **Verbindungen** Salesforce und tippe auf **Zeigen, was sich ändern würde**.
2. Prüf die Liste und tippe dann auf **Einschalten** oder **Nicht jetzt**.

Woran es sich hält:

- Nur Daten in den eigenen Worten der Person, etwa aus ihrem LinkedIn- oder Slack-Profil, oder solche, die du auf ihrer Seite eingetragen hast. Nie eine Vermutung.
- Nur wenn die Angabe neuer ist als die letzte Änderung am Kontakt in Salesforce. Eine Änderung dort gewinnt.
- Nur Felder, die sich unterscheiden, und nie ein leerer Wert. Es ändert nie die E-Mail-Adresse oder den Account.
- Jede Änderung ist eine datierte Zeile auf der Seite der Person.

Tippe auf **Ausschalten**, um aufzuhören. Eine Verbindung, die deine Fleet teilt, liest nur.

## Entfernen

- Im Dashboard: **Verbindungen**, Salesforce öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## In Salesforce widerrufen

Öffne in Salesforce deine persönlichen Einstellungen, dann Connected Apps OAuth Usage, oder frag deinen Admin, und widerrufe The Machine. Es kann dann nichts mehr lesen oder ändern.
