---
title: Beloftes
area: cards
summary: Wat je hebt beloofd en wat anderen jou hebben beloofd. Wordt automatisch bijgehouden.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: b624394de7ff77b1
---
Houd bij wat je hebt beloofd en wat anderen jou hebben beloofd. Je Machine herkent beloftes in je berichten automatisch.

## Waar je ze vindt

Onder **Beloftes** op de pagina To-do's:

- Wat je hebt beloofd en aan wie: **Jouw beloftes**.
- Wat anderen hebben beloofd: **Aan jou beloofd**.

Bij elke belofte staat een menu **⋯**:

- **Doe het** bij jouw beloftes: die wordt meteen een to-do en je Machine bereidt hem voor. **Herinneren** bij beloftes van anderen: je Machine maakt een kort vervolgbericht als concept op de plek waar ze de belofte hebben gedaan, terwijl jij op de lijst blijft. Je ziet een korte melding dat het eraan komt, met **Open to-do**, en de belofte krijgt de status 'nu een to-do'. Er wordt niets verstuurd totdat jij het verstuurt. Een belofte die al een to-do is, opent die to-do.
- **Als gedaan markeren**: de belofte is nagekomen.
- **Gaat niet door**: de belofte wordt niet nagekomen, dus je Machine houdt hem niet langer bij en maakt er geen to-do van.

Een open belofte wordt rond de datum vanzelf een to-do. Bij jouw beloftes gebeurt dat de ochtend ervoor, zodat je een dag hebt om het te doen. Bij beloftes van anderen gebeurt dat de ochtend erna, als ze nog openstaan. De belofte verschijnt op de betreffende dag in de [Agenda](calendar.md). Een belofte die nu een to-do is, linkt naar die to-do. Met **Als gedaan markeren** of **Gaat niet door** sluit je die to-do ook af. Zodra je Machine ziet dat de belofte is nagekomen, worden ze allebei gesloten en verschijnt er een melding.

Een antwoord waarin alleen wordt beloofd dat het werk wordt gedaan, zoals 'Ik stuur de bestanden uiterlijk dinsdag', voltooit de to-do niet. De to-do blijft open met die datum en de belofte linkt ernaar. De verzendcontrole laat dit zien voordat je het bericht verstuurt. Als je de tekst eerst wijzigt, verdwijnen de oude belofte en datum. De to-do blijft open totdat je Machine ziet dat het werk is gedaan. Een belofte in wat je verstuurt, wordt eraan gekoppeld.

Is de belofte al nagekomen, bijvoorbeeld in een antwoord dat je hebt verstuurd of tijdens een meeting? Dan wordt die vanzelf gesloten, zonder to-do.

Als iemand antwoordt over een belofte die diegene heeft gedaan, blijft die open totdat uit het antwoord blijkt dat de belofte is nagekomen. Een 'Zeker' of een gedeeltelijke reactie geldt niet als nakoming. Stond er een herinnering klaar om te versturen, dan wordt die geannuleerd en blijft de to-do open met de melding 'Ze hebben weer geschreven'. Een automatisch afwezigheidsbericht verandert niets.

Krijgt een belofte later een nieuwe datum, zoals 'dan liever volgende week'? Dan verschuift dezelfde belofte, en ook de bijbehorende to-do, zonder dat er een tweede bijkomt. Op de pagina van de belofte zie je de nieuwe datum en het nieuwere bericht.

Een belofte zonder datum krijgt een **opvolgdag**: drie dagen nadat jij de belofte hebt gedaan, of een week nadat de ander dat heeft gedaan. Staat die dan nog open? Dan wordt het een to-do.

Beloftes uit Slack tonen de naam van de persoon.

Een belofte per e-mail van iemand aan wie je nog nooit hebt geschreven, wordt ook bijgehouden, met de markering **niet-geverifieerde afzender**: je kunt alleen op hun woord afgaan. De to-do begint met 'Niet geverifieerd: je hebt die persoon nog niet eerder gemaild.'

## Terugbetalingen

Als een winkel, luchtvaartmaatschappij, verhuurder of verzekeraar belooft je geld terug te betalen, bijvoorbeeld voor een geannuleerde bestelling of een goedgekeurde claim, houdt je Machine het bedrag, de betaler en de verwachte datum bij. De belofte verschijnt onder **Aan jou beloofd**. Alleen als het bericht alle drie duidelijk vermeldt.

Als het geld eerder terugkomt, bijvoorbeeld via een e-mail dat de terugbetaling is verwerkt, een melding van een betaaldienst of een melding van je bankapp op je telefoon, wordt de belofte vanzelf gesloten, zonder to-do.

Nog niet binnen op die dag? Dan verschijnt er één stille to-do: 'Vraag na waar de terugbetaling van €42 van … blijft', met een korte e-mail waarin het bestel- of zaaknummer staat. Er wordt niets verstuurd totdat jij het verstuurt. Komt het geld later alsnog binnen, dan wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem één dag terug.

In het [weekoverzicht](weekly-recap.md) zie je hoeveel beloftes zijn nagekomen en hoeveel er nog openstaan. Op je eigen computer geeft `assistant promises` ze weer in een terminal.
