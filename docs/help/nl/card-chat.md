---
title: Chat over een to-do
area: cards
summary: Stel vragen over een to-do of pas het concept aan in de chat die bij die to-do hoort.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 18a428fbe38a70e7
---
## Openen

Klik op **Chat** bij de to-do of kies de to-do in de lijst in de zijbalk. Klik of tik op de titel om die aan te passen.

## E-mails in de chat

Elke e-mail toont alleen wat er nieuw in staat. Eerdere berichten die erin worden geciteerd, staan ingeklapt onder **Eerdere berichten**. Met **Lees de thread** open je de volledige e-mails.

## Wat er is gebeurd

Terwijl de chat aan het werk is, staat **Ermee bezig…** boven het berichtvak en zie je typstipjes in de chat. Als de chat de browser gebruikt, zie je ook een kleine afbeelding van de pagina.

Wat er tijdens elke uitvoering gebeurt, staat op één rustige regel met een oplopend aantal, bijvoorbeeld: "12 dingen gecontroleerd". Open de regel om elk soort stap één keer te zien, met het aantal keer dat die is uitgevoerd: "Browser gebruikt op example.com · 7". De regel noemt de website, nooit het adres, een opdracht of een bestand.

Bij Claude Code verschijnen de stappen niet in de chat terwijl die aan het werk is. De meest recente stap staat dan boven de typstipjes, bijvoorbeeld "De e-mail lezen". Boven het berichtvak staat niets.

Als de chat stopt om je iets te vragen, zie je de vraag ook op een rustige regel, bijvoorbeeld "Gevraagd: vandaag versturen of maandag?". Je bericht eronder bevat alleen je antwoord.

## Wat je kunt vragen

Voordat je iets typt, kan de chat maximaal drie suggesties tonen waarop je kunt tikken. Die zijn gebaseerd op de to-do, bijvoorbeeld "Stel dinsdag om 10.00 uur voor". Tik op een suggestie om die in het berichtvak te zetten. Je kunt de tekst vervolgens versturen of aanpassen. Als er geen passende suggesties zijn, verschijnen ze niet.

- Over de thread, de mensen of de achtergrond: "Wat vroegen ze de vorige keer?"
- Om het concept aan te passen: "Maak het korter" of "Vermeld de nieuwe datum".

Een vraag krijgt antwoord, maar verandert het concept niet. Versturen kan alleen met de knoppen van de to-do. De chat verstuurt nooit een concept in hetzelfde antwoord waarin die het heeft opgesteld. Een wijziging die je vraagt en die niemand anders bereikt, zoals een document opschonen, wordt meteen uitgevoerd, zonder extra bevestiging. Voor alles wat verder gaat dan wat je hebt gevraagd, wacht de chat op je akkoord. Een to-do met meerdere stappen blijft open totdat alle stappen zijn afgerond.

Op een computer verstuur je met Enter of Ctrl+Enter (Cmd+Enter op een Mac). Met Shift+Enter begin je een nieuwe regel. Gebruik op een telefoon de verstuurknop.

## Als er iets niet klopt

Laat het weten in de chat, bijvoorbeeld: "Die persoon is niet de CEO" of "Die persoon werkt niet meer bij het bedrijf". The Machine corrigeert de informatie bij de bron: een functie, bedrijf, titel, projectfase, project van de to-do of een regel die hij heeft geleerd. De chat laat zien wat er is gewijzigd, bijvoorbeeld: "Gecorrigeerd: Sams functie is Head of Sales, volgens de e-mailhandtekening", met **Ongedaan maken**. Met Ongedaan maken herstel je de oude waarde, tenzij die inmiddels is gewijzigd.

Andere concepten die op de verkeerde waarde zijn gebaseerd, worden één voor één opnieuw opgesteld. In de chat daarvan staat **Concept opnieuw opstellen na een correctie**. Concepten die je hebt aangepast of goedgekeurd, en concepten die worden verstuurd, blijven ongewijzigd. In het antwoord staat hoeveel er van elk zijn.

Op een GBrain-pagina verandert alleen de eigen sectie van The Machine. Wat je daar hebt geschreven, blijft staan. Als The Machine niet kan achterhalen waar iets vandaan komt, leert hij in plaats daarvan van je notitie.

## Model en denkwerk

Onder het berichtvak zie je het model en het denkwerkniveau van de chat, bijvoorbeeld "GPT-6.2 Sol" en "Weinig denkwerk". Tik op een van beide om alleen voor deze chat iets anders te kiezen. Nieuwe chats gebruiken wat je hebt ingesteld bij **Instellingen**, **Model** (zie [Model](model.md)).

Met **Snel**, onderaan het modelmenu, reageren chats voor to-do's sneller, voor ongeveer twee keer zoveel kosten (of twee keer zoveel van je abonnement). Dit geldt voor de berichten die je verstuurt en **Doe het** in al je chats voor to-do's, niet voor werk op de achtergrond. De optie staat standaard uit en is grijs als het model deze niet ondersteunt.

## Een antwoord stoppen

Terwijl de chat een antwoord schrijft, verandert de verstuurknop in **Stoppen**. Daarmee stop je het antwoord meteen en bewaar je wat er al is geschreven, met de status **Gestopt**. Schrijf een nieuw bericht om verder te gaan of tik op **Opnieuw proberen**.

## Bestanden toevoegen

Tik op de paperclip, plak een schermafbeelding of sleep bestanden naar de chat. Elk bestand verschijnt boven het berichtvak. Met × verwijder je het weer. Je bericht mag alleen uit bestanden bestaan.

- Afbeeldingen (PNG, JPEG, GIF, WebP) van maximaal 5 MB gaan als afbeeldingen naar het model.
- PDF's, tekstbestanden, spreadsheets (CSV) en Office-bestanden van maximaal 10 MB: The Machine leest ze en kan ze aan een concept toevoegen.
- Maximaal 5 bestanden per bericht.

Bestanden blijven op je Machine en worden net als je berichten versleuteld. Bestanden die je toevoegt maar niet verstuurt, worden na een dag verwijderd. Je kunt ook bestanden toevoegen aan een nieuwe to-do via **Nieuwe to-do** (zie [Zelf een to-do maken](cards.md#make-one-yourself)).
