---
title: Organisationsdetails
area: graph
summary: Branche, Größe, Standort und Logo für jede Organisation, anhand ihrer Webadresse ermittelt.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: f403410953e50582
---
## Woher die Angaben stammen

- Auf einer gehosteten Machine werden die Organisationsdetails kostenlos für dich abgerufen.
- Auf deinem eigenen Computer ist die Funktion deaktiviert, bis du einen Schlüssel für einen Dienst zum Nachschlagen hinzufügst, zum Beispiel Apollo, People Data Labs oder Hunter. Lies dazu die [Konfigurationsanleitung](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Gesendet wird nur die Webadresse einer Organisation, niemals deine Nachrichten oder wen du dort kennst. Eine gehostete Machine oder eine Machine auf The Machine Network schlägt bis zu 1.000 Adressen pro Tag nach, ansonsten sind es bis zu 50. Jede Adresse wird alle 90 Tage erneut abgerufen. Allgemein genutzte Websites und E-Mail-Anbieter wie gmail.com werden nie nachgeschlagen. Für Personen gibt es einen eigenen Abruf: siehe [Berufsbezeichnung und Foto](people.md#job-title-and-photo).

Wenn beim Abruf kein Logo gefunden wird, verwendet The Machine das Symbol von der Website der Organisation und speichert es auf deiner Machine. Kein Logo-Dienst erfährt, mit wem du zu tun hast. Wenn beides vorhanden ist, wird in kleinen Elementen wie der Zeile einer Aufgabe das quadratische Symbol angezeigt.

Wenn beim Abruf Fachgebiete gefunden werden, erscheinen bis zu 5 davon unter der Beschreibung der Organisation. Außerdem kannst du die Organisationsliste nach einem Fachgebiet filtern: **Filtern** und dann **Fachgebiet**. Wenn beim Abruf einer Person auch Details zu ihrem Unternehmen ermittelt werden, werden diese auch für die Organisation übernommen. So ist kein eigener Abruf nötig. Details, die in den letzten 90 Tagen abgerufen wurden, bleiben unverändert.

## Falsche Angaben korrigieren

Auf der Seite der Organisation:

- Mit **Bearbeiten** kannst du Name, Branche, Größe, Standort, Gründungsjahr, Beschreibung, Website, LinkedIn, Notizen und deine Beziehung zur Organisation ändern. Deine Änderungen bleiben erhalten. Leere ein Feld, um wieder den abgerufenen Wert zu verwenden.
- Wähle in **Bearbeiten** die Option **Falsche Firma, Details löschen**, wenn die falsche Firma ausgewählt wurde.
- Mit **Neu nachschlagen** kannst du aktuelle Details abrufen. Die Option wird angezeigt, sobald die alten Details gelöscht wurden.
