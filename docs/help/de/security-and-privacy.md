---
title: Sicherheit und Datenschutz
area: security
summary: Deine eigene private Machine, verschlüsselt gespeicherte Mails und nichts wird ohne dein Okay gesendet. Das Wichtigste in Kürze, mit Links.
covers:
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: 27c910c92b215ad3
---
## Kurz gesagt

- Deine eigene Machine: Eine gehostete Machine läuft in der EU-Cloud, nur für dich und niemals gemeinsam mit anderen. Oder du betreibst sie auf deinem eigenen Computer.
- Wir lesen deine E-Mails nicht: Nachrichten werden verschlüsselt gespeichert und unsere Support-Tools können sie nicht öffnen.
- Nichts wird ohne dein Okay gesendet: Die Machine liest und erstellt Entwürfe. Du entscheidest, was rausgeht. Siehe [Ausführen](do-it.md).
- Deine Daten werden nicht zum Trainieren von KI verwendet: Wir haben keine eigene KI. Dein Anbieter arbeitet mit deinem Konto und nach seinen Bedingungen.
- Erkenntnisse fürs Team, sofern du sie nicht deaktivierst: Hin und wieder werden ein paar allgemeine Tipps geteilt, nichts Persönliches. Du prüfst sie, bevor sie weitergegeben werden. Siehe [Erkenntnisse teilen](share-learnings.md).
- Fehlerberichte, sofern du sie nicht deaktivierst: Wenn etwas schiefläuft, werden die Art des Fehlers und die Stelle im Code erfasst. Niemals deine Nachrichten, Namen oder Adressen. Siehe [Fehlerberichte](error-reports.md).
- Nutzungszahlen bei einer gehosteten Machine: tägliche Zählungen deiner Aktivitäten, etwa geöffnete Aufgaben oder gesendete E-Mails, niemals deren Inhalte. Außerdem wird erfasst, wie schnell dein Dashboard lädt. Dabei werden nur Ladezeiten erfasst, egal ob du ein Handy oder einen Computer, die App oder einen Browser verwendest.
- Nimm deine Daten mit oder lösche sie: Exportiere alles unter **Einstellungen** › **Allgemein** oder lösche deine Machine samt Backups mit einem Klick. Siehe [Kündigen oder löschen](cancel-and-delete.md).
- Unser Zugriff wird protokolliert: Jedes Mal, wenn unser Team den Bericht oder die Protokolle deiner gehosteten Machine liest. Inhaber und Admins einer Fleet sehen das unter **Aktivität**. Siehe [Fleets](fleet.md).

## Backups

Eine gehostete Machine sichert deine Daten jede Nacht. Das Backup wird auf deiner Machine verschlüsselt, bevor es diese verlässt, und in Microsoft Azure in den Niederlanden (EU) gespeichert. Die letzten 7 täglichen, 4 wöchentlichen und 3 monatlichen Backups bleiben erhalten, also etwa 3 Monate lang. Wenn deine Machine gelöscht wird, werden sie ebenfalls gelöscht.

Können wir sie öffnen? Ja, um eine ausgefallene Machine wiederherzustellen. Wir verwahren den Schlüssel getrennt von den Backups. Die Nachrichten in einem Backup werden zusätzlich mit einem zweiten Schlüssel verschlüsselt, den wir ebenfalls verwahren. Er ist versiegelt und befindet sich niemals im Backup.

Backups sind ein Sicherheitsnetz. Bewahre daher eine eigene Kopie von allem auf, was du nicht verlieren möchtest: **Alles** unter **Einstellungen** › **Allgemein** › **Exportieren**. Siehe [Auf einen anderen Computer umziehen](moving.md).

Auf deinem eigenen Computer werden keine automatischen Backups erstellt und wir haben keine Kopie. Ein nächtliches verschlüsseltes Backup deines Home-Ordners reicht aus: siehe [Erste Schritte](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md#later).

## Sicherheitsstufen

„**Standard**“ behält die heutigen Standardeinstellungen bei. „**Vorsichtig**“ zeigt keine Texte in Benachrichtigungen an, speichert keine Anmeldedaten und behält weniger Daten. Admins einer Work Fleet können die Fleet auf „**Vorsichtig**“ einstellen. Siehe [Sicherheitsstufen](security-levels.md).

## Anmeldung

Für ein gehostetes Dashboard brauchst du einen Passkey oder eine Anmeldung über Google oder Microsoft mit einem Authenticator-Code.

## Verbindungen

Im Artikel zu jeder Verbindung erfährst du, was sie liest und was sie senden kann. Du kannst jede Verbindung jederzeit trennen: siehe [Verbindungen](connections.md).

## Hilfe

Die Hilfe läuft auf deiner Machine und kann deine Daten nicht sehen. Nur das Thema jeder Frage wird an das Team von The Machine gesendet, niemals deine Worte. Siehe [Hilfe fragen](help-chat.md#what-the-team-sees).

## Mehr

- [Sicherheit](/security): wie die Sicherheit umgesetzt ist, was unsere Mitarbeitenden sehen können und was nicht und wie wir nach Problemen suchen.
- [Datenschutzhinweis](/privacy) und [Bedingungen zur Datenverarbeitung](/dpa).
- Sicherheitsproblem entdeckt? Lies unsere [Sicherheitsrichtlinie](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md).
