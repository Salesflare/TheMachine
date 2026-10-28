---
title: Organisationsdetails
area: graph
summary: Branche, Größe, Ort und ein Logo bei jeder Organisation, nachgeschlagen über ihre Webadresse.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 2
---
## Woher sie kommen

- Auf einer gehosteten Machine werden Organisationsdetails für dich nachgeschlagen, ohne Kosten.
- Auf deinem eigenen Computer ist das aus, bis du einen Schlüssel für einen Nachschlagedienst hinzufügst, den du nutzt, etwa Apollo, People Data Labs oder Hunter. Siehe den [Konfigurations-Leitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Nur die Webadresse einer Organisation wird gesendet, nie deine Nachrichten oder wen du dort kennst. Es werden jeweils ein paar nachgeschlagen, höchstens 50 am Tag, und alle 90 Tage aktualisiert. Personen werden eigens nachgeschlagen: siehe [Position und Foto](graph.md#job-title-and-photo). Gemeinsame Hosts und Mail-Anbieter wie google.com, sites.google.com oder gmail.com werden nie nachgeschlagen: Sie sind nicht die Website einer einzelnen Firma.

## Falsche Details korrigieren

Auf der Seite der Organisation:

- **Bearbeiten**, um Name, Branche, Größe, Ort, Gründungsjahr, Beschreibung, Website, LinkedIn und das, was sie für dich ist, zu ändern. Deine Änderungen bleiben. Leere ein Feld, um wieder den nachgeschlagenen Wert zu nutzen.
- **Falsche Firma, Details löschen**, wenn die falsche Firma gewählt wurde.
- **Neu nachschlagen**, um frische Details zu holen.
