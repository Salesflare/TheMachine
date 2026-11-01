---
title: Vrienden en het Network
area: fleet
summary: Voeg vrienden toe op gebruikersnaam, vind mensen die je kent met een Machine, en koppel een Machine op je eigen computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Vrienden

Voeg iemand toe met de exacte gebruikersnaam, in het tabblad **Fleet** onder Vrienden. Vrienden kunnen vragen wie iemand kent, context voor een afspraak en warme introducties krijgen, en zien wanneer je bezet bent (alleen bezette tijden, nooit waarmee). Je kunt een vriend altijd verwijderen of blokkeren.

## Mensen vinden die je kent

In het paneel Network:

- "Kijk welke van mijn contacten een Machine hebben" stelt mensen voor die je kent.
- "Laat mensen die mijn e-mailadres hebben me vinden" laat hen jou vinden.

Allebei staan standaard aan, en uit bij het beveiligingsniveau Voorzichtig. Zet ze uit wanneer je wilt; je keuze blijft. Mensen vinden je via je login-e-mailadres en je gekoppelde adressen, behalve gedeelde zoals info@: die blijven uit tot je ze aanzet.

Mensen die je kent en die op het Network zitten, worden meteen voorgesteld als je het aanzet, en wanneer iemand later aansluit. Een match komt met Verbinden, Niet nu of **Nooit voorstellen**. **Het Network verlaten** haalt je eraf.

## Afspreken met andere Machines

Schrijft iemand met een Machine "laten we volgende week afspreken", dan vraagt je Machine de hunne naar vrije tijden en zoekt hij er een die jullie allebei past, binnen je werkuren. Jullie krijgen elk één to-do, zoals "Afspraak met Alex Example", met de tijd eronder. Tik op **Boek het**, **Andere tijd** of **Niet nodig**. De uitnodiging gaat pas weg als jullie allebei op Boek het tikten.

Alleen vrij of bezet gaat over, end-to-end versleuteld, voor hoogstens 14 dagen en afgerond op 15 minuten. Privé-afspraken tellen als bezet. Een Machine kan alleen vragen als jullie elkaar over en weer mailden. Stel het in in het paneel Network onder **Wat andere Machines de mijne mogen vragen**: **Vrij/bezet om af te spreken** of **Uit**, met de duur van een afspraak, je buffer en voorkeurstijden. Elke vraag staat in Activiteit, onder Agenda.

Geen Machine of geen antwoord: het concept van de e-mail krijgt een link waar de ander een van je vrije tijden kiest. Die keuze wordt een to-do met **Boek het**; er wordt niets geboekt voor je erop tikt.

De link toont alleen vrije tijden, volgens dezelfde regels, en verder niets over jou. Hij loopt af zodra de afspraak geboekt is, of na 14 dagen. In de e-mail staat hij als "Pick a time". Onderaan zegt de pagina dat je Machine deze tijden vond, met "Get yours." en je voornaam. Zet dat uit met **Voettekst bij boekingslinks**. Elke link en keuze staat in Activiteit.

## Een Machine op je eigen computer

Zo sluit je aan op het Network vanaf een Machine die je zelf draait:

1. Druk op je accountpagina op app.themachine.computer op **Een zelf gehoste Machine koppelen**. De code werkt één keer, 15 minuten lang.
2. Voer op je computer `assistant fleet-pair` uit met de code, en herstart.

Maximaal 5 Machines per account. Elke Machine kun je daar ontkoppelen.
