---
title: Chat over een to-do
area: cards
summary: Stel vragen over een to-do of wijzig het concept in een chat die bij die to-do hoort.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 340b9cfc0e3a424d
---
## Openen

Tik op je telefoon op de titel van de to-do. Druk op een computer op **Bekijk in chat ›** of op de chatlink van de to-do. Als je op een computer op de titel klikt, wijzig je de naam van de to-do.

## E-mails in de chat

Elke e-mail toont alleen wat er nieuw in staat. Eerdere berichten die erin worden geciteerd, zijn ingeklapt onder **Eerdere berichten**. Met **Lees de thread** open je de volledige e-mails.

## Wat er is gedaan

Elke uitvoering verschijnt als één subtiele regel, zoals "12 dingen nagekeken". Open de regel om elk soort stap één keer te zien, met het aantal keer dat die is uitgevoerd: "Browser gebruikt op example.com · 7". De regel vermeldt de website, nooit het adres, een opdracht of een bestand.

Als de uitvoering is gestopt om je iets te vragen, verschijnt de vraag ook als een subtiele regel, zoals "Gevraagd: vandaag of maandag versturen?". Je bericht eronder bevat alleen je antwoord.

## Wat je kunt vragen

Voordat je iets schrijft, kan de chat maximaal drie suggesties tonen op basis van deze to-do, zoals "Stel dinsdag om 10:00 voor". Tik op een suggestie om die in het berichtveld te zetten. Je kunt die daarna versturen of aanpassen. Als er geen passende suggesties zijn, worden er geen getoond.

- Over de thread, de mensen of de achtergrond: "Wat vroegen ze de vorige keer?"
- Om het concept aan te passen: "Maak het korter" of "Vermeld de nieuwe datum".

Een vraag wordt beantwoord zonder het concept aan te passen. Je verstuurt het concept via de knoppen van de to-do. De chat verstuurt nooit een concept in hetzelfde antwoord waarin hij het schrijft. Een wijziging die je vraagt en die niemand anders bereikt, zoals een document opruimen, wordt meteen uitgevoerd, zonder extra bevestiging. Voor alles wat je niet hebt gevraagd, wordt eerst op je akkoord gewacht. Een to-do met meer dan één stap blijft open totdat elke stap is afgerond.

Op een computer verstuur je een bericht met Enter of Ctrl+Enter (Cmd+Enter op een Mac). Met Shift+Enter begin je een nieuwe regel. Gebruik op je telefoon de verzendknop.

## Als er iets niet klopt

Zeg dat in de chat, bijvoorbeeld: "Die persoon is niet de CEO" of "Die persoon werkt niet meer bij het bedrijf". The Machine corrigeert de informatie bij de bron: een rol, bedrijf, titel, projectfase, het project van de to-do of een regel die hij heeft geleerd. In de chat zie je wat er is gewijzigd, bijvoorbeeld: "Gecorrigeerd: Sam is Head of Sales, op basis van de e-mailhandtekening", met **Ongedaan maken**. Met Ongedaan maken wordt de oude waarde teruggezet, tenzij die intussen is gewijzigd.

Andere concepten die op de onjuiste waarde zijn gebaseerd, worden één voor één opnieuw opgesteld. In de chat daarvan staat **Concept wordt opnieuw gemaakt na een correctie**. Concepten die je hebt bewerkt of goedgekeurd, en concepten die worden verstuurd, blijven ongewijzigd. In het antwoord staat hoeveel concepten er van elk soort zijn.

Op een GBrain-pagina wordt alleen de eigen sectie van The Machine aangepast. Wat je daar hebt geschreven, blijft staan. Als niet duidelijk is waar iets vandaan komt, gebruikt The Machine je opmerking om ervan te leren.

## Model en denkwerk

Onder het berichtveld zie je welk model en welk niveau van denkwerk de chat gebruikt, bijvoorbeeld "GPT-6.2 Sol" en "Weinig denkwerk". Tik op een van beide om alleen voor deze chat iets anders te kiezen. Nieuwe chats gebruiken wat je hebt ingesteld bij **Instellingen**, **Model** (zie [Model](model.md)).

Met **Snel** onderaan het modelmenu reageren chats over to-do's sneller, tegen ongeveer twee keer de kosten (of twee keer zoveel van je abonnement). Dit geldt voor de berichten die je verstuurt en voor **Doe het**, in al je chats over to-do's. Achtergrondwerk valt er niet onder. Deze optie staat standaard uit en is grijs weergegeven voor modellen die deze optie niet ondersteunen.

## Een antwoord stoppen

Terwijl een antwoord wordt geschreven, verandert de verzendknop in **Stoppen**. Hiermee stop je het antwoord meteen en bewaar je wat er al is geschreven, met de status **Gestopt**. Schrijf een nieuw bericht om verder te gaan of tik op **Opnieuw proberen**.

## Bestanden toevoegen

Tik op de paperclip, plak een screenshot of sleep bestanden naar de chat. Elk bestand verschijnt boven het berichtveld. Tik op × om het weer te verwijderen. Een bericht mag alleen uit bestanden bestaan.

- Afbeeldingen (PNG, JPEG, GIF, WebP) van maximaal 5 MB worden als afbeeldingen naar het model gestuurd.
- Pdf's, tekstbestanden, spreadsheets (CSV) en Office-bestanden van maximaal 10 MB: The Machine leest ze en kan ze aan een concept toevoegen.
- Maximaal 5 bestanden per bericht.

Bestanden blijven op je Machine en worden net als je berichten versleuteld. Bestanden die je toevoegt maar nooit verstuurt, worden na een dag verwijderd. Je kunt ook bestanden toevoegen aan een nieuwe to-do via **Nieuwe to-do** (zie [Zelf een to-do maken](cards.md#make-one-yourself)).
