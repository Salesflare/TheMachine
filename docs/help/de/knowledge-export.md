---
title: Wissen für eine andere KI
area: settings
summary: Nimm das Wissen, das deine Machine gesammelt hat, als einfache Dateien mit zu jeder anderen KI. Jede KI kann sie lesen.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: db1c7f4768a71630
---
Alles, was deine Machine lernt, gehört dir. Gib es einer anderen KI wie ChatGPT oder Claude oder behalte es.

## Exportieren

1. Öffne **Einstellungen** › **Allgemein** › **Exportieren** und wähle neben **Wissen für eine andere KI** die Option **Exportieren**.
2. **Nachrichtentext** ist standardmäßig deaktiviert: Enthalten sind nur die Herkunft und der Zeitpunkt der einzelnen Elemente. Aktiviere die Option, um den Text hinzuzufügen.
3. Aktiviere **Privat und Vorsichtig** nur, wenn du nur für dich sichtbare Projekte, private Threads und vorsichtige Fleets hinzufügen möchtest.
4. Lege optional eine **Passphrase** fest (mindestens 10 Zeichen), um die Datei zu verschlüsseln.
5. Wähle **Herunterladen**. Die Datei kann nur einmal heruntergeladen werden.

Das funktioniert bei einer gehosteten Machine genauso wie auf deinem eigenen Computer.

## Was enthalten ist

- Personen, Organisationen und Projekte: jeweils eine Markdown-Seite mit ihren Beziehungen untereinander.
- Fakten und Vorlieben: Was deine Machine über dich und die anderen weiß.
- Frühere Fakten: Was nicht mehr gilt, weil es beendet oder ersetzt wurde, und wodurch es ersetzt wurde. Entfernte Fakten bleiben außen vor.
- Regeln, dein Schreibstil und Signaturen: Daran orientieren sich deine Entwürfe.
- Skills: Deine Anleitungen, aktiv und inaktiv.
- Kontext: Team-Briefings, Zusammenfassungen, Versprechen und offene Aufgaben.
- Quellen: Woher die einzelnen Elemente stammen, nach ID und Datum.

Kontakte und Aufgaben sind auch als Tabellen (CSV) enthalten. Eine README-Datei am Anfang erklärt der KI, wie sie alles lesen soll. Lade die ZIP-Datei als Wissensdatei oder Projekt in die KI hoch.

## Was nicht enthalten ist

Passwörter, Schlüssel und Anmeldedaten werden nie aufgenommen. Auch die Daten, Einstellungen und Fotos von Teammitgliedern bleiben außen vor. Wie du deine ganze Machine umziehst, erfährst du unter [Auf einen anderen Computer umziehen](moving.md).

Für Entwickler: [das Dateiformat](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
