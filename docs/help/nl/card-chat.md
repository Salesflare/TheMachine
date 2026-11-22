---
title: Chat bij een to-do
area: cards
summary: Stel vragen over een to-do of pas het concept aan in een chat die bij die to-do hoort.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 64a15c6ce46c6679
---
## Openen

Tik op je telefoon op de titel van de to-do. Druk op een computer op **Bekijk in chat ›** of op de chatlink van de to-do. Als je op een computer op de titel klikt, krijgt de to-do een andere naam.

## E-mails in de chat

Elke e-mail toont alleen wat er nieuw in is. Eerdere berichten waarnaar de e-mail verwijst, staan ingeklapt onder **Eerdere berichten**. Met **Lees de thread** open je de volledige e-mails.

## Wat hij heeft gedaan

Terwijl The Machine aan je bericht werkt, zie je de laatste stap boven de typstipjes, bijvoorbeeld ‘De e-mail lezen’. Net als bij de to-do zie je dit terwijl hij zich voorbereidt. Als hij de browser gebruikt, zie je ook een kleine afbeelding van de pagina.

Elke afgeronde uitvoering verschijnt als één subtiele regel, bijvoorbeeld ‘12 dingen gecontroleerd’. Open die regel om elke soort stap één keer te zien, met het aantal keer dat die is uitgevoerd: ‘Browser gebruikt op example.com · 7’. Hij noemt de site, nooit het adres, een opdracht of een bestand.

Als hij is gestopt om je iets te vragen, verschijnt de vraag ook als een subtiele regel, bijvoorbeeld ‘Gevraagd: Vandaag versturen of maandag?’. Je bericht eronder bevat alleen je antwoord.

## Wat je kunt vragen

Voordat je iets schrijft, kan de chat maximaal drie suggesties tonen op basis van deze to-do, zoals ‘Stel dinsdag 10:00 voor’. Als je erop tikt, komt de suggestie in het berichtveld te staan. Je kunt die versturen of aanpassen. Als er niets specifieks past, verschijnen er geen suggesties.

- Over de thread, de mensen of de achtergrond: ‘Wat vroegen ze de vorige keer?’
- Om het concept aan te passen: ‘Maak het korter’ of ‘Noem de nieuwe datum’.

Een vraag wordt beantwoord zonder het concept aan te passen. Je verstuurt het concept via de knoppen van de to-do. De chat verstuurt nooit een concept in hetzelfde antwoord waarin hij het heeft geschreven. Een wijziging die je vraagt en die niemand anders bereikt, zoals een opschoning in een document, gebeurt meteen, zonder extra bevestiging. Voor alles wat verder gaat dan wat je hebt gevraagd, wacht hij op je akkoord. Een to-do met meerdere stappen blijft open totdat elke stap is afgerond.

Op een computer verstuur je het bericht met Enter of Ctrl+Enter (Cmd+Enter op een Mac). Met Shift+Enter begin je een nieuwe regel. Gebruik op een telefoon de verstuurknop.

## Als er iets niet klopt

Zeg het in de chat, bijvoorbeeld ‘Ze zijn niet de CEO’ of ‘Ze werken niet meer bij het bedrijf’. The Machine corrigeert het bij de bron: een rol, een bedrijf, een titel, de fase van een project, het project van de to-do of een regel die hij heeft geleerd. In de chat zie je wat er is gewijzigd, bijvoorbeeld ‘Gecorrigeerd: Sams rol is Head of Sales, volgens de e-mailhandtekening’, met **Ongedaan maken**. Met Ongedaan maken wordt de oude waarde teruggezet, tenzij die ondertussen is gewijzigd.

Andere concepten die zijn gebaseerd op de onjuiste waarde, worden één voor één opnieuw opgesteld. In de chat staat **Concept opnieuw maken na een correctie**. Concepten die je hebt bewerkt of goedgekeurd, en concepten die worden verstuurd, blijven zoals ze zijn. In het antwoord staat hoeveel concepten er van elk soort zijn.

Op een GBrain-pagina wordt alleen de eigen sectie van The Machine gewijzigd. Wat je daar hebt geschreven, blijft staan. Als hij niet kan achterhalen waar iets vandaan komt, leert hij in plaats daarvan van je opmerking.

## Model en denkwerk

Onder het berichtveld toont de chat het model en het denkwerkniveau, bijvoorbeeld ‘GPT-6.2 Sol’ en ‘Weinig denkwerk’. Tik op een van beide om voor alleen deze chat iets anders te kiezen. Nieuwe chats gebruiken wat je hebt ingesteld in **Instellingen**, **Model** (zie [Model](model.md)).

Met **Snel**, onderaan het modelmenu, reageren chats voor to-do's sneller. Dat kost ongeveer twee keer zoveel (of twee keer zoveel van je abonnement). Het geldt voor de berichten die je verstuurt en voor Doe het, in al je chats voor to-do's, maar nooit voor werk op de achtergrond. De functie staat standaard uit en is grijs als het model deze niet ondersteunt.

## Een antwoord stoppen

Terwijl een antwoord wordt geschreven, verandert de verstuurknop in **Stoppen**. Stoppen beëindigt het antwoord meteen en bewaart wat hij tot dan toe heeft geschreven, met de status **Gestopt**. Schrijf een nieuw bericht om verder te gaan, of tik op **Opnieuw proberen**.

## Bestanden toevoegen

Tik op de paperclip, plak een screenshot of sleep bestanden naar de chat. Elk bestand verschijnt boven het berichtveld. Met × verwijder je het weer. Een bericht mag alleen uit bestanden bestaan.

- Afbeeldingen (PNG, JPEG, GIF, WebP) van maximaal 5 MB worden als afbeeldingen naar het model gestuurd.
- PDF's, tekstbestanden, spreadsheets (CSV) en Office-bestanden van maximaal 10 MB: The Machine leest ze en kan ze aan een concept toevoegen.
- Maximaal 5 bestanden per bericht.

Bestanden blijven op je Machine staan en zijn versleuteld, net als je berichten. Bestanden die je toevoegt maar nooit verstuurt, worden na een dag verwijderd. Je kunt ook bestanden toevoegen aan een nieuwe to-do, via **Nieuwe to-do** (zie [Zelf een to-do maken](cards.md#make-one-yourself)).
