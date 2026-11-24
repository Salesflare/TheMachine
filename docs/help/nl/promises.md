---
title: Beloftes
area: cards
summary: Wat je hebt beloofd en wat anderen jou hebben beloofd. Wordt vanzelf bijgehouden.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 0bc6594bbd8f4c0b
---
Houd bij wat je hebt beloofd en wat anderen jou hebben beloofd. Je Machine herkent beloftes vanzelf in je berichten.

## Waar je ze vindt

Onder **Beloftes** op de pagina To-do's:

- Wat jij zei dat je zou doen, en voor wie: **Jouw beloftes**.
- Wat anderen zeiden dat ze zouden doen: **Aan jou beloofd**.

Bij elke belofte staat een menu **⋯**:

- **Doe het** bij jouw beloftes: de belofte wordt meteen een to-do en je Machine maakt die voor je klaar. **Herinneren** bij hun beloftes: je Machine maakt een korte herinnering als concept op de plek waar ze het hebben beloofd, terwijl jij in de lijst blijft. Een korte melding zegt dat die eraan komt, met **Open to-do**, en bij de belofte staat ‘nu een to-do’. Er wordt niets verstuurd totdat jij het verstuurt. Is het al een to-do, dan wordt die geopend.
- **Als gedaan markeren**: de belofte is nagekomen.
- **Gaat niet door**: het gaat niet gebeuren, dus je Machine houdt het niet langer bij en maakt er geen to-do van.

Een open belofte wordt rond de datum vanzelf ook een to-do (die van jou de ochtend ervoor, zodat je een dag hebt om het te doen; die van hen de ochtend erna, als de belofte nog openstaat). De belofte staat ook op de betreffende dag in de [Agenda](calendar.md). Is het nu een to-do, dan linkt de belofte ernaartoe. Met **Als gedaan markeren** of **Gaat niet door** wordt die to-do ook gesloten. Zodra je Machine ziet dat de belofte is nagekomen, worden ze allebei gesloten en verschijnt er een melding.

Een antwoord waarin iemand alleen belooft het werk te doen, zoals ‘Ik stuur de bestanden dinsdag’, voltooit de to-do niet. De to-do blijft open met die datum en de belofte linkt ernaartoe. De controle voordat je iets verstuurt, vermeldt dit.

Is de belofte al nagekomen, bijvoorbeeld doordat je een antwoord hebt verstuurd of het onderwerp tijdens een meeting is besproken? Dan wordt die vanzelf gesloten, zonder to-do.

Als iemand antwoordt op een belofte die diegene heeft gedaan, blijft de belofte open totdat uit het antwoord blijkt dat die is nagekomen. Een ‘Zeker’ of een gedeeltelijke uitvoering is niet genoeg. Staat er een herinnering klaar om te versturen, dan wordt die geannuleerd en blijft de to-do open met de melding ‘Ze hebben opnieuw geschreven’. Een automatisch afwezigheidsbericht verandert niets.

Krijg je later een nieuwe datum, bijvoorbeeld ‘toch volgende week’? Dan wordt dezelfde belofte verplaatst, net als de bijbehorende to-do. Er komt geen tweede to-do bij. Op de pagina van de belofte staan de nieuwe datum en het nieuwere bericht.

Een belofte zonder datum krijgt een opvolgdatum: drie dagen nadat jij die hebt gedaan, of een week nadat iemand anders die heeft gedaan. Staat de belofte dan nog open? Dan wordt die een to-do.

Bij beloftes uit Slack staat de naam van de persoon.

Een belofte per e-mail van iemand aan wie je nog nooit hebt geschreven, wordt ook bijgehouden en gemarkeerd als **niet-geverifieerde afzender**: je hebt alleen hun woord. De to-do begint met ‘Niet geverifieerd: je hebt deze persoon nog niet eerder geschreven.’

## Terugbetalingen

Als een winkel, luchtvaartmaatschappij, verhuurder of verzekeraar je geld terug belooft, bijvoorbeeld een terugbetaling voor een geannuleerde bestelling of een goedgekeurde claim, houdt je Machine het bedrag, de betaler en de verwachte datum bij. Je vindt dit onder **Aan jou beloofd**. Alleen als het bericht alle drie duidelijk vermeldt.

Komt het geld eerst terug, bijvoorbeeld via een e-mail met ‘terugbetaling verwerkt’, een melding van een betaaldienst of een melding van je bankapp op je telefoon? Dan wordt de belofte vanzelf gesloten, zonder to-do.

Is het geld er op die datum nog niet? Dan verschijnt er één stille to-do: ‘Vraag naar de terugbetaling van €42 bij …’, met een korte e-mail waarin het bestel- of dossiernummer staat. Er wordt niets verstuurd totdat jij het verstuurt. Komt het geld alsnog binnen, dan wordt de to-do vanzelf gesloten. Met **Ongedaan maken** kun je die een dag lang terugzetten.

In het [wekelijkse overzicht](weekly-recap.md) staan de nagekomen en open beloftes. Op je eigen computer toont `assistant promises` ze in een terminal.
