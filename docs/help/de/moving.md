---
title: Auf einen anderen Computer umziehen
area: getting-started
summary: Exportiere alles, was deine Machine weiß, in eine verschlüsselte Datei und importiere sie auf einer anderen Machine, in der Cloud oder auf deinem eigenen Computer.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
translated: a08d8cd091c7d47b
---
Alles, was deine Machine lernt, gehört dir: Nachrichten, Aufgaben, Entwürfe, der Graph, Erinnerungen und Skills. Nimm alles auf eine andere Machine mit oder bewahre eine Kopie auf.

## Exportieren

Auf deinem eigenen Computer:

1. Öffne **Einstellungen** › **Allgemein** › **Exportieren** und klicke neben „Alles“ auf **Exportieren**.
2. Optional kannst du eine Passphrase festlegen. Ohne Passphrase erhältst du einen Exportcode. Schreib ihn auf, denn du brauchst ihn für den Import.
3. Aktiviere optional **Schlüssel und Tokens einschließen** (erfordert eine Passphrase), damit du deine Quellen nicht erneut verbinden musst.
4. Klicke auf **Export starten** und dann auf **Herunterladen**. Die Datei wird nach 24 Stunden gelöscht oder sofort, wenn du auf **Löschen** klickst.

Bei einer gehosteten Machine öffnet **Exportieren** neben „Alles“ deine Kontoseite. Klicke auf **Alles exportieren** und dann auf **Herunterladen**. Deine Machine löscht die Datei nach 24 Stunden oder sofort, wenn du auf **Jetzt löschen** klickst.

Die Datei ist immer verschlüsselt. Unter **Einstellungen** siehst du anschließend, was sie enthält und was nicht. Bei Google- und Microsoft-Konten, die über unsere gehostete Anmeldung verbunden sind, musst du dich auf der anderen Seite erneut anmelden.

## Importieren

1. Öffne **Einstellungen** › **Allgemein** › **Exportieren**, klicke neben „Importieren“ auf **Datei wählen** und wähle den Export aus.
2. Gib die Passphrase oder den Exportcode ein und klicke auf **Öffnen**. The Machine prüft zuerst die gesamte Datei.
3. Gehostet: Klicke auf **Jetzt importieren**. Auf deinem eigenen Computer: Klicke auf **Durch diesen Export ersetzen** und dann auf **Ersetzen**. The Machine startet in wenigen Minuten damit neu und unter **Einstellungen** steht **Importiert**.

Der Import ersetzt den aktuellen Stand dieser Machine, nachdem eine Kopie erstellt wurde. Es wird nichts automatisch versendet: Ausstehende Nachrichten warten auf dich.

Wenn sich The Machine auf deinem Computer nicht über **Einstellungen** neu starten lässt, werden stattdessen die auszuführenden Befehle angezeigt.

Richte auf einem neuen Computer zuerst [The Machine ein](self-hosted-setup.md). Kündige dann deinen gehosteten Tarif, wenn du ihn nicht mehr brauchst: siehe [Kündigen oder löschen](cancel-and-delete.md).
