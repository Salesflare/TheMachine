---
title: Andere AI’s koppelen
area: connections
summary: Laat Claude, ChatGPT, Cursor, Codex of GBrain je to-do’s en Graph lezen. Met Lezen en bewerken kunnen ze ook wijzigingen aanbrengen die je ongedaan kunt maken.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: a8637260c99df309
---
## Wat een andere AI kan doen

Claude, ChatGPT, Cursor, Codex, GBrain en andere AI’s kunnen koppelen met je Machine. Ze kunnen je to-do’s, beloftes, teambriefings en de personen en bedrijven in je Graph lezen.

Met **Lezen en bewerken** kunnen ze ook een to-do of een e-mailconcept toevoegen en je Graph bijwerken: een feit opslaan, gegevens, velden en tags corrigeren of een regel toevoegen aan de samenvatting van een persoon.

Elke wijziging verschijnt bij **Activiteit**, met **Ongedaan maken**. Ze voegen nooit records samen, verwijderen ze niet en delen ze niet. Wat ze opslaan, wordt gemarkeerd met **AI:** en hun naam. Je Machine behandelt het als hun bewering, nooit als jouw instructie.

Een concept blijft staan totdat je het zelf leest en op Versturen drukt. Een gekoppelde AI verstuurt nooit iets en handelt nooit namens jou.

## Eén AI koppelen

Open **Instellingen** en **Apps**. Onder **De apps van The Machine** vind je **Toevoegen in ChatGPT** en **Toevoegen in Claude**. Onder **Of voeg hem toe met een adres** staan het ene adres van de officiële app voor elke Machine, `https://mcp.themachine.computer/mcp`, en **Je adres**, `https://<your name>.mcp.themachine.computer/mcp`, allebei met **Kopiëren**.

Gebruik je een Machine op je eigen computer? Druk dan eerst onder **Je adres ophalen** op **Instellen**. Er wordt een pagina in je account geopend. Controleer of daarop dezelfde code staat, bevestig en kies een naam. Je Machine wordt automatisch gekoppeld, zonder opnieuw opstarten. Dit is voor beide manieren nodig.

Je Machine stelt daarna zelf het beveiligde adres in. Dat duurt een paar minuten.

Voor Claude druk je op **Toevoegen in Claude** of open je [The Machine in Claude's directory](https://claude.ai/directory/the-machine) en druk je op Connect. Bij Team en Enterprise voegt een eigenaar de app toe via Organization settings.

Wil je in plaats daarvan een adres gebruiken in Claude? Open dan Customize, Connectors, druk op + Add en daarna op Add custom connector. Geef de connector de naam The Machine, plak het adres, druk op Continue en daarna op Add.

Voor ChatGPT druk je op **Toevoegen in ChatGPT** of open je [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) en druk je op Install plugin. Bij Business en Enterprise moet een beheerder de app mogelijk eerst toestaan.

De officiële app maakt verbinding met een gehoste Machine en met een Machine op je eigen computer zodra die een adres heeft.

Gebruik je je privé-adres of een Machine die niet op de Network staat? Voeg dan in plaats daarvan een aangepaste MCP-server toe in ChatGPT: open chatgpt.com/plugins, druk op + en daarna op Add custom MCP server. Geef de server de naam The Machine, plak het adres en kies OAuth. Bevestig de waarschuwing en druk op Create as a plugin. Je abonnement of werkruimte moet aangepaste MCP-servers toestaan.

Met de officiële app vraagt de AI je om in te loggen met je The Machine-account. Kies deze Machine als je er meer dan één hebt en keur de aanvraag daarna goed op de eigen pagina van je Machine. Met het privé-adres maakt de AI rechtstreeks verbinding met je Machine.

AI’s op een apparaat in je privé-netwerk (Tailscale), zoals Claude Code of Cursor, kunnen ook het adres van je dashboard gebruiken, gevolgd door `/mcp`. Met **Deze Machine ontkoppelen** onderaan **Instellingen** en **Account** haal je een Machine op je eigen computer weer uit je account.

Je Machine laat zien welke AI de aanvraag doet. Kan hij dat niet vaststellen, dan laat hij zien waar de aanvraag vandaan komt. Koppel alleen als je de aanvraag net zelf hebt gestart.

Kies wat de AI mag doen: **Lezen** of **Lezen en bewerken**. Heb je zowel een Werk- als een Persoonlijk account, kies dan wat de AI mag zien. Kies daarna hoe lang de toegang duurt: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Koppelen**, of op **Annuleren** om de aanvraag af te wijzen.

## Officiële app of privé-adres

De officiële app is de makkelijke optie: één adres voor iedereen, en je account vindt je Machine. Onze cloud geeft aanvragen door en slaat de inhoud ervan nooit op.

Met je privé-adres is alles versleuteld tot aan je Machine. De cloud geeft de inhoud alleen door en kan die niet lezen.

Hoe je ook koppelt, je Machine beslist. Alleen een AI die je op de eigen pagina hebt goedgekeurd, krijgt toegang, met de rechten die je hebt gekozen. Bij een AI die via de officiële app is gekoppeld, staat **Officiële app** onder **Instellingen** en **Apps**.

## Wat de AI kan zien

Een koppeling ziet alleen de eigen omgeving. Werk omvat de to-do’s en beloftes van je werkaccounts, werkcontacten, bedrijven, projecten en de teambriefing van je Werk-Fleet. Persoonlijk omvat de rest. Berichttekst blijft op je Machine, tenzij je **Berichten** inschakelt. Zonder die optie ziet een AI bij een to-do alleen de afzender, het onderwerp en de datum van de bronberichten.

Gegevens uit de Team-Graph van teamgenoten worden nooit gedeeld met externe AI’s.

## Berichten

Met **Berichten** kan een AI je e-mail, Slack, WhatsApp en andere chats doorzoeken en lezen. De optie staat uit totdat je hem inschakelt, op de pagina waar je de AI koppelt of later via **Instellingen** en **Apps**. De AI kan alleen lezen. Hij verstuurt of verwijdert niets en markeert niets.

De AI leest alleen berichten uit de eigen omgeving. Sommige berichten worden nooit gedeeld: eenmalige codes en inloglinks, berichten van een bord of project met **Alleen jij**, gesprekken die The Machine als gevoelig heeft aangemerkt (deals, HR, juridische zaken, gezondheid en geld), gesprekken die je privé hebt gehouden en verwijderde berichten.

Elke keer dat de AI iets leest, verschijnt dat bij **Activiteit**, met het aantal berichten en de gesprekken, maar nooit de tekst. Je Machine geeft de tekst door als gegevens, zodat de AI instructies in een bericht niet hoort op te volgen.

Zolang Berichten aanstaat, wachten wijzigingen in Graph van een AI met **Lezen en bewerken** op jouw goedkeuring. Druk bij de wijziging in **Activiteit** op **Toepassen** of **Afwijzen**.

## In Instellingen

Open **Instellingen** en **Apps** om elke AI te zien die ooit verbinding heeft gemaakt, met de toegang, omgeving, einddatum en het laatste gebruik. Je kunt **Berichten** daar in- en uitschakelen. Druk op **Wijzigen** om de toegang, omgeving of duur aan te passen. De volgende aanvraag gebruikt de nieuwe instellingen. **Activiteit** toont elke aanvraag, ook geweigerde. **Nu uitzetten** pauzeert de toegang: elke login wordt beëindigd, maar de geschiedenis blijft staan. Met **Verwijderen** verwijder je de AI en de geschiedenis.

Wanneer je opnieuw inlogt bij dezelfde AI, vervangt de nieuwe goedkeuring de eerdere.

Een AI die niet zelfstandig kan inloggen, kan een sleutel gebruiken. Geef de sleutel onder **Sleutel toevoegen** een naam, kies de toegang en de duur en druk op **Sleutel maken**. Kopieer de sleutel meteen: hij wordt maar één keer getoond. De AI stuurt hem mee als `Authorization: Bearer <key>`.

## Houd het veilig

Elke aanvraag wordt geregistreerd, ook geweigerde aanvragen. Een verlopen of uitgeschakelde koppeling wordt geweigerd totdat je de instellingen wijzigt. Je Machine bewaart alleen een vingerafdruk van elke login. Met een kopie daarvan krijg je geen toegang.
