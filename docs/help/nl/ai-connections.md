---
title: Andere AI's koppelen
area: connections
summary: Laat Claude, ChatGPT, Cursor, Codex of GBrain je to-do's en Graph lezen. Met Lezen en bewerken kunnen ze ook wijzigingen aanbrengen die je ongedaan kunt maken.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 7681c632f712e93c
---
## Wat een andere AI kan doen

Claude, ChatGPT, Cursor, Codex, GBrain en andere AI's kunnen verbinding maken met je Machine. Ze kunnen je to-do's, beloftes, teambriefings en de mensen en bedrijven in je Graph lezen.

Met **Lezen en bewerken** kunnen ze ook een to-do of e-mailconcept toevoegen en je Graph bijwerken: een feit opslaan, gegevens, velden en tags corrigeren of een regel toevoegen aan iemands samenvatting.

Elke wijziging verschijnt bij **Activiteit**, met **Ongedaan maken**. AI's voegen nooit gegevens samen, verwijderen ze niet en delen ze niet. Wat ze opslaan, krijgt het label **AI:** met hun naam. Je Machine ziet het als een bewering van die AI, nooit als jouw instructie.

Een concept blijft staan tot je het zelf leest en op Versturen drukt. Een gekoppelde AI verstuurt niets en doet niets namens jou.

## Wat de AI van je leert

Wanneer een chat begint, krijgt de AI een korte briefing: wie je bent, je belangrijkste regels en wat er is veranderd sinds het vorige bezoek. De AI kan ook lezen wat er bij **Leren** staat: je regels, algemene feiten en hoe je in elk kanaal schrijft. Zo schrijft de AI zoals jij.

Met **Lezen en bewerken** kan de AI opslaan wat je in de chat vastlegt. Een feit wordt meteen opgeslagen, met **Ongedaan maken** bij **Activiteit**. Een regel bepaalt hoe je Machine zelf werkt. Daarom blijft die bij **Leren** staan tot je op **Goedkeuren** of **Afwijzen** drukt. De regel verandert niet hoe je schrijft.

Een concept met iets dat nog ingevuld moet worden, een bestand waarnaar wordt verwezen maar dat de AI niet heeft, of alleen jouw eigen adres erin, gaat eerst terug naar de AI om te worden aangepast. Vraagt een AI twee keer na elkaar om dezelfde to-do of hetzelfde concept, dan krijg je er maar één.

## Een AI koppelen

Open **Instellingen**, **Apps**. Onder **De apps van The Machine** staan **Toevoegen in ChatGPT** en **Toevoegen in Claude**. Onder **Of voeg hem toe met een adres** staan het ene adres van de officiële app voor elke Machine, `https://mcp.themachine.computer/mcp`, en **Je adres**, `https://<your name>.mcp.themachine.computer/mcp`, beide met **Kopiëren**.

Druk op een Machine op je eigen computer eerst op **Instellen** onder **Je adres ophalen**. Er wordt een pagina in je account geopend. Controleer of daar dezelfde code staat, bevestig en kies een naam. Je Machine wordt vanzelf gekoppeld, zonder opnieuw opstarten. Dit is voor beide manieren nodig.

Daarna stelt je Machine zelf zijn beveiligde adres in. Dit duurt een paar minuten.

Voor Claude druk je op **Toevoegen in Claude** of open je [The Machine in de Claude-directory](https://claude.ai/directory/the-machine) en druk je op Connect. In Team- en Enterprise-abonnementen voegt een eigenaar de koppeling toe via de organisatie-instellingen.

De skill van The Machine vertelt Claude wanneer je Machine moet worden gebruikt: eerst de briefing, daarna je regels en schrijfstijl, voordat Claude iets opstelt. Druk naast **Claude-skill** op **Downloaden**. Open daarna in Claude Customize, Skills en upload de skill.

Wil je in Claude liever een adres gebruiken, open dan Customize, Connectors, druk op + Add en daarna op Add custom connector. Geef de koppeling de naam The Machine, plak het adres, druk op Continue en daarna op Add.

Voor ChatGPT druk je op **Toevoegen in ChatGPT** of open je [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) en druk je op Install plugin. In Business- en Enterprise-abonnementen moet een beheerder de koppeling mogelijk eerst toestaan.

De officiële app maakt verbinding met een gehoste Machine en met een Machine op je eigen computer zodra die een adres heeft.

Gebruik voor je privé-adres of een Machine die niet op het Network staat liever een aangepaste MCP-server in ChatGPT: open chatgpt.com/plugins, druk op + en daarna op Add custom MCP server. Geef de server de naam The Machine, plak het adres en kies OAuth. Bevestig de waarschuwing en druk op Create as a plugin. Je abonnement of werkruimte moet aangepaste MCP-servers toestaan.

Met de officiële app vraagt de AI je om in te loggen met je The Machine-account. Kies deze Machine als je er meer dan één hebt en keur de koppeling daarna goed op de eigen pagina van je Machine. Met het privé-adres maakt de AI rechtstreeks verbinding met je Machine.

AI's op een apparaat in je privénetwerk (Tailscale), zoals Claude Code of Cursor, kunnen ook het adres van je dashboard gebruiken, gevolgd door `/mcp`. Met **Deze Machine ontkoppelen** onderaan **Instellingen**, **Account** haal je een Machine op je eigen computer weer uit je account.

Je Machine laat zien welke AI verbinding probeert te maken. Kan hij dat niet vaststellen, dan laat hij zien waar het verzoek vandaan komt. Koppel alleen als je dit zelf net hebt gestart.

Kies wat de AI mag doen: **Lezen** of **Lezen en bewerken**. Heb je zowel een werk- als een persoonlijk account, kies dan wat de AI mag zien. Kies daarna hoe lang de toegang geldt: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Koppelen**, of op **Annuleren** om de AI zonder toegang terug te sturen.

## Officiële app of privé-adres

De officiële app is de makkelijkste manier: één adres voor iedereen, en je account vindt je Machine. Onze cloud stuurt verzoeken door en slaat nooit op wat erin staat.

Met je privé-adres is alles van begin tot eind versleuteld, tot aan je Machine. De cloud stuurt alleen verzoeken door en kan ze niet lezen.

Hoe je ook verbinding maakt, je Machine beslist. Alleen een AI die je op de eigen pagina hebt goedgekeurd, krijgt toegang, met de rechten die je hebt gekozen. Een AI die via de officiële app verbinding maakt, krijgt **Officiële app** te zien bij **Instellingen**, **Apps**.

## Wat de AI kan zien

Een verbinding heeft alleen toegang tot het bijbehorende gebied. Werk omvat de to-do's en beloftes van je werkaccounts, zakelijke contacten, bedrijven, projecten en de teambriefing van je Werk-Fleet. Persoonlijk omvat de rest. Berichten blijven op je Machine, tenzij je **Berichten** inschakelt. Zonder die instelling ziet een AI bij de bronnen van een to-do alleen de afzender, het onderwerp en de datum.

Gegevens uit de Team-Graph van teamgenoten worden nooit met een externe AI gedeeld.

## Berichten

Met **Berichten** kan een AI je e-mail, Slack, WhatsApp en andere chats doorzoeken en lezen. Deze functie staat uit tot je die inschakelt, op de pagina waar je de AI koppelt of later via **Instellingen**, **Apps**. De AI kan alleen lezen. Hij verstuurt, verwijdert of markeert nooit iets.

De AI leest alleen berichten uit het bijbehorende gebied. Sommige berichten worden nooit gedeeld: eenmalige codes en inloglinks, berichten op een bord of in een project met de instelling **Alleen jij**, gesprekken die The Machine als gevoelig heeft aangemerkt (deals, HR, juridische zaken, gezondheid, geld), gesprekken die je privé hebt gehouden en verwijderde berichten.

Elke keer dat de AI iets leest, verschijnt dit bij **Activiteit** met het aantal berichten en de gesprekken, maar nooit met de tekst. Je Machine geeft de tekst door als gegevens, zodat de AI geen instructies in een bericht hoort op te volgen.

Zolang Berichten is ingeschakeld, moet je wijzigingen die een AI met **Lezen en bewerken** in Graph voorstelt, eerst goedkeuren. Druk bij de wijziging in **Activiteit** op **Toepassen** of **Afwijzen**.

## In Instellingen

Open **Instellingen**, **Apps** om alle AI's te zien die ooit verbinding hebben gemaakt, met hun toegangsrechten, gebied, einddatum en laatste gebruik. Je kunt **Berichten** daar in- en uitschakelen. Druk op **Wijzigen** om de toegangsrechten, het gebied of de geldigheidsduur aan te passen. De volgende keer dat de AI verbinding maakt, gelden de nieuwe instellingen. Bij **Activiteit** staan alle verzoeken, ook geweigerde. Met **Nu uitzetten** pauzeer je de toegang: alle logins worden beëindigd, maar de geschiedenis blijft staan. Met **Verwijderen** verwijder je de AI en de bijbehorende geschiedenis.

Wanneer je opnieuw inlogt bij dezelfde AI, vervangt de nieuwe goedkeuring de eerdere. Op plekken waar die AI al was ingelogd, blijft hij verbonden met de nieuwe toegangsrechten. Een AI die je gebruikt, blijft ingelogd tot de einddatum. Gebruik je de AI 90 dagen niet, dan moet je opnieuw inloggen.

Een AI die niet zelf kan inloggen, kan een sleutel gebruiken. Geef de sleutel een naam onder **Sleutel toevoegen**, kies de toegangsrechten en geldigheidsduur en druk op **Sleutel maken**. Kopieer de sleutel meteen: je kunt hem maar één keer zien. De AI stuurt hem mee als `Authorization: Bearer <key>`.

## Veilig houden

Elk verzoek wordt geregistreerd, ook geweigerde verzoeken. Een verlopen of uitgeschakelde verbinding wordt geweigerd tot je de instellingen wijzigt. Je Machine bewaart alleen een vingerafdruk van elke login. Met een kopie van die gegevens krijgt niemand toegang.
