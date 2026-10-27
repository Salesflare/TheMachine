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

## In de Codex-app

- **Openen in Codex** opent de thread van de opdracht in de Codex-app. Zolang Codex er hier aan werkt, kan de app hem nog niet openen. Hij opent zodra het klaar is.
- **Wijzigen** op een thread die open staat in de Codex-app gaat verder in datzelfde gesprek daar, en de to-do volgt het.
- Een opdracht stopt alleen als Codex 30 minuten niets doet, of na 6 uur in totaal. Een herstart van The Machine stopt hem niet.

## Instellen

In **Instellingen**, **Algemeen**, onder **Codeeragents**:

- **Claude Code-sessie**: het adres van een Claude Code-sessie.
- **Codex-cloudomgeving**: de id van de omgeving, voor Codex-cloud.
- **Draait op**, en eventueel een **Branch**.

Claude stuurt zijn resultaat terug via de connector van The Machine. Voeg die één keer toe in claude.ai, Settings, Connectors, Add custom connector, met het adres dat daar staat.

## Waar Codex draait

Op een gehoste Machine kies je het op je setuppagina, onder **Voeg later meer toe**, **Codex**:

- **Op mijn computer** (standaard): de opdracht draait op je eigen computer, met de Codex waarmee daar ingelogd is. Er staat niets van Codex op je server, en de opdracht is versleuteld voor alleen die computer: het Network geeft hem door maar kan hem niet lezen. Installeer The Machine op die computer, koppel hem op je pagina Account, en voer daar `codex login` uit. Laat The Machine erop draaien. De opdracht verschijnt als thread in de Codex-app op die computer, en het resultaat komt terug op de to-do. Staat de computer uit, dan wachten opdrachten tot hij terug is.
- **Codex-cloud**: de opdracht draait in de cloud van OpenAI. Druk op **Codex koppelen**. Het gebruikt hetzelfde ChatGPT-abonnement als je model, en OpenAI vraagt nog één code, voor Codex. Vul daarna de Codex-cloudomgeving in bij Instellingen.

Op een gehoste Machine verschijnt Codeeragents zodra GitHub of Codex gekoppeld is. Het verschijnt ook bij setups die opdrachten elders draaien. Meer in de [gids over agents](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
