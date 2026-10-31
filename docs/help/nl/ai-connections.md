---
title: Andere AI's koppelen
area: connections
summary: Laat Claude, ChatGPT, Cursor, Codex of GBrain je to-do's en Graph lezen via MCP, elk met eigen toegang en vervaldatum.
covers: ai-connections
code: ai_access.py, ai_app.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Wat een andere AI kan doen

Andere AI's kunnen via MCP met je Machine koppelen: Claude, ChatGPT, Cursor, Codex, GBrain en meer. Ze kunnen je to-do's, beloftes, teambriefings en de mensen en bedrijven in je Graph lezen.

Hoogstens voegen ze een to-do toe, of een to-do met een e-mailconcept. Een concept wacht in je Machine tot je het leest en zelf op **Versturen** drukt. Een gekoppelde AI verstuurt nooit iets en doet nooit iets in jouw naam. Do it en de agents van je Machine zelf horen hier niet bij.

## Er een koppelen

Voeg in de andere AI een eigen connector of MCP-server toe met het adres van je Machine plus `/mcp`. Op een gehoste Machine is dat `https://<jouw naam>.app.themachine.computer/mcp`. Op een Machine op je eigen computer is het het adres van je dashboard, dat alleen apparaten in je tailnet bereiken.

De AI stuurt je naar je Machine om in te loggen. Je Machine toont welke AI het is. Een AI die hij niet herkent, toont het adres waar hij vandaan komt: koppel alleen als je dit net zelf hebt gestart.

Kies wat hij mag doen, **Lezen** of **Lezen en concepten**. Met zowel werk- als privéaccounts kies je ook wat hij mag zien. Kies daarna hoe lang: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Verbinden**, of op **Annuleren** om hem zonder iets terug te sturen.

## Wat hij ziet

Een koppeling ziet alleen haar gebied. Werk omvat de to-do's en beloftes van je werkaccounts, werkcontacten, bedrijven, projecten en de teambriefing van je Work Fleet. Privé omvat de rest. Berichttekst blijft op je Machine: een AI ziet de bronnen van een to-do alleen met afzender, onderwerp en datum.

Team Graph-gegevens van teamgenoten gaan nooit naar een AI van buiten.

## Veilig houden

Elke oproep wordt bijgehouden, ook geweigerde. Een koppeling die verlopen is of uitstaat, wordt geweigerd tot je ze aanpast. Inloggen gebeurt met OAuth en PKCE. Je Machine bewaart van elk token alleen een vingerafdruk, dus een kopie van zijn gegevens opent niets.
