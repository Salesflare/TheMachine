---
title: Nagebootste afzenders
area: security
summary: Mail van een adres dat lijkt op dat van iemand met wie je contact hebt, wordt gemarkeerd op de bijbehorende to-do. Concepten worden nooit naar dat adres gestuurd.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## Wat The Machine herkent

Sommige oplichters gebruiken een adres dat lijkt op een adres dat je kent: `examp1e.com` in plaats van `example.com`, `example-billing.com` of met één letter verschil. The Machine vergelijkt het domein van elke afzender met de domeinen waarmee je al contact hebt. Als het nieuwere domein alleen maar lijkt op een bekend domein, ziet hij het als een nagebootst domein.

Dezelfde naam met een andere extensie, zoals `example.nl` naast `example.com`, is dezelfde organisatie en geen nagebootst domein. Gratis e-maildiensten zoals gmail.com tellen nooit mee.

## Bij een to-do

Bij een to-do over zo'n bericht staat dat er duidelijk bij, bijvoorbeeld: "Dit is Alex niet. Het bericht komt van examp1e.com, niet van example.com." De afzender wordt alleen met het e-mailadres weergegeven, zonder foto of link naar de persoon die hij nadoet.

## Wat The Machine niet doet

- Hij geeft een nagebootste afzender nooit een rol in je Graph.
- Hij voegt nagebootste afzenders nooit samen met de persoon die ze nadoen en stelt ze nooit voor onder **Zelfde persoon?**.
- Een antwoord dat hij opstelt, gaat naar het bekende adres, niet naar het nagebootste adres.

Je eigen keuze gaat altijd voor: je kunt ze nog steeds een rol geven, samenvoegen of naar elk adres schrijven.
