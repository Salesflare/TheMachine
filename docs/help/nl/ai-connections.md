---
title: Andere AI’s koppelen
area: connections
summary: Laat Claude, ChatGPT, Cursor, Codex of GBrain je to-do’s en Graph lezen. Met Lezen en bewerken kunnen ze ook wijzigingen aanbrengen die je ongedaan kunt maken.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: cf0776c294917228
---
## Wat een andere AI kan doen

Claude, ChatGPT, Cursor, Codex, GBrain en andere AI’s kunnen verbinding maken met je Machine. Ze kunnen je to-do’s, beloftes, teamoverzichten en de mensen en bedrijven in je Graph lezen.

Met **Lezen en bewerken** kunnen ze ook een to-do of e-mailconcept toevoegen en je Graph bijwerken: een feit opslaan, gegevens, velden en tags corrigeren of een regel toevoegen aan de samenvatting van iemand.

Elke wijziging staat in **Activiteit**, met **Ongedaan maken**. Ze voegen nooit gegevens samen, verwijderen ze niet en delen ze niet. Wat ze opslaan, krijgt de markering **AI:** met hun naam. Je Machine beschouwt het als hun bewering, nooit als jouw opdracht.

Een concept wacht tot je het zelf leest en op **Versturen** drukt. Een gekoppelde AI verstuurt nooit iets en handelt nooit namens jou.

Een concept waarin nog iets moet worden ingevuld, waarin een genoemd bestand ontbreekt of dat alleen je eigen adres als ontvanger heeft, gaat eerst terug naar de AI om te worden aangepast. Vraagt een AI twee keer achter elkaar om dezelfde to-do of hetzelfde concept, dan krijg je er maar één.

## Een AI koppelen

Open **Instellingen** en **Apps**. Onder **De apps van The Machine** vind je **Toevoegen in ChatGPT** en **Toevoegen in Claude**. Onder **Of voeg hem toe met een adres** vind je het ene adres van de officiële app voor elke Machine, `https://mcp.themachine.computer/mcp`, en **Je adres**, `https://<your name>.mcp.themachine.computer/mcp`. Bij allebei staat **Kopiëren**.

Druk op een Machine op je eigen computer eerst op **Instellen** onder **Je adres ophalen**. Er wordt een pagina in je account geopend: controleer of daar dezelfde code staat, bevestig en kies een naam. Je Machine wordt automatisch gekoppeld, zonder opnieuw opstarten. Dit is voor beide manieren nodig.

Je Machine stelt daarna zelf het beveiligde adres in. Dat duurt een paar minuten.

Druk voor Claude op **Toevoegen in Claude** of open [The Machine in de Claude-directory](https://claude.ai/directory/the-machine) en druk op **Koppelen**. Bij Team en Enterprise voegt een eigenaar de app toe via de instellingen van de organisatie.

Wil je in Claude liever een adres gebruiken? Open dan Customize, Connectors, druk op + Add en vervolgens op Add custom connector. Geef de connector de naam The Machine, plak het adres, druk op Continue en daarna op Add.

Druk voor ChatGPT op **Toevoegen in ChatGPT** of open [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) en druk op Install plugin. Bij Business en Enterprise moet een beheerder de app mogelijk eerst toestaan.

De officiële app maakt verbinding met een gehoste Machine en met een Machine op je eigen computer zodra die een adres heeft.

Wil je je privé-adres gebruiken of een Machine die niet op de Network staat? Voeg dan in ChatGPT een aangepaste MCP-server toe: open chatgpt.com/plugins, druk op + en vervolgens op Add custom MCP server. Geef de server de naam The Machine, plak het adres en kies OAuth. Bevestig de waarschuwing en druk op Create as a plugin. Je abonnement of werkruimte moet aangepaste MCP-servers toestaan.

Met de officiële app vraagt de AI je om in te loggen met je account van The Machine. Kies deze Machine als je er meer dan één hebt en keur de koppeling daarna goed op de eigen pagina van je Machine. Met het privé-adres maakt de AI rechtstreeks verbinding met je Machine.

AI’s op een apparaat in je privénetwerk (Tailscale), zoals Claude Code of Cursor, kunnen ook het adres van je dashboard gebruiken, gevolgd door `/mcp`. Met **Deze Machine ontkoppelen** onderaan **Instellingen**, **Account**, verwijder je een Machine op je eigen computer weer uit je account.

Je Machine laat zien welke AI verbinding probeert te maken. Als hij dat niet kan bepalen, laat hij zien waar het verzoek vandaan komt. Koppel alleen als je dit zelf net hebt gestart.

Kies wat de AI mag doen: **Lezen** of **Lezen en bewerken**. Heb je zowel een Werk- als Persoonlijk account, kies dan wat de AI mag zien. Kies vervolgens hoe lang de toegang geldig is: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Koppelen**, of op **Annuleren** om de AI zonder toegang terug te sturen.

## Officiële app of privé-adres

De officiële app is de eenvoudige optie: één adres voor iedereen, en je account vindt je Machine. Onze cloud geeft verzoeken door en slaat de inhoud ervan nooit op.

Met je privé-adres wordt alles versleuteld tot aan je Machine. De cloud geeft het alleen door en kan het niet lezen.

In beide gevallen beslist je Machine. Alleen een AI die je op de eigen pagina hebt goedgekeurd, krijgt toegang, met de rechten die je hebt gekozen. In **Instellingen**, **Apps** staat bij een AI die via de officiële app verbinding maakt **Officiële app**.

## Wat de AI kan zien

Een verbinding heeft alleen toegang tot het eigen gebied. Werk omvat de to-do’s en beloftes van je werkaccounts, zakelijke contacten, bedrijven, projecten en het teamoverzicht van je Werk-Fleet. Persoonlijk omvat al het andere. Berichtteksten blijven op je Machine, tenzij je **Berichten** inschakelt. Zonder die instelling ziet een AI bij de bronnen van een to-do alleen de afzender, het onderwerp en de datum.

Gegevens uit de Team-Graph van teamgenoten worden nooit met een externe AI gedeeld.

## Berichten

Met **Berichten** kan een AI je e-mail, Slack, WhatsApp en andere chats doorzoeken en lezen. De optie staat uit tot je die inschakelt, op de pagina waar je de AI koppelt of later via **Instellingen**, **Apps**. De AI kan alleen lezen. Hij verstuurt of verwijdert niets en markeert ook niets.

De AI leest alleen berichten uit het eigen gebied. Sommige berichten worden nooit gedeeld: eenmalige codes en inloglinks, berichten op een bord of project met de instelling **Alleen jij**, gesprekken die The Machine als gevoelig heeft aangemerkt (deals, HR, juridisch, gezondheid, geld), gesprekken die je privé hebt gehouden en verwijderde berichten.

Elke leesactie staat in **Activiteit**, met het aantal berichten en de gesprekken, maar nooit de tekst. Je Machine geeft de tekst door als gegevens, zodat de AI geen instructies in een bericht hoort op te volgen.

Als **Berichten** is ingeschakeld, wachten wijzigingen van een AI met **Lezen en bewerken** in je Graph op jouw goedkeuring. Druk bij de wijziging in **Activiteit** op **Toepassen** of **Afwijzen**.

## In Instellingen

Open **Instellingen** en **Apps** om te zien welke AI’s verbinding hebben gemaakt, elk één keer, met hun toegangsrechten, gebied, einddatum en laatste gebruik. Je kunt **Berichten** daar in- en uitschakelen. Druk op **Wijzigen** om de toegangsrechten, het gebied of de geldigheidsduur aan te passen. Het volgende verzoek gebruikt de nieuwe instellingen. In **Activiteit** staan alle verzoeken, ook geweigerde. Met **Nu uitzetten** pauzeer je de toegang: alle logins worden beëindigd, maar de geschiedenis blijft staan. Met **Verwijderen** verwijder je de AI en de geschiedenis.

Als je opnieuw inlogt bij dezelfde AI, vervangt de nieuwe toestemming de eerdere.

Een AI die niet zelf kan inloggen, kan een sleutel gebruiken. Geef de sleutel onder **Sleutel toevoegen** een naam, kies de toegangsrechten en de geldigheidsduur en druk op **Sleutel maken**. Kopieer de sleutel meteen: hij wordt maar één keer getoond. De AI stuurt hem mee als `Authorization: Bearer <key>`.

## Veilig houden

Elk verzoek wordt vastgelegd, ook geweigerde verzoeken. Een verlopen of uitgeschakelde verbinding wordt geweigerd totdat je de instellingen wijzigt. Je Machine bewaart alleen een vingerafdruk van elke login. Met een kopie van de gegevens krijg je dus nergens toegang.
