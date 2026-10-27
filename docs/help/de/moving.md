---
title: Auf deinen eigenen Computer umziehen
area: getting-started
summary: Exportiere alles von einer gehosteten Machine in einer verschlüsselten Datei und importiere sie auf deinem eigenen Computer.
covers: moving
code: moving.py, cli.py
site: Export everything, Delete it now, Download
order: 5
---
## Exportieren

1. Öffne auf deiner Kontoseite Daten und tippe auf **Alles exportieren**.
2. Lege optional eine Passphrase fest, um deine Schlüssel mitzunehmen. Ohne bekommt der Export einen Code, und diese Quellen müssen neu verbunden werden.
3. Tippe auf **Herunterladen**. Die Datei kommt direkt von deinem Server, der sie nach 24 Stunden löscht, oder sofort mit **Jetzt löschen**.

Die Datei ist immer verschlüsselt. Google braucht auf der anderen Seite immer eine neue Anmeldung. Die Anmeldung für dein Modell und dein Chatverlauf bleiben zurück.

## Importieren

[Installiere The Machine](self-hosted-setup.md) auf deinem eigenen Computer und führe dann `assistant import` mit der Datei aus.

Kündige danach deinen gehosteten Tarif, wenn du ihn nicht mehr brauchst: siehe [Kündigen oder löschen](cancel-and-delete.md).
