---
title: Organisationsdetails
area: graph
summary: Branche, Größe, Standort und Logo für jede Organisation, ermittelt anhand ihrer Webadresse.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: 1690f417d7a70829
---
## Woher die Angaben stammen

- Auf einer gehosteten Machine werden die Organisationsdetails kostenlos für dich nachgeschlagen.
- Auf deinem eigenen Computer ist die Funktion deaktiviert, bis du einen Schlüssel für einen Nachschlagedienst wie Apollo, People Data Labs oder Hunter hinzufügst. Weitere Informationen findest du in der [Konfigurationsanleitung](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Übermittelt wird nur die Webadresse einer Organisation, niemals deine Nachrichten oder wen du dort kennst. Eine gehostete Machine oder eine im The Machine Network schlägt täglich bis zu 1.000 Organisationen nach, andere bis zu 50. Die Angaben werden alle 90 Tage aktualisiert. Gemeinsam genutzte Websites und E-Mail-Anbieter wie gmail.com werden nie nachgeschlagen. Für Personen gibt es eine eigene Suche: siehe [Berufsbezeichnung und Foto](people.md#job-title-and-photo).

Wenn bei der Suche kein Logo gefunden wird, verwendet The Machine das Symbol, das auf der Website der Organisation angegeben ist. Es wird auf deiner Machine gespeichert. Kein Logodienst erfährt, mit wem du zu tun hast. Sind beide vorhanden, wird in kleinen Ansichten wie der Zeile einer Aufgabe das quadratische Symbol angezeigt.

Wenn die Suche Fachgebiete findet, werden bis zu 5 davon unter der Beschreibung der Organisation angezeigt. Die Organisationsliste lässt sich nach einem Fachgebiet filtern: „**Filtern**“ und dann „**Fachgebiet**“. Wenn bei der Suche nach einer Person auch Angaben zu ihrem Unternehmen gefunden werden, werden diese auch bei der Organisation ergänzt. Dann ist keine eigene Suche nach der Organisation nötig. Angaben, die in den letzten 90 Tagen nachgeschlagen wurden, bleiben unverändert.

## Falsche Angaben korrigieren

Auf der Seite der Organisation:

- Mit „**Bearbeiten**“ kannst du Name, Branche, Größe, Standort, Gründungsjahr, Beschreibung, Website, LinkedIn, Notizen und die Bedeutung der Organisation für dich ändern. Deine Änderungen bleiben erhalten. Leere ein Feld, um wieder den nachgeschlagenen Wert zu verwenden.
- Wähle in „**Bearbeiten**“ die Option „**Falsche Firma, Details löschen**“, wenn die falsche Firma gefunden wurde.
- Mit „**Neu nachschlagen**“, das nach dem Löschen angezeigt wird, rufst du aktuelle Angaben ab.
