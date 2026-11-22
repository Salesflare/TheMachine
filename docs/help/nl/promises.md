---
title: Beloftes
area: cards
summary: Wat jij hebt beloofd en wat anderen jou hebben beloofd. Wordt automatisch bijgehouden.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: ba0e2190e1b8b791
---
Houd bij wat jij hebt beloofd en wat anderen jou hebben beloofd. Je Machine herkent zelf beloftes in je berichten.

## Waar je ze vindt

Onder **Beloftes** op de pagina To-do's:

- Wat jij hebt beloofd te doen, en voor wie: **Jouw beloftes**.
- Wat anderen hebben beloofd te doen: **Aan jou beloofd**.

Bij elke belofte staat een menu **⋯**:

- **Doe het** bij jouw beloftes: de belofte wordt meteen een to-do en je Machine bereidt die voor. **Herinneren** bij hun beloftes: je Machine maakt een kort vervolgbericht als concept op de plek waar ze het hebben beloofd, terwijl jij op de lijst blijft. Je ziet een kort bericht dat het eraan komt, met **Open to-do**, en bij de belofte staat ‘nu een to-do’. Er wordt niets verstuurd totdat jij het verstuurt. Is het al een to-do, dan wordt die geopend.
- **Als gedaan markeren**: de belofte is nagekomen.
- **Gaat niet door**: de belofte wordt niet nagekomen, dus je Machine houdt die niet meer bij. Er wordt geen to-do aangemaakt.

Een open belofte wordt rond de datum vanzelf ook een to-do. Bij jouw beloftes gebeurt dat de ochtend ervoor, zodat je een dag hebt om het te doen. Bij beloftes van anderen gebeurt dat de ochtend erna, als de belofte dan nog openstaat. De belofte staat op de betreffende dag in de [Agenda](calendar.md). Is het al een to-do, dan linkt de belofte ernaar. Met **Als gedaan markeren** of **Gaat niet door** wordt die to-do ook gesloten. Zodra je Machine ziet dat de belofte is nagekomen, worden beide gesloten en staat erbij dat dat is gebeurd.

Een antwoord waarin iemand alleen belooft het werk te doen, zoals ‘Ik stuur de bestanden uiterlijk dinsdag’, maakt de to-do niet af. De to-do blijft open met die datum en de belofte linkt ernaartoe. Je ziet dit in het verzendoverzicht voordat je het bericht verstuurt.

Is de belofte al nagekomen, bijvoorbeeld in een antwoord dat je hebt verstuurd of tijdens een meeting? Dan wordt die vanzelf gesloten, zonder to-do.

Als iemand antwoordt op een belofte die diegene heeft gedaan, blijft die open totdat uit het antwoord blijkt dat de belofte is nagekomen. Een ‘Zeker’, een automatisch antwoord of slechts een deel van de belofte telt niet als nakoming. Stond er een herinnering klaar om te versturen, dan wordt die geannuleerd en blijft de to-do open met ‘Ze hebben weer geschreven’.

Krijgt de belofte later een nieuwe datum, bijvoorbeeld ‘toch volgende week’? Dan wordt dezelfde belofte verplaatst, net als de to-do. Er komt geen tweede to-do bij. Op de pagina zie je de nieuwe datum en het nieuwere bericht.

Een belofte zonder datum krijgt een **opvolgdag**: drie dagen nadat jij die hebt gedaan, of een week nadat iemand anders die heeft gedaan. Staat de belofte dan nog open? Dan wordt het een to-do.

Bij beloftes uit Slack staat de naam van de persoon.

Ook een belofte per e-mail van iemand aan wie je nooit eerder hebt geschreven, wordt bijgehouden. Die krijgt het label **niet-geverifieerde afzender**: je hebt alleen het woord van die persoon. De to-do begint met ‘Niet geverifieerd: je hebt die persoon nog niet eerder geschreven.’

## Terugbetalingen

Als een winkel, luchtvaartmaatschappij, verhuurder of verzekeraar je geld terug belooft, bijvoorbeeld voor een geannuleerde bestelling of een goedgekeurde claim, houdt je Machine het bedrag, de betaler en de verwachte datum bij. De belofte staat onder **Aan jou beloofd**. Alleen als het bericht alle drie duidelijk vermeldt.

Komt het geld eerst terug, bijvoorbeeld via een e-mail waarin staat dat de terugbetaling is verwerkt, een bericht van een betaaldienst of een melding van de bankapp op je telefoon? Dan wordt de belofte vanzelf gesloten, zonder to-do.

Is het geld die dag nog niet binnen? Dan verschijnt er één stille to-do: ‘Vraag naar de terugbetaling van €42 bij …’, met een korte e-mail aan de betreffende partij waarin het bestel- of zaaknummer staat. Er wordt niets verstuurd totdat jij het verstuurt. Komt het geld uiteindelijk toch binnen, dan wordt de to-do vanzelf gesloten. Met **Ongedaan maken** kun je die nog een dag terughalen.

In het [wekelijkse overzicht](weekly-recap.md) staan de nagekomen en open beloftes. Op je eigen computer geeft `assistant promises` ze weer in een terminal.
