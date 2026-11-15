---
title: Notities
area: graph
summary: Eén overzichtelijke pagina per onderwerp, zoals een reis of je huis, gekoppeld aan de mensen en projecten die erbij horen.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a32102a88a8b3856
---
Een notitie geeft een overzicht van één onderwerp: een reis, je huis of hoe je facturen betaalt. Notities staan in de Graph naast Personen, Organisaties en Projecten. Ze blijven op je Machine en worden niet gedeeld met je team.

## Een notitie starten

Klik bovenaan Notities op **Nieuwe notitie**. Geef de notitie een titel en klik op **Notitie starten** om de pagina te openen. Met **Regel toevoegen** voeg je iets toe dat je wilt bewaren. Elke regel tekst wordt een aparte regel.

## Koppelen aan mensen, projecten en andere notities

Typ @ en een paar letters van een naam in een regel. Kies een persoon, organisatie, project of notitie uit de lijst. De naam wordt dan een link. Op de pagina van datgene waarnaar je linkt, staat onder **Gelinkt vanuit** jouw notitie.

## Notities onder andere notities

Een notitie kan onder een andere notitie staan, bijvoorbeeld Apparaten onder Thuis. Notities toont ze als een boomstructuur: met de pijl naast een notitie open je de notities eronder. Wil je een notitie verplaatsen, klik dan op **Bewerken** en kies onder **Onder** waar de notitie moet komen. Met **Nieuwe notitie onder deze** in het ⋯-menu maak je daar meteen een notitie.

## Notities die je Machine bijhoudt

Je Machine schrijft ook zelf notities op basis van je berichten en houdt ze actueel. Bij elke regel staat waar die vandaan komt, bijvoorbeeld wie de e-mail heeft gestuurd. Tik erop om het bericht te openen. Bij een regel uit **Wat ik heb geleerd** staat **Uit wat ik heb geleerd**.

Je wijzigingen blijven altijd staan. Hernoem een notitie, verplaats die, wijzig de datums of pas een regel aan. Je Machine laat dat zo wanneer hij de notitie bijwerkt. Verwijder je een regel of notitie, dan komt die niet terug. Nieuwe notities over hetzelfde onderwerp komen later terecht waar je de eerste hebt gezet.

Met **Terug naar het origineel** zie je weer de eigen woorden van je Machine. Als je een regel bewerkt die je Machine heeft geleerd, verandert die ook onder **Wat ik heb geleerd**. Zo blijft er maar één versie.

## Reizen

Als een boeking voor een vlucht, hotel, trein, bus, veerboot of huurauto in je e-mail binnenkomt, voegt je Machine die toe aan een reis onder **Reizen**. Boekingen voor één reis komen samen op één reis: de heenreis, het hotel en de terugreis. Bij elke regel staan de boekingscode, stoel en ticket, op volgorde van tijd. Ook staan de datums van de reis erbij. In [Agenda](calendar.md) wordt de reis als één balk over die dagen weergegeven. Klik erop om de reis te openen.

Je Machine leest de boekingsgegevens uit de bevestigingsmails van luchtvaartmaatschappijen, hotels en boekingssites. Een e-mail zonder die gegevens leidt niet tot een reis. Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking wordt verwijderd. Als alle boekingen van een reis zijn geannuleerd, verdwijnt de reis ook.

## Gebeurtenissen

Als tickets voor een concert, wedstrijd, festival of conferentie in je e-mail binnenkomen, voegt je Machine de gebeurtenis toe onder **Gebeurtenissen**, met één notitie per gebeurtenis. Op een regel staat waar de gebeurtenis plaatsvindt, met de boekingscode, stoel en het aantal tickets. Een tweede bestelling voor dezelfde gebeurtenis komt in dezelfde notitie. Net als bij een reis staan de datums erbij. In [Agenda](calendar.md) wordt de gebeurtenis als een balk weergegeven. Klik erop om de notitie te openen.

- Bij elke regel staat van wie de tickets komen, bijvoorbeeld **Van Example Tickets**. Klik erop om die e-mail te openen.
- Is er een to-do aangemaakt op basis van de ticketmail, bijvoorbeeld om de tickets te betalen, dan zie je die met **De to-do openen**.
- Een gebeurtenis die je via je werkmail hebt geboekt, is Werk. Anders is het Privé.

Je Machine leest de ticketgegevens uit de bevestigingsmails van ticketverkopers, zonder AI. Een e-mail zonder die gegevens leidt niet tot een gebeurtenis. Een geannuleerde boeking wordt verwijderd. Als alle tickets voor een gebeurtenis zijn geannuleerd, verdwijnt de gebeurtenis ook.

## Thuis

Onder **Thuis** houdt je Machine bij wat hij over je huis weet: **Rekeningen en abonnementen**, **Apparaten**, **Reparaties en onderhoud** en **Het huis**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Een rekening die regelmatig terugkomt, zoals voor energie of water, krijgt een regel met hoe vaak die rekening komt en de datum van de laatste rekening. Met **De to-do openen** open je de rekening zelf. Het bedrag en de betaalgegevens staan daar.
- Een abonnement dat je hebt gehouden, krijgt een regel die de to-do **Abonnementen** opent. Een opgezegd abonnement wordt niet getoond.
- Ook wat je Machine over je huis heeft geleerd, zoals het merk van je vaatwasser, krijgt een regel. Als je die bewerkt, verandert die ook onder **Wat ik heb geleerd**.
- Heb je zelf een notitie in een onderdeel, bijvoorbeeld over je vaatwasser onder **Apparaten**, dan komt alles over dat apparaat in jouw notitie. Je Machine maakt niet zelf zulke notities aan.

Alleen Privérekeningen en -abonnementen worden gebruikt. Notities onder Thuis zijn altijd Privé. Je Machine vraagt zijn AI één keer over elke nieuwe rekening, elk abonnement en alles wat hij heeft geleerd, om te bepalen of het over je huis gaat. Voor een rekening stuurt hij mee van wie die komt, maar nooit het bedrag.

## Gezondheid

Onder **Gezondheid** houdt je Machine bij wat hij over je gezondheid weet: **Afspraken**, **Artsen en zorg**, **Medicijnen**, **Allergieën en aandoeningen** en **Rekeningen en verzekeringen**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Een afspraak in je agenda waar alleen jij naartoe gaat, zoals een tandartsafspraak, krijgt een regel met de eerstvolgende datum of de laatste datum. Met **Uit je agenda** open je de afspraak.
- Een rekening van een arts, tandarts of apotheek krijgt een regel die de bijbehorende to-do opent. Het bedrag staat daar.
- Ook wat je Machine over je gezondheid heeft geleerd, zoals een allergie, krijgt een regel. Als je die bewerkt, verandert die ook onder **Wat ik heb geleerd**.
- Heb je zelf een notitie in een onderdeel, bijvoorbeeld over je fysiotherapeut onder **Afspraken**, dan komt alles over die zorgverlener daarin.

Notities onder Gezondheid zijn altijd Privé, ook als een rekening op je werkadres binnenkwam. Je Machine vraagt zijn AI één keer over elke nieuwe afspraak, rekening en alles wat hij heeft geleerd, om te bepalen of het over je eigen gezondheid gaat. Van een afspraak stuurt hij de naam mee, maar nooit de notities of wie er nog meer is uitgenodigd.

## Kinderen

Onder **Kinderen** houdt je Machine bij wat hij over je kinderen weet: **School**, **Activiteiten**, **Artsen en zorg** en **Rekeningen en kosten**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Wat je Machine over je kind heeft geleerd, zoals de naam van de leerkracht of de zwemdag, krijgt een regel die naar de pagina van je kind linkt. Hij herkent iemand als je kind als bij **Voor jou** bijvoorbeeld dochter of zoon staat.
- Een gebeurtenis in je agenda waar alleen jij naartoe gaat, zoals een ouderavond, krijgt een regel met de eerstvolgende datum of de laatste datum. Met **Uit je agenda** open je de gebeurtenis.
- Een rekening voor school, een club of kinderopvang krijgt een regel die de bijbehorende to-do opent. Het bedrag staat daar.
- Heb je zelf een notitie voor een van je kinderen in een onderdeel, bijvoorbeeld voor Isla onder **School**, dan komt alles over dat kind daarin.

Notities onder Kinderen zijn altijd Privé, ook als de school naar je werkadres mailt. Je Machine vraagt zijn AI één keer over elk nieuw onderwerp, om te bepalen of het over je kinderen gaat.

## Samenvoegen, verwijderen en ongedaan maken

Met **Samenvoegen in…** in het ⋯-menu verplaats je de regels en onderliggende notities van een notitie naar een andere notitie. Je Machine voegt nieuwe informatie vanaf dat moment aan die notitie toe. **Verwijderen** verwijdert een notitie. Bij beide acties kun je even **Ongedaan maken** kiezen. Dat kan ook nadat je een regel hebt verwijderd.

## Niet hetzelfde als vergadernotities

Vergadernotities en notities bij een persoon of organisatie blijven staan waar ze stonden. De notities hier zijn aparte pagina's.
