---
title: Notities
area: graph
summary: Eén overzichtelijke pagina per onderwerp, zoals een reis of je huis, gekoppeld aan de mensen en projecten die erbij horen.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 88cfd4099bf27f38
---
Een notitie is het overzicht van één onderwerp: een reis, je huis of hoe facturen worden afgehandeld. Notities staan in de Graph naast Mensen, Organisaties en Projecten. Ze blijven op je Machine en worden niet met je team gedeeld.

## Een notitie starten

Tik bovenaan Notities op **Nieuwe notitie**. Geef de notitie een titel en tik op **Notitie starten**. De pagina wordt geopend. Met **Regel toevoegen** voeg je iets toe dat je wilt bewaren. Elke tekstregel wordt een eigen regel.

## Koppelen aan mensen, projecten en andere notities

Typ @ en een paar letters van een naam in een regel. Kies een persoon, organisatie, project of notitie uit de lijst. De naam wordt dan als link toegevoegd. Op de pagina van het gekoppelde item staat bij **Gelinkt vanuit** een link naar je notitie.

## Notities onder andere notities

Een notitie kan onder een andere notitie staan, zoals Apparaten onder Thuis. Notities worden als een boomstructuur weergegeven: tik op het pijltje naast een notitie om de notities eronder te openen. Verplaats een notitie met **Bewerken** en kies onder **Onder** waar de notitie moet komen. Met **Nieuwe notitie onder deze** in het ⋯-menu maak je daar meteen een notitie aan.

Bovenaan een notitiepagina zie je waar de notitie staat, zoals **Notities › Kinderen**. Tik op een onderdeel om ernaartoe te gaan. Op een telefoon zijn de notities ertussen samengevouwen in ⋯.

## Notities die je Machine bijhoudt

Je Machine schrijft ook zelf notities op basis van je berichten en houdt die actueel. Bij elke regel staat waar die vandaan komt, bijvoorbeeld wie de e-mail heeft gestuurd. Tik erop om het bericht te openen. Bij een regel uit **Wat ik heb geleerd** staat **Uit wat ik heb geleerd**. Een vergadering of afspraak in je agenda wordt nooit als losse regel toegevoegd: die blijft in [Agenda](calendar.md).

**Thuis**, **Gezondheid** en **Kinderen** worden pas weergegeven zodra je Machine daar minstens twee concrete dingen over te melden heeft, zoals een rekening of iets wat hij heeft geleerd. Tot die tijd staan ze niet in de lijst. Als er later niets meer in staat, verdwijnen ze weer.

Je wijzigingen blijven altijd behouden. Hernoem een notitie, verplaats die, wijzig de datums of pas een regel aan, en je Machine behoudt die wijzigingen wanneer hij de notitie bijwerkt. Verwijder je een regel of notitie, dan komt die niet terug. Latere notities over hetzelfde onderwerp komen terecht op de plek waar je de eerste notitie hebt gezet.

Met **Terug naar het origineel** zie je de eigen woorden van je Machine weer. Als je een regel bewerkt die afkomstig is van wat je Machine heeft geleerd, wordt die ook aangepast onder **Wat ik heb geleerd**. Zo blijft er maar één versie.

## Geschreven pagina's

Zodra een notitie minstens twee regels bevat uit je berichten of uit wat je Machine heeft geleerd, schrijft je Machine bovenaan de pagina. Hij leest de gesprekken zelf, niet alleen de onderwerpen ervan:

- Een korte samenvatting: waar het over gaat en wat de stand van zaken is.
- **Belangrijke feiten**, **Beslissingen**, **Openstaande punten** en een **Tijdlijn**, maar alleen als er iets concreets te melden is.
- De regels van de notitie staan eronder, genummerd onder **Bronnen**. Elke zin eindigt met de nummers van de regels waarop die gebaseerd is. Tik op een nummer om naar die regel te gaan.

De pagina wordt alleen opnieuw geschreven als de regels in de notitie veranderen, en hooguit ongeveer één keer per dag. Als de bronnen niets concreets bevatten, wordt er geen pagina gemaakt en zie je alleen de regels. Verwijder je een regel, dan verdwijnt ook alles op de pagina wat alleen uit die regel afkomstig is. In de lijst Notities staat onder de naam van elke notitie het begin van de samenvatting.

Een project of organisatie heeft al een eigen pagina in de Graph, met bovenaan een beschrijving. Gesprekken daarover komen op die pagina, niet in een notitie.

## Notities uit je gesprekken

Je Machine leest volledige gesprekken en sorteert elk gesprek in de notitie waar het over gaat: een e-mailwisseling uit een van je mailboxen, een chat in WhatsApp, Slack, Telegram, LinkedIn of een andere gekoppelde app, en je vergadernotities. Chatberichten tellen als één gesprek totdat het twee dagen stil is.

- Een gesprek over een project of organisatie in je Graph komt op die pagina, niet in een nieuwe notitie.
- Een gesprek kan terechtkomen in een onderdeel van **Thuis**, **Gezondheid** of **Kinderen**, in een notitie van jezelf of in een notitie die je Machine aanmaakt onder **Werk**, **Auto**, **Belastingen** of een andere map.
- Je Machine maakt alleen een nieuwe notitie aan voor een onderwerp waar minstens twee gesprekken over zijn, of waarover je zelf iets hebt geschreven en dat duidelijk nog speelt.
- Elke regel staat voor één gesprek, met het nieuwste bovenaan. Tik erop om het gesprek te openen.

Je Machine stuurt een kort deel van elk gesprek naar de AI, zonder geciteerde antwoorden of handtekeningen. Elk gesprek wordt één keer verwerkt. Nieuwe berichten worden eraan toegevoegd.

Bulkmail en chats komen nooit in een notitie terecht en worden nooit naar de AI gestuurd: spam, reclame, nieuwsbrieven en andere mailinglijstberichten, meldingen van no-reply-adressen, bots en uitzendkanalen. Een gesprek waaraan je zelf hebt deelgenomen telt wel mee, net als boekingsmails voor **Reizen** en **Gebeurtenissen**.

De eerste keer verwerkt je Machine in een paar uur je e-mails van de afgelopen drie maanden, buiten de nacht en alleen als er ruimte is binnen je AI-abonnement. Daarna sorteert hij nieuwe gesprekken zodra er tien klaarstaan of één gesprek een halve dag heeft gewacht.

## Reizen

Zodra een boeking voor een vlucht, hotel, trein, bus, veerboot of huurauto in je mailbox binnenkomt, voegt je Machine die toe aan een reis onder **Reizen**. Boekingen voor één reis komen samen op één reis: de heenreis, het hotel en de terugreis. Bij elke regel staan de boekingscode, stoel en het ticket. De regels staan op tijd gesorteerd en de reisdatums worden weergegeven. In [Agenda](calendar.md) verschijnt de reis als één balk over die dagen. Tik erop om de reis te openen.

Je Machine leest de boekingsgegevens die luchtvaartmaatschappijen, hotels en boekingssites in hun bevestigingsmails zetten. Een e-mail zonder die gegevens leidt niet tot een reis. Boekingsmails van eerder, binnen het jaar aan [geschiedenis](history.md) dat je Machine bijhoudt, worden op de achtergrond gelezen zodra die geschiedenis is geladen. Eerst worden je Persoonlijke mailboxen verwerkt. Een oudere bevestiging die later wordt gelezen, wordt toegevoegd aan de reis die er al staat.

Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen van een reis zijn geannuleerd, verdwijnt de reis ook.

## Gebeurtenissen

Zodra tickets voor een concert, wedstrijd, festival of conferentie in je mailbox binnenkomen, voegt je Machine de gebeurtenis toe onder **Gebeurtenissen**, met één notitie per gebeurtenis. Op een regel staat waar de gebeurtenis plaatsvindt, met de boekingscode, stoel en het aantal tickets. Een tweede bestelling voor dezelfde gebeurtenis komt op dezelfde notitie. Net als een reis worden de datums van de gebeurtenis weergegeven. In [Agenda](calendar.md) verschijnt die als een balk waarop je kunt tikken om de notitie te openen.

- Bij elke regel staat van wie de tickets komen, zoals **Van Example Tickets**, en je kunt erop tikken om de e-mail te openen.
- Als er een to-do is aangemaakt op basis van de ticketmail, bijvoorbeeld om de tickets te betalen, zie je die met **De to-do openen**.
- Een gebeurtenis die via je werkmailbox is geboekt, is Werk. Anders is die Persoonlijk.

Je Machine leest de ticketgegevens die ticketverkopers in hun bevestigingsmail zetten, zonder AI. Een e-mail zonder die gegevens leidt niet tot een gebeurtenis. Een geannuleerde boeking verdwijnt. Als alle tickets voor een gebeurtenis zijn geannuleerd, verdwijnt de gebeurtenis ook.

## Thuis

Onder **Thuis** houdt je Machine bij wat hij over je huis weet: **Rekeningen en abonnementen**, **Apparaten**, **Reparaties en onderhoud** en **Het huis**. Een onderdeel wordt weergegeven zodra het minstens twee regels bevat.

- Een rekening die regelmatig terugkomt, zoals voor energie of water, krijgt een regel met hoe vaak die komt en de datum van de laatste rekening. Met **De to-do openen** open je de rekening zelf. Het bedrag en de betaalgegevens staan daar.
- Een abonnement dat je behoudt, krijgt een regel waarmee je de to-do **Abonnementen** opent. Een opgezegd abonnement staat er niet bij.
- Wie regelmatig over je huis mailt, zoals je energieleverancier, internetprovider of gemeente, krijgt een regel met hoe vaak die mailt. Tik erop om de nieuwste e-mail te openen.
- Ook wat je Machine over je huis heeft geleerd, zoals het merk van je vaatwasser, krijgt een regel. Als je die bewerkt, wordt die ook aangepast onder **Wat ik heb geleerd**.
- Als je zelf een notitie bijhoudt in een onderdeel, bijvoorbeeld voor je vaatwasser onder **Apparaten**, komt informatie over dat apparaat in jouw notitie terecht. Je Machine maakt zulke notities niet zelf aan.

Alleen Persoonlijke rekeningen, abonnementen en e-mails worden gebruikt. Notities onder Thuis zijn altijd Persoonlijk. Je Machine vraagt zijn AI één keer per nieuwe rekening, nieuw abonnement of nieuw geleerd gegeven om te bepalen of het over je huis gaat. Bij een rekening stuurt hij mee van wie die afkomstig is, nooit het bedrag.

Zoals hierboven beschreven bij **Notities uit je gesprekken**, komen je gesprekken ook in deze notities terecht.

## Gezondheid

Onder **Gezondheid** houdt je Machine bij wat hij over je eigen gezondheid weet: **Afspraken**, **Testresultaten**, **Artsen en zorg**, **Medicijnen**, **Allergieën en aandoeningen** en **Rekeningen en verzekeringen**. Een onderdeel wordt weergegeven zodra het minstens twee regels bevat.

- Een rekening van een arts, tandarts of apotheek krijgt een regel waarmee je de bijbehorende to-do opent. Het bedrag staat daar.
- Elke e-mail van je huisartsenpraktijk, een ziekenhuis, laboratorium of zorgverzekeraar wordt een gedateerde regel met het onderwerp. Zo bouw je in de loop van de tijd een overzicht op. Tik erop om de e-mail te openen.
- Ook wat je Machine over je gezondheid heeft geleerd, zoals een allergie, krijgt een regel. Als je die bewerkt, wordt die ook aangepast onder **Wat ik heb geleerd**.
- In een eigen notitie binnen een onderdeel, bijvoorbeeld voor je fysiotherapeut onder **Afspraken**, komt informatie over die zorgverlener terecht.

Notities onder Gezondheid zijn altijd Persoonlijk, ook als een rekening op je werkadres binnenkomt. Je Machine vraagt zijn AI één keer per nieuwe rekening of nieuw geleerd gegeven om te bepalen of het over je eigen gezondheid gaat.

## Kinderen

Onder **Kinderen** houdt je Machine bij wat hij over je kinderen weet: **School**, **Activiteiten**, **Kinderopvang**, **Artsen en zorg** en **Rekeningen en kosten**. Een oppas of kinderdagverblijf valt onder Kinderopvang, nooit onder Artsen en zorg. Een onderdeel wordt weergegeven zodra het minstens twee regels bevat.

- Wat je Machine over je kind heeft geleerd, zoals de naam van de leerkracht of de zwemdag, krijgt een regel met een link naar de pagina van je kind. Iemand wordt als je kind gezien als bij **Voor jou** bijvoorbeeld dochter of zoon staat.
- Een rekening voor school, een club of kinderopvang krijgt een regel waarmee je de bijbehorende to-do opent. Het bedrag staat daar.
- Elke e-mail van school, een club of de kinderopvang, bijvoorbeeld over een schoolreisje of een wijziging van de plannen, wordt een gedateerde regel met het onderwerp. Zo staat alles wat ze sturen op één plek. Tik erop om de e-mail te openen.
- In een eigen notitie voor een kind binnen een onderdeel, bijvoorbeeld voor Isla onder **School**, komt informatie over dat kind terecht.

Notities onder Kinderen zijn altijd Persoonlijk, ook als school naar je werkadres mailt. Je Machine vraagt zijn AI één keer per nieuw gegeven om te bepalen of het over je kinderen gaat.

## Samenvoegen, verwijderen en ongedaan maken

Met **Samenvoegen in…** in het ⋯-menu verplaats je de regels en onderliggende notities van een notitie naar een andere notitie. Vanaf dat moment voegt je Machine nieuwe informatie aan die notitie toe. Met **Verwijderen** verwijder je een notitie. Bij beide opties kun je even **Ongedaan maken** kiezen. Dat kan ook nadat je een regel hebt verwijderd.

## Niet hetzelfde als vergadernotities

Vergadernotities en notities over een persoon of organisatie blijven staan waar ze stonden. De notities hier zijn zelfstandige pagina's.
