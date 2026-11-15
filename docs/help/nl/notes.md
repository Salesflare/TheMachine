---
title: Notities
area: graph
summary: Eén overzichtelijke pagina per onderwerp, zoals een reis of je huis, gekoppeld aan de mensen en projecten die erbij horen.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: b88647412222409d
---
Een notitie geeft een overzicht van één onderwerp: een reis, je huis of hoe facturen worden afgehandeld. Notities staan in de Graph, naast Personen, Organisaties en Projecten. Ze blijven op je Machine en worden niet met je team gedeeld.

## Een notitie starten

Klik bovenaan Notities op **Nieuwe notitie**. Geef de notitie een titel en klik op **Notitie starten**. De pagina wordt geopend. Met **Regel toevoegen** voeg je iets toe dat je wilt bewaren. Elke regel tekst wordt een eigen regel.

## Koppelen aan mensen, projecten en andere notities

Typ @ en een paar letters van een naam in een regel. Kies een persoon, organisatie, project of notitie uit de lijst. De naam wordt als link toegevoegd. Op de pagina van het gekoppelde item staat **Gelinkt vanuit** met jouw notitie.

## Notities onder notities

Een notitie kan onder een andere notitie staan, zoals Apparaten onder Thuis. Notities toont ze als een boomstructuur: met de pijl naast een notitie open je de notities eronder. Verplaatsen doe je via **Bewerken**. Kies onder **Onder** waar de notitie moet komen. Met **Nieuwe notitie onder deze** in het ⋯-menu maak je daar meteen een notitie aan.

## Notities die je Machine bijhoudt

Je Machine maakt ook zelf notities op basis van je berichten en houdt die actueel. Bij elke regel staat waar die vandaan komt, bijvoorbeeld wie de e-mail heeft gestuurd. Tik op de regel om het bericht te openen. Bij een regel uit **Wat ik heb geleerd** staat **Uit wat ik heb geleerd**.

Je wijzigingen blijven altijd behouden. Hernoem een notitie, verplaats die of wijzig de datums of een regel. Je Machine houdt dat zo wanneer hij de notitie bijwerkt. Verwijder je een regel of notitie, dan komt die niet terug. Nieuwe notities over hetzelfde onderwerp komen later op de plek die je voor de eerste notitie hebt gekozen.

Met **Terug naar het origineel** zie je weer de eigen woorden van je Machine. Als je een regel bewerkt die afkomstig is van wat je Machine heeft geleerd, wordt die ook aangepast onder **Wat ik heb geleerd**. Zo blijft er maar één versie.

## Reizen

Wanneer een boeking voor een vlucht, hotel, trein, bus, veerboot of huurauto in je mail binnenkomt, voegt je Machine die toe aan een reis onder **Reizen**. Boekingen voor één reis komen bij elkaar op één reis: de heenreis, het hotel en de terugreis. Bij elke regel staan de boekingscode, stoel en ticket, op volgorde van tijd. Ook staan de reisdatums erbij. In [Agenda](calendar.md) wordt de reis als één balk over die dagen weergegeven. Als je erop klikt, wordt de reis geopend.

Je Machine leest de boekingsgegevens die luchtvaartmaatschappijen, hotels en boekingssites in hun bevestigingsmail zetten. Een mail zonder die gegevens maakt geen reis aan. Boekingsmails van eerder in het jaar waaruit je Machine [geschiedenis](history.md) bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen. Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking wordt verwijderd. Als alle boekingen van een reis zijn geannuleerd, wordt ook de reis verwijderd.

## Gebeurtenissen

Wanneer tickets voor een concert, wedstrijd, festival of conferentie in je mail binnenkomen, voegt je Machine de gebeurtenis toe onder **Gebeurtenissen**, met één notitie per gebeurtenis. Een regel vermeldt waar de gebeurtenis plaatsvindt, met de boekingscode, stoel en het aantal tickets. Een tweede bestelling voor dezelfde gebeurtenis komt in dezelfde notitie. Net als een reis worden de datums getoond. In [Agenda](calendar.md) staat de gebeurtenis als een balk die de notitie opent.

- Bij elke regel staat van wie de tickets komen, bijvoorbeeld **Van Voorbeeldtickets**. De regel opent die mail.
- Als er een to-do is aangemaakt op basis van de ticketmail, bijvoorbeeld om de tickets te betalen, zie je die via **De to-do openen**.
- Een gebeurtenis die via je werkmailbox is geboekt, is Werk. Anders is die Persoonlijk.

Je Machine leest de ticketgegevens die ticketverkopers in hun bevestigingsmail zetten, zonder AI. Een mail zonder die gegevens maakt geen gebeurtenis aan. Een geannuleerde boeking wordt verwijderd. Als alle tickets voor een gebeurtenis zijn geannuleerd, wordt ook de gebeurtenis verwijderd.

## Thuis

Onder **Thuis** houdt je Machine bij wat hij over je huis weet: **Rekeningen en abonnementen**, **Apparaten**, **Reparaties en onderhoud** en **Het huis**. Een onderdeel verschijnt zodra het minstens twee regels heeft.

- Een rekening die regelmatig binnenkomt, zoals voor energie of water, krijgt een regel met hoe vaak die binnenkomt en de datum van de laatste rekening. Met **De to-do openen** open je de rekening zelf. Het bedrag en de betaalgegevens staan daar.
- Een abonnement dat je hebt gehouden, krijgt een regel die de to-do **Abonnementen** opent. Een opgezegd abonnement wordt niet getoond.
- Wat je Machine over je huis heeft geleerd, zoals het merk van je vaatwasser, krijgt ook een regel. Als je die bewerkt, wordt die ook aangepast onder **Wat ik heb geleerd**.
- Heb je zelf een notitie in een onderdeel, bijvoorbeeld over je vaatwasser onder **Apparaten**, dan komt informatie over dat apparaat in jouw notitie. Je Machine maakt zelf geen notities van dit soort aan.

Alleen Persoonlijke rekeningen en abonnementen worden gebruikt. Thuisnotities zijn altijd Persoonlijk. Je Machine vraagt zijn AI één keer per nieuwe rekening, abonnement of nieuw geleerd gegeven of het over je huis gaat. Bij een rekening vermeldt hij van wie die komt, nooit het bedrag.

## Gezondheid

Onder **Gezondheid** houdt je Machine bij wat hij over je gezondheid weet: **Afspraken**, **Artsen en zorg**, **Medicijnen**, **Allergieën en aandoeningen** en **Rekeningen en verzekeringen**. Een onderdeel verschijnt zodra het minstens twee regels heeft.

- Een afspraak in je agenda waar alleen jij naartoe gaat, zoals een tandartsafspraak, krijgt een regel met de eerstvolgende datum of de laatste datum. Met **Uit je agenda** open je de afspraak.
- Een rekening van een arts, tandarts of apotheek krijgt een regel die de bijbehorende to-do opent. Het bedrag staat daar.
- Wat je Machine over je gezondheid heeft geleerd, zoals een allergie, krijgt ook een regel. Als je die bewerkt, wordt die ook aangepast onder **Wat ik heb geleerd**.
- In je eigen notitie bij een onderdeel, bijvoorbeeld een notitie over je fysiotherapeut onder **Afspraken**, komt informatie over dat onderwerp.

Gezondheidsnotities zijn altijd Persoonlijk, ook als een rekening op je werkadres is binnengekomen. Je Machine vraagt zijn AI één keer per nieuwe afspraak, rekening of nieuw geleerd gegeven of het over je eigen gezondheid gaat. Hij stuurt de naam van een afspraak mee, maar nooit de notities of de namen van andere genodigden.

## Kinderen

Onder **Kinderen** houdt je Machine bij wat hij over je kinderen weet: **School**, **Activiteiten**, **Artsen en zorg** en **Rekeningen en kosten**. Een onderdeel verschijnt zodra het minstens twee regels heeft.

- Wat je Machine over je kind heeft geleerd, zoals de naam van de leerkracht of de zwemdag, krijgt een regel die naar de pagina van je kind linkt. Iemand wordt als je kind gezien als bij **Voor jou** bijvoorbeeld dochter of zoon staat.
- Een gebeurtenis in je agenda waar alleen jij naartoe gaat, zoals een ouderavond, krijgt een regel met de eerstvolgende datum of de laatste datum. Met **Uit je agenda** open je de gebeurtenis.
- Een rekening voor school, een club of kinderopvang krijgt een regel die de bijbehorende to-do opent. Het bedrag staat daar.
- In je eigen notitie voor een kind bij een onderdeel, bijvoorbeeld een notitie voor Isla onder **School**, komt informatie over dat kind.

Kindernotities zijn altijd Persoonlijk, ook als de school naar je werkadres mailt. Je Machine vraagt zijn AI één keer per nieuw gegeven of het over je kinderen gaat.

## Samenvoegen, verwijderen en ongedaan maken

Met **Samenvoegen in…** in het ⋯-menu verplaats je de regels en onderliggende notities van een notitie naar een andere notitie. Vanaf dat moment voegt je Machine nieuwe informatie aan die notitie toe. Met **Verwijderen** verwijder je een notitie. Bij beide acties kun je even op **Ongedaan maken** klikken. Dat kan ook nadat je een regel hebt verwijderd.

## Niet hetzelfde als vergadernotities

Vergadernotities en notities over een persoon of organisatie blijven op hun eigen plek staan. De notities hier zijn zelfstandige pagina's.
