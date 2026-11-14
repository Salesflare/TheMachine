---
title: Beloftes
area: cards
summary: Wat jij hebt beloofd en wat anderen jou hebben beloofd. Wordt automatisch bijgehouden.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 8e5ce7b371ab7fd0
---
Houd bij wat jij hebt beloofd en wat anderen jou hebben beloofd. Je Machine herkent beloftes vanzelf in je berichten.

## Waar je ze vindt

Onder **Beloftes** op de pagina To-do's:

- Wat jij hebt gezegd dat je zou doen, en voor wie: **Jouw beloftes**.
- Wat anderen hebben gezegd dat ze zouden doen: **Aan jou beloofd**.

Bij elke belofte staat een menu **⋯**:

- **Doe het** bij jouw beloftes: die wordt meteen een to-do en je Machine bereidt hem voor. **Herinneren** bij hun beloftes: je Machine maakt een kort concept voor een herinnering op de plek waar ze het beloofd hebben, terwijl jij in de lijst blijft. Er verschijnt een kort bericht dat het eraan komt, met **Open to-do**, en bij de belofte staat ‘nu een to-do’. Er wordt niets verstuurd totdat jij het verstuurt. Een belofte die al een to-do is, opent die to-do.
- **Markeer als gedaan**: de belofte is nagekomen.
- **Gaat niet door**: de belofte gaat niet door. Je Machine houdt hem niet langer bij en maakt er geen to-do van.

Een open belofte wordt rond de datum ook vanzelf een to-do: jouw belofte de ochtend ervoor, zodat je een dag hebt om die na te komen; die van iemand anders de ochtend erna, als hij dan nog openstaat. De belofte staat op de bijbehorende dag in de [Agenda](calendar.md). Een belofte die nu een to-do is, linkt ernaartoe. Met **Markeer als gedaan** of **Gaat niet door** sluit je die to-do ook af. Zodra je Machine ziet dat de belofte is nagekomen, sluit hij ze allebei af en verschijnt er een melding.

Is de belofte al nagekomen, bijvoorbeeld met een antwoord dat je hebt verstuurd of een vergadering waarin je het hebt besproken? Dan wordt die vanzelf afgesloten, zonder to-do.

Krijg je later een nieuwe datum, bijvoorbeeld ‘toch volgende week’? Dan wordt dezelfde belofte verplaatst, net als de bijbehorende to-do. Er komt geen tweede to-do bij. Op de pagina staat de nieuwe datum en het nieuwere bericht.

Een belofte zonder datum krijgt een opvolgdag: drie dagen nadat jij die hebt gedaan, of een week nadat iemand anders die heeft gedaan. Staat de belofte dan nog open? Dan wordt die een to-do.

Bij beloftes uit Slack staat de naam van de persoon.

Een belofte per e-mail van iemand aan wie je nog nooit hebt geschreven, wordt ook bijgehouden. Die krijgt het label **onbekende afzender**: je hebt alleen hun woord. De bijbehorende to-do begint met ‘Ongeverifieerd: je hebt nog niet eerder met deze persoon geschreven.’

In het [wekelijkse overzicht](weekly-recap.md) zie je hoeveel beloftes zijn nagekomen en hoeveel er nog openstaan. Op je eigen computer geeft `assistant promises` ze weer in een terminal.
