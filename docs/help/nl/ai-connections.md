---
title: Andere AI's verbinden
area: connections
summary: Laat Claude, ChatGPT, Cursor, Codex of GBrain je to-do's en Graph lezen. Met **Lezen en bewerken** kunnen ze wijzigingen aanbrengen die je ongedaan kunt maken.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## Wat een andere AI kan doen

Claude, ChatGPT, Cursor, Codex, GBrain en andere AI's kunnen verbinding maken met je Machine. Ze kunnen je to-do's, beloftes, teambriefs en de personen en bedrijven in je Graph lezen.

Met **Lezen en bewerken** kunnen ze ook een to-do of e-mailconcept toevoegen en je Graph bijwerken: een feit opslaan, gegevens, velden en tags corrigeren of een regel toevoegen aan de samenvatting van iemand.

Elke wijziging verschijnt bij **Activiteit**, met **Ongedaan maken** erbij. AI's voegen records nooit samen, verwijderen ze niet en delen ze niet. Wat ze opslaan, wordt gemarkeerd met **AI:** en hun naam. Je Machine behandelt het als hun bewering, nooit als jouw opdracht.

Een concept blijft staan totdat je het zelf leest en op **Verzenden** drukt. Een verbonden AI verstuurt nooit iets en handelt nooit namens jou.

## Eén AI verbinden

Open **Instellingen**, **Apps**. Onder **De apps van The Machine** vind je **Toevoegen in ChatGPT** en **Toevoegen in Claude**. Onder **Of voeg hem toe met een adres** staan het ene adres van de officiële app voor elke Machine, `https://mcp.themachine.computer/mcp`, en **Je adres**, `https://<your name>.mcp.themachine.computer/mcp`, elk met **Kopiëren** erbij.

Gebruik je een Machine op je eigen computer, druk dan eerst op **Instellen** onder **Krijg je adres**. Er wordt een pagina in je account geopend. Controleer of daar dezelfde code staat, bevestig en kies een naam. Je Machine wordt automatisch gekoppeld, zonder opnieuw op te starten. Dit is voor beide manieren nodig.

Daarna stelt je Machine zelf het beveiligde adres in. Dit duurt een paar minuten.

Druk voor Claude op **Toevoegen in Claude** of open [The Machine in de directory van Claude](https://claude.ai/directory/the-machine) en druk op **Verbinden**. Bij Team en Enterprise voegt een eigenaar de app toe via de organisatie-instellingen.

Wil je in Claude liever een adres gebruiken? Open dan **Aanpassen**, **Connectors**, druk op **+ Toevoegen** en daarna op **Aangepaste connector toevoegen**. Geef de connector de naam The Machine, plak het adres, druk op **Doorgaan** en daarna op **Toevoegen**.

Druk voor ChatGPT op **Toevoegen in ChatGPT** of open [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) en druk op **Plugin installeren**. Bij Business en Enterprise moet een beheerder de app mogelijk eerst toestaan.

De officiële app maakt verbinding met een gehoste Machine en met een Machine op je eigen computer zodra die een adres heeft.

Wil je je privé-adres gebruiken of verbinding maken met een Machine die niet op het Network staat? Voeg dan in ChatGPT een aangepaste MCP-server toe: open chatgpt.com/plugins, druk op + en daarna op **Aangepaste MCP-server toevoegen**. Geef de server de naam The Machine, plak het adres en kies OAuth. Bevestig de waarschuwing en druk op **Maken als plug-in**. Je abonnement of workspace moet aangepaste MCP-servers toestaan.

Met de officiële app vraagt de AI je om in te loggen met je The Machine-account. Kies deze Machine als je er meer dan één hebt en keur de verbinding daarna goed op de eigen pagina van je Machine. Met het privé-adres maakt de AI rechtstreeks verbinding met je Machine.

AI's op een apparaat in je privénetwerk (Tailscale), zoals Claude Code of Cursor, kunnen ook het adres van je dashboard gebruiken, gevolgd door `/mcp`. Met **Deze Machine ontkoppelen**, onderaan **Instellingen**, **Account**, haal je een Machine op je eigen computer weer uit je account.

Je Machine laat zien welke AI verbinding probeert te maken. Kan hij dat niet vaststellen, dan laat hij zien waar het verzoek vandaan komt. Maak alleen verbinding als je dit zelf net hebt gestart.

Kies wat de AI mag doen: **Lezen** of **Lezen en bewerken**. Heb je zowel een Work- als Personal-account, kies dan wat de AI mag zien. Kies daarna hoelang de toegang geldt: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Verbinden** of op **Annuleren** om de AI zonder toegang terug te sturen.

## Officiële app of privé-adres

De officiële app is de eenvoudige optie: één adres voor iedereen en je account vindt je Machine. Onze cloud geeft verzoeken door en slaat niets op.

Met je privé-adres is alles van begin tot eind versleuteld, helemaal tot aan je Machine. De cloud geeft de verzoeken alleen door en kan ze niet lezen.

In beide gevallen beslist je Machine. Alleen een AI die je op de pagina hebt goedgekeurd, krijgt toegang, met de rechten die je hebt gekozen. In **Instellingen**, **Apps** staat bij een AI die via de officiële app is verbonden **Officiële app**.

## Wat de AI kan zien

Een verbinding ziet alleen de eigen omgeving. Work omvat de to-do's en beloftes van je werkaccounts, werkcontacten, bedrijven, projecten en de teambrief van je Work Fleet. Personal omvat de rest. Berichtteksten blijven op je Machine, tenzij je **Berichten** inschakelt. Zonder die optie ziet een AI bij de bronnen van een to-do alleen de afzender, het onderwerp en de datum.

Records uit de Team Graph van teamgenoten worden nooit met een externe AI gedeeld.

## Berichten

Met **Berichten** kan een AI je e-mail, Slack, WhatsApp en andere chats doorzoeken en lezen. Deze optie staat uit totdat je hem inschakelt, op de pagina waar je de AI verbindt of later via **Instellingen**, **Apps**. De AI kan alleen lezen. Hij verstuurt of verwijdert nooit berichten en markeert ze ook niet.

De AI leest alleen berichten uit zijn eigen omgeving. Sommige berichten worden nooit gedeeld: eenmalige codes en inloglinks, berichten op een bord of project met **Alleen jij**, gesprekken die The Machine als gevoelig heeft aangemerkt (deals, HR, juridisch, gezondheid en geld), gesprekken die je privé hebt gehouden en verwijderde berichten.

Elke leesactie verschijnt bij **Activiteit**, met het aantal berichten en de gesprekken erbij, maar nooit de tekst. Je Machine geeft de tekst door als gegevens, zodat de AI geen instructies in een bericht hoort op te volgen.

Zolang Berichten aanstaat, wachten wijzigingen in Graph van een AI met **Lezen en bewerken** op jouw goedkeuring. Druk bij de wijziging in **Activiteit** op **Toepassen** of **Afwijzen**.

## In Instellingen

Open **Instellingen**, **Apps** om alle AI's te zien die verbinding hebben gemaakt, samen met hun toegang, omgeving, einddatum en laatste gebruik. Je kunt **Berichten** daar in- en uitschakelen. Druk op **Wijzigen** om de toegang, de omgeving of de duur aan te passen. De volgende keer dat de AI verbinding maakt, gelden de nieuwe instellingen. Bij **Activiteit** staan alle verzoeken, ook de geweigerde. Met **Nu uitzetten** pauzeer je de toegang: alle sessies worden beëindigd, maar de geschiedenis blijft staan. Met **Verwijderen** verwijder je de AI en de geschiedenis.

Als je opnieuw inlogt bij dezelfde AI, vervangt de nieuwe goedkeuring de eerdere.

Een AI die niet zelfstandig kan inloggen, kan een sleutel gebruiken. Geef de sleutel onder **Sleutel toevoegen** een naam, kies de toegang en hoelang die geldt, en druk op **Sleutel maken**. Kopieer de sleutel meteen: je ziet hem maar één keer. De AI verstuurt hem als `Authorization: Bearer <key>`.

## Veilig houden

Elk verzoek wordt geregistreerd, ook geweigerde verzoeken. Een verlopen of uitgeschakelde verbinding wordt geweigerd totdat je de instellingen wijzigt. Je Machine bewaart alleen een vingerafdruk van elke aanmelding. Met een kopie van die gegevens kan dus niemand inloggen.
