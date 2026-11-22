---
title: Beloftes
area: cards
summary: Wat je hebt gezegd dat je zou doen en wat anderen je hebben beloofd. Wordt automatisch bijgehouden.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Houd bij wat je hebt beloofd en wat anderen jou hebben beloofd. Je Machine herkent beloftes in je berichten automatisch.

## Waar je ze vindt

Onder **Beloftes** op de pagina To-do's:

- Wat jij hebt gezegd dat je zou doen, en voor wie: **Jouw beloftes**.
- Wat anderen hebben gezegd dat ze zouden doen: **Aan jou beloofd**.

Bij elke belofte staat een menu **⋯**:

- **Doe het** bij jouw beloftes: de belofte wordt meteen een to-do en je Machine bereidt die voor. **Herinneren** bij beloftes van anderen: je Machine maakt een korte herinnering als concept op de plek waar ze het hebben beloofd, terwijl jij op de lijst blijft. Je ziet een korte melding dat die eraan komt, met **Open to-do**. Bij de belofte staat dan ‘nu een to-do’. Er wordt niets verstuurd totdat jij het verstuurt. Is het al een to-do, dan wordt die geopend.
- **Markeren als gedaan**: de belofte is nagekomen.
- **Gaat niet door**: de belofte wordt niet nagekomen, dus je Machine houdt die niet meer bij en maakt er geen to-do van.

Een open belofte wordt rond de datum automatisch ook een to-do: jouw belofte de ochtend ervoor, zodat je een dag hebt om die uit te voeren; die van iemand anders de ochtend erna, als die nog openstaat. De belofte verschijnt op die dag in de [agenda](calendar.md). Is het nu een to-do, dan linkt de belofte daarnaar. Met **Markeren als gedaan** of **Gaat niet door** wordt ook die to-do gesloten. Zodra je Machine ziet dat de belofte is nagekomen, worden beide gesloten en verschijnt er een melding.

Een antwoord waarin iemand alleen belooft het werk te doen, zoals ‘Ik stuur de bestanden uiterlijk dinsdag’, rondt de to-do niet af. De to-do blijft open met die datum en de belofte linkt ernaar. In de controle voordat je iets verstuurt, staat dit vermeld.

Is de belofte al nagekomen, bijvoorbeeld met een antwoord dat je hebt verstuurd of tijdens een vergadering? Dan wordt die automatisch gesloten, zonder to-do.

Krijgt de belofte later een nieuwe datum, bijvoorbeeld ‘toch volgende week’? Dan wordt dezelfde belofte verplaatst, net als de to-do. Er komt geen tweede. Op de pagina staat de nieuwe datum en het nieuwere bericht.

Een belofte zonder datum krijgt een **herinneringsdag**: drie dagen nadat jij die hebt gedaan, of een week nadat iemand anders die heeft gedaan. Staat die dan nog open? Dan wordt die een to-do.

Bij beloftes uit Slack staat de naam van de persoon.

Ook een belofte per e-mail van iemand aan wie je nog nooit hebt geschreven, wordt bijgehouden. Die krijgt het label **onbekende afzender**: je hebt alleen hun woord. De to-do begint met ‘Onbekend: je hebt die persoon nog nooit geschreven.’

## Terugbetalingen

Als een winkel, luchtvaartmaatschappij, verhuurder of verzekeraar belooft je geld terug te betalen, bijvoorbeeld voor een geannuleerde bestelling of een goedgekeurde claim, houdt je Machine het bedrag, de betaler en de verwachte datum bij. De belofte staat onder **Aan jou beloofd**. Alleen als het bericht alle drie duidelijk vermeldt.

Komt het geld eerst terug, bijvoorbeeld via een e-mail met ‘terugbetaling verwerkt’, een melding van een betaaldienst of een melding van je bankapp op je telefoon? Dan wordt de belofte automatisch gesloten, zonder to-do.

Is het geld die dag nog niet binnen? Dan verschijnt er één rustige to-do: ‘Vraag naar de terugbetaling van €42 bij …’, met een korte e-mail aan de betaler waarin het bestel- of zaaknummer staat. Er wordt niets verstuurd totdat jij het verstuurt. Komt het geld alsnog binnen, dan wordt de to-do automatisch gesloten. Met **Ongedaan maken** zet je die voor één dag terug.

In het [wekelijkse overzicht](weekly-recap.md) staan de nagekomen en open beloftes. Op je eigen computer geeft `assistant promises` ze weer in een terminal.
