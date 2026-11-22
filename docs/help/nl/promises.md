---
title: Beloftes
area: cards
summary: Wat jij zou doen en wat anderen je hebben beloofd. Wordt automatisch bijgehouden.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Houd bij wat jij hebt beloofd en wat anderen je hebben beloofd. Je Machine herkent beloftes automatisch in je berichten.

## Waar je ze vindt

Onder **Beloftes** op de pagina To-do's:

- Wat jij zei dat je zou doen, en voor wie: **Jouw beloftes**.
- Wat anderen zeiden dat ze zouden doen: **Aan jou beloofd**.

Bij elke belofte staat een menu **⋯**:

- **Doe het** bij jouw beloftes: de belofte wordt meteen een to-do en je Machine bereidt die voor. **Herinneren** bij hun beloftes: je Machine maakt een korte herinnering als concept op de plek waar ze het beloofden, terwijl jij in de lijst blijft. Je ziet een korte melding dat de herinnering eraan komt, met **Open to-do**, en de belofte krijgt de status ‘nu een to-do’. Er wordt niets verstuurd totdat jij het verstuurt. Is er al een to-do, dan wordt die geopend.
- **Markeren als gedaan**: de belofte is nagekomen.
- **Gaat niet door**: de belofte komt niet uit. Je Machine houdt die niet langer bij en maakt er geen to-do van.

Een open belofte wordt rond de datum ervan vanzelf ook een to-do (jouw belofte de ochtend ervoor, zodat je een dag hebt om die uit te voeren; die van iemand anders de ochtend erna, als die nog openstaat). De belofte verschijnt op die dag in de [Agenda](calendar.md). Is er nu een to-do van gemaakt, dan linkt de belofte daarnaar. **Markeren als gedaan** of **Gaat niet door** sluit die to-do ook. Zodra je Machine ziet dat de belofte is nagekomen, sluit hij beide af en laat hij dat weten.

Een antwoord waarin iemand alleen belooft het werk te doen, zoals ‘Ik stuur de bestanden uiterlijk dinsdag’, rondt de to-do niet af. De to-do blijft open met die datum en de belofte linkt ernaar. Je ziet dit in de controle voordat je het bericht verstuurt.

Is de belofte al nagekomen, bijvoorbeeld met een antwoord dat je hebt verstuurd of tijdens een vergadering? Dan wordt die vanzelf afgesloten, zonder to-do.

Krijg je later een nieuwe datum, zoals ‘toch volgende week’? Dan wordt dezelfde belofte verplaatst, net als de bijbehorende to-do. Er komt geen tweede bij. Op de pagina van de belofte staan de nieuwe datum en het recentere bericht.

Een belofte zonder datum krijgt een **opvolgdag**: drie dagen nadat jij de belofte hebt gedaan, of een week nadat iemand anders die heeft gedaan. Staat de belofte dan nog open? Dan wordt die een to-do.

Bij beloftes uit Slack staat de naam van de persoon.

Een belofte per e-mail van iemand aan wie je nooit eerder hebt geschreven, wordt ook bijgehouden. Die krijgt het label **onbekende afzender**: je hebt alleen diens woord. De to-do begint met ‘Onbekend: je hebt deze persoon nog nooit gemaild.’

## Terugbetalingen

Als een winkel, luchtvaartmaatschappij, verhuurder of verzekeraar je geld belooft, bijvoorbeeld een terugbetaling voor een geannuleerde bestelling of een goedgekeurde claim, houdt je Machine het bedrag, de betaler en de verwachte datum bij. Je ziet de belofte onder **Aan jou beloofd**. Dat gebeurt alleen als het bericht alle drie duidelijk maakt.

Komt het geld eerst terug, bijvoorbeeld via een e-mail met ‘terugbetaling verwerkt’, een melding van een betaaldienst of een melding van je bankapp op je telefoon? Dan wordt de belofte vanzelf afgesloten, zonder to-do.

Is het geld die dag nog niet binnen? Dan verschijnt er één to-do, zonder verdere melding: ‘Vraag naar de terugbetaling van €42 bij …’, met een korte e-mail aan de betaler waarin het bestel- of claimnummer staat. Er wordt niets verstuurd totdat jij het verstuurt. Komt het geld uiteindelijk toch binnen, dan wordt de to-do vanzelf afgesloten. Met **Ongedaan maken** kun je die nog een dag terugzetten.

De [Weekoverzicht](weekly-recap.md) telt nagekomen en open beloftes. Op je eigen computer toont `assistant promises` ze in een terminal.
