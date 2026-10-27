---
title: Overdragen aan Claude Code of Codex
area: cards
summary: Stuur een programmeer-to-do naar Claude Code of Codex. Het resultaat komt terug op de to-do.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time
order: 5
---
## Een to-do overdragen

1. Open **Meer** op de to-do en kies **Overdragen aan Codex** of **Overdragen aan Claude Code**. Dat verschijnt zodra die tool ingesteld is.
2. Bekijk de samenvatting en wat hij meekrijgt, voeg eventueel een notitie toe en druk op **Overdragen**. **Bekijk de volledige opdracht** toont de hele briefing.

De to-do toont dan dat er aan gewerkt wordt, en het resultaat als het klaar is, met **Wijzigingen tonen**. **Wijzigen** vraagt om aanpassingen; **Opnieuw overdragen** begint opnieuw.

Een opdracht verstuurt nooit iets voor je.

## Instellen

In **Instellingen**, **Algemeen**, onder **Codeeragents**:

- **Claude Code-sessie**: het adres van een Claude Code-sessie.
- **Codex-cloudomgeving**: de id van de omgeving.
- **Draait op**, en eventueel een **Branch**.

Claude stuurt zijn resultaat terug via de connector van The Machine. Voeg die één keer toe in claude.ai, Settings, Connectors, Add custom connector, met het adres dat daar staat. Voor Codex op een gehoste Machine druk je eerst op **Codex koppelen** op je setuppagina, onder **Voeg later meer toe**. Het gebruikt hetzelfde ChatGPT-abonnement als je model, en OpenAI vraagt nog één code, voor Codex.

Op een gehoste Machine verschijnt Codeeragents zodra GitHub of Codex gekoppeld is. Het verschijnt ook bij setups die opdrachten elders draaien. Meer in de [gids over agents](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
