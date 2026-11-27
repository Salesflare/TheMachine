---
title: Andere AI’s koppelen
area: connections
summary: Geef Claude, ChatGPT, Cursor, Codex of GBrain toegang om je to-do’s en Graph te lezen. Met Lezen en bewerken kunnen ze ook wijzigingen aanbrengen die je ongedaan kunt maken.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: acdce4a5793f7c67
---
## Wat een andere AI kan doen

Claude, ChatGPT, Cursor, Codex, GBrain en andere AI’s kunnen verbinding maken met je Machine. Ze kunnen je to-do’s, beloftes, teambriefings en de mensen en bedrijven in je Graph lezen.

Met **Lezen en bewerken** kunnen ze ook een to-do of e-mailconcept toevoegen en je Graph bijwerken: een feit opslaan, gegevens, velden en tags corrigeren of een regel toevoegen aan de samenvatting van iemand.

Elke wijziging verschijnt in **Activiteit**, met **Ongedaan maken**. AI’s voegen nooit gegevens samen, verwijderen ze niet en delen ze niet. Wat ze opslaan, wordt gemarkeerd met **AI:** en hun naam. Je Machine behandelt het als een bewering van die AI, nooit als een opdracht van jou.

Een concept blijft klaarstaan totdat je het leest en zelf op **Versturen** drukt. Een gekoppelde AI verstuurt nooit iets en handelt nooit namens jou.

Een concept waarin nog iets moet worden ingevuld, dat verwijst naar een bestand dat de AI niet heeft, of waarop alleen jouw eigen adres staat, gaat eerst terug naar de AI om het te laten aanpassen. Vraagt een AI twee keer achter elkaar om dezelfde to-do of hetzelfde concept, dan krijg je er maar één.

## Een AI koppelen

Open **Instellingen** en **Apps**. Onder **De apps van The Machine** vind je **Toevoegen in ChatGPT** en **Toevoegen in Claude**. Onder **Of voeg hem toe met een adres** staan het adres van de officiële app, `https://mcp.themachine.computer/mcp`, dat voor elke Machine hetzelfde is, en **Je adres**, `https://<your name>.mcp.themachine.computer/mcp`. Bij allebei staat **Kopiëren**.

Staat je Machine op je eigen computer, druk dan eerst op **Instellen** onder **Je adres ophalen**. Er wordt een pagina in je account geopend. Controleer of daar dezelfde code staat, bevestig en kies een naam. Je Machine wordt automatisch gekoppeld, zonder opnieuw opstarten. Dit is voor beide manieren nodig.

Daarna stelt je Machine automatisch zijn beveiligde adres in. Dat duurt een paar minuten.

Voor Claude druk je op **Toevoegen in Claude** of open je [The Machine in de directory van Claude](https://claude.ai/directory/the-machine) en druk je op Connect. Bij Team en Enterprise voegt een eigenaar de app toe via de instellingen van de organisatie.

Wil je in plaats daarvan een adres gebruiken in Claude, open dan Customize, Connectors, druk op + Add en daarna op Add custom connector. Geef de app de naam The Machine, plak het adres, druk op Continue en daarna op Add.

Voor ChatGPT druk je op **Toevoegen in ChatGPT** of open je [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) en druk je op Install plugin. Bij Business en Enterprise moet een beheerder de app mogelijk eerst toestaan.

De officiële app maakt verbinding met een gehoste Machine en met een Machine op je eigen computer zodra die een adres heeft.

Gebruik voor je privé-adres of voor een Machine die niet op het Network staat in plaats daarvan een aangepaste MCP-server in ChatGPT. Open chatgpt.com/plugins, druk op + en daarna op Add custom MCP server. Geef de server de naam The Machine, plak het adres en kies OAuth. Bevestig de waarschuwing en druk op Create as a plugin. Je abonnement of werkruimte moet aangepaste MCP-servers toestaan.

Met de officiële app vraagt de AI je om in te loggen met je account bij The Machine. Kies deze Machine als je er meer dan één hebt en keur de koppeling daarna goed op de eigen pagina van je Machine. Met het privé-adres maakt de AI rechtstreeks verbinding met je Machine.

AI’s op een apparaat in je privénetwerk (Tailscale), zoals Claude Code of Cursor, kunnen ook het adres van je dashboard gebruiken, gevolgd door `/mcp`. Met **Deze Machine ontkoppelen** onderaan **Instellingen**, **Account** verwijder je een Machine op je eigen computer weer uit je account.

Je Machine laat zien welke AI verbinding probeert te maken. Kan hij dat niet bepalen, dan laat hij zien waar het verzoek vandaan komt. Koppel alleen als je dit zelf net hebt gestart.

Kies wat de AI mag doen: **Lezen** of **Lezen en bewerken**. Heb je zowel een Werk- als een Persoonlijk account, kies dan wat de AI mag zien. Kies daarna hoe lang de toegang duurt: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Koppelen** of op **Annuleren** om de AI zonder toegang terug te sturen.

## Officiële app of privé-adres

De officiële app is de eenvoudige optie: iedereen gebruikt hetzelfde adres en je account vindt je Machine. Onze cloud geeft verzoeken door en slaat nooit op wat erin staat.

Met je privé-adres is alles versleuteld tot aan je Machine. De cloud geeft de gegevens alleen door en kan ze niet lezen.

In beide gevallen beslist je Machine. Alleen een AI die je op de pagina ervan hebt goedgekeurd, krijgt toegang, met de rechten die je hebt gekozen. In **Instellingen**, **Apps** staat bij een AI die via de officiële app verbinding maakte **Officiële app**.

## Wat de AI kan zien

Een verbinding ziet alleen de gegevens binnen het gekozen gebied. Werk omvat de to-do’s en beloftes van je werkaccounts, je werkcontacten, bedrijven en projecten, en de teambrief van je Werk-Fleet. Persoonlijk omvat de rest. Berichtteksten blijven op je Machine, tenzij je **Berichten** inschakelt. Zonder die optie ziet een AI bij de bronnen van een to-do alleen de afzender, het onderwerp en de datum.

Gegevens uit de Team-Graph van teamgenoten worden nooit met een externe AI gedeeld.

## Berichten

Met **Berichten** kan een AI je e-mail, Slack, WhatsApp en andere chats doorzoeken en lezen. Deze optie staat uit totdat je hem inschakelt op de pagina waar je de AI koppelt of later via **Instellingen**, **Apps**. De AI kan alleen lezen: hij verstuurt of verwijdert niets en markeert niets.

De AI leest alleen berichten binnen het gekozen gebied. Sommige berichten worden nooit gedeeld: eenmalige codes en inloglinks, berichten op een bord of project met de instelling **Alleen jij**, gesprekken die The Machine als gevoelig heeft beoordeeld (deals, HR, juridische zaken, gezondheid en geld), gesprekken die je privé hebt gehouden en verwijderde berichten.

Elke leesactie verschijnt in **Activiteit**, met het aantal berichten en de gesprekken, maar nooit de tekst. Je Machine geeft de tekst door als gegevens, zodat de AI geen instructies hoort te volgen die in een bericht staan.

Zolang Berichten is ingeschakeld, wachten wijzigingen in Graph van een AI met **Lezen en bewerken** op jouw goedkeuring. Druk op **Toepassen** of **Afwijzen** bij de wijziging in **Activiteit**.

## In Instellingen

Open **Instellingen**, **Apps** om elke AI te zien die verbinding heeft gemaakt, met de toegangsrechten, het gebied, de einddatum en het laatste gebruik. Je kunt **Berichten** daar in- en uitschakelen. Druk op **Wijzigen** om de toegangsrechten, het gebied of de duur aan te passen. De wijziging geldt vanaf het volgende verzoek. **Activiteit** toont alle verzoeken, ook geweigerde. Met **Nu uitzetten** pauzeer je de toegang: alle logins worden beëindigd, maar de geschiedenis blijft staan. Met **Verwijderen** verwijder je de AI en de bijbehorende geschiedenis.

Log je opnieuw in bij dezelfde AI, dan vervangt de nieuwe goedkeuring de eerdere. Op plekken waar je al bij die AI was ingelogd, blijft de verbinding actief met de nieuwe toegangsrechten. Een AI die je gebruikt, blijft ingelogd tot de einddatum. Gebruik je een AI 90 dagen niet, dan moet je opnieuw inloggen.

Een AI die niet zelfstandig kan inloggen, kan een sleutel gebruiken. Geef de sleutel onder **Sleutel toevoegen** een naam, kies de toegangsrechten en de duur en druk op **Sleutel maken**. Kopieer de sleutel meteen: je ziet hem maar één keer. De AI verstuurt hem als `Authorization: Bearer <key>`.

## Veilig houden

Elk verzoek wordt vastgelegd, ook geweigerde verzoeken. Een verlopen of uitgeschakelde verbinding wordt geweigerd totdat je de instellingen wijzigt. Je Machine bewaart alleen een vingerafdruk van elke login, zodat niemand met een kopie van de gegevens toegang krijgt.
