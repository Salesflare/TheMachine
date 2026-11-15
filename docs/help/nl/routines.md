---
title: Routines
area: cards
summary: Werk dat je Machine zelfstandig en volgens een vast ritme uitvoert, zoals elke maandag een overzicht van je openstaande deals. Hij leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours
translated: 3e6d9d8d446a5dde
---
## Een routine maken

Open **Routines** in de zijbalk en beschrijf in één regel wat de routine moet doen en wanneer: ‘elke maandag om 9 uur een overzicht van mijn openstaande deals’ of ‘elke ochtend op werkdagen een lijst van de mails waarop ik nog moet antwoorden’. Klik daarna op **Toevoegen**.

Als je geen tijd opgeeft, wordt de routine om 8:00 uitgevoerd. De tijd is gebaseerd op de klok van je Machine. De eerste keer dat de routine wordt uitgevoerd, krijgt hij een korte naam.

Met **Toevoegen** wordt eerst een test uitgevoerd, zodat je ziet wat het oplevert voordat je de routine bewaart. Er wordt niets verstuurd of opgeslagen. Daarna zorgt **Toevoegen** ervoor dat de routine volgens het opgegeven ritme blijft lopen. Met **Wijzigen** kun je andere woorden of een nieuwe naam proberen. Met **Annuleren** verwijder je de routine.

## Sjablonen

Onder **Sjablonen** onderaan Routines kun je met **Toevoegen** een kant-en-klare routine inschakelen. Die wordt meteen één keer uitgevoerd en daarna elke ochtend om 7:30 (Spam opruimen elk uur, Tweedehandsvondsten elke 3 uur, Abonnementen en proefperiodes één keer per maand). Op de kaart staan de woorden van de routine, net als bij elke andere routine. Met **Bewerken** kun je de woorden of de naam aanpassen.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen is uitgeschakeld (25 of meer in een week, van minstens 5 afzenders), staat er boven je to-do's hoeveel nieuwsbrieven je hebt ontvangen en wat de routine ermee zou doen. Je ziet ook **Zet het aan** en **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier aangeboden als er in een week minstens 5 mails handmatig naar spam zijn verplaatst. Met **Zet het aan** voeg je de routine toe, net als met **Toevoegen** op deze pagina. Als je **Nee, bedankt** kiest, wordt de routine niet opnieuw aangeboden. Dat geldt ook voor sjablonen die je eerder hebt afgewezen.

Met **Nieuwsbrieven opruimen** maakt de routine één to-do per gebied (werk en privé) met de nieuwsbrieven van de afgelopen dag. Bij elke nieuwsbrief kun je **Houden** of **Afmelden** kiezen. Afmelden gebeurt via de afmeldlink van de mailinglijst, of via een afmeldmail vanaf jouw adres als mail versturen is ingeschakeld. Anders meldt The Machine je af op de pagina van de mailinglijst, in zijn eigen browser. Je moet zelf inloggen, een captcha invullen of keuzes maken op die pagina. In de regel staat waarom, met **Afmeldpagina openen**.

Bonnetjes, bestellingen en betalingsmeldingen worden overgeslagen. Mails die via een groepsadres zijn verstuurd, zoals een Google Group, worden weergegeven onder de naam van de afzender en melden je nooit af van de groep. Als de afzender geen eigen afmeldoptie heeft, staat er **Zelf afmelden** bij de mail.

Met **Spam opruimen** maakt de routine één to-do per gebied met mails van onbekende afzenders die op spam lijken. Bij elke mail kun je **Spam** of **Geen spam** kiezen. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert die als spam. De routine controleert elk uur, dus spam staat meestal al klaar voordat je eraan toekomt. Nieuwe spam wordt toegevoegd aan dezelfde to-do zolang die openstaat.

Gmail dat alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan geen mails naar spam verplaatsen. Daar geeft **Spam** een link om de mail in Gmail te markeren, en onthoudt The Machine de afzender als spam. Als er geen mailaccount is gekoppeld, staat **Mail koppelen** in het sjabloon in plaats van **Toevoegen**.

Een afzender is onbekend als je diegene nooit hebt gemaild. Een ‘Re:’ telt alleen als een gesprek in een thread waarin jij zelf hebt gemaild. Als er opnieuw mail binnenkomt van een afzender die je als spam hebt gemarkeerd, via de to-do of in je mailbox, staat die in de volgende to-do met de melding **Eerder als spam gemarkeerd**. Mails die je zelf naar spam hebt verplaatst, helpen de routine ook om soortgelijke mails te herkennen.

Er verandert niets totdat je dit bevestigt in de to-do. Tik op een afzender om de mail eerst te lezen. De mail blijft ongelezen en er verandert niets. In Spam opruimen worden afbeeldingen van het web niet geladen, zodat de afzender niet kan zien dat de mail is geopend. Er wordt niet opnieuw naar je beslissing over een afzender gevraagd. Als je een dag geen nieuwsbrieven of spam hebt, wordt er geen to-do gemaakt. Deze to-do's sturen nooit een melding.

Zodra je over elke afzender een beslissing hebt genomen, staat er in de to-do dat die is afgerond. Ook staat **Markeer als gedaan** erbij.

Met **Dagelijks overzicht** worden elke dag de paar nieuwsbriefartikelen uitgekozen die je tijd waard zijn. Ze komen samen in één to-do. Bij elk artikel staat in één regel waarom het voor jou relevant is. Tik erop om de mail te lezen of kies **Openen in je mail**. De routine kijkt alleen naar nieuwsbrieven, nooit naar mails van mensen, bonnetjes of afzenders waarop je je hebt afgemeld. Ook mails die je al hebt gelezen worden overgeslagen. Als er niets uitspringt, wordt er geen to-do gemaakt.

De routine leert wat je belangrijk vindt op basis van wat je opent, met een ster markeert of ongelezen archiveert, en van **Meer zoals dit** en **Minder zoals dit** bij elk artikel. De onderwerpen waarop de routine let, staan op de routinekaart onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg er zelf een toe. Onderwerpen met een stippellijn zijn automatisch geleerd. Een nieuw overzicht vervangt het openstaande overzicht. De routine stuurt nooit een melding.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief. Daarna stelt hij je AI er één korte vraag over, met een dagelijkse limiet om de kosten laag te houden. Met **Wanneer wijzigen** stel je de tijd in. Zodra je de woorden van de routine aanpast, werkt die net als elke andere routine op basis van jouw woorden.

Met **Verjaardagen** wordt er een to-do gemaakt voor elk belangrijk contact dat vandaag jarig is: mensen aan wie je zelf schrijft, zoals vrienden, familie en vaste contacten. Bij elke verjaardag staat een korte begroeting als concept, op de plek waar je meestal met die persoon praat, zoals in hun WhatsApp-chat of je e-mailthread, en in hun taal. De begroeting wordt pas verstuurd als je die zelf verstuurt. Op dagen zonder verjaardagen wordt er geen to-do gemaakt.

Verjaardagen komen uit je agenda's (Google-verjaardagsevenementen en de verjaardagsagenda, die elke ochtend wordt gelezen, ook als deze niet is gesynchroniseerd, en de verjaardagsagenda van Outlook), je Google-contacten op een zelfgehoste Machine en een datumveld met de naam Birthday bij een persoon in de Graph. Als er nog nergens een verjaardag staat, meldt het resultaat **Nog geen verjaardagsgegevens** en staat erbij hoe je die kunt toevoegen.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen is ingeschakeld, stelt een to-do voor om de verjaardagenpagina van Facebook te lezen. Tik op **Importeren** en The Machine opent de pagina in zijn browser, scrolt tot alle maanden zijn geladen en leest de naam en verjaardag van elke vriend. Je ziet hoeveel verjaardagen hij heeft gevonden en welke mensen overeenkomen met personen in je Graph op basis van voor- en achternaam. Namen die bij meerdere personen horen, worden overgeslagen en vermeld.

Alleen met **Opslaan** worden de gegevens bewaard op de pagina van elke persoon: de verjaardag en de Facebook-profielfoto van iemand die nog geen foto heeft. Een verjaardag of foto die je daar instelt, blijft staan. Een foto die iemand al heeft, wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

De routine leest de gegevens niet vanzelf opnieuw. Dat gebeurt wel als je **Opnieuw importeren** kiest in de to-do. Je moet in de browser bij Facebook zijn aangemeld. Is dat niet zo, tik dan in de to-do op **Aanmelden bij Facebook** en meld je daar aan. Daarna leest de routine de pagina vanzelf. The Machine meldt je nooit zelf aan.

Vrienden die niemand in je Graph kent, worden geteld en er worden een paar namen getoond. Met **… toevoegen als privécontacten** voeg je ze allemaal tegelijk toe, ook nadat je op Opslaan hebt getikt. Ze worden toegevoegd met hun naam en verjaardag en nooit gedeeld met een Work Fleet. Namen die al voorkomen bij iemand in je Graph, of van iemand die je definitief hebt verwijderd, worden overgeslagen. Je krijgt nog steeds alleen verjaardagsherinneringen voor mensen aan wie je zelf schrijft.

Met **Ongedaan maken** in de to-do verwijder je precies die personen weer, ook nadat je **Opnieuw importeren** hebt gebruikt.

Met **Abonnementen en proefperiodes** leest de routine één keer per maand je bonnetjes, facturen en verlengingsmeldingen. Je abonnementen komen samen in één to-do. Bij elk abonnement staat wat het kost, wanneer de volgende betaling plaatsvindt en of een proefperiode afloopt of de prijs omhooggaat. Alleen abonnementen waarover de routine zeker is, worden vermeld. Als er niets wordt gevonden, wordt er geen to-do gemaakt.

Kies bij elk abonnement **Houden** of **Opzeggen**. Naar een abonnement dat je houdt, wordt niet opnieuw gevraagd, tenzij de prijs verandert. Met **Opzeggen** krijg je de opzegpagina of een concept waarin je vraagt om het abonnement op te zeggen. Dat wordt pas verstuurd als je het zelf verstuurt. Tussen de maandelijkse controles door controleert de routine elke dag of een proefperiode of verlenging binnen 7 dagen wordt afgeschreven. Zo nodig maakt hij een to-do.

Met **Contact houden** krijg je af en toe een herinnering om contact op te nemen met iemand die belangrijk voor je is, maar alleen als daar een goede reden voor is. Op de routinekaart kies je wie erbij hoort uit een korte lijst met mensen met wie je zelf heen en weer schrijft, verspreid over meerdere maanden. Verwijder iemand met ×.

Je krijgt alleen een herinnering als je veel langer dan gewoonlijk geen contact hebt gehad en er iets specifieks is om te zeggen: nieuws dat diegene heeft gedeeld, een belofte die nog openstaat of een bericht waarop je nooit hebt geantwoord. Er wordt één to-do gemaakt met de reden en een kort bericht als concept op de plek waar je meestal praat, in de taal van die persoon. Het bericht wordt pas verstuurd als je het zelf verstuurt. Als er niets te zeggen is, wordt er geen to-do gemaakt.

De routine stuurt maximaal twee herinneringen per week, maximaal één per persoon per maand en geen herinneringen voor iemand met wie je onlangs contact had. Met **Niet nodig** bij een herinnering wacht de routine langer voordat hij die persoon opnieuw voorstelt. Elke keer wordt die wachttijd langer. De routine stuurt nooit een melding en blijft privé: hij wordt nooit gedeeld met een Work Fleet.

Met **Tweedehandsvondsten** houdt de routine een zoekopdracht op een tweedehandssite in de gaten, zoals Marktplaats, Vinted, eBay of Facebook Marketplace. Zoek daar met de gewenste filters, kopieer het adres van de resultaten en plak het na **Toevoegen**. Je kunt desgewenst filters in je eigen woorden toevoegen, zoals ‘onder 300, binnen 30 km, geen “voor onderdelen”’. Elke zoekopdracht is een aparte routine. Voeg de routine dus opnieuw toe voor een volgende zoekopdracht.

Elke 3 uur opent de routine de zoekopdracht in de eigen browser van The Machine en zoekt hij naar advertenties die hij nog niet eerder heeft gezien. Prijs, afstand en woorden die je hebt uitgesloten, worden eerst gecontroleerd met gewone code.

Elke nieuwe advertentie die door de eerste controle komt, wordt geopend. Je AI beoordeelt de staat aan de hand van de foto en beschrijving, en de verkoper aan de hand van recensies, beoordeling en hoe oud het account is. De goede advertenties komen samen in één to-do, elk met een foto, titel, prijs en oordeel van één regel. Tik op een advertentie om die in de browser van The Machine te openen.

Zolang de to-do openstaat, worden nieuwe vondsten bovenaan toegevoegd, loopt het aantal op en krijg je opnieuw een melding, omdat goede deals snel weg zijn. Markeer de to-do als gedaan om met de volgende vondst een nieuwe to-do te beginnen. Als een controle niets goeds oplevert, verandert er niets.

De routine blijft netjes en goedkoop: één keer de zoekopdracht lezen per controle, maximaal 6 advertenties per controle openen met een pauze ertussen en maximaal 40 advertenties per dag controleren voor al je zoekopdrachten samen. Elke controle bestaat uit één korte vraag aan je AI met één foto. De eerste controle bekijkt de nieuwste paar advertenties en markeert de rest als gezien. Bij volgende controles komen dus alleen nieuwe advertenties voorbij.

Als de site je vraagt om in te loggen, een robotcontrole toont of het lezen blokkeert, staat dat in een to-do, met **Openen** om de site te bekijken in de browser van The Machine. Log zelf in of voer daar zelf de controle uit. Bij de volgende controle wordt de pagina opnieuw gelezen. The Machine logt nooit voor je in en lost nooit controles voor je op. Hij neemt nooit contact op met een verkoper, doet geen bod en koopt niets.

Met **Zoekopdracht wijzigen** op de routinekaart kun je een nieuw adres of nieuwe filters opgeven. Met **Wanneer wijzigen** kies je een ander ritme, zoals ‘elke 6 uur’.

Zolang de routine van een sjabloon de woorden van het sjabloon gebruikt, werkt hij met eigen code, zonder je AI-abonnement (Spam opruimen toont eerst nieuwe mails van onbekende afzenders met code en stelt je AI alleen één korte vraag als er mails zijn; Contact houden vraagt alleen naar de één of twee mensen die de routine heeft uitgekozen). Een nieuwe naam verandert daar niets aan. Zodra je de woorden van de routine aanpast, werkt die net als elke andere routine op basis van jouw woorden.

Nieuwsbrieven opruimen en Spam opruimen eindigen nog steeds in dezelfde to-do, met een keuze per mail. Een aangepaste Verjaardagen-routine geeft het resultaat en maximaal één concept, geen to-do per persoon. Met **Terug naar het sjabloon** in **Bewerken** zet je de oorspronkelijke woorden terug.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat hij nodig heeft, zoals je berichten, vergaderingen en de Graph, en zet het resultaat op de pagina Routines. Bij elk resultaat staat **Klaargezet**, **Niets nieuws** (met uitleg) of **Lukte niet** (met uitleg). Een uitvoering die eindigt zonder resultaat, telt als mislukt en nooit als voltooid.

Routines lezen alleen: je berichten, webpagina's, GitHub en websites zoals X in de browser. Ze versturen, beantwoorden of plaatsen niets en veranderen niets. Alleen een sjabloon kan mail aanpassen, en alleen wat je bevestigt in de bijbehorende to-do.

Als een routine eindigt met het plaatsen van een bericht of het versturen van een mail, voert hij alles tot die stap uit en toont hij het concept, zoals **Zou plaatsen op X:**. Na een echte uitvoering krijg je het als to-do om goed te keuren. Bij een test wordt het alleen getoond. De naam vermeldt waar het over gaat en waar het bericht naartoe gaat. De knop vermeldt de stap, zoals **Plaatsen**. Met **Van je routine** eronder open je de routine.

De to-do komt terecht in het gebied van de account van waaruit het bericht wordt verstuurd, zoals Werk voor het X-account van je bedrijf. Je hoeft de to-do dus nooit te verplaatsen.

Een uitvoering kan gebruikmaken van je ingeschakelde [skills](skills.md), gekozen op basis van wat de routine doet. Alleen skills die van toepassing zijn, worden volledig gelezen. De gebruikte skills staan bij **Gebruikt:**. Een skill zorgt er nooit voor dat een routine iets verstuurt of verandert.

Je routines staan onder **Je routines**, onder eventuele suggesties. Een lang resultaat wordt ingeklapt tot een korte voorvertoning. Met **Meer tonen** of door erop te tikken, open je het resultaat.

Bij elke uitvoering wordt het vorige resultaat gebruikt, zodat de routine kan aangeven wat er sindsdien is veranderd.

Na een goede uitvoering kan je Machine zelf een recept schrijven voor leeswerk dat elke keer hetzelfde is, zoals welke mails of GitHub-wijzigingen moeten worden bekeken. Bij volgende uitvoeringen wordt dat eerst met gewone code gelezen. Daarna kiest de AI alleen wat belangrijk is en schrijft hij het resultaat, met minder tokens. Een recept leest alleen. Als het niet meer werkt, leest de routine de gegevens zelf en herstelt hij het recept. Je vindt het onder **Geavanceerd: scriptstappen** in het ⋯-menu.

## Gemiste dagen

Als je Machine uit stond of bezig was, worden gemiste uitvoeringen niet opgestapeld. Alleen de meest recente wordt één keer uitgevoerd. Elke datum wordt één keer uitgevoerd, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als er weinig gebruiksruimte over is in je AI-abonnement, net als al het achtergrondwerk. Met **Nu uitvoeren** start je de routine meteen. Het resultaat verschijnt op de kaart zodra het klaar is.

## Wijzigen of stoppen

Je vindt deze opties in het ⋯-menu van de routine. Met **Bewerken** pas je de naam en de taak aan. Het uitvoermoment en de resultaten tot nu toe blijven behouden. Met **Wanneer wijzigen** geef je in je eigen woorden een nieuw ritme op, zoals ‘elke werkdag om 8 uur’. Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het venster klikken om te annuleren.

Met **Probeer het** in **Bewerken** wordt de nieuwe tekst één keer uitgevoerd en verschijnt het resultaat daar. De routine blijft hetzelfde totdat je op **Opslaan** tikt.

Met **Pauzeren** stop je de uitvoeringen totdat je op de kaart **Hervatten** kiest. Gepauzeerde routines staan onder **Gepauzeerd**, onder je routines. Uitvoeringen die tijdens de pauze zijn gemist, worden daarna niet alsnog uitgevoerd. Met **Stoppen** beëindig je een routine definitief.

Je kunt maximaal 20 routines hebben, inclusief gepauzeerde routines. Stop een routine om er nog een toe te voegen.

Als je bij een to-do van een routine **Wijzigingen vragen** gebruikt of iets in de chat schrijft, en je opmerking bedoeld is voor elke uitvoering, zoals ‘gebruik nooit emoji’, biedt de to-do **Ook de routine aanpassen** aan. Die optie staat op de to-do en in de chat onder het antwoord. Je ziet wat er in de woorden van de routine verandert. De routine wordt pas aangepast als je op **Aanpassen** tikt. Met **Laat zo** blijft alles hetzelfde. Als je alleen het concept wilt aanpassen, wordt deze optie niet aangeboden.

## Geavanceerd: scriptstappen

Je hebt geen script nodig: beschrijf in je eigen woorden wat een routine moet doen en je Machine regelt de rest.

Als je meer ervaring hebt, kun je een routine ook je eigen opdrachten laten uitvoeren op je Machine. Kies daarvoor **Geavanceerd: scriptstappen** in het ⋯-menu. **Bewerken** toont de stappen pas als de routine er een heeft. Met **Gegevens ophalen** voer je eerst een opdracht uit, in de bijbehorende map (of in je thuismap als je geen map opgeeft) en maximaal zo lang als het ingestelde aantal seconden. De uitvoer van de opdracht wordt door de routine gebruikt. Als je geen verdere instructies opgeeft, is de uitvoer het resultaat.

Met **Controle** krijgt de opdracht na de uitvoering het resultaat als invoer. Als de opdracht met een fout stopt, toont de uitvoering **Lukte niet** met de melding van de controle. Een mislukte opdracht voor Gegevens ophalen wordt op dezelfde manier weergegeven.

Een opdracht bestaat uit één regel en wordt zonder shell uitgevoerd: je kunt geen pipes of variabelen gebruiken. Scriptstappen zijn van jou en worden alleen ingesteld op je dashboard. Een testuitvoering en **Probeer het** voeren ook de opdracht voor Gegevens ophalen uit en melden dat. Ze versturen of bewaren nog steeds niets. Een routine verstuurt nooit iets, dus een scriptstap mag alleen lezen.

## Van je OpenClaw-taken

Als je eerder geplande taken in OpenClaw hebt gemaakt, leest je Machine die (hij verandert ze nooit) en biedt hij passende taken aan als routines onder **Voorgesteld**. Elke taak is één keer uitgevoerd, zodat je een echt resultaat ziet.

De routine behoudt je aanpassingen aan de taak en laat weg wat die heeft verstuurd of geplaatst. Als een taak een script uitvoerde of gegevens las die door een scripttaak waren verzameld, neemt de routine die mee als Gegevens ophalen. Met **Toevoegen** maak je er een routine van. Met **Nee, bedankt** wordt die taak niet opnieuw aangeboden. Een taak die je ergens aan herinnerde, wordt op To-do's aangeboden als een terugkerende to-do.

Voordat je een suggestie toevoegt, kun je die in het ⋯-menu aanpassen met **Bewerken** en **Wanneer wijzigen**, net als elke andere routine. Met **Opnieuw uitvoeren** voer je de routine nu uit met de huidige woorden, zodat je recentere resultaten kunt zien, bijvoorbeeld na een rustig weekend. De routine leest alleen, wordt één keer per tik uitgevoerd en vervangt het oude resultaat door het nieuwe.

Er kunnen maximaal drie suggesties tegelijk klaarstaan. Na een week met goede uitvoeringen vraagt de routine **De oude OpenClaw-taak uitzetten?**. De taak wordt alleen uitgezet als je op **Uitzetten** tikt. Je kunt hem weer inschakelen in OpenClaw. Met **Houden** blijven beide actief.

## Op basis van wat je doet

Je Machine merkt ook werk op dat je regelmatig doet en biedt dat aan als routine onder **Voorgesteld**, ook zonder OpenClaw. Hij let op:

- dezelfde vraag drie keer of vaker achter elkaar, zoals ‘geef elke maandag een overzicht van de openstaande supporttickets’;
- een mail die je regelmatig verstuurt, zoals een wekelijks rapport aan je team;
- nieuwsbrieven en updatemails die elke week blijven binnenkomen;
- een druk Slack-kanaal waarin anderen elke week schrijven;
- mails die je één voor één doorstuurt naar dezelfde persoon, zoals school- en clubmails naar je partner. Een wekelijks overzicht voor die persoon bespaart je het doorsturen;
- dezelfde vraag die je regelmatig beantwoordt, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Elke suggestie vermeldt wat de routine heeft opgemerkt, zoals ‘4 keer achter elkaar gevraagd’ of ‘6 mails in 3 weken doorgestuurd naar Sam’. De routine is ook één keer uitgevoerd, zodat je een echt resultaat ziet. Denk bijvoorbeeld aan een teamoverzicht, een briefing voor een wekelijks gesprek, een support- of dev-overzicht, een overzicht van je cijfers of een overzicht van de nieuwsbrieven die je ontvangt.

De routine stelt alleen iets voor als het specifiek voor jou is en duidelijk nuttig is: een nieuwsoverzicht bevat alleen je eigen nieuwsbrieven, nooit algemene nieuwsbrieven. Als niets geschikt is, wordt er geen suggestie gedaan.

De routine controleert dit maximaal één keer per dag en doet maximaal één nieuwe suggestie per week, zonder melding. Met **Nee, bedankt** wordt die suggestie nooit opnieuw getoond. Doorgestuurde mails en antwoorden blijven bij de account van waaruit ze zijn verstuurd, zodat Werk en Privé niet door elkaar lopen. Alles blijft op je Machine. Een to-do die je regelmatig sluit, wordt in plaats daarvan aangeboden als terugkerende to-do.

## Routines en terugkerende to-do's

Een [terugkerende to-do](recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelfstandig uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor ‘de huur betalen op de eerste dag van de maand’ en een routine voor ‘vertel me elke vrijdag welke deals zijn stilgevallen’.
