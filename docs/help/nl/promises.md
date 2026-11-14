---
title: Beloftes
area: cards
summary: Wat jij hebt gezegd dat je doet en wat anderen je hebben beloofd. Wordt vanzelf bijgehouden.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: dbac0241c54b0ec6
---
Houd bij wat jij hebt beloofd en wat anderen jou hebben beloofd. Je Machine herkent beloftes vanzelf in je berichten.

## Waar je ze vindt

Onder **Beloftes** op de pagina To-do's:

- Wat jij hebt gezegd dat je doet, en voor wie: **Jouw beloftes**.
- Wat anderen hebben gezegd dat ze doen: **Aan jou beloofd**.

Bij elke belofte staat een menu **⋯**:

- **Doe het** bij jouw beloftes: de belofte wordt meteen een to-do en je Machine bereidt die voor. **Herinneren** bij hun beloftes: je Machine maakt een kort concept voor een herinnering op de plek waar ze het hebben beloofd. Jij blijft ondertussen op de lijst. Je krijgt een korte melding dat het eraan komt, met **Open to-do**, en bij de belofte staat ‘nu een to-do’. Er wordt niets verstuurd tot jij het verstuurt. Is het al een to-do, dan opent die to-do.
- **Markeer als gedaan**: de belofte is nagekomen.
- **Gaat niet door**: de belofte wordt niet nagekomen. Je Machine houdt die niet meer bij en maakt er geen to-do van.

Een open belofte wordt ook vanzelf een to-do wanneer de deadline nadert: bij jouw beloftes gebeurt dat de ochtend ervoor, zodat je een dag hebt om het te doen. De belofte staat op de dag zelf in de [Agenda](calendar.md). Is de belofte al een to-do, dan linkt die ernaartoe. Met **Markeer als gedaan** of **Gaat niet door** sluit je die to-do ook af. Zodra je Machine ziet dat de belofte is nagekomen, worden beide gesloten en verschijnt er een regel die dat aangeeft.

Is een belofte al nagekomen, bijvoorbeeld door een antwoord dat je hebt verstuurd of een vergadering waarin je het hebt besproken? Dan wordt die vanzelf gesloten, zonder to-do.

Krijgt een belofte later een nieuwe datum, bijvoorbeeld ‘toch volgende week’? Dan wordt dezelfde belofte verplaatst, net als de bijbehorende to-do. Er komt geen tweede to-do bij. Op de pagina zie je de nieuwe datum en het nieuwere bericht.

Een belofte zonder datum krijgt een **herinneringsdag**: drie dagen nadat jij de belofte hebt gedaan, of een week nadat iemand anders dat deed. Staat die dan nog open? Dan wordt het een to-do.

Bij beloftes uit Slack staat de naam van de persoon.

Ook een belofte per e-mail van iemand aan wie je nog nooit hebt geschreven, wordt bijgehouden. Die krijgt het label **onbekende afzender**: je hebt alleen hun woord. De bijbehorende to-do begint met ‘Ongeverifieerd: je hebt deze persoon nog niet eerder geschreven.’

In het [weekoverzicht](weekly-recap.md) zie je hoeveel beloftes zijn nagekomen en hoeveel er nog openstaan. Op je eigen computer geeft `assistant promises` ze weer in een terminal.
