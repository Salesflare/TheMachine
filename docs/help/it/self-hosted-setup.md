---
title: Usa la tua Machine sul tuo computer
area: getting-started
summary: Installa l’app open source su Linux, macOS o Windows. È gratis e usa il tuo modello e i tuoi dati.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
translated: 73526b82818f009d
---
Usa gratis la tua Machine sul tuo computer. È open source (AGPL) e i tuoi dati restano con te. Per installarla serve un terminale. Collegare i tuoi account, invece, non ne richiede uno.

## Requisiti

- OpenClaw 2026.11.2 o versioni successive, l’agente open source su cui si basa The Machine. Il programma di installazione ti proporrà di installarlo.
- Python 3.12 o versioni successive e Node.js 24 (24.22.1 o versioni successive) oppure 26.12.1 o versioni successive, non la versione 25.
- Tailscale, per raggiungere la dashboard dal telefono.
- Un normale account utente, non root.

## Installazione

Su Linux o macOS (macOS è in beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Su Windows (beta), l’app viene eseguita in WSL2. In PowerShell, esegui `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. Configura WSL2 con Ubuntu e tutto ciò che serve all’app, poi esegue `./install.sh`.

Il programma di installazione trova i tuoi account, li collega uno alla volta e mostra un’anteprima della settimana scorsa prima di attivare qualsiasi cosa.

## Dopo l’installazione

- Collega la tua posta: in cima a **Attività**, premi **Gmail** (o **Outlook**), poi **Abbina questa Machine** per abbinarla al tuo account. Se non hai un account, **Usa la tua app** si trova subito sotto.
- Poi premi **Accedi con Google** (oppure **Accedi con Microsoft** per Outlook). Posta e calendario vengono collegati insieme.
- Per le altre fonti, vai su **Connessioni** e poi scegli il tipo di fonte. Per usare il tuo client Google o la tua app Entra: esegui `assistant connect` in un terminale.
- Verifica che sia tutto a posto con `assistant doctor`. Il comando mostra una soluzione per ogni problema.
- Viene installata la versione firmata più recente. Anche gli aggiornamenti vengono distribuiti come versioni firmate.
- Abbina la tua Machine al tuo account: dopo aver effettuato l’accesso, l’app per telefono la aprirà. Se annulli l’abbinamento, il collegamento viene rimosso.

La guida completa si trova nel repository: [Guida introduttiva](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
