---
title: Afzenders die zich voordoen als bekenden
area: security
summary: Mail van een adres dat lijkt op dat van iemand met wie je contact hebt, wordt gemarkeerd in de bijbehorende to-do. Concepten worden nooit naar dat adres gestuurd.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## Wat The Machine herkent

Sommige scams komen van een adres dat lijkt op een adres dat je kent: `examp1e.com` voor `example.com`, `example-billing.com` of een adres met één andere letter. The Machine vergelijkt het domein van elke afzender met de domeinen van mensen met wie je al contact hebt. Lijkt het nieuwere domein alleen maar op een bekend domein, dan markeert hij het als een lookalike.

Dezelfde naam met een andere extensie, zoals `example.nl` naast `example.com`, hoort bij dezelfde organisatie en is geen lookalike. Gratis e-mail zoals gmail.com telt nooit mee.

## In een to-do

In een to-do over zo'n bericht staat duidelijk wat er aan de hand is, bijvoorbeeld: "Dit is Alex niet. Het bericht komt van examp1e.com, niet van example.com." De afzender wordt weergegeven als het kale e-mailadres, zonder profielfoto of link naar de persoon die hij imiteert.

## Wat The Machine niet doet

- Hij geeft een lookalike-afzender nooit een rol in je Graph.
- Hij voegt zo'n afzender nooit samen met de persoon die hij imiteert en stelt hem nooit voor onder **Zelfde persoon?**.
- Een antwoord dat hij opstelt, gaat naar het geregistreerde adres, niet naar het lookalike-adres.

Je eigen keuze gaat altijd voor: je kunt die afzender nog steeds een rol geven, samenvoegen of naar elk adres schrijven.
