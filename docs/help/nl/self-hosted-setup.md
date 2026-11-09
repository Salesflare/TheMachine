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

- OpenClaw 2026.11.2 of nieuwer. Het installatieprogramma biedt aan om het te installeren.
- Python 3.12 of nieuwer, en Node.js 24 (24.22.1 of nieuwer) of 26.12.1 of nieuwer, niet 25.
- Tailscale, om je dashboard vanaf je telefoon te bereiken.
- Je eigen gebruikersaccount, niet root.

## Installeren

Op Linux of macOS (macOS is in bèta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Op Windows (bèta) draait het in WSL2. Voer in PowerShell `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex` uit. Dat zet WSL2 op met Ubuntu en alles wat de app nodig heeft, en voert dan `./install.sh` uit.

Het installatieprogramma vindt je accounts, koppelt ze een voor een en toont een voorbeeld van vorige week voordat er iets aangaat.

## Na de installatie

- Koppel je mail: bovenaan **To-do's** druk je op **Gmail** (of **Outlook**), dan op **Koppel deze Machine** om hem aan je account te koppelen. Zonder account staat **Je eigen app gebruiken** er meteen onder.
- Druk dan op **Inloggen met Google** (of **Inloggen met Microsoft** voor Outlook). Mail en agenda koppelen samen.
- Andere bronnen: **Koppelingen**, dan **+ Toevoegen**. Je eigen Google-client of Entra-app: `assistant connect` in een terminal.
- Controleer alles met `assistant doctor`. Het toont een oplossing voor elk probleem.
- Het installatieprogramma neemt de nieuwste ondertekende release, en ook updates komen als ondertekende releases.
- Gekoppeld aan The Machine Network deelt je Machine zijn Tailscale-adres met je account, zodat de app op je telefoon hem opent nadat je je aanmeldt. Ontkoppelen wist het.

De volledige gids staat in de repository: [Aan de slag](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
