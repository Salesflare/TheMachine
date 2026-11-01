---
title: Auf deinem eigenen Computer betreiben
area: getting-started
summary: Installiere die Open-Source-App unter Linux, macOS oder Windows. Kostenlos, mit deinem eigenen Modell und deinen eigenen Daten.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
The Machine ist Open Source (AGPL). Auf deinem eigenen Computer ist sie kostenlos, und deine Daten bleiben dort.

## Was sie braucht

- OpenClaw 2026.10.7 oder neuer. Der Installer bietet an, es zu installieren.
- Python 3.12 oder neuer und Node.js 24 (24.22.1 oder neuer) oder 26.12.1 oder neuer, nicht 25.
- Tailscale, um dein Dashboard von deinem Handy aus zu erreichen.
- Dein eigenes Benutzerkonto, nicht root.

## Installieren

Unter Linux oder macOS (macOS ist in der Beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Unter Windows (Beta) läuft sie in WSL2. Führe in PowerShell `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex` aus. Das richtet WSL2 mit Ubuntu und allem ein, was die App braucht, und führt dann `./install.sh` aus.

Der Installer findet deine Konten, verbindet sie eins nach dem anderen und zeigt eine Vorschau der letzten Woche, bevor irgendetwas eingeschaltet wird.

## Nach der Installation

- Füge Quellen mit `assistant connect` hinzu, oder im Dashboard über **Verbindungen**, dann **+ Hinzufügen**.
- Prüfe alles mit `assistant doctor`. Es zeigt für jedes Problem eine Lösung.
- Updates kommen als signierte Releases.

Die vollständige Anleitung steht im Repository: [Erste Schritte](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
