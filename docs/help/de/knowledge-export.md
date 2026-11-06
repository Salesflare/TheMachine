---
title: Wissen für eine andere KI
area: settings
summary: Nimm mit, was deine Machine gelernt hat, zu jeder anderen KI, als einfache Markdown-, JSONL- und CSV-Dateien.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
Alles, was deine Machine lernt, gehört dir. Nimm es zu einer anderen KI mit oder behalte es, auch wenn du The Machine nicht mehr nutzt.

## Exportieren

1. Drücke in **Einstellungen** › **Allgemein** auf **Exportieren** neben **Wissen für eine andere KI**.
2. Lass **Nachrichtentext** aus, dann steht nur drin, woher alles kam und wann. Schalte es ein, um den Text dazuzunehmen.
3. **Privat und Vorsichtig** bleibt aus, außer du willst auch Nur-du-Projekte, private Verläufe und Fleets auf Vorsichtig darin haben.
4. Setze optional eine **Passphrase** mit mindestens 10 Zeichen, um die Datei zu verschlüsseln.
5. Drücke auf **Herunterladen**. Die Datei entsteht auf deiner Machine und lässt sich einmal herunterladen.

Auf einer gehosteten Machine geht es genauso, in den Einstellungen deiner Machine. Auf deinem eigenen Computer macht `assistant export-knowledge` dieselbe Datei.

## Was drin ist

- Personen, Organisationen und Projekte: je eine Markdown-Seite, mit ihren Beziehungen.
- Fakten und Vorlieben: was deine Machine weiß, über dich und über sie.
- Regeln, wie du schreibst, und Signaturen: wonach sich deine Entwürfe richten.
- Skills: deine Anleitungen, an und aus.
- Kontext: Team-Briefings, Zusammenfassungszeilen, Versprechen und offene Aufgaben.
- Quellen: woher alles kam, mit ID und Datum.

Datensätze sind JSONL, Kontakte und Aufgaben auch CSV. Eine README.md ganz oben erklärt den Aufbau und sagt einer KI, wie sie es nutzt. Gib der KI den Ordner oder die ZIP-Datei als Wissensdatei oder Projekt.

## Was draußen bleibt

Passwörter, Schlüssel und Anmeldungen kommen nie hinein. Was wie ein Schlüssel aussieht, wird ersetzt. Daten von Teamkollegen und anderen Machines, Einstellungen und Fotos bleiben auch draußen. Für eine vollständige Kopie zum Umziehen deiner Machine siehe [Auf deinen eigenen Computer umziehen](moving.md).

Das Format ist offen und versioniert: siehe [das Schema](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
