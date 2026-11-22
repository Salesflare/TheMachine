---
title: Andere AI's koppelen
area: connections
summary: Geef Claude, ChatGPT, Cursor, Codex of GBrain toegang tot je to-do's en Graph. Met Lezen en bewerken kunnen ze ook wijzigingen aanbrengen die je ongedaan kunt maken.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## Wat een andere AI kan doen

Je kunt Claude, ChatGPT, Cursor, Codex, GBrain en andere AI's aan je Machine koppelen. Ze kunnen je to-do's, beloftes, teamoverzichten en de personen en bedrijven in je Graph lezen.

Met **Lezen en bewerken** kunnen ze ook een to-do of een e-mailconcept toevoegen en je Graph bijwerken: een feit opslaan, gegevens, velden en tags corrigeren of een regel toevoegen aan de samenvatting van iemand.

Elke wijziging verschijnt in **Activiteit**, met **Ongedaan maken**. Ze voegen nooit gegevens samen, verwijderen ze niet en delen ze niet. Wat ze opslaan, krijgt het label **AI:** met hun naam. Je Machine behandelt het als hun bewering, nooit als jouw opdracht.

Een concept blijft staan tot je het zelf leest en op Versturen drukt. Een gekoppelde AI verstuurt nooit iets en handelt nooit namens jou.

## Eén AI koppelen

Open **Instellingen**, **Apps**. Onder **De apps van The Machine** vind je **Toevoegen in ChatGPT** en **Toevoegen in Claude**. Onder **Of voeg hem toe met een adres** vind je het ene adres van de officiële app voor elke Machine, `https://mcp.themachine.computer/mcp`, en **Je adres**, `https://<your name>.mcp.themachine.computer/mcp`. Bij beide staat **Kopiëren**.

Gebruik je een Machine op je eigen computer? Druk dan eerst op **Instellen** onder **Je adres ophalen**. Er wordt een pagina in je account geopend. Controleer of daar dezelfde code staat, bevestig en kies een naam. Je Machine wordt automatisch gekoppeld, zonder opnieuw opstarten. Dit is voor beide manieren nodig.

Je Machine stelt daarna zelf het beveiligde adres in. Dit duurt een paar minuten.

Druk voor Claude op **Toevoegen in Claude** of open [The Machine in Claude's directory](https://claude.ai/directory/the-machine) en druk op Connect. In Team en Enterprise voegt een eigenaar de app toe via Organization settings.

Wil je in plaats daarvan een adres in Claude gebruiken? Open dan Customize, Connectors, druk op + Add en vervolgens op Add custom connector. Geef de connector de naam The Machine, plak het adres, druk op Continue en daarna op Add.

Druk voor ChatGPT op **Toevoegen in ChatGPT** of open [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) en druk op Install plugin. In Business en Enterprise moet een beheerder de app mogelijk eerst toestaan.

De officiële app maakt verbinding met een gehoste Machine en met een Machine op je eigen computer zodra die een adres heeft.

Wil je je privéadres gebruiken of een Machine die niet op het Network staat? Voeg dan in plaats daarvan een aangepaste MCP-server toe in ChatGPT: open chatgpt.com/plugins, druk op + en daarna op Add custom MCP server. Geef de server de naam The Machine, plak het adres en kies OAuth. Bevestig de waarschuwing en druk op Create as a plugin. Je abonnement of werkruimte moet aangepaste MCP-servers toestaan.

Via de officiële app vraagt de AI je om in te loggen met je The Machine-account. Heb je meer dan één Machine, kies dan de juiste en keur de koppeling goed op de eigen pagina van je Machine. Met het privéadres maakt de AI rechtstreeks verbinding met je Machine.

AI's op een apparaat in je privénetwerk (Tailscale), zoals Claude Code of Cursor, kunnen ook het adres van je dashboard gebruiken, gevolgd door `/mcp`. Met **Deze Machine ontkoppelen** onderaan **Instellingen**, **Account** haal je een Machine op je eigen computer weer uit je account.

Je Machine laat zien welke AI toegang vraagt. Kan hij dat niet vaststellen, dan laat hij zien waar het verzoek vandaan komt. Koppel alleen als je dit zelf net hebt gestart.

Kies wat de AI mag doen: **Lezen** of **Lezen en bewerken**. Heb je zowel Werk- als Privé-accounts, kies dan wat de AI mag zien. Kies daarna hoe lang de toegang geldt: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Koppelen**, of op **Annuleren** om de AI zonder toegang weg te sturen.

## Officiële app of privéadres

De officiële app is de eenvoudigste manier: één adres voor iedereen, en je account vindt je Machine. Onze cloud geeft verzoeken door en slaat niets op.

Met je privéadres is alles versleuteld tot aan je Machine. De cloud geeft verzoeken alleen door en kan ze niet lezen.

In beide gevallen beslist je Machine. Alleen een AI die je op de pagina hebt goedgekeurd, krijgt toegang, met de rechten die je hebt gekozen. In **Instellingen**, **Apps** staat bij een AI die via de officiële app verbinding maakt **Officiële app**.

## Wat de AI kan zien

Een koppeling ziet alleen de gegevens binnen het gekozen gebied. Werk omvat de to-do's en beloftes van je werkaccounts, werkcontacten, bedrijven, projecten en het teamoverzicht van je Werk-Fleet. Privé omvat de rest. Berichtteksten blijven op je Machine, tenzij je **Berichten** inschakelt. Zonder die optie ziet een AI bij de bronnen van een to-do alleen de afzender, het onderwerp en de datum.

Team-Graph-gegevens van je teamgenoten worden nooit met een externe AI gedeeld.

## Berichten

Met **Berichten** kan een AI je e-mail, Slack, WhatsApp en andere chats doorzoeken en lezen. Deze optie staat uit tot je hem inschakelt op de pagina waar je de AI koppelt, of later via **Instellingen**, **Apps**. De AI kan alleen lezen. Hij verstuurt of verwijdert niets en markeert ook niets.

De AI leest alleen berichten binnen het gekozen gebied. Sommige berichten worden nooit gedeeld: eenmalige codes en inloglinks, berichten van een bord of project dat op **Alleen jij** staat, gesprekken die The Machine als gevoelig heeft beoordeeld (deals, HR, juridische zaken, gezondheid, geld), gesprekken die je privé hebt gehouden en verwijderde berichten.

Elke leesactie verschijnt in de **Activiteit** van de AI, met het aantal berichten en de gesprekken, maar nooit de tekst. Je Machine geeft de tekst door als gegevens, zodat de AI geen instructies in een bericht hoort op te volgen.

Zolang Berichten is ingeschakeld, wachten wijzigingen in Graph van een AI met **Lezen en bewerken** op jouw goedkeuring. Druk bij de wijziging in **Activiteit** op **Toepassen** of **Afwijzen**.

## In Instellingen

Open **Instellingen**, **Apps** om te zien welke AI's gekoppeld zijn, met hun toegangsrechten, gebied, einddatum en laatste gebruik. Je kunt **Berichten** daar in- en uitschakelen. Druk op **Wijzigen** om de toegangsrechten, het gebied of de duur aan te passen. Bij het volgende verzoek van de AI gelden de nieuwe instellingen. In **Activiteit** staan alle verzoeken, ook geweigerde. Met **Nu uitzetten** pauzeer je de toegang: alle inlogsessies worden beëindigd, maar de geschiedenis blijft staan. Met **Verwijderen** haal je de AI weg, inclusief de geschiedenis.

Log je opnieuw in bij dezelfde AI, dan vervangt de nieuwe goedkeuring de eerdere.

Een AI die niet zelf kan inloggen, kan een sleutel gebruiken. Geef de sleutel onder **Sleutel toevoegen** een naam, kies de toegangsrechten en de duur en druk op **Sleutel maken**. Kopieer de sleutel meteen: hij wordt maar één keer getoond. De AI stuurt hem mee als `Authorization: Bearer <key>`.

## Houd het veilig

Elk verzoek wordt geregistreerd, ook geweigerde verzoeken. Een koppeling die verlopen of uitgeschakeld is, wordt geweigerd tot je de instellingen wijzigt. Je Machine bewaart alleen een vingerafdruk van elke inlogsessie. Een kopie van de gegevens geeft dus geen toegang.
