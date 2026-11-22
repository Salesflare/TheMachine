---
title: Draai The Machine op je eigen computer
area: getting-started
summary: Installeer de opensource-app op Linux, macOS of Windows. Gratis, met je eigen model en gegevens.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
translated: 73526b82818f009d
---
Gebruik The Machine gratis op je eigen computer. De app is opensource (AGPL) en je gegevens blijven van jou. Voor de installatie heb je een terminal nodig. Je accounts koppelen kan gewoon zonder.

## Wat je nodig hebt

- OpenClaw 2026.11.2 of nieuwer, de opensource-agent waarop The Machine draait. De installateur biedt aan om OpenClaw te installeren.
- Python 3.12 of nieuwer en Node.js 24 (24.22.1 of nieuwer) of 26.12.1 of nieuwer, geen 25.
- Tailscale, om het dashboard vanaf je telefoon te openen.
- Een normaal gebruikersaccount, geen root.

## Installeren

Op Linux of macOS (macOS is in bèta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Op Windows (bèta) draait de app in WSL2. Voer in PowerShell `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex` uit. Hiermee wordt WSL2 met Ubuntu en alles wat de app nodig heeft ingesteld. Daarna wordt `./install.sh` uitgevoerd.

De installateur vindt je accounts, koppelt ze een voor een en toont een voorbeeld van de afgelopen week voordat er iets wordt ingeschakeld.

## Na de installatie

- Koppel je e-mail: klik bovenaan **To-do's** op **Gmail** (of **Outlook**) en daarna op **Koppel deze Machine** om hem aan je account te koppelen. **Je eigen app gebruiken** staat er direct onder als je geen account hebt.
- Klik daarna op **Inloggen met Google** (of **Inloggen met Microsoft** voor Outlook). Je e-mail en agenda worden samen gekoppeld.
- Andere bronnen: **Koppelingen**, gevolgd door het type bron. Je eigen Google-client of Entra-app instellen: voer `assistant connect` uit in een terminal.
- Controleer alles met `assistant doctor`. De opdracht geeft voor elk probleem een oplossing.
- De nieuwste ondertekende versie wordt geïnstalleerd. Updates worden ook als ondertekende versies uitgebracht.
- Koppel hem aan je account. Nadat je bent ingelogd, opent de telefoon-app hem. Als je de koppeling verwijdert, wordt deze link gewist.

De volledige handleiding staat in de repository: [Aan de slag](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
