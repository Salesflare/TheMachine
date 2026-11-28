---
title: Andere AI's koppelen
area: connections
summary: Laat Claude, ChatGPT, Cursor, Codex of GBrain je to-do's en Graph lezen. Met Lezen en bewerken kunnen ze ook wijzigingen aanbrengen die je ongedaan kunt maken.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 3a7200b2a076c274
---
## Wat een andere AI kan doen

Claude, ChatGPT, Cursor, Codex, GBrain en andere AI's kunnen aan je Machine worden gekoppeld. Ze kunnen je to-do's, beloftes, teambriefs en de mensen en bedrijven in je Graph lezen.

Met **Lezen en bewerken** kunnen ze ook een to-do of e-mailconcept toevoegen en je Graph bijwerken: een feit opslaan, gegevens, velden en tags corrigeren of een regel toevoegen aan de samenvatting van iemand.

Elke wijziging staat in **Activiteit**, met **Ongedaan maken**. Ze voegen nooit gegevens samen, verwijderen of delen ze niet. Wat ze opslaan, wordt gemarkeerd met **AI:** en hun naam. Je Machine beschouwt het als hun bewering, nooit als jouw instructie.

Een concept blijft staan totdat je het zelf leest en op Versturen drukt. Een gekoppelde AI verstuurt nooit iets en handelt nooit namens jou.

## Wat de AI van je leert

Wanneer een chat begint, krijgt de AI een korte briefing: wie je bent, je belangrijkste regels en wat er is veranderd sinds het vorige bezoek. De AI kan ook lezen wat er bij **Leren** staat: je regels, algemene feiten en hoe je in elk kanaal schrijft. Zo schrijft hij zoals jij.

Met **Lezen en bewerken** kan de AI opslaan wat je in de chat hebt afgesproken. Een feit wordt meteen opgeslagen, met **Ongedaan maken** in **Activiteit**. Een regel stuurt het werk van je Machine zelf aan, dus die blijft bij **Leren** staan totdat je op **Goedkeuren** of **Afwijzen** drukt. De regel verandert nooit hoe je schrijft.

Een concept waarin nog iets moet worden ingevuld, met een bestand dat de AI noemt maar niet heeft, of met alleen jouw eigen adres erop, gaat eerst terug naar de AI om te worden aangepast. Als een AI twee keer achter elkaar om dezelfde to-do of hetzelfde concept vraagt, krijg je er maar één.

## Een AI koppelen

Open **Instellingen** en kies **Apps**. Onder **De apps van The Machine** staan **Toevoegen in ChatGPT** en **Toevoegen in Claude**. Onder **Of voeg hem toe met een adres** staan het ene adres van de officiële app voor elke Machine, `https://mcp.themachine.computer/mcp`, en **Je adres**, `https://<your name>.mcp.themachine.computer/mcp`, allebei met **Kopiëren**.

Druk op een Machine op je eigen computer eerst onder **Je adres ophalen** op **Instellen**. Er wordt een pagina in je account geopend. Controleer of daar dezelfde code staat, bevestig en kies een naam. Je Machine wordt vanzelf gekoppeld, zonder opnieuw op te starten. Dit is voor beide manieren nodig.

Je Machine stelt daarna zelf het beveiligde adres in. Dat duurt een paar minuten.

Druk voor Claude op **Toevoegen in Claude** of open [The Machine in de Claude-directory](https://claude.ai/directory/the-machine) en druk op Koppelen. In Team en Enterprise voegt een eigenaar de app toe bij de instellingen van de organisatie.

De skill van The Machine vertelt Claude wanneer hij je Machine moet gebruiken: eerst de briefing, daarna je regels en schrijfstijl, voordat hij iets opstelt. Druk naast **Claude-skill** op **Downloaden**. Open vervolgens in Claude Customize, Skills en upload het bestand.

Wil je in plaats daarvan een adres gebruiken in Claude? Open dan Customize en Connectors, druk op + Add en daarna op Add custom connector. Geef de connector de naam The Machine, plak het adres en druk op Continue en daarna op Add.

Druk voor ChatGPT op **Toevoegen in ChatGPT** of open [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) en druk op Install plugin. In Business en Enterprise moet een beheerder dit mogelijk eerst toestaan.

De officiële app maakt verbinding met een gehoste Machine en met een Machine op je eigen computer zodra die een adres heeft.

Gebruik voor je privé-adres of een Machine die niet op de Network staat liever een aangepaste MCP-server in ChatGPT: open chatgpt.com/plugins, druk op + en daarna op Add custom MCP server. Geef de server de naam The Machine, plak het adres en kies OAuth. Bevestig de waarschuwing en druk op Create as a plugin. Je abonnement of werkruimte moet aangepaste MCP-servers toestaan.

Met de officiële app vraagt de AI je om in te loggen met je account van The Machine. Kies deze Machine als je er meer dan één hebt en keur de aanvraag daarna goed op de eigen pagina van je Machine. Met het privé-adres maakt de AI rechtstreeks verbinding met je Machine.

AI's op een apparaat in je privénetwerk (Tailscale), zoals Claude Code of Cursor, kunnen ook het adres van je dashboard gebruiken, gevolgd door `/mcp`. Met **Deze Machine ontkoppelen** onderaan **Instellingen**, **Account**, haal je een Machine op je eigen computer weer van je account af.

Je Machine laat zien welke AI toegang vraagt. Als hij dat niet kan vaststellen, laat hij zien waar het verzoek vandaan komt. Koppel alleen als je dit zelf net hebt gestart.

Kies wat de AI mag doen: **Lezen** of **Lezen en bewerken**. Heb je zowel een Werk- als een persoonlijk account, kies dan wat de AI mag zien. Kies daarna hoelang de toegang duurt: **1 dag**, **7 dagen**, **30 dagen** of **1 jaar**. Druk op **Koppelen** of op **Annuleren** om de aanvraag af te wijzen.

## Officiële app of privé-adres

De officiële app is de makkelijkste optie: één adres voor iedereen, en je account vindt je Machine. Onze cloud geeft verzoeken door en slaat nooit op wat ze bevatten.

Met je privé-adres is alles volledig versleuteld tot aan je Machine. De cloud geeft het alleen door en kan het niet lezen.

In beide gevallen beslist je Machine. Alleen een AI die je op de eigen pagina hebt goedgekeurd, krijgt toegang, met de rechten die je hebt gekozen. In **Instellingen**, **Apps** staat bij een AI die via de officiële app is gekoppeld **Officiële app**.

## Wat de AI kan zien

Een verbinding heeft alleen toegang tot het eigen gebied. Werk omvat de to-do's en beloftes van je werkaccounts, werkcontacten, bedrijven, projecten en de teambrief van je Werk-Fleet. Persoonlijk omvat de rest. Berichttekst blijft op je Machine, tenzij je **Berichten** inschakelt. Zonder die instelling ziet een AI bij de bronnen van een to-do alleen de afzender, het onderwerp en de datum.

Gegevens uit de Team-Graph van teamgenoten worden nooit met een externe AI gedeeld.

## Berichten

Met **Berichten** kan een AI je e-mail, Slack, WhatsApp en andere chats doorzoeken en lezen. Deze functie staat uit totdat je hem inschakelt, op de pagina waar je de AI koppelt of later via **Instellingen**, **Apps**. De AI kan alleen lezen. Hij verstuurt, verwijdert of markeert nooit iets.

De AI leest alleen berichten in het eigen gebied. Sommige berichten worden nooit gedeeld: eenmalige codes en inloglinks, berichten van een bord of project met **Alleen jij**, gesprekken die The Machine als gevoelig heeft aangemerkt (deals, HR, juridische zaken, gezondheid, geld), gesprekken die je privé hebt gehouden en verwijderde berichten.

Elke leesactie staat in **Activiteit**, met het aantal berichten en de gesprekken, maar nooit de tekst. Je Machine geeft de tekst door als gegevens, zodat de AI geen instructies hoort op te volgen die in een bericht staan.

Zolang Berichten is ingeschakeld, wachten wijzigingen van een AI met **Lezen en bewerken** in je Graph op jouw goedkeuring. Druk op **Toepassen** of **Afwijzen** bij de wijziging in **Activiteit**.

## Gebeurtenissen

Met **Gebeurtenissen** kan een AI zoals ChatGPT zelf aan de slag gaan wanneer er iets gebeurt, bijvoorbeeld als er een nieuwe to-do is, als er een briefing voor een meeting van morgen nodig is of als er morgen een belofte afloopt. Elke gebeurtenis staat uit totdat je die inschakelt onder **Wijzigen**. De AI krijgt dan de titel en een korte uitleg, maar geen informatie die hij niet al kon lezen en nooit informatie van eerder.

De AI kan nog steeds niets versturen. Wijzigingen staan in **Activiteit**, met **Ongedaan maken**. Als je een gebeurtenis of de AI uitzet, stopt die meteen.

## In Instellingen

Open **Instellingen**, **Apps** om alle AI's te zien die ooit zijn gekoppeld, met hun toegang, gebied, einddatum en laatste gebruik. Je kunt **Berichten** daar meteen in- en uitschakelen. Druk op **Wijzigen** om de toegang, het gebied of de duur aan te passen. De volgende aanvraag gebruikt de nieuwe instellingen. In **Activiteit** staan alle aanvragen, ook geweigerde. Met **Nu uitzetten** pauzeer je een AI: elke login wordt beëindigd, maar de geschiedenis blijft bewaard. Met **Verwijderen** haal je de AI en de geschiedenis weg.

Wanneer je opnieuw inlogt bij dezelfde AI, vervangt de nieuwe goedkeuring de vorige. Op plekken waar je al bij die AI was ingelogd, blijft de verbinding actief met de nieuwe toegangsrechten. Een AI die je gebruikt, blijft ingelogd tot de einddatum. Heb je een AI 90 dagen niet gebruikt, dan vraagt die je opnieuw in te loggen.

Een AI die niet zelf kan inloggen, kan een sleutel gebruiken. Kies onder **Sleutel toevoegen** een naam, de toegangsrechten en de duur, en druk op **Sleutel maken**. Kopieer de sleutel meteen: je ziet hem maar één keer. De AI stuurt hem mee als `Authorization: Bearer <key>`.

## Veilig houden

Elke aanvraag wordt geregistreerd, ook geweigerde aanvragen. Een verlopen of uitgeschakelde verbinding wordt geweigerd totdat je de instellingen wijzigt. Je Machine bewaart alleen een vingerafdruk van elke login, dus met een kopie van de gegevens krijgt niemand toegang.
