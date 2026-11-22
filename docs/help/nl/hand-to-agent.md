---
title: Overdragen aan Claude Code of Codex
area: cards
summary: Stuur een programmeer-to-do naar Claude Code of Codex. Het resultaat komt terug op de to-do.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 22e1b9b950988a58
---
## Een to-do overdragen

1. Open **…** op de to-do, dan **Overdragen…**, en kies **Codex** of **Claude Code**. Alleen de tools die je hebt ingesteld, verschijnen.
2. Bekijk de samenvatting en wat hij meekrijgt, voeg eventueel een notitie toe en druk op **Overdragen**. **Volledige taak bekijken** toont de hele briefing.

De to-do toont dat er aan gewerkt wordt en daarna het resultaat, met **Wat het deed** en **Wijzigingen tonen**. **Wijzigingen vragen** geeft door wat er anders moet. **Overdragen…** onder **…** begint opnieuw. **Verbergen** legt het resultaat weg. Een vastgelopen to-do die je overdraagt, toont **Bezig…** in plaats van **Vastgelopen** zolang de taak loopt.

Een taak verstuurt nooit iets voor je. Laat hij een stap om te publiceren of te deployen voor jou over, dan voert **Doe het** op de to-do die stap uit. Een antwoord dat hij schreef, blijft een concept dat je zelf verstuurt.

## In de Codex-app

- **Openen in Codex** opent de thread van de taak in de Codex-app, zodra de taak klaar is.
- **Wijzigingen vragen** gaat verder in datzelfde Codex-gesprek, en de to-do volgt het.
- Een taak stopt na 30 minuten zonder voortgang, of na 6 uur in totaal. Een herstart stopt hem niet.

## Instellen

In **Instellingen**, **Model**, onder **Codex en Claude Code**:

- **Codex**: waar het draait. Op je Machine of je computer is hier niets meer nodig; **Wijzigen** opent je installatiepagina.
- **Codex cloud**: de id van de omgeving, uit Codex, en eventueel een **Branch** om van te starten.
- **Claude Code**: de link van een Claude Code-sessie.

Claude stuurt zijn resultaat terug via de connector van The Machine. Voeg die één keer toe in claude.ai, Settings, Connectors, Add custom connector, met het adres dat onder de sessie staat.

## Waar Codex draait

Op een gehoste Machine kies je dat op je installatiepagina, onder **Voeg altijd meer toe**, **Codex**:

- **Op je Machine** (standaard): druk op **Codex koppelen** en vul de code die verschijnt in bij OpenAI. Het gebruikt hetzelfde ChatGPT-abonnement als je model, en taken draaien op je Machine. Geen terminal nodig. Ingelogd op hetzelfde ChatGPT-account kan je Machine er ook de resets van je gebruikslimiet mee zien en gebruiken.
- **Andere manieren**, **Op mijn computer**: de taak draait op je eigen computer, met de Codex waarmee je daar bent ingelogd. Hij gaat versleuteld onderweg, alleen voor die computer. Installeer The Machine daar, koppel hem op je pagina Account, voer `codex login` uit en laat The Machine draaien. Het resultaat komt terug op de to-do. Staat de computer uit, dan wachten taken.
- **Andere manieren**, **Codex cloud**: de taak draait in de cloud van OpenAI. Druk op **Codex koppelen**. Het gebruikt hetzelfde ChatGPT-abonnement als je model, en OpenAI vraagt nog één code, voor Codex. Vul daarna de Codex-cloudomgeving in bij Instellingen.

Of log in vanaf je dashboard: **Koppelingen**, **Projecten en code**, **Codex**, **Code ophalen**. Een zelf gehoste Machine doet die login zelf.

Op een gehoste Machine verschijnt **Codex en Claude Code** in Instellingen zodra GitHub of Codex gekoppeld is. Voor ontwikkelaars: de [gids over agents](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
