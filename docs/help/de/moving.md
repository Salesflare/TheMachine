---
title: Auf einen anderen Computer umziehen
area: getting-started
summary: Exportiere alles, was deine Machine weiß, in einer verschlüsselten Datei und importiere sie auf einer anderen Machine, gehostet oder deiner eigenen.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
---
Alles, was deine KI lernt, gehört dir: Nachrichten, Unterhaltungen, Aufgaben mit ihrem Verlauf, Entwürfe, der Graph, Erinnerungen, Skills und Agent-Jobs. Du kannst alles mitnehmen, auch wenn du The Machine nicht mehr nutzt.

## Exportieren

Auf deinem eigenen Computer:

1. Tippe in **Einstellungen** › **Allgemein** › **Exportieren** bei Alles auf **Exportieren**.
2. Wähle optional eine Passphrase. Ohne bekommst du einen Exportcode: Schreib ihn auf, der Import braucht ihn.
3. Schalte optional **Schlüssel und Tokens einschließen** ein (braucht eine Passphrase), dann musst du deine Quellen nicht neu verbinden.
4. Tippe auf **Export starten** und dann auf **Herunterladen**. Die Datei wird nach 24 Stunden gelöscht, oder sofort mit **Löschen**.

Auf einer gehosteten Machine öffnet **Exportieren** bei Alles deine Kontoseite. Tippe auf **Alles exportieren** und dann auf **Herunterladen**. Deine Machine löscht die Datei nach 24 Stunden, oder sofort mit **Jetzt löschen**.

Die Datei ist immer verschlüsselt. Nach einem Export zeigen die Einstellungen, was darin ist, mit Anzahlen, und was nicht darin ist und warum. Anmeldungen bei Google und Microsoft über den gehosteten Dienst brauchen auf der anderen Seite immer eine neue Anmeldung.

## Importieren

1. Tippe in **Einstellungen** › **Allgemein** › **Exportieren** bei Importieren auf **Datei wählen** und wähle den Export.
2. Gib seine Passphrase oder seinen Exportcode ein und tippe auf **Öffnen**. The Machine prüft zuerst die ganze Datei.
3. Gehostet: Tippe auf **Jetzt importieren**. The Machine startet in ein paar Minuten damit neu. Auf deinem eigenen Computer: Tippe auf **Durch diesen Export ersetzen** und dann auf **Ersetzen**. The Machine startet in ein, zwei Minuten damit neu, und die Einstellungen zeigen **Importiert**.

Der Import ersetzt, was diese Machine jetzt hat, und behält davon zuerst eine Kopie. Nichts, was wartete, geht von selbst raus: Sendungen in der Warteschlange warten, bis du sie neu sendest.

Für Fortgeschrittene: Auf einem Computer, auf dem The Machine ohne Dienstverwaltung läuft, zeigen die Einstellungen stattdessen die Befehle. Du kannst sie auch selbst ausführen: `assistant service stop`, `assistant import --staged --force`, `assistant service start`.

Auf einem neuen Computer [installierst du zuerst The Machine](self-hosted-setup.md). Kündige danach dein gehostetes Abo, wenn du es nicht mehr brauchst: siehe [Kündigen oder löschen](cancel-and-delete.md).
