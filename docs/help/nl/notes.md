---
title: Notities
area: graph
summary: Per onderwerp, zoals een reis of je huis, één overzichtelijke pagina met links naar de mensen en projecten die erbij horen.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, folder_overview.py, memory_seed.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 1087ac0970878932
---
Een notitie geeft een overzicht van één onderwerp: een reis, je huis of hoe facturen worden afgehandeld. Notities staan in de Graph, naast People, Organizations en Projects. Ze blijven op je Machine en worden niet met je team gedeeld.

## Een notitie starten

Kies bovenaan Notities **Nieuwe notitie**. Geef de notitie een titel en kies **Notitie starten**. De pagina wordt geopend. Met **Regel toevoegen** voeg je toe wat je wilt bewaren. Elke tekstregel wordt een aparte regel.

## Koppelen aan mensen, projecten en andere notities

Typ @ en een paar letters van een naam in een regel. Kies een persoon, organisatie, project of notitie uit de lijst. De naam wordt dan een link. Op de pagina van dat item staat bij **Gelinkt vanuit** een link naar je notitie.

## Notities onder andere notities

Een notitie kan onder een andere notitie staan, zoals Apparaten onder Thuis. Notities worden als een boomstructuur weergegeven. Met de pijl naast een notitie open je de notities eronder. Verplaats een notitie met **Bewerken** en kies onder **Onder** waar de notitie moet komen. Met **Nieuwe notitie onder deze** in het ⋯-menu maak je daar meteen een notitie aan.

Bovenaan de pagina van een notitie zie je waar die staat, bijvoorbeeld **Notities › Kinderen**. Tik op een onderdeel om ernaartoe te gaan. Op een telefoon worden tussenliggende notities samengevouwen in ⋯.

## Notities die je Machine bijhoudt

Je Machine maakt ook zelf notities op basis van je berichten en houdt die actueel. Bij elke regel staat waar die vandaan komt, bijvoorbeeld wie de e-mail heeft verstuurd. Tik erop om het bericht te openen. Bij een regel uit **Wat ik heb geleerd** staat **Uit wat ik heb geleerd**.

Een vergadering of afspraak in je agenda wordt nooit een aparte regel: die blijft in [Agenda](calendar.md). De e-mail erover blijft daar ook, zoals de uitnodiging, antwoorden, updates en annuleringen.

**Thuis**, **Gezondheid** en **Kinderen** verschijnen pas als je Machine daar minstens twee concrete dingen over kan vermelden, zoals een rekening of iets wat hij heeft geleerd. Tot die tijd staan ze niet in de lijst. Als er later weer niets in staat, verdwijnen ze.

Je wijzigingen blijven altijd staan. Hernoem een notitie, verplaats die, wijzig de datums of pas een regel aan. Je Machine houdt die wijzigingen aan wanneer hij de notitie bijwerkt. Verwijder je een regel of notitie, dan komt die niet terug. Nieuwe notities over hetzelfde onderwerp komen op de plek van de eerste notitie.

Met **Terug naar het origineel** zie je weer de eigen woorden van je Machine. Als je een regel bewerkt die afkomstig is van wat je Machine heeft geleerd, wordt die ook aangepast onder **Wat ik heb geleerd**. Zo blijft er één versie.

## Pagina's met tekst

Zodra een notitie minstens twee regels bevat uit je berichten of uit wat je Machine heeft geleerd, schrijft je Machine bovenaan de pagina. Hij leest de gesprekken zelf, niet alleen de onderwerpen:

- Een korte samenvatting van waar het over gaat en wat de stand van zaken is.
- **Belangrijke feiten**, **Beslissingen**, **Openstaande punten** en een **Tijdlijn**, alleen als er concrete informatie is.
- Daaronder staan de regels van de notitie, genummerd onder **Bronnen**. Elke zin eindigt met de nummers van de regels waarop die is gebaseerd. Tik op een nummer om naar die regel te gaan.

De pagina wordt alleen opnieuw geschreven als de regels van de notitie veranderen, en hooguit ongeveer één keer per dag. Als de bronnen niets concreets bevatten, wordt er geen pagina aangemaakt en zie je alleen de regels. Verwijder je een regel, dan verdwijnt ook alles op de pagina wat alleen daarop gebaseerd was. In de lijst met notities staat onder de naam van elke notitie het begin van de samenvatting.

Een project of organisatie heeft al een eigen pagina in de Graph, met bovenaan een beschrijving. Gesprekken daarover komen op die pagina, niet in een notitie.

## Overzichten

Een notitie met notities eronder, zoals **Werk** of **Thuis**, krijgt bovenaan een kort overzicht zodra minstens twee onderliggende notities nieuws bevatten. Dat bestaat uit een of twee zinnen over wat er speelt en een paar dingen die onlangs zijn veranderd of binnenkort gebeuren. Aan het einde van elk punt staan de namen van de notities waar het vandaan komt. Tik op een naam om die notitie te openen.

Het overzicht wordt samengesteld op basis van de pagina's en nieuwste regels van de onderliggende notities, hooguit één keer per dag en alleen als die zijn gewijzigd. Als er niets actueels is, verschijnt er geen overzicht. In de lijst met notities staat onder de mapnaam het begin van het overzicht.

## Notities uit je gesprekken

Je Machine leest volledige gesprekken en zet elk gesprek in de notitie over het onderwerp: een e-mailthread uit een van je mailboxen, een chat in WhatsApp, Slack, Telegram, LinkedIn of een andere gekoppelde app, of je vergadernotities. Chatberichten tellen als één gesprek totdat de chat twee dagen stil is.

- Een gesprek over een project of organisatie in je Graph komt op die pagina, niet in een nieuwe notitie.
- Een gesprek kan terechtkomen in een onderdeel van **Thuis**, **Gezondheid** of **Kinderen**, in een notitie die je zelf hebt gemaakt, of in een notitie die je Machine aanmaakt onder **Werk**, **Auto**, **Belastingen** of een andere map.
- Je Machine maakt alleen een nieuwe notitie aan voor een onderwerp met minstens twee gesprekken, of voor een onderwerp waarover je zelf hebt geschreven en dat duidelijk nog speelt.
- Elke regel bevat één gesprek, met de nieuwste bovenaan. Tik erop om het gesprek te openen.

De AI krijgt een kort fragment uit elk gesprek, zonder geciteerde antwoorden of handtekeningen. Elk gesprek wordt één keer verwerkt. Nieuwe berichten in dat gesprek worden daarna ook meegenomen.

Bulkmail en chats komen nooit in een notitie terecht en worden nooit naar de AI gestuurd. Het gaat om spam, aanbiedingen, nieuwsbrieven en andere mailinglijsten, meldingen van no-reply-adressen, bots en uitzendkanalen. Een gesprek waaraan je zelf hebt deelgenomen telt wel mee, net als boekingsmails voor **Reizen** en **Gebeurtenissen**.

De eerste keer worden je gesprekken van de afgelopen drie maanden binnen een paar uur verwerkt, buiten de nacht en alleen als er ruimte is in je AI-abonnement. Daarna worden nieuwe gesprekken verwerkt zodra er tien klaarstaan of één gesprek een halve dag heeft gewacht.

## Notities uit OpenClaw-geheugen

Als je OpenClaw eerder hebt gebruikt, leest je Machine één keer de onderwerppagina's in de geheugenmap, bijvoorbeeld een pagina over een reis of je gezondheid. Informatie die relevant blijft, komt in de notitie over dat onderwerp of in een nieuwe notitie. Bij elke regel staat van welke pagina die afkomstig is, bijvoorbeeld **Uit je geheugenpagina's · Lissabon**, met de datum erbij. Houd de aanwijzer erboven om te zien om welke pagina het gaat.

Je Machine past die pagina's nooit aan en slaat dagelijkse logboeken, pagina's over de assistent zelf en mappen die als gevoelig of privé zijn gemarkeerd over. Hij leest maximaal 80 pagina's, een paar tegelijk, en doet dat maar één keer.

## Reizen

Als er een boeking voor een vlucht, hotel, trein, bus, veerboot of huurauto in je e-mail binnenkomt, voegt je Machine die toe aan een reis onder **Reizen**. Boekingen voor één reis komen bij elkaar op één reisnotitie: de heenreis, het hotel en de terugreis. Elke regel bevat de boekingscode, stoel en het ticket. De regels staan op volgorde van tijd en de reisnotitie toont de reisdatums. In [Agenda](calendar.md) verschijnt de reis als één balk over die dagen. Tik erop om de reisnotitie te openen.

Je Machine leest de boekingsgegevens die luchtvaartmaatschappijen, hotels en boekingssites in hun bevestigingsmails zetten. Zonder die gegevens wordt er geen reis aangemaakt. Boekingsmails van eerder worden op de achtergrond gelezen zodra de [geschiedenis](history.md) is ingeladen die je Machine bewaart voor het betreffende jaar. Je persoonlijke mailboxen worden als eerste verwerkt. Een oudere bevestiging die later wordt gelezen, wordt toegevoegd aan de bestaande reis.

Een gewijzigde boeking werkt de regel bij. Een geannuleerde boeking wordt verwijderd. Zijn alle boekingen van een reis geannuleerd, dan wordt ook de reis verwijderd.

## Gebeurtenissen

Als er tickets voor een concert, wedstrijd, festival of conferentie in je e-mail binnenkomen, voegt je Machine de gebeurtenis toe onder **Gebeurtenissen**. Elke gebeurtenis krijgt een eigen notitie. Een regel vermeldt waar de gebeurtenis plaatsvindt, met de boekingscode, stoel en het aantal tickets. Een tweede bestelling voor dezelfde gebeurtenis komt in dezelfde notitie. Net als bij een reis toont de notitie de datums. In [Agenda](calendar.md) verschijnt de gebeurtenis als een balk. Tik erop om de notitie te openen.

- Bij elke regel staat van wie de tickets komen, bijvoorbeeld **Van Example Tickets**. Tik erop om de e-mail te openen.
- Is er een to-do aangemaakt op basis van de e-mail met tickets, bijvoorbeeld om de tickets te betalen, dan kun je die openen met **De to-do openen**.
- Een gebeurtenis die is geboekt via je werkmailbox is Werk. Anders is het Persoonlijk.

Je Machine leest de ticketgegevens die ticketverkopers in hun bevestigingsmails zetten, zonder AI. Zonder die gegevens wordt er geen gebeurtenis aangemaakt. Een geannuleerde boeking wordt verwijderd. Zijn alle tickets voor een gebeurtenis geannuleerd, dan wordt ook de gebeurtenis verwijderd.

## Thuis

Onder **Thuis** houdt je Machine bij wat hij over je huis weet: **Rekeningen en abonnementen**, **Apparaten**, **Reparaties en onderhoud** en **Het huis**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Een terugkerende rekening, zoals voor energie of water, krijgt een regel met hoe vaak die binnenkomt en de datum van de laatste rekening. Met **De to-do openen** open je de rekening zelf. Het bedrag en de betaalgegevens staan daar.
- Een abonnement dat je nog hebt, krijgt een regel die de to-do **Abonnementen** opent. Een opgezegd abonnement staat er niet bij.
- Wie regelmatig over je huis schrijft, zoals je energieleverancier, internetprovider of gemeente, krijgt een regel met hoe vaak die contact opneemt. Tik erop om de nieuwste e-mail te openen.
- Wat je Machine over je huis heeft geleerd, zoals het merk van je vaatwasser, krijgt ook een regel. Als je die bewerkt, wordt die ook aangepast onder **Wat ik heb geleerd**.
- Heb je zelf een notitie gemaakt in een onderdeel, bijvoorbeeld voor je vaatwasser onder **Apparaten**, dan komt informatie over dat apparaat in jouw notitie terecht. Je Machine maakt zelf geen notities van dit soort aan.

Alleen persoonlijke rekeningen, abonnementen en e-mails worden gebruikt. Notities onder Thuis zijn altijd Persoonlijk. Je Machine vraagt de AI één keer voor elke nieuwe rekening, elk nieuw abonnement en elk nieuw ding dat hij heeft geleerd, om te bepalen of het over je huis gaat. Bij een rekening stuurt hij alleen informatie over de afzender mee, nooit het bedrag.

Gesprekken komen ook in deze notities terecht, zoals hierboven beschreven onder **Notities uit je gesprekken**.

## Gezondheid

Onder **Gezondheid** houdt je Machine bij wat hij over je gezondheid weet: **Afspraken**, **Testresultaten**, **Artsen en zorg**, **Medicijnen**, **Allergieën en aandoeningen** en **Rekeningen en verzekeringen**. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Een rekening van een arts, tandarts of apotheek krijgt een regel die de bijbehorende to-do opent. Het bedrag blijft daar staan.
- Elke e-mail van je huisartsenpraktijk, een ziekenhuis, laboratorium of zorgverzekeraar krijgt een gedateerde regel met het onderwerp. Zo bouwt je overzicht zich na verloop van tijd op. Tik op een regel om de e-mail te openen.
- Wat je Machine over je gezondheid heeft geleerd, zoals een allergie, krijgt ook een regel. Als je die bewerkt, wordt die ook aangepast onder **Wat ik heb geleerd**.
- Heb je zelf een notitie gemaakt in een onderdeel, bijvoorbeeld voor je fysiotherapeut onder **Afspraken**, dan komt informatie over die zorgverlener in jouw notitie terecht.

Notities onder Gezondheid zijn altijd Persoonlijk, ook als een rekening op je werkadres binnenkwam. Je Machine vraagt de AI één keer voor elke nieuwe rekening en elk nieuw ding dat hij heeft geleerd, om te bepalen of het over je eigen gezondheid gaat.

## Kinderen

Onder **Kinderen** houdt je Machine bij wat hij over je kinderen weet: **School**, **Activiteiten**, **Kinderopvang**, **Artsen en zorg** en **Rekeningen en kosten**. Een oppas of kinderdagverblijf valt onder Kinderopvang, nooit onder Artsen en zorg. Een onderdeel verschijnt zodra het minstens twee regels bevat.

- Wat je Machine over je kind heeft geleerd, zoals de naam van de leerkracht of de zwemdag, krijgt een regel met een link naar de pagina van je kind. Je Machine beschouwt iemand als je kind als bij **Voor jou** bijvoorbeeld dochter of zoon staat.
- Een rekening voor school, een club of kinderopvang krijgt een regel die de bijbehorende to-do opent. Het bedrag blijft daar staan.
- Elke e-mail van de school, een club of de kinderopvang, bijvoorbeeld over een uitje of een wijziging van de plannen, krijgt een gedateerde regel met het onderwerp. Zo staan alle berichten op één plek. Tik op een regel om de e-mail te openen.
- Heb je zelf een notitie voor een van je kinderen gemaakt in een onderdeel, bijvoorbeeld voor Isla onder **School**, dan komt informatie over dat kind in jouw notitie terecht.

Notities onder Kinderen zijn altijd Persoonlijk, ook als de school naar je werkadres mailt. Je Machine vraagt de AI één keer voor elk nieuw gegeven om te bepalen of het over je kinderen gaat.

## Samenvoegen, verwijderen en ongedaan maken

Met **Samenvoegen in…** in het ⋯-menu verplaats je de regels en onderliggende notities naar een andere notitie. Vanaf dat moment voegt je Machine nieuwe informatie aan die notitie toe. Met **Verwijderen** verwijder je een notitie. Beide acties tonen even **Ongedaan maken**. Die optie verschijnt ook wanneer je een regel verwijdert.

## Niet hetzelfde als vergadernotities

Vergadernotities en notities over een persoon of organisatie blijven staan waar ze stonden. De notities hier zijn zelfstandige pagina's.
