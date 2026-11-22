---
title: Overdragen aan Claude Code of Codex
area: cards
summary: Stuur een programmeer-to-do naar Claude Code of Codex. Het resultaat verschijnt op de to-do.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 22e1b9b950988a58
---
## Een to-do overdragen

1. Open op de to-do **…**, tik op **Overdragen…** en kies **Codex** of **Claude Code**. Alleen de tools die je hebt ingesteld, worden weergegeven.
2. Controleer de samenvatting en wat de tool ontvangt. Voeg eventueel een notitie toe en tik op **Overdragen**. Met **Volledige job bekijken** zie je de volledige opdracht.

De to-do laat zien dat de job bezig is en toont daarna het resultaat, met **Wat het deed** en **Wijzigingen tonen**. Met **Wijzigingen vragen** geef je door wat er moet veranderen. Met **Overdragen…** in **…** begin je opnieuw. Met **Verbergen** verberg je het resultaat. Bij een vastgelopen to-do die je overdraagt, wordt **Bezig…** weergegeven in plaats van **Vastgelopen** zolang de job loopt.

Een job verstuurt nooit iets namens jou. Als de job stopt bij een publicatie- of implementatiestap die jij moet uitvoeren, voer je die stap uit via **Doe het** op de to-do. Een antwoord dat de job schrijft, blijft een concept dat je zelf verstuurt.

## In de Codex-app

- Met **Openen in Codex** open je de conversatie van de job in de Codex-app zodra de job klaar is.
- **Wijzigingen vragen** gaat verder in dezelfde Codex-conversatie en de to-do wordt bijgewerkt.
- Een job stopt na 30 minuten zonder voortgang, of na maximaal 6 uur. Een herstart telt niet als stop.

## Instellen

Ga in **Instellingen** naar **Model** en vervolgens naar **Codex en Claude Code**:

- **Codex**: waar de job wordt uitgevoerd. Op je Machine of je computer hoef je hier verder niets in te stellen. Met **Wijzigen** open je de instelpagina.
- **Codex cloud**: de omgevings-ID uit Codex en eventueel een **Branch** om mee te beginnen.
- **Claude Code**: de link naar een Claude Code-sessie.

Claude stuurt het resultaat terug via de The Machine-connector. Voeg deze eenmalig toe op claude.ai via Settings, Connectors, Add custom connector, met het adres dat onder de sessie wordt weergegeven.

## Waar Codex wordt uitgevoerd

Op een gehoste Machine kies je dit op de instelpagina, onder **Later meer toevoegen** en **Codex**:

- **Op je Machine** (de standaard): tik op **Codex verbinden** en voer de code in die je bij OpenAI ziet. Deze optie gebruikt hetzelfde ChatGPT-abonnement als je model en voert jobs uit op je Machine. Je hebt geen terminal nodig. Als je met hetzelfde ChatGPT-account bent aangemeld, kan je Machine ook zien wanneer je gebruikslimiet wordt gereset en die reset gebruiken.
- **Andere opties**, **Op mijn computer**: de job wordt uitgevoerd op je eigen computer, met het Codex-account dat daar is aangemeld. De overdracht is versleuteld en geldt alleen voor die computer. Installeer The Machine daar, koppel hem via je Accountpagina, voer `codex login` uit en laat The Machine actief. Het resultaat verschijnt op de to-do. Als de computer uitstaat, wachten jobs.
- **Andere opties**, **Codex cloud**: de job wordt uitgevoerd in de cloud van OpenAI. Tik op **Codex verbinden**. Deze optie gebruikt hetzelfde ChatGPT-abonnement als je model. OpenAI vraagt daarna om nog een code voor Codex. Voer vervolgens de Codex cloud-omgeving in bij Instellingen.

Je kunt je ook aanmelden via je dashboard: **Koppelingen**, **Projecten en code**, **Codex**, **Code ophalen**. Een zelfgehoste Machine voert diezelfde aanmelding zelf uit.

Op een gehoste Machine verschijnt **Codex en Claude Code** in Instellingen zodra GitHub of Codex is gekoppeld. Voor ontwikkelaars: de [handleiding voor agents](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
