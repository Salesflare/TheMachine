---
title: Andere AI's koppelen
area: connections
summary: Laat Claude, ChatGPT, Cursor, Codex of GBrain je to-do's en Graph lezen via MCP, elk met eigen toegang en vervaldatum.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Wat een andere AI kan doen

Andere AI's kunnen via MCP met je Machine koppelen: Claude, ChatGPT, Cursor, Codex, GBrain en meer. Ze kunnen je to-do's, beloftes, teambriefings en de mensen en bedrijven in je Graph lezen.

Met **Lezen en bewerken** kunnen ze ook een to-do toevoegen, of een to-do met een e-mailconcept, en je Graph aanpassen: een feit over een persoon of bedrijf bewaren, gegevens, velden en tags verbeteren, of een regel aan iemands samenvatting toevoegen.

Elke wijziging staat in **Activiteit** met **Ongedaan maken**. Ze voegen nooit records samen, verwijderen of delen ze nooit. Wat ze bewaren toont **AI:** en hun naam, in hun gebied. Je kunt het aanpassen of verwijderen, en The Machine kan een samenvattingsregel later herschrijven. Je Machine ziet het als hun bewering, nooit als jouw opdracht.

Een concept wacht in je Machine tot je het leest en zelf op **Versturen** drukt. Een gekoppelde AI verstuurt nooit iets en doet nooit iets in jouw naam. Do it en de agents van je Machine zelf horen hier niet bij.

## Er een koppelen

Open **Instellingen**, **AI's**. Bovenaan staat het adres van je Machine voor AI's, `https://<jouw naam>.mcp.themachine.computer/mcp`, met **Kopiëren**. Op een Machine op je eigen computer druk je eerst op **Krijg je adres**. Er opent een pagina in je account: controleer of die dezelfde code toont, bevestig en kies een naam. Je Machine koppelt zichzelf, zonder herstart.

Daarna haalt hij een eigen certificaat voor het adres. Dat duurt een paar minuten en vraagt het pakket `cryptography` voor Python.

Open in ChatGPT chatgpt.com/plugins, druk op + en dan op Add custom MCP server. Noem hem The Machine, plak het adres en kies OAuth. Bevestig de waarschuwing en druk op Create as a plugin. Je abonnement of werkruimte moet eigen MCP-servers toestaan.

Open in Claude Customize, Connectors, druk op + Add en dan op Add custom connector. Noem hem The Machine, plak het adres en druk op Continue en dan op Add. Bij Team en Enterprise voegt een eigenaar hem toe in Organization settings.

AI's op een apparaat in je tailnet, zoals Claude Code of Cursor, kunnen ook het adres van je dashboard plus `/mcp` gebruiken. **Ontkoppelen** haalt een Machine op je eigen computer weer van je account.

De AI stuurt je naar je Machine om in te loggen. Je Machine toont welke AI het is. Een AI die hij niet herkent, toont het adres waar hij vandaan komt: koppel alleen als je dit net zelf hebt gestart.

Kies wat hij mag doen, **Lezen** of **Lezen en bewerken**. Met zowel werk- als privéaccounts kies je ook wat hij mag zien. Kies daarna hoe lang: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Verbinden**, of op **Annuleren** om hem zonder iets terug te sturen.

## Wat hij ziet

Een koppeling ziet alleen haar gebied. Werk omvat de to-do's en beloftes van je werkaccounts, werkcontacten, bedrijven, projecten en de teambriefing van je Work Fleet. Privé omvat de rest. Berichttekst blijft op je Machine: een AI ziet de bronnen van een to-do alleen met afzender, onderwerp en datum.

Team Graph-gegevens van teamgenoten gaan nooit naar een AI van buiten.

## In Instellingen

Open **Instellingen**, **AI's** om elke gekoppelde AI te zien, met wanneer hij het laatst werd gebruikt en hoeveel oproepen hij deed. Pas daar zijn toegang, zijn gebied of de duur aan. De volgende oproep gebruikt het meteen. **Nu uitzetten** beëindigt al zijn logins in één keer. **Activiteit** toont elke oproep, ook geweigerde. **Verwijderen** haalt hem weg.

Een AI die niet zelf kan inloggen, kan een sleutel gebruiken. Geef hem onder **Sleutel toevoegen** een naam, kies de toegang en de duur en druk op **Sleutel maken**. Kopieer de sleutel meteen: hij wordt maar één keer getoond. De AI stuurt hem als `Authorization: Bearer <key>`.

## Veilig houden

Elke oproep wordt bijgehouden, ook geweigerde. Een koppeling die verlopen is of uitstaat, wordt geweigerd tot je ze aanpast. Inloggen gebeurt met OAuth en PKCE. Je Machine bewaart van elk token alleen een vingerafdruk, dus een kopie van zijn gegevens opent niets.
