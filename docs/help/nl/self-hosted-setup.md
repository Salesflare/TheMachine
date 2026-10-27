---
title: Op je eigen computer draaien
area: getting-started
summary: Installeer de opensource-app op Linux, macOS of Windows. Gratis, met je eigen model en je eigen gegevens.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
The Machine is open source (AGPL). Op je eigen computer is het gratis, en je gegevens blijven daar.

## Wat het nodig heeft

- OpenClaw 2026.10.7 of nieuwer. Het installatieprogramma biedt aan om het te installeren.
- Python 3.12 of nieuwer, en Node.js 24.22.1 of nieuwer (of 26.12.1 of nieuwer).
- Tailscale, om je dashboard vanaf je telefoon te bereiken.
- Je eigen gebruikersaccount, niet root.

## Installeren

Op Linux of macOS (macOS is in bèta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Op Windows (bèta) draait het in WSL2. Voer in PowerShell `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex` uit. Dat zet WSL2 op met Ubuntu en alles wat de app nodig heeft, en voert dan `./install.sh` uit.

Het installatieprogramma vindt je accounts, koppelt ze een voor een en toont een voorbeeld van vorige week voordat er iets aangaat.

## Na de installatie

- Voeg bronnen toe met `assistant connect`, of met **Koppelingen**, dan **+ Toevoegen**, in het dashboard.
- Controleer alles met `assistant doctor`. Het toont een oplossing voor elk probleem.
- Updates komen als ondertekende releases.

De volledige gids staat in de repository: [Aan de slag](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
