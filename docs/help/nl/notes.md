---
title: Notities
area: graph
summary: Eén overzichtelijke pagina per onderwerp, zoals een reis of je huis, gekoppeld aan de mensen en projecten die erbij horen.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 8e27b2c69f77196d
---
Een notitie geeft een overzicht van één onderwerp: een reis, je huis of hoe facturen worden afgehandeld. Notities staan in de Graph, naast Personen, Organisaties en Projecten. Ze blijven op je Machine en worden niet gedeeld met je team.

## Een notitie starten

Tik bovenaan in Notities op **Nieuwe notitie**. Geef de notitie een titel en tik op **Notitie starten**. De pagina wordt geopend. Met **Regel toevoegen** voeg je iets toe dat je wilt bewaren. Elke tekstregel wordt een eigen regel.

## Koppelen aan mensen, projecten en andere notities

Typ @ en een paar letters van een naam in een regel. Kies een persoon, organisatie, project of notitie uit de lijst. De naam wordt als link toegevoegd. Op de pagina van het gekoppelde item staat onder **Gelinkt vanuit** een link naar je notitie.

## Notities onder andere notities

Een notitie kan onder een andere notitie staan, zoals Apparaten onder Thuis. In Notities zie je ze als een boomstructuur: tik op de pijl naast een notitie om de notities eronder te openen. Als je een notitie wilt verplaatsen, tik je op **Bewerken** en kies je onder **Onder** waar de notitie moet komen. Met **Nieuwe notitie onder deze** in het ⋯-menu maak je daar meteen een notitie aan.

Bovenaan de pagina van een notitie zie je waar die staat, bijvoorbeeld **Notities › Kinderen**. Tik op een deel van het pad om daarheen te gaan. Op een telefoon worden tussenliggende notities samengevouwen in ⋯.

## Notities die je Machine bijhoudt

Je Machine maakt ook zelf notities op basis van je berichten en houdt ze actueel. Bij elke regel staat waar die vandaan komt, bijvoorbeeld wie de e-mail heeft gestuurd. Tik erop om het bericht te openen. Bij een regel uit **Wat ik heb geleerd** staat **Uit wat ik heb geleerd**. Een vergadering of afspraak in je agenda wordt nooit als losse regel toegevoegd: die blijft in [Agenda](calendar.md).

**Thuis**, **Gezondheid** en **Kinderen** verschijnen pas als je Machine er minstens twee concrete dingen over te melden heeft, zoals een rekening of iets wat hij heeft geleerd. Tot die tijd staan ze niet in de lijst. Als er later niets meer in staat, verdwijnen ze weer.

Je wijzigingen blijven altijd behouden. Geef een notitie een andere naam, verplaats hem, wijzig de datums of pas een regel aan, en je Machine houdt dat zo wanneer hij de notitie bijwerkt. Verwijder je een regel of notitie, dan komt die niet terug. Nieuwe notities over hetzelfde onderwerp komen later op de plek die je voor de eerste notitie hebt gekozen.

Met **Terug naar het origineel** zie je weer de eigen woorden van je Machine. Als je een regel bewerkt die afkomstig is uit wat je Machine heeft geleerd, wordt die ook aangepast onder **Wat ik heb geleerd**. Zo blijft er maar één versie.

## Reizen

Als een boeking voor een vlucht, hotel, trein, bus, veerboot of huurauto in je e-mail binnenkomt, voegt je Machine die toe aan een reis onder **Reizen**. Boekingen voor dezelfde reis komen bij elkaar: de heenreis, het hotel en de terugreis. Bij elke regel van de reis staan de boekingscode, stoel en het ticket, op volgorde van tijd. Ook staan de reisdatums erbij. In [Agenda](calendar.md) wordt de reis als één balk over die dagen weergegeven. Tik erop om de reis te openen.

Je Machine leest de boekingsgegevens die luchtvaartmaatschappijen, hotels en boekingssites in hun bevestigingsmail zetten. Zonder die gegevens wordt er geen reis aangemaakt. Boekingsmails uit de periode vóór het afgelopen jaar aan [geschiedenis](history.md) die je Machine bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen. Je persoonlijke mailboxen worden als eerste ingeladen.

Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking wordt verwijderd. Als alle boekingen van een reis zijn geannuleerd, wordt ook de reis verwijderd.

## Gebeurtenissen

Als kaartjes voor een concert, wedstrijd, festival of conferentie in je e-mail binnenkomen, voegt je Machine de gebeurtenis toe onder **Gebeurtenissen**. Er komt één notitie per gebeurtenis. In een regel staan de locatie, boekingscode, stoel en het aantal kaartjes. Een tweede bestelling voor dezelfde gebeurtenis komt in dezelfde notitie. Net als bij een reis staan de datums erbij en wordt de gebeurtenis als een balk in [Agenda](calendar.md) weergegeven. Tik erop om de notitie te openen.

- Bij elke regel staat van wie de kaartjes komen, zoals **Van Example Tickets**. Tik erop om de e-mail te openen.
- Als er een to-do is aangemaakt op basis van de e-mail met de kaartjes, bijvoorbeeld om voor de kaartjes te betalen, zie je die met **De to-do openen**.
- Een gebeurtenis die via je werkmailbox is geboekt, is Werk. Anders is die Persoonlijk.

Je Machine leest de kaartgegevens die kaartverkopers in hun bevestigingsmail zetten, zonder AI. Zonder die gegevens wordt er geen gebeurtenis aangemaakt. Een geannuleerde boeking wordt verwijderd. Als alle kaartjes voor een gebeurtenis zijn geannuleerd, wordt ook de gebeurtenis verwijderd.

## Thuis

Onder **Thuis** houdt je Machine bij wat hij weet over je huis: **Rekeningen en abonnementen**, **Apparaten**, **Reparaties en onderhoud** en **Het huis**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Een rekening die regelmatig terugkomt, zoals voor energie of water, krijgt een regel met hoe vaak die binnenkomt en de datum van de laatste rekening. Met **De to-do openen** open je de rekening zelf. Het bedrag en de betaalgegevens staan daar.
- Een abonnement dat je hebt behouden, krijgt een regel die de to-do voor **Abonnementen** opent. Een abonnement dat je hebt opgezegd, staat er niet bij.
- Wie regelmatig over je huis mailt, zoals je energieleverancier, internetprovider of gemeente, krijgt een regel met hoe vaak die mailt. Tik erop om de nieuwste e-mail te openen.
- Wat je Machine over je huis heeft geleerd, zoals het merk van je vaatwasser, krijgt ook een regel. Als je die bewerkt, wordt die ook aangepast onder **Wat ik heb geleerd**.
- Als je zelf een notitie bijhoudt in een onderdeel, bijvoorbeeld een notitie over je vaatwasser onder **Apparaten**, komt alles over dat apparaat in jouw notitie te staan. Je Machine maakt dit soort notities niet zelf aan.

Alleen persoonlijke rekeningen, abonnementen en e-mails worden gebruikt. Notities onder Thuis zijn altijd Persoonlijk. Je Machine vraagt zijn AI één keer per nieuwe rekening, nieuw abonnement of nieuw geleerd gegeven of het over je huis gaat. Bij een rekening stuurt hij de naam van de afzender mee, nooit het bedrag.

Voor **Thuis**, **Gezondheid** en **Kinderen** samen vraagt je Machine zijn AI ook één keer per afzender van je persoonlijke e-mail of de e-mails over die onderwerpen gaan. Hij stuurt de naam van de afzender, het aantal e-mails dat die heeft gestuurd en de nieuwste onderwerpen, waarbij de nummers verborgen zijn. De e-mails zelf stuurt hij nooit mee.

De eerste keer doorzoekt hij de e-mails van het afgelopen jaar in een paar uur, buiten de nacht en alleen als er ruimte is in je AI-abonnement. Daarna controleert hij elke zes uur nieuwe afzenders.

## Gezondheid

Onder **Gezondheid** houdt je Machine bij wat hij weet over je eigen gezondheid: **Afspraken**, **Testresultaten**, **Artsen en zorg**, **Medicijnen**, **Allergieën en aandoeningen** en **Rekeningen en verzekeringen**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Een rekening van een arts, tandarts of apotheek krijgt een regel die de bijbehorende to-do opent. Het bedrag staat daar.
- Elke e-mail van je huisartspraktijk, een ziekenhuis, laboratorium of zorgverzekeraar krijgt een gedateerde regel met het onderwerp. Zo bouwt je geschiedenis zich in de loop van de tijd op. Tik erop om de e-mail te openen.
- Wat je Machine over je gezondheid heeft geleerd, zoals een allergie, krijgt ook een regel. Als je die bewerkt, wordt die ook aangepast onder **Wat ik heb geleerd**.
- Als je zelf een notitie bijhoudt in een onderdeel, bijvoorbeeld een notitie over je fysiotherapeut onder **Afspraken**, komt alles over die zorgverlener in jouw notitie te staan.

Notities onder Gezondheid zijn altijd Persoonlijk, ook als een rekening op je werkadres is binnengekomen. Je Machine vraagt zijn AI één keer per nieuwe rekening of nieuw geleerd gegeven of het over je eigen gezondheid gaat.

## Kinderen

Onder **Kinderen** houdt je Machine bij wat hij weet over je kinderen: **School**, **Activiteiten**, **Kinderopvang**, **Artsen en zorg** en **Rekeningen en kosten**. Een oppas of kinderdagverblijf valt onder Kinderopvang, nooit onder Artsen en zorg. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Wat je Machine over je kind heeft geleerd, zoals de naam van de leerkracht of de zwemdag, krijgt een regel met een link naar de pagina van je kind. Hij ziet iemand als je kind als bij **Voor jou** bijvoorbeeld dochter of zoon staat.
- Een rekening voor school, een club of kinderopvang krijgt een regel die de bijbehorende to-do opent. Het bedrag staat daar.
- Elke e-mail van school, een club of de kinderopvang, zoals de wekelijkse nieuwsbrief of een bericht over een schoolreis, krijgt een gedateerde regel met het onderwerp. Zo staan alle berichten van die afzender op één plek. Tik erop om de e-mail te openen.
- Als je zelf een notitie bijhoudt voor een kind in een onderdeel, bijvoorbeeld een notitie voor Isla onder **School**, komt alles over dat kind in jouw notitie te staan.

Notities onder Kinderen zijn altijd Persoonlijk, ook als de school naar je werkadres mailt. Je Machine vraagt zijn AI één keer per nieuw gegeven of het over je kinderen gaat.

## Samenvoegen, verwijderen en ongedaan maken

Met **Samenvoegen in…** in het ⋯-menu verplaats je de regels en onderliggende notities van een notitie naar een andere notitie. Vanaf dat moment voegt je Machine nieuwe informatie aan die notitie toe. Met **Verwijderen** verwijder je een notitie. Beide acties bieden even de optie **Ongedaan maken**. Dat geldt ook als je een regel verwijdert.

## Niet hetzelfde als vergadernotities

Vergadernotities en notities over een persoon of organisatie blijven staan waar ze stonden. De notities hier zijn zelfstandige pagina's.
