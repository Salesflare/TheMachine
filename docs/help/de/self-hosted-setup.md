---
title: Auf deinem eigenen Computer ausführen
area: getting-started
summary: Installiere die Open-Source-App unter Linux, macOS oder Windows. Kostenlos, mit deinem eigenen Modell und deinen eigenen Daten.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
translated: 73526b82818f009d
---
Führe The Machine kostenlos auf deinem eigenen Computer aus. Die App ist Open Source (AGPL), und deine Daten bleiben bei dir. Für die Installation brauchst du ein Terminal. Deine Konten zu verbinden, geht ohne.

## Voraussetzungen

- OpenClaw 2026.11.2 oder neuer, der Open-Source-Agent, auf dem The Machine läuft. Das Installationsprogramm bietet an, ihn zu installieren.
- Python 3.12 oder neuer und Node.js 24 (24.22.1 oder neuer) oder 26.12.1 oder neuer, nicht 25.
- Tailscale, damit du dein Dashboard von deinem Handy aus erreichst.
- Ein normales Benutzerkonto, nicht root.

## Installation

Unter Linux oder macOS (macOS ist in der Beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Unter Windows (Beta) läuft die App in WSL2. Führe in PowerShell `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex` aus. Dadurch wird WSL2 mit Ubuntu und allem eingerichtet, was die App braucht. Anschließend wird `./install.sh` ausgeführt.

Das Installationsprogramm findet deine Konten, verbindet sie nacheinander und zeigt eine Vorschau der letzten Woche, bevor etwas aktiviert wird.

## Nach der Installation

- Verbinde deine E-Mails: Klicke oben bei **Aufgaben** auf **Gmail** (oder **Outlook**) und dann auf **Diese Machine koppeln**, um sie mit deinem Konto zu koppeln. **Eigene App nutzen** findest du direkt darunter, wenn du kein Konto hast.
- Klicke dann auf **Mit Google anmelden** (bei Outlook auf **Mit Microsoft anmelden**). E-Mail und Kalender werden gemeinsam verbunden.
- Weitere Quellen: **Verbindungen** und dann den Quellentyp. Für deinen eigenen Google-Client oder deine eigene Entra-App: Führe in einem Terminal `assistant connect` aus.
- Überprüfe alles mit `assistant doctor`. Für jedes Problem wird eine Lösung angezeigt.
- Installiert wird die neueste signierte Version. Auch Updates werden als signierte Versionen bereitgestellt.
- Kopple die App mit deinem Konto. Nach der Anmeldung öffnet sie sich in der Handy-App. Durch das Entkoppeln wird diese Verknüpfung entfernt.

Die vollständige Anleitung findest du im Repository: [Erste Schritte](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
