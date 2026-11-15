---
title: Notities
area: graph
summary: Eén overzichtelijke pagina per onderwerp, zoals een reis of je huis, gekoppeld aan de mensen en projecten die erbij horen.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a71c5e46042cddd0
---
Een notitie geeft een overzicht van één onderwerp: een reis, je huis of hoe facturen worden afgehandeld. Notities staan in de Graph naast Personen, Organisaties en Projecten. Ze blijven op je Machine en worden niet met je team gedeeld.

## Een notitie starten

**Nieuwe notitie** bovenaan Notities. Geef de notitie een titel en tik op **Notitie starten**. De pagina wordt geopend. Met **Regel toevoegen** voeg je toe wat je wilt bewaren. Elke tekstregel wordt een eigen regel.

## Koppelen aan personen, projecten en andere notities

Typ @ en een paar letters van een naam in een regel. Kies een persoon, organisatie, project of notitie uit de lijst. De naam wordt als link toegevoegd. Op de pagina van het gekoppelde item staat onder **Gelinkt vanuit** een link naar je notitie.

## Notities onder andere notities

Een notitie kan onder een andere notitie staan, bijvoorbeeld Apparaten onder Thuis. Notities toont ze als een boomstructuur: met de pijl naast een notitie open je de notities eronder. Verplaats een notitie met **Bewerken** en kies onder **Onder** waar die moet komen. Met **Nieuwe notitie onder deze** in het ⋯-menu start je daar een nieuwe notitie.

Bovenaan de pagina van een notitie staat waar die zich bevindt, bijvoorbeeld **Notities › Kinderen**. Tik op een deel om daarnaartoe te gaan. Op een telefoon zijn tussenliggende notities samengevouwen in ⋯.

## Notities die je Machine bijhoudt

Je Machine maakt ook zelf notities op basis van je berichten en houdt ze actueel. Bij elke regel staat waar die vandaan komt, bijvoorbeeld wie de e-mail heeft gestuurd. Tik erop om het bericht te openen. Bij een regel uit **Wat ik heb geleerd** staat **Uit wat ik heb geleerd**.

Een vergadering of afspraak in je agenda wordt nooit een losse regel: die blijft in [Agenda](calendar.md). Hetzelfde geldt voor de bijbehorende e-mail: de uitnodiging, reacties, updates en annuleringen.

**Thuis**, **Gezondheid** en **Kinderen** verschijnen pas zodra je Machine er minstens twee concrete dingen over te vertellen heeft, zoals een rekening of iets wat hij heeft geleerd. Tot die tijd staan ze helemaal niet in de lijst. Als ze later weer leeg zijn, verdwijnen ze.

Je wijzigingen blijven altijd staan. Hernoem een notitie, verplaats die, wijzig de datums of pas een regel aan, en je Machine laat dat zo wanneer hij de notitie bijwerkt. Verwijder je een regel of notitie, dan komt die niet terug. Latere notities over hetzelfde onderwerp komen terecht op de plek van de eerste.

Met **Terug naar het origineel** zie je weer de eigen woorden van je Machine. Als je een regel bewerkt die afkomstig is van iets wat je Machine heeft geleerd, verandert die ook onder **Wat ik heb geleerd**. Zo blijft er maar één versie.

## Pagina's opstellen

Zodra een notitie minstens twee regels bevat uit je berichten of uit wat je Machine heeft geleerd, schrijft je Machine bovenaan de pagina. Hij leest de gesprekken zelf, niet alleen de onderwerpen:

- Een korte samenvatting: waar het over gaat en wat de stand van zaken is.
- **Belangrijke feiten**, **Beslissingen**, **Openstaande punten** en een **Tijdlijn**, maar alleen als er concrete informatie is.
- De regels van de notitie staan eronder, genummerd onder **Bronnen**. Aan het eind van elke zin staan de nummers van de regels waarop die is gebaseerd. Tik op een nummer om naar die regel te gaan.

De pagina wordt alleen opnieuw opgesteld als de regels van de notitie veranderen, hooguit ongeveer één keer per dag. Als de bronnen niets concreets bevatten, is er geen pagina en staan er alleen regels. Verwijder je een regel, dan verdwijnt ook alles van de pagina wat alleen op die regel was gebaseerd. In de lijst met Notities staat onder de naam van elke notitie het begin van de samenvatting.

Een project of organisatie heeft al een eigen pagina in de Graph, met bovenaan een beschrijving. Gesprekken daarover komen op die pagina, niet in een notitie.

## Notities uit je gesprekken

Je Machine leest volledige gesprekken en zet elk gesprek in de notitie waar het over gaat: een e-mailthread uit een van je mailboxen, een chat in WhatsApp, Slack, Telegram, LinkedIn of een andere gekoppelde app, en je vergadernotities. Chatberichten tellen als één gesprek totdat de chat twee dagen stil is.

- Een gesprek over een project of organisatie in je Graph komt op die pagina, niet in een nieuwe notitie.
- Een gesprek kan terechtkomen in een onderdeel van **Thuis**, **Gezondheid** of **Kinderen**, in een notitie van jezelf of in een notitie die je Machine aanmaakt onder **Werk**, **Auto**, **Belastingen** of een andere map.
- Je Machine start alleen een nieuwe notitie voor een onderwerp met minstens twee gesprekken, of voor iets waarover je zelf een bericht hebt geschreven en dat duidelijk nog speelt.
- Elke regel staat voor één gesprek, met het nieuwste bovenaan. Tik erop om het gesprek te openen.

Je Machine stuurt een kort deel van elk gesprek naar de AI, zonder geciteerde reacties of handtekeningen. Elk gesprek wordt één keer verwerkt; nieuwe berichten worden eraan toegevoegd.

Bulkmail en chats komen nooit in een notitie en worden nooit naar de AI gestuurd: spam, reclame, nieuwsbrieven en andere mailinglijstberichten, meldingen van no-reply-adressen, bots en omroepkanalen. Een gesprek waarin je zelf hebt geschreven telt wel mee, net als boekingsmails voor **Reizen** en **Gebeurtenissen**.

De eerste keer verwerkt je Machine in een paar uur de afgelopen drie maanden, buiten de nacht en alleen zolang er ruimte is in je AI-abonnement. Daarna sorteert hij nieuwe gesprekken zodra er tien klaarstaan of zodra één gesprek een halve dag heeft gewacht.

## Reizen

Als er een boeking voor een vlucht, hotel, trein, bus, veerboot of huurauto in je e-mail binnenkomt, voegt je Machine die toe aan een reis onder **Reizen**. Boekingen voor één reis komen samen op één reis: de heenreis, het hotel en de terugreis. De reis bevat voor elke regel de boekingscode, stoel en het ticket, op volgorde van tijd, en toont de datums. In [Agenda](calendar.md) wordt de reis als één balk over die dagen weergegeven. Tik erop om de reis te openen.

Je Machine leest de boekingsgegevens die luchtvaartmaatschappijen, hotels en boekingssites in hun bevestigingsmails zetten. Zonder die gegevens wordt er geen reis aangemaakt. Boekingsmails van eerder worden op de achtergrond gelezen zodra de [geschiedenis](history.md) die je Machine bewaart is binnengehaald, te beginnen met je persoonlijke mailboxen. Een oudere bevestiging die later wordt gelezen, wordt toegevoegd aan de reis die al bestaat.

Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking wordt verwijderd. Als alle boekingen van een reis zijn geannuleerd, verdwijnt ook de reis.

## Gebeurtenissen

Als er tickets voor een concert, wedstrijd, festival of conferentie in je e-mail binnenkomen, voegt je Machine de gebeurtenis toe onder **Gebeurtenissen**, met één notitie per gebeurtenis. Een regel vermeldt waar de gebeurtenis is, met de boekingscode, stoel en het aantal tickets. Een tweede bestelling voor dezelfde gebeurtenis komt in dezelfde notitie. Net als een reis toont de gebeurtenis de datums en staat die in [Agenda](calendar.md) als een balk die de notitie opent.

- Bij elke regel staat van wie de tickets komen, bijvoorbeeld **Van Voorbeeldtickets**, en wordt de betreffende e-mail geopend.
- Als er een to-do uit de ticketmail is gemaakt, bijvoorbeeld om de tickets te betalen, toont **De to-do openen** die.
- Een gebeurtenis die via je werkmailbox is geboekt, valt onder Werk. Anders valt die onder Persoonlijk.

Je Machine leest de ticketgegevens die ticketverkopers in hun bevestigingsmails zetten, zonder AI. Zonder die gegevens wordt er geen gebeurtenis aangemaakt. Een geannuleerde boeking wordt verwijderd. Als alle tickets voor een gebeurtenis zijn geannuleerd, verdwijnt ook de gebeurtenis.

## Thuis

Onder **Thuis** houdt je Machine bij wat hij over je huis weet: **Rekeningen en abonnementen**, **Apparaten**, **Reparaties en onderhoud** en **Het huis**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Een rekening die regelmatig terugkomt, bijvoorbeeld voor energie of water, krijgt een regel met hoe vaak die binnenkomt en de datum van de laatste rekening. Met **De to-do openen** open je de rekening zelf. Het bedrag en de betalingsgegevens blijven daar staan.
- Een abonnement dat je hebt behouden, krijgt een regel die de to-do **Abonnementen** opent. Een abonnement dat je hebt opgezegd, wordt niet vermeld.
- Wie regelmatig contact opneemt over je huis, zoals je energieleverancier, internetprovider of gemeente, krijgt een regel met hoe vaak die contact opneemt. Tik erop om de nieuwste e-mail te openen.
- Ook informatie die je Machine over je huis heeft geleerd, zoals het merk van je vaatwasser, krijgt een regel. Als je die bewerkt, verandert die ook onder **Wat ik heb geleerd**.
- Als je zelf een notitie bijhoudt in een onderdeel, bijvoorbeeld een notitie over je vaatwasser onder **Apparaten**, komt informatie over dat apparaat in jouw notitie terecht. Je Machine maakt dit soort notities niet zelf aan.

Alleen persoonlijke rekeningen, abonnementen en e-mails worden gebruikt. Notities onder Thuis zijn altijd persoonlijk. Je Machine vraagt zijn AI één keer naar elke nieuwe rekening, elk abonnement en elk nieuw ding dat hij heeft geleerd, om te bepalen of het over je huis gaat. Bij een rekening stuurt hij alleen informatie over de afzender, nooit het bedrag.

Je gesprekken komen ook in deze notities terecht, zoals hierboven beschreven onder **Notities uit je gesprekken**.

## Gezondheid

Onder **Gezondheid** houdt je Machine bij wat hij weet over je gezondheid: **Afspraken**, **Testresultaten**, **Artsen en zorg**, **Medicijnen**, **Allergieën en aandoeningen** en **Rekeningen en verzekeringen**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Een rekening van een arts, tandarts of apotheek krijgt een regel die de bijbehorende to-do opent. Het bedrag blijft daar staan.
- Elke e-mail van je huisartsenpraktijk, een ziekenhuis, laboratorium of zorgverzekeraar wordt een gedateerde regel met het onderwerp. Zo bouw je in de loop van de tijd een overzicht op. Tik erop om de e-mail te openen.
- Ook informatie die je Machine over je gezondheid heeft geleerd, zoals een allergie, krijgt een regel. Als je die bewerkt, verandert die ook onder **Wat ik heb geleerd**.
- Als je zelf een notitie bijhoudt in een onderdeel, bijvoorbeeld een notitie over je fysiotherapeut onder **Afspraken**, komt informatie over die zorgverlener in jouw notitie terecht.

Notities onder Gezondheid zijn altijd persoonlijk, ook als een rekening op je werkadres is binnengekomen. Je Machine vraagt zijn AI één keer naar elke nieuwe rekening en elk nieuw ding dat hij heeft geleerd, om te bepalen of het over je gezondheid gaat.

## Kinderen

Onder **Kinderen** houdt je Machine bij wat hij over je kinderen weet: **School**, **Activiteiten**, **Kinderopvang**, **Artsen en zorg** en **Rekeningen en kosten**. Een oppas of kinderdagverblijf valt onder Kinderopvang, nooit onder Artsen en zorg. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Informatie die je Machine over je kind heeft geleerd, zoals de leerkracht of zwemdag, krijgt een regel met een link naar de pagina van je kind. Je Machine ziet iemand als je kind als er onder **Voor jou** bijvoorbeeld dochter of zoon staat.
- Een rekening voor school, een club of kinderopvang krijgt een regel die de bijbehorende to-do opent. Het bedrag blijft daar staan.
- Elke e-mail van school, een club of kinderopvang, bijvoorbeeld over een uitje of een wijziging van plannen, wordt een gedateerde regel met het onderwerp. Zo staat alles wat ze sturen op één plek. Tik erop om de e-mail te openen.
- Als je zelf voor een kind een notitie bijhoudt in een onderdeel, bijvoorbeeld een notitie voor Isla onder **School**, komt informatie over dat kind in jouw notitie terecht.

Notities onder Kinderen zijn altijd persoonlijk, ook als de school naar je werkadres mailt. Je Machine vraagt zijn AI één keer naar elk nieuw ding om te bepalen of het over je kinderen gaat.

## Samenvoegen, verwijderen en ongedaan maken

Met **Samenvoegen in…** in het ⋯-menu verplaats je de regels en onderliggende notities van een notitie naar een andere notitie. Vanaf dan voegt je Machine nieuwe informatie aan die notitie toe. Met **Verwijderen** verwijder je een notitie. Bij beide acties verschijnt even **Ongedaan maken**. Dat gebeurt ook als je een regel verwijdert.

## Niet hetzelfde als vergadernotities

Vergadernotities en notities over een persoon of organisatie blijven waar ze al stonden. De notities hier zijn zelfstandige pagina's.
