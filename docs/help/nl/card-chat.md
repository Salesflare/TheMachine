---
title: To-dochat
area: cards
summary: Stel vragen over een to-do of pas het concept aan in een chat die bij die to-do hoort.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 224f6163a84e80ca
---
## Openen

Druk op **Chat** bij de to-do of kies de to-do in de lijst in de zijbalk. Tik of klik op de titel om die aan te passen.

## E-mails in de chat

Elke e-mail toont alleen wat er nieuw in is. Eerdere berichten die erin worden geciteerd, zijn ingeklapt onder **Eerdere berichten**. Met **Lees de thread** open je de e-mails volledig.

## Wat hij heeft gedaan

Terwijl hij aan je bericht werkt, zie je de laatste stap boven de typstipjes, bijvoorbeeld ‘De mail lezen’. Dat zie je ook bij de to-do terwijl hij zich voorbereidt. Als hij de browser gebruikt, zie je ook een kleine afbeelding van de pagina.

Elke afgeronde uitvoering wordt weergegeven als één subtiele regel, bijvoorbeeld ‘12 dingen gecontroleerd’. Open de regel om elke soort stap één keer te zien, met het aantal keer: ‘Browser gebruikt op example.com · 7’. Hij toont de naam van de site, nooit het adres, een opdracht of een bestand.

Als hij is gestopt om je iets te vragen, wordt de vraag ook als subtiele regel getoond, bijvoorbeeld ‘Gevraagd: vandaag of maandag versturen?’. Je bericht eronder toont alleen je antwoord.

## Wat je kunt vragen

Voordat je iets typt, kan de chat maximaal drie suggesties doen op basis van deze to-do, zoals ‘Stel dinsdag om 10.00 uur voor’. Als je op een suggestie tikt, komt die in het berichtvak te staan. Je kunt hem versturen of aanpassen. Als geen enkele suggestie past, worden er geen getoond.

- Over de thread, de mensen of de achtergrond: ‘Wat vroegen ze de vorige keer?’
- Om het concept aan te passen: ‘Maak het korter’ of ‘Noem de nieuwe datum’.

Een vraag wordt beantwoord zonder het concept aan te passen. Je kunt alleen versturen via de knoppen van de to-do. De chat verstuurt nooit een concept in hetzelfde antwoord waarin hij het heeft geschreven. Een wijziging die je vraagt en die niemand anders bereikt, zoals een document opschonen, wordt meteen uitgevoerd, zonder extra bevestiging. Voor alles wat verder gaat dan je vraag, wacht hij op je akkoord. Een to-do met meerdere stappen blijft open totdat elke stap is afgerond.

Op een computer verstuur je met Enter of Ctrl+Enter (Cmd+Enter op een Mac). Met Shift+Enter begin je een nieuwe regel. Gebruik op een telefoon de verzendknop.

## Als er iets niet klopt

Zeg het in de chat, bijvoorbeeld ‘Die persoon is niet de CEO’ of ‘Die persoon werkt niet meer bij het bedrijf’. The Machine herstelt de informatie bij de bron: een rol, bedrijf, titel, fase van een project, project van de to-do of aangeleerde regel. De chat toont wat er is gewijzigd, bijvoorbeeld ‘Gecorrigeerd: Sams rol is Head of Sales, volgens de e-mailhandtekening’, met **Ongedaan maken**. Met Ongedaan maken wordt de oude waarde teruggezet, tenzij die intussen is gewijzigd.

Je andere concepten die op de verkeerde waarde waren gebaseerd, worden opnieuw opgesteld, één voor één. In de chat staat **Concept opnieuw maken na een correctie**. Concepten die je hebt aangepast of goedgekeurd, en concepten die worden verstuurd, blijven ongewijzigd. In het antwoord staat hoeveel er van elk zijn.

Op een GBrain-pagina wordt alleen de eigen sectie van The Machine gewijzigd. Wat je daar zelf hebt geschreven, blijft staan. Als hij niet kan achterhalen waar iets vandaan komt, leert hij in plaats daarvan van je notitie.

## Model en denkwerk

Onder het berichtvak toont de chat het model en het denkwerkniveau, bijvoorbeeld ‘GPT-6.2 Sol’ en ‘Weinig denkwerk’. Tik op een van beide om die alleen voor deze chat aan te passen. Nieuwe chats gebruiken de instellingen die je hebt gekozen bij **Instellingen**, **Model** (zie [Model](model.md)).

Met **Snel**, onderaan het modelmenu, reageren to-dochats sneller. Dat kost ongeveer twee keer zoveel (of gebruikt twee keer zoveel van je abonnement). Dit geldt voor de berichten die je verstuurt en voor Doe het, in al je to-dochats. Achtergrondwerk valt er niet onder. Deze optie staat standaard uit en is grijs als het model die niet ondersteunt.

## Een antwoord stoppen

Terwijl een antwoord wordt geschreven, verandert de verzendknop in **Stoppen**. Daarmee stop je het meteen en bewaar je wat er tot dan toe is geschreven, met de markering **Gestopt**. Schrijf een nieuw bericht om verder te gaan of tik op **Opnieuw proberen**.

## Bestanden toevoegen

Tik op de paperclip, plak een screenshot of sleep bestanden naar de chat. Elk bestand wordt boven het berichtvak getoond. Met × verwijder je het weer. Een bericht mag alleen uit bestanden bestaan.

- Afbeeldingen (PNG, JPEG, GIF, WebP) van maximaal 5 MB worden als afbeeldingen naar het model gestuurd.
- PDF-, tekst-, spreadsheet- (CSV-) en Office-bestanden van maximaal 10 MB: The Machine leest ze en kan ze aan een concept toevoegen.
- Maximaal 5 bestanden per bericht.

Bestanden blijven op je Machine en worden net als je berichten versleuteld. Bestanden die je toevoegt maar nooit verstuurt, worden na een dag verwijderd. Je kunt ook bestanden toevoegen aan een nieuwe to-do via **Nieuwe to-do** (zie [Zelf een to-do maken](cards.md#make-one-yourself)).
