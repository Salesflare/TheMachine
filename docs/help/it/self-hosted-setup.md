---
title: Usala sul tuo computer
area: getting-started
summary: Installa l'app open source su Linux, macOS o Windows. Gratis, con il tuo modello e i tuoi dati.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
The Machine è open source (AGPL). Sul tuo computer è gratis, e i tuoi dati restano lì.

## Cosa serve

- OpenClaw 2026.10.7 o più recente. Il programma di installazione si offre di installarlo.
- Python 3.12 o più recente, e Node.js 24 (24.22.1 o più recente) oppure 26.12.1 o più recente, non 25.
- Tailscale, per raggiungere la dashboard dal telefono.
- Il tuo account utente, non root.

## Installala

Su Linux o macOS (macOS è in beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Su Windows (beta), funziona dentro WSL2. In PowerShell, esegui `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. Configura WSL2 con Ubuntu e tutto ciò che serve all'app, poi esegue `./install.sh`.

Il programma di installazione trova i tuoi account, li collega uno alla volta e mostra un'anteprima della settimana scorsa prima di attivare qualsiasi cosa.

## Dopo l'installazione

- Aggiungi fonti con `assistant connect`, oppure con **Connessioni**, poi **+ Aggiungi**, nella dashboard.
- Controlla tutto con `assistant doctor`. Mostra una soluzione per ogni problema.
- Gli aggiornamenti arrivano come release firmate.

La guida completa è nel repository: [Getting started](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
