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

Onder **Beloftes** op de To-do's-pagina:

- Wat jij zei dat je zou doen, en voor wie: **Jouw beloftes**.
- Wat anderen zeiden dat ze zouden doen: **Aan jou beloofd**.

Bij elke belofte staat een menu **⋯**:

- **Doe het** bij jouw beloftes: de belofte wordt meteen een to-do en je Machine bereidt die voor. **Herinneren** bij beloftes aan jou: je Machine maakt een kort opvolgbericht in het gesprek waarin ze het hebben beloofd, terwijl jij op de lijst blijft. Je ziet een kort bericht dat die eraan komt, met **Open to-do**, en bij de belofte staat ‘nu een to-do’. Er wordt niets verstuurd totdat jij dat doet. Is het al een to-do, dan wordt die geopend.
- **Als gedaan markeren**: de belofte is nagekomen.
- **Gaat niet door**: de belofte gaat niet door. Je Machine houdt die niet meer bij en maakt er geen to-do van.

Een open belofte wordt rond de datum vanzelf ook een to-do (jouw belofte de ochtend ervoor, zodat je een dag hebt om die na te komen; een belofte aan jou de ochtend erna, als die nog openstaat). De belofte verschijnt op die dag in de [Agenda](calendar.md). Is het nu een to-do, dan linkt de belofte ernaartoe. Met **Als gedaan markeren** of **Gaat niet door** wordt die to-do ook gesloten. Zodra je Machine ziet dat de belofte is nagekomen, worden ze allebei gesloten en verschijnt er een regel die dat aangeeft.

Een antwoord dat het werk alleen belooft, zoals "Ik stuur de bestanden dinsdag", rondt de to-do niet af. De to-do blijft open met die datum en de belofte verwijst ernaar. Dat staat in het nakijkscherm voordat je verstuurt.

Is de belofte al nagekomen, bijvoorbeeld met een antwoord dat je hebt verstuurd of een meeting waarin die is afgehandeld? Dan wordt die vanzelf gesloten, zonder to-do.

Krijgt de belofte later een nieuwe datum, bijvoorbeeld ‘toch volgende week’? Dan wordt dezelfde belofte verplaatst, net als de bijbehorende to-do. Er komt geen tweede to-do bij. Op de pagina van de belofte staan de nieuwe datum en het nieuwere bericht.

Een belofte zonder datum krijgt een **opvolgdag**: drie dagen nadat jij de belofte hebt gedaan, of een week nadat de ander dat heeft gedaan. Staat die dan nog open? Dan wordt het een to-do.

Bij beloftes in Slack staat de naam van de persoon.

Een belofte per e-mail van iemand aan wie je nog nooit hebt geschreven, wordt ook bijgehouden en gemarkeerd als **niet-geverifieerde afzender**: het is alleen hun woord. De bijbehorende to-do begint met ‘Niet bevestigd: je hebt deze persoon nog nooit geschreven.’

## Terugbetalingen

Als een winkel, luchtvaartmaatschappij, verhuurder of verzekeraar belooft je geld terug te betalen, bijvoorbeeld voor een geannuleerde bestelling of een goedgekeurde claim, houdt je Machine het bedrag, de betaler en de verwachte datum bij. De belofte staat onder **Aan jou beloofd**. Dat gebeurt alleen als het bericht alle drie duidelijk vermeldt.

Komt het geld eerder terug, bijvoorbeeld volgens een e-mail met ‘terugbetaling verwerkt’, een melding van een betaaldienst of een melding van je bankapp op je telefoon? Dan wordt de belofte vanzelf gesloten, zonder to-do.

Is het geld er die dag nog niet? Dan verschijnt er één onopvallende to-do: ‘Vraag de terugbetaling van €42 na bij …’, met een korte e-mail aan de betaler waarin het bestel- of dossiernummer staat. Er wordt niets verstuurd totdat jij dat doet. Komt het geld uiteindelijk toch binnen, dan wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je die één dag terug.

In het [wekelijkse overzicht](weekly-recap.md) staan nagekomen en open beloftes. Op je eigen computer toont `assistant promises` ze in een terminal.
