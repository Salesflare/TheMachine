---
title: Routines
area: cards
summary: Werk dat je Machine zelfstandig en volgens een vast ritme doet, zoals elke maandag een overzicht van je openstaande deals. Hij leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 3b0405616881de74
---
## Een routine maken

Open **Routines** in de zijbalk en beschrijf in één regel wat de routine moet doen en wanneer: "elke maandag om 9 uur, geef me een overzicht van mijn openstaande deals" of "elke werkdag ’s ochtends, geef me een lijst met mails waarop ik nog moet antwoorden". Klik daarna op **Toevoegen**.

Als je geen tijd opgeeft, wordt de routine om 8:00 uitgevoerd. De tijd is die van je Machine. De eerste keer dat de routine wordt uitgevoerd, krijgt hij een korte naam.

Met **Toevoegen** wordt eerst een testrun uitgevoerd. Zo zie je wat de routine oplevert voordat je hem bewaart. Er wordt niets verstuurd of opgeslagen. Met **Toevoegen** laat je de routine daarna volgens het vaste ritme lopen. Met **Wijzigen** probeer je andere woorden of een nieuwe naam. Met **Annuleren** verwijder je de routine.

## Sjablonen

Onder **Sjablonen** onderaan Routines zet **Toevoegen** een kant-en-klare routine aan. Die wordt meteen één keer uitgevoerd en daarna elke ochtend om 7:30 (Spam opruimen elk uur, Tweedehandsvondsten elke 3 uur, Abonnementen en proefperiodes één keer per maand). Op de kaart staan de woorden van de routine, net als bij elke andere routine. Met **Bewerken** wijzig je de woorden of de naam.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen uitstaat (25 of meer in een week, van minstens 5 afzenders), verschijnt er boven je to-do's een regel met het aantal nieuwsbrieven en wat de routine ermee zou doen, met **Aanzetten** en **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier voorgesteld als je in een week 5 of meer mails handmatig naar spam hebt verplaatst. Met **Aanzetten** voeg je de routine toe, net als met **Toevoegen** hier. Met **Nee, bedankt** zorg je ervoor dat de routine niet opnieuw wordt voorgesteld. Een sjabloon dat je eerder hebt afgewezen, wordt nooit opnieuw voorgesteld.

Met **Nieuwsbrieven opruimen** maakt de routine één to-do per gebied (werk en privé) met de nieuwsbrieven van de afgelopen dag. Je kunt per nieuwsbrief kiezen voor **Houden** of **Afmelden**. Afmelden gebruikt de eenkliklink van de mailinglijst, of stuurt vanaf jouw adres een afmeldmail als versturen is ingeschakeld. Anders meldt The Machine je af via de pagina van de mailinglijst in zijn eigen browser. Een login, captcha of keuzes op die pagina moet je zelf regelen. In de rij staat waarom, met **Afmeldpagina openen**.

Wil je geen to-do's van een mailinglijst, maar wel de mails blijven ontvangen? Zeg dan in de chat van een mail van die lijst: "Voor deze lijst hoef ik geen to-do's".

Ontvangstbewijzen, bestellingen en betalingsmeldingen worden overgeslagen. Mails die via een groepsadres zijn verstuurd, zoals een Google Group, worden getoond onder de naam van de afzender en melden je nooit af voor de groep. Als de afzender zelf geen afmeldoptie heeft, staat er **Zelf afmelden** in de rij.

Met **Spam opruimen** maakt de routine één to-do per gebied met mails van onbekende afzenders die op spam lijken. Je kunt per mail kiezen voor **Spam** of **Geen spam**. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert de mail als spam. De routine controleert elk uur, dus spam staat meestal al klaar voordat je eraan toekomt. Nieuwe spam wordt toegevoegd aan dezelfde to-do zolang die openstaat.

Gmail dat alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan geen mail naar spam verplaatsen. In dat geval geeft **Spam** een link waarmee je de mail in Gmail kunt markeren. The Machine onthoudt de afzender dan als spam. Als er geen mailaccount is gekoppeld, staat **Mail koppelen** op de plek van **Toevoegen** in het sjabloon.

Onbekend betekent dat je de afzender nooit zelf hebt gemaild. Een "Re:" telt alleen als gesprek in een thread waarin je zelf hebt geschreven. Als er opnieuw mail binnenkomt van een afzender die je als spam hebt gemarkeerd, via de to-do of in je mailbox, staat die in de volgende to-do als **Eerder als spam gemarkeerd**. Wat je zelf naar spam hebt verplaatst, helpt de routine ook om vergelijkbare mails te herkennen.

Er verandert niets totdat je dit bevestigt in de to-do. Tik op een afzender om de mail eerst te lezen. De mail blijft ongelezen en er verandert niets. Bij Spam opruimen worden afbeeldingen van internet niet geladen, zodat de afzender niet kan zien dat je de mail hebt geopend. Je krijgt geen nieuwe vraag over afzenders waarover je al een keuze hebt gemaakt. Op een dag zonder nieuwsbrieven of spam wordt er geen to-do gemaakt. Deze to-do's sturen nooit een melding.

Zodra je voor elke afzender een keuze hebt gemaakt, meldt de to-do dat hij klaar is en staat **Als gedaan markeren** erbij.

Met **Dagelijks overzicht** selecteert de routine één keer per dag de interessante artikelen uit je nieuwsbrieven en zet die in één to-do. Bij elk artikel staat in één regel waarom het voor jou relevant is. Tik erop om de mail te lezen of gebruik **Openen in je mail**. De routine kijkt alleen naar nieuwsbrieven, nooit naar mails van mensen, ontvangstbewijzen of afzenders waarvoor je je hebt afgemeld. Ook mails die je al hebt gelezen worden overgeslagen. Als niets eruit springt, wordt er geen to-do gemaakt.

De routine leert waar je interesse in hebt op basis van wat je opent, een ster geeft of ongelezen archiveert, en van **Meer zoals dit** en **Minder zoals dit** bij elk artikel. De onderwerpen waarop de routine let, staan op de routinekaart onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg zelf een onderwerp toe. Gestreepte onderwerpen heeft de routine zelf ontdekt. Een nieuw overzicht vervangt het vorige zolang dat nog openstaat. De routine stuurt nooit een melding.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief. Daarna stelt hij je AI één korte vraag over de nieuwsbrief, met een dagelijkse limiet om de kosten laag te houden. Met **Wanneer wijzigen** stel je het tijdstip in. Zodra je de tekst van de routine wijzigt, wordt hij uitgevoerd zoals elke andere routine op basis van jouw tekst.

Met **Verjaardagen** maakt de routine een to-do voor elke goede bekende die vandaag jarig is: mensen aan wie je zelf schrijft, zoals vrienden, familie en vaste contacten. Bij elke persoon staat een korte felicitatie die is opgesteld op de plek waar je meestal met die persoon praat, zoals de WhatsApp-chat of je mailthread, en in diens taal. De felicitatie wordt pas verstuurd als jij dat doet. Op een dag zonder verjaardagen wordt er geen to-do gemaakt.

Verjaardagen komen uit je agenda's (de verjaardagsevenementen en verjaardagsagenda van Google, die elke ochtend worden gelezen, ook als ze niet zijn gesynchroniseerd, en de verjaardagsagenda van Outlook), je Google-contacten op een zelf gehoste Machine en een datumveld met de naam Birthday bij een persoon in de Graph. Als er nog nergens een verjaardag staat, geeft het resultaat **Nog geen verjaardagsgegevens** en wordt uitgelegd hoe je die kunt toevoegen.

Met **Verjaardagen importeren uit Facebook** biedt een to-do aan om de verjaardagenpagina van Facebook te lezen zodra Verjaardagen aanstaat. Tik op **Importeren**. The Machine opent de pagina in zijn browser, scrolt tot alle maanden zijn geladen en leest de naam en verjaardag van elke vriend uit. Je ziet hoeveel verjaardagen zijn gevonden en wie overeenkomt met personen in je Graph op basis van voor- en achternaam. Namen die bij meer dan één persoon horen, worden overgeslagen en vermeld.

Alleen met **Opslaan** worden de gegevens bewaard op de pagina van elke persoon: de verjaardag en de Facebook-profielfoto van iemand die nog geen foto heeft. Een verjaardag of foto die je daar zelf hebt ingesteld, blijft staan. Een foto die iemand al heeft, wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

De routine leest de pagina niet vanzelf opnieuw. Daarvoor gebruik je **Opnieuw importeren** op de to-do. In de browser moet je bij Facebook zijn ingelogd. Is dat niet zo, tik dan op **Inloggen bij Facebook** op de to-do en log daar in. Zodra je bent ingelogd, leest de routine de pagina vanzelf. The Machine logt nooit voor je in.

Vrienden die niemand in je Graph kent, worden geteld en er worden een paar namen getoond. Met **Voeg … toe als persoonlijke contacten** voeg je ze allemaal tegelijk toe, ook na **Opslaan**. Elk contact krijgt een naam en verjaardag en wordt nooit gedeeld met een Werk-Fleet. Namen die al bij iemand in je Graph horen of eerder bij iemand hoorden die je definitief hebt verwijderd, worden overgeslagen. Herinneringen voor verjaardagen krijg je nog steeds alleen voor mensen aan wie je zelf schrijft.

Met **Ongedaan maken** op de to-do verwijder je precies die personen weer, ook nadat je **Opnieuw importeren** hebt gebruikt.

**Abonnementen en proefperiodes** leest één keer per maand je ontvangstbewijzen, facturen en verlengingsberichten. De routine zet je abonnementen in één to-do, met de kosten, de volgende afschrijfdatum en een waarschuwing als een proefperiode afloopt of de prijs stijgt. Alleen abonnementen waar de routine zeker van is, worden getoond. Als er niets wordt gevonden, wordt er geen to-do gemaakt.

Kies **Houden** of **Opzeggen** voor elk abonnement. Over een abonnement dat je wilt houden, krijg je geen nieuwe vraag, tenzij de prijs verandert. Met **Opzeggen** krijg je de opzegpagina of een conceptbericht waarin je om opzegging vraagt. Het bericht wordt pas verstuurd als jij dat doet. Tussen de maandelijkse controles door kijkt de routine elke dag of een proefperiode of verlenging binnen 7 dagen kosten met zich meebrengt. Zo ja, dan maakt hij een to-do.

**Contact houden** herinnert je af en toe eraan om contact op te nemen met iemand die je goed kent, maar alleen als daar een goede reden voor is. Kies op de kaart uit een korte lijst met mensen met wie je al maandenlang over en weer zelf schrijft. Verwijder iemand met ×.

Je krijgt alleen een herinnering als je veel langer dan gewoonlijk geen contact hebt gehad en er iets specifieks is om over te praten: nieuws dat die persoon heeft gedeeld, een belofte die nog openstaat of een bericht waarop je nooit hebt geantwoord. Er wordt één to-do gemaakt met de reden en een kort bericht in de taal van die persoon, opgesteld op de plek waar je meestal met die persoon praat. Het bericht wordt pas verstuurd als jij dat doet. Als er niets is om te zeggen, wordt er geen to-do gemaakt.

De routine stuurt hoogstens twee herinneringen per week en één per persoon per maand. Iemand met wie je onlangs contact hebt gehad, krijgt er geen. Met **Niet nodig** bij een herinnering wacht de routine langer voordat je opnieuw een herinnering over die persoon krijgt. Elke keer wordt die wachttijd langer. De routine stuurt nooit een melding en blijft privé. Hij wordt nooit gedeeld met een Werk-Fleet.

**Tweedehandsvondsten** houdt een zoekopdracht op een tweedehandssite in de gaten, zoals Marktplaats, Vinted, eBay of Facebook Marketplace. Zoek daar met de gewenste filters, kopieer het adres van de zoekresultaten en plak het na **Toevoegen**. Je kunt zelf filters in gewone woorden toevoegen, zoals "onder 300, binnen 30 km, geen 'voor onderdelen'". Elke zoekopdracht is een eigen routine. Voeg dus opnieuw een routine toe voor de volgende zoekopdracht.

Elke 3 uur opent de routine de zoekopdracht in de eigen browser van The Machine en zoekt hij naar advertenties die hij nog niet eerder heeft gezien. De prijs, afstand en woorden die je hebt uitgesloten, worden eerst gecontroleerd met eenvoudige code.

Elke nieuwe advertentie die aan je criteria voldoet, wordt geopend. Je AI beoordeelt de staat op basis van de foto en beschrijving, en de verkoper op basis van recensies, beoordeling en accountleeftijd. De goede advertenties komen in één to-do, elk met een foto, titel, prijs en oordeel van één regel. Tik op een advertentie om die in de browser van The Machine te openen.

Zolang de to-do openstaat, worden nieuwe vondsten eraan toegevoegd. Het aantal loopt op en je krijgt opnieuw een melding, want goede deals zijn snel weg. Markeer de to-do als gedaan en de volgende vondst komt in een nieuwe to-do. Een run zonder goede vondsten verandert niets.

De routine gaat zorgvuldig en zuinig te werk: hij leest de zoekopdracht één keer per run, opent hoogstens 6 advertenties per run met een pauze ertussen en controleert per dag hoogstens 40 advertenties voor al je zoekopdrachten. Elke controle bestaat uit één korte vraag aan je AI met één foto. Tijdens de eerste run controleert de routine de nieuwste advertenties en markeert hij de rest als gezien. Latere runs tonen dus alleen nieuwe advertenties.

Als de site vraagt om in te loggen, een robotcontrole toont of het lezen tegenhoudt, meldt een to-do dat. Met **Openen** kun je de pagina in de browser van The Machine bekijken. Log zelf in of voltooi daar de controle. Bij de volgende run probeert de routine de pagina opnieuw te lezen. The Machine logt nooit voor je in, lost nooit een controle voor je op en neemt nooit contact op met een verkoper. Hij biedt nergens op en koopt niets.

Met **Zoekopdracht wijzigen** op de routinekaart stel je een nieuw adres of andere filters in. Met **Wanneer wijzigen** stel je een ander ritme in, zoals "elke 6 uur".

**Nabestellingen** leest bevestigingen van online bestellingen in je mail en merkt op welke producten je steeds opnieuw koopt, zoals koffie, dierenvoer of vitamines. Wanneer een product waarschijnlijk bijna op is, maakt de routine een to-do met het product, de winkel, de laatste prijs en de datum van je laatste aankoop. Met **Openen in de winkel** ga je naar de productpagina om het zelf te kopen. Er wordt niets voor je gekocht.

Er zijn minstens drie bestellingen van hetzelfde product met een regelmatig interval nodig. Een eenmalige aankoop of een afwijkend interval levert dus geen to-do op. Voorlopig leest de routine bestellingen bij winkels die op Shopify draaien. Je AI leest per run alleen nieuwe bestelbevestigingen van die winkels, met één korte vraag. Deze to-do's sturen nooit een melding. Als je het product opnieuw bestelt, wordt de openstaande to-do gesloten.

Zolang de routine van een sjabloon de tekst van het sjabloon gebruikt, wordt hij uitgevoerd met eigen code, zonder je AI-abonnement. Spam opruimen toont bijvoorbeeld eerst nieuwe mails van onbekende afzenders met code en stelt je AI pas één korte vraag als er mails zijn. Contact houden vraagt alleen naar de een of twee personen die de routine heeft geselecteerd. Als je de tekst van de routine wijzigt, wordt hij uitgevoerd zoals elke andere routine op basis van jouw tekst.

Nieuwsbrieven opruimen en Spam opruimen leveren nog steeds dezelfde to-do op, met een keuze voor elke mail. Een aangepaste routine voor Verjaardagen geeft het resultaat en hoogstens één concept, geen aparte to-do per persoon. Met **Terug naar het sjabloon** in **Bewerken** zet je de oorspronkelijke tekst terug.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat nodig is, zoals je berichten, meetings en de Graph, en zet hij het resultaat op de pagina Routines. Elk resultaat krijgt de status **Klaargezet**, **Niets nieuws** (met uitleg) of **Lukte niet** (met uitleg). Een run die zonder resultaat eindigt, geldt als mislukt en nooit als voltooid.

Routines lezen alleen: je berichten, webpagina's, GitHub en sites zoals X in de browser. Ze versturen niets, beantwoorden niets, plaatsen niets en veranderen niets. Ze openen pagina's die ze vinden in wat ze lezen of in een zoekopdracht, gewone webadressen en bekende sites. Ze openen nooit een adres dat speciaal is gemaakt om de inhoud die ze hebben gelezen mee te sturen. Alleen een sjabloon verandert mail, en dan alleen wat je bevestigt in de to-do.

Als het werk van een routine eindigt met een bericht of post, doet hij alles tot aan die stap en toont hij het concept, bijvoorbeeld **Zou op X plaatsen:**. Na een echte run krijg je het als to-do om goed te keuren. Bij een testrun wordt het alleen getoond.

De naam beschrijft waar de routine over gaat en waar het resultaat terechtkomt. Met **Van je routine** eronder open je de routine. De knop beschrijft de stap, zoals **Bericht voorbereiden**. Daarmee wordt het bericht klaargezet, maar niet geplaatst. Je plaatst het zelf vanuit het resultaat. Als The Machine het niet voor je kan plaatsen, opent de knop daar de pagina waarop je dat kunt doen.

De to-do komt in het gebied van het account waarmee hij wordt verstuurd. Zo komt een post voor het X-account van je bedrijf bijvoorbeeld bij Werk terecht. Je hoeft hem dus nooit naar een ander gebied te verplaatsen.

Een run kan de ingeschakelde [skills](skills.md) volgen die passen bij wat de routine doet. Alleen de skills die van toepassing zijn, worden helemaal gelezen. Het resultaat noemt ze onder **Gebruikt:**. Een skill laat een routine nooit iets versturen of veranderen.

Je routines staan onder **Je routines**, onder eventuele suggesties. Een lang resultaat wordt ingeklapt tot een korte voorvertoning. Met **Meer tonen** of door erop te tikken, open je het resultaat.

Elke run kent het vorige resultaat en kan dus vertellen wat er sindsdien is veranderd.

Na een geslaagde run kan je Machine zelf een recept maken voor leeswerk dat elke keer hetzelfde is, zoals welke mails of GitHub-wijzigingen hij moet bekijken. Bij volgende runs gebruikt hij eerst dat recept, in eenvoudige code. De AI selecteert alleen wat belangrijk is en schrijft het resultaat. Zo zijn er minder tokens nodig. Een recept leest alleen. Als het niet meer werkt, leest de run vanzelf verder en herstelt hij het recept. Je vindt het recept onder **Geavanceerd: scriptstappen** in het ⋯-menu.

## Gemiste dagen

Als je Machine uitstaat of bezig is, worden gemiste runs niet opgestapeld. Alleen de nieuwste run wordt één keer uitgevoerd. Elke datum wordt één keer uitgevoerd, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als je AI-abonnement weinig gebruiksruimte heeft, net als ander achtergrondwerk. Met **Nu uitvoeren** start je de routine meteen. Het resultaat verschijnt op de kaart zodra het klaar is.

## Een routine wijzigen of stoppen

Deze opties vind je in het ⋯-menu van de routine. Met **Bewerken** wijzig je de naam en wat de routine doet. Het ritme en de resultaten tot nu toe blijven hetzelfde. Met **Wanneer wijzigen** stel je in je eigen woorden een nieuw ritme in, zoals "elke werkdag om 8 uur". Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het venster klikken om te annuleren.

Met **Probeer het** in **Bewerken** voer je de nieuwe tekst één keer uit en zie je daar het resultaat. De routine blijft ongewijzigd totdat je op **Opslaan** klikt.

Met **Pauzeren** stop je de runs totdat je op de kaart op **Hervatten** klikt. Gepauzeerde routines staan onder **Gepauzeerd**, onder je routines. Runs die tijdens de pauze zijn gemist, worden daarna niet alsnog uitgevoerd. Met **Stoppen** beëindig je een routine voorgoed.

Je kunt maximaal 20 routines hebben, inclusief gepauzeerde routines. Stop een routine om er een toe te voegen.

Als je bij de to-do van een routine **Wijzigingen vragen** gebruikt of iets in de chat schrijft dat voor elke run moet gelden, zoals "gebruik nooit emoji's", biedt de to-do **Ook de routine aanpassen** aan. Die optie staat op de to-do en in de chat onder het antwoord. Je ziet wat er in de tekst van de routine verandert. De routine wordt pas aangepast als je op **Aanpassen** tikt. Met **Zo laten** blijft de routine hetzelfde. Als je alleen dat concept wilt aanpassen, wordt deze optie niet aangeboden.

## Geavanceerd: scriptstappen

Je hebt geen script nodig. Beschrijf in je eigen woorden wat een routine moet doen en je Machine bedenkt de rest.

Voor gevorderde gebruikers kan een routine ook eigen opdrachten op je Machine uitvoeren. Kies daarvoor **Geavanceerd: scriptstappen** in het ⋯-menu. **Bewerken** toont de scriptstappen alleen als de routine er al heeft. Met **Gegevens ophalen** wordt eerst een opdracht uitgevoerd, in de bijbehorende map (of je thuismap als er geen map is opgegeven) en maximaal het opgegeven aantal seconden. De uitvoer wordt aan de run gegeven om mee te werken. Als er geen verdere instructies zijn, is de uitvoer het resultaat.

Met **Controle** krijgt de opdracht na de run het resultaat als invoer. Als de opdracht eindigt met een fout, toont de run **Lukte niet** met de melding van de controle. Als een opdracht voor Gegevens ophalen mislukt, wordt dat op dezelfde manier getoond.

Een opdracht bestaat uit één regel en wordt zonder shell uitgevoerd. Pijplijnen en variabelen zijn dus niet mogelijk. Jij beheert de scriptstappen en stelt ze alleen in op je dashboard. Een testrun en een run met **Probeer het** voeren ook Gegevens ophalen uit en laten dat weten. Ze versturen en bewaren nog steeds niets. Een routine verstuurt nooit iets, dus een scriptstap mag alleen lezen.

## Vanuit je OpenClaw-taken

Als je eerder geplande taken in OpenClaw hebt gemaakt, leest je Machine die in (hij verandert ze nooit) en stelt hij taken die geschikt zijn als routines voor onder **Voorgesteld**. Elke taak is één keer uitgevoerd, dus je ziet een echt resultaat.

Je aanpassingen aan de taak blijven behouden, maar wat de taak heeft verstuurd of geplaatst wordt weggelaten. Als de taak een script uitvoerde of las wat een scripttaak had verzameld, wordt dat meegenomen als Gegevens ophalen. Met **Toevoegen** maak je er een routine van. Met **Nee, bedankt** wordt er nooit meer naar die taak gevraagd. Een taak die je ergens aan herinnerde, wordt in To-do's aangeboden als terugkerende to-do.

Voordat je een suggestie toevoegt, kun je die via **Bewerken** en **Wanneer wijzigen** in het ⋯-menu aanpassen, net als elke andere routine. Met **Opnieuw uitvoeren** voer je de taak meteen opnieuw uit met de huidige tekst, zodat je nieuwere resultaten kunt bekijken, bijvoorbeeld na een rustig weekend. De routine leest alleen en wordt één keer uitgevoerd per tik. Het nieuwe resultaat vervangt het oude.

Er kunnen hoogstens drie suggesties tegelijk klaarstaan. Na een week met geslaagde runs vraagt de routine **De oude OpenClaw-taak uitzetten?** De taak wordt alleen uitgezet als je op **Uitzetten** tikt. Je kunt hem in OpenClaw weer aanzetten. Met **Houden** blijven beide actief.

## Op basis van wat je doet

Je Machine merkt ook werk op dat je regelmatig doet en stelt dat voor als routine onder **Voorgesteld**, ook zonder OpenClaw. Hij zoekt naar:

- dezelfde vraag die je drie keer of vaker achter elkaar stelt, zoals "geef elke maandag een overzicht van de openstaande supporttickets";
- een mail die je regelmatig verstuurt, zoals een wekelijks rapport aan je team;
- nieuwsbrieven en updatemails die elke week binnenkomen;
- een druk Slack-kanaal waarin anderen elke week schrijven;
- mails die je steeds één voor één naar dezelfde persoon doorstuurt, zoals mails van school en de vereniging naar je partner. Een wekelijks overzicht scheelt het doorsturen;
- hetzelfde verzoek dat je regelmatig beantwoordt, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Elke suggestie vertelt wat de routine heeft opgemerkt, zoals "4 keer achter elkaar gevraagd" of "6 mails naar Sam doorgestuurd in 3 weken". De routine is één keer uitgevoerd, zodat je een echt resultaat ziet. Denk bijvoorbeeld aan een samenvatting voor je team, een briefing voor een wekelijks gesprek, een overzicht van support of development, een stand van zaken van je cijfers of een overzicht van je nieuwsbrieven.

De routine stelt alleen iets voor als het specifiek voor jou is en duidelijk nuttig is. Een nieuwsoverzicht gaat bijvoorbeeld alleen over je eigen nieuwsbrieven, nooit over algemeen nieuws. Als niets geschikt is, krijg je geen suggestie.

De routine controleert hoogstens één keer per dag en voegt hoogstens één nieuwe suggestie per week toe, zonder melding. Met **Nee, bedankt** komt die suggestie niet meer terug. Doorgestuurde mails en antwoorden blijven bij het account waarmee ze zijn verstuurd, zodat Werk en Privé niet door elkaar lopen. Alles blijft op je Machine. Een to-do die je regelmatig sluit, wordt in plaats daarvan aangeboden als terugkerende to-do.

## Routines en terugkerende to-do's

Een [terugkerende to-do](recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelfstandig uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor "betaal de huur op de eerste van de maand" en een routine voor "vertel me elke vrijdag welke deals zijn stilgevallen".
