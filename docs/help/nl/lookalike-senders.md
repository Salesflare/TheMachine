---
title: Afzenders die zich voordoen als iemand anders
area: security
summary: Mail van een adres dat lijkt op dat van iemand met wie je contact hebt, wordt gemarkeerd in de bijbehorende to-do. Concepten worden nooit naar dat adres gestuurd.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 15a6a5dafcfa807b
---
## Wat wordt herkend

Sommige oplichters gebruiken een adres dat lijkt op een adres dat je kent: `examp1e.com` in plaats van `example.com`, `example-billing.com`, met één andere letter of met twee verwisselde letters. The Machine vergelijkt het domein van elke afzender met de domeinen waarmee je al contact hebt.

Van twee op elkaar lijkende adressen is het adres waarnaar je zelf hebt gemaild, waarvan je de afzender hebt ontmoet of dat je zelf hebt ingesteld het echte adres, zelfs als het andere adres als eerste heeft gemaild. Als geen van beide zich op die manier onderscheidt, geldt het nieuwste adres als het adres dat zich voordoet als het andere.

Dezelfde naam met een andere extensie, zoals `example.nl` naast `example.com`, hoort bij dezelfde organisatie en is geen imitatie. Gratis e-mailadressen zoals gmail.com tellen nooit mee.

## In een to-do

In een to-do over zo'n bericht staat duidelijk wat er aan de hand is, bijvoorbeeld: "Dit is Alex niet. Het bericht komt van examp1e.com, niet van example.com." De afzender wordt weergegeven met alleen het e-mailadres, zonder afbeelding of link naar de persoon die wordt nagebootst.

## Wat The Machine niet doet

- Hij geeft een afzender die zich voordoet als iemand anders nooit een rol in je Graph en maakt van diens domein nooit de organisatie van een project.
- Hij voegt die afzender nooit samen met de persoon die wordt nagebootst, zelfs niet als ze onder dezelfde naam in hetzelfde gesprek schrijven. Hij stelt die afzender ook nooit voor onder **Zelfde persoon?**.
- Een antwoord dat hij voorbereidt, gaat naar het bekende adres en niet naar het adres dat zich voordoet als het andere.

Je eigen keuze gaat altijd voor: je kunt die afzender nog steeds een rol geven, samenvoegen of naar elk adres schrijven.
