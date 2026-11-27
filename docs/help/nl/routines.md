---
title: Routines
area: cards
summary: Werk dat je Machine zelfstandig en volgens een vast ritme doet, zoals elke maandag een overzicht van je openstaande deals. Je Machine leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 6d74cb93df1bf494
---
## Een routine maken

Open **Routines** in de zijbalk en beschrijf in één regel wat de routine moet doen en wanneer: "elke maandag om 9 uur, geef een overzicht van mijn openstaande deals" of "elke werkdag ’s ochtends, geef een lijst van de mails waarop ik nog moet antwoorden". Klik daarna op **Toevoegen**.

Zonder opgegeven tijd wordt de routine om 8.00 uur uitgevoerd. De tijd is gebaseerd op de klok van je Machine. De eerste keer dat de routine wordt uitgevoerd, krijgt hij een korte naam.

Met **Toevoegen** wordt eerst een test uitgevoerd, zodat je ziet wat de routine oplevert voordat je hem bewaart. Er wordt niets verstuurd of opgeslagen. Daarna zet **Toevoegen** de routine aan, met **Wijzigen** kun je andere woorden of een nieuwe naam proberen en met **Annuleren** verwijder je de routine.

## Sjablonen

Onder **Sjablonen** onderaan Routines kun je met **Toevoegen** een kant-en-klare routine aanzetten. Die wordt meteen één keer uitgevoerd en daarna elke ochtend om 7.30 uur (Spam opruimen elk uur, Tweedehandsvondsten elke 3 uur, Abonnementen en proefperiodes één keer per maand). Op de kaart zie je de tekst, net als bij elke andere routine. Met **Bewerken** wijzig je de tekst of de naam.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen uitstaat (25 of meer in een week, van minstens 5 afzenders), staat er boven je to-do’s hoeveel nieuwsbrieven je hebt ontvangen en wat de routine ermee zou doen. Je kunt kiezen voor **Aanzetten** of **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier aangeboden als je in een week minstens 5 mails handmatig naar spam hebt verplaatst. Met **Aanzetten** wordt de routine toegevoegd, net als met **Toevoegen** hier. Als je **Nee, bedankt** kiest, wordt de routine niet opnieuw aangeboden. Een sjabloon dat je eerder hebt afgewezen, wordt ook nooit opnieuw aangeboden.

Met **Nieuwsbrieven opruimen** wordt één to-do gemaakt per onderdeel (werk en privé) met de nieuwsbrieven van de afgelopen dag. Bij elke nieuwsbrief kun je kiezen voor **Houden** of **Afmelden**. Afmelden gebeurt via de eenkliklink van de mailinglijst, of met een afmeldmail vanaf jouw adres als versturen is ingeschakeld. Anders meldt The Machine je af op de pagina van de mailinglijst in zijn eigen browser. Een login, captcha of keuze op die pagina moet je zelf afhandelen. Bij de nieuwsbrief staat waarom, met de optie **Afmeldpagina openen**.

Wil je geen to-do’s van een mailinglijst, maar wel de mails blijven ontvangen? Zeg dan "Van deze lijst hoeft niets een to-do te worden" in de chat van een van die mails.

Ontvangstbewijzen, bestellingen en betalingsmeldingen worden overgeslagen. Mails die via een groepsadres zijn binnengekomen, zoals een Google Group, worden vermeld onder de naam van de afzender en melden je nooit af bij de groep. Als de afzender geen eigen afmeldoptie heeft, staat er bij de mail **Zelf afmelden**.

Met **Spam opruimen** wordt één to-do per onderdeel gemaakt met mails van onbekende afzenders die op spam lijken. Bij elke mail kun je kiezen voor **Spam** of **Geen spam**. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert de mail als spam. De routine controleert elk uur, dus spam staat er meestal al voordat je erbij bent. Nieuwe spam wordt aan dezelfde to-do toegevoegd zolang die openstaat.

Gmail dat alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan geen mails naar spam verplaatsen. Daar bevat **Spam** een link om de mail in Gmail te markeren. The Machine onthoudt de afzender dan als spam. Als er geen mailaccount is gekoppeld, staat er **Mail koppelen** in plaats van **Toevoegen**.

Een afzender is onbekend als je die persoon nooit zelf hebt geschreven. Een "Re:" telt alleen als gesprek in een thread waarin jij zelf hebt geschreven. Als er opnieuw mail binnenkomt van een afzender die je als spam hebt gemarkeerd, via de to-do of in je mailbox, staat die in de volgende to-do met de aanduiding **Eerder als spam gemarkeerd**. Mails die je zelf naar spam hebt verplaatst, helpen de routine ook om vergelijkbare mails te herkennen.

Er verandert niets voordat je dit bevestigt via de to-do. Tik op een afzender om eerst de mail te lezen: die blijft ongelezen en er verandert niets. Afbeeldingen van internet worden niet geladen vanuit Spam opruimen, zodat de afzender niet kan zien dat de mail is geopend. Over afzenders waarover je een keuze hebt gemaakt, wordt je niet opnieuw gevraagd. Als er een dag geen nieuwsbrieven of spam zijn, wordt er geen to-do gemaakt. Deze to-do’s sturen nooit een melding.

Als je voor alle afzenders een keuze hebt gemaakt, staat er dat de to-do klaar is en verschijnt **Als gedaan markeren**.

Met **Dagelijks overzicht** worden één keer per dag de paar nieuwsbriefartikelen geselecteerd die je tijd waard zijn. Ze komen samen in één to-do. Bij elk artikel staat in één regel waarom het voor jou relevant is. Tik erop om de mail te lezen of kies **Openen in je mail**. Alleen nieuwsbrieven worden meegenomen, nooit mails van mensen, ontvangstbewijzen of afzenders waarvan je je hebt afgemeld. Ook mails die je al hebt gelezen, worden niet meegenomen. Als niets opvalt, wordt er geen to-do gemaakt.

De routine leert wat je belangrijk vindt aan de hand van wat je opent, met een ster markeert of ongelezen archiveert, en van **Meer zoals dit** en **Minder zoals dit** bij elk artikel. De onderwerpen waarop de routine zoekt, staan op de kaart onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg er zelf een toe. Onderwerpen met een stippellijn heeft de routine zelf geleerd. Een nieuw overzicht vervangt het openstaande overzicht en stuurt nooit een melding.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief. Daarna stelt hij je AI één korte vraag over de mails, met een dagelijks maximum, zodat het weinig kost. Met **Wanneer wijzigen** stel je het tijdstip in. Zodra je de tekst aanpast, werkt de routine zoals elke andere routine op basis van jouw tekst.

Met **Verjaardagen** wordt een to-do gemaakt voor elk contact met wie je veel contact hebt en die vandaag jarig is: mensen aan wie je zelf schrijft, zoals vrienden, familie en vaste contacten. Bij elke verjaardag staat een korte felicitatie als concept, op de plek waar je meestal met die persoon praat, zoals in hun WhatsApp-chat of jullie mailthread, en in hun taal. De felicitatie wordt pas verstuurd als jij dat doet. Als er die dag niemand jarig is, wordt er geen to-do gemaakt.

Verjaardagen komen uit je agenda’s (de verjaardagsevenementen in Google en de agenda Verjaardagen, die elke ochtend wordt uitgelezen, ook als die niet is gesynchroniseerd, en de agenda Verjaardagen in Outlook), je Google-contacten op een zelfgehoste Machine en een datumveld met de naam Birthday bij een persoon in de Graph. Als er nog nergens een verjaardag staat, wordt als resultaat **Nog geen verjaardagsgegevens** getoond, met uitleg over hoe je die kunt toevoegen.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen aanstaat, biedt een to-do aan om de verjaardagenpagina van Facebook uit te lezen. Tik op **Importeren**. The Machine opent de pagina in zijn browser, scrolt totdat alle maanden zijn geladen en leest de naam en verjaardag van elke vriend uit. Je ziet hoeveel verjaardagen zijn gevonden en wie er op basis van voor- en achternaam is gekoppeld aan mensen in je Graph. Namen die bij meer dan één persoon horen, worden overgeslagen en vermeld.

Alleen met **Opslaan** worden de gegevens bewaard op de pagina van elke persoon: de verjaardag en, voor iemand die nog geen foto heeft, diens Facebook-profielfoto. Een verjaardag of foto die je daar instelt, blijft staan. Een foto die iemand al heeft, wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

De pagina wordt niet automatisch opnieuw uitgelezen. Dat gebeurt wel als je op de to-do **Opnieuw importeren** kiest. Je moet in de browser bij Facebook zijn ingelogd. Zo niet, tik dan op **Inloggen bij Facebook** in de to-do en log daar in. Zodra je bent ingelogd, wordt de pagina automatisch uitgelezen. The Machine logt nooit voor je in.

Vrienden die niet in je Graph staan, worden meegeteld en er worden enkele namen getoond. Met **… toevoegen als privécontacten** voeg je ze allemaal tegelijk toe, ook nadat je op Opslaan hebt getikt. Elk contact krijgt een naam en verjaardag en wordt nooit gedeeld met een Werk-Fleet. Een naam die al bij iemand in je Graph hoort, of van iemand die je definitief hebt verwijderd, wordt overgeslagen. Je krijgt alleen herinneringen voor mensen aan wie je zelf schrijft.

Met **Ongedaan maken** in de to-do verwijder je precies die mensen weer, ook nadat je **Opnieuw importeren** hebt gebruikt.

Met **Abonnementen en proefperiodes** worden je ontvangstbewijzen, facturen en meldingen over verlengingen één keer per maand uitgelezen. Je abonnementen komen samen in één to-do, met de kosten, de volgende afschrijfdatum en een melding als een proefperiode eindigt of de prijs stijgt. Alleen abonnementen waar de routine zeker van is, worden vermeld. Als er niets wordt gevonden, wordt er geen to-do gemaakt.

Kies **Houden** of **Opzeggen** voor elk abonnement. Je krijgt geen nieuwe vraag over een abonnement dat je wilt houden, tenzij de prijs verandert. Met **Opzeggen** krijg je de opzeggingspagina of een concept waarin je om opzegging vraagt. Dat wordt pas verstuurd als jij het verstuurt. Tussen de maandelijkse controles door wordt elke dag gecontroleerd. Als een proefperiode of verlenging binnen 7 dagen afloopt, wordt er een to-do gemaakt.

Met **Contact houden** krijg je af en toe een herinnering om contact op te nemen met iemand die je goed kent, maar alleen als daar een goede reden voor is. Op de kaart kies je wie erbij hoort uit een korte lijst van mensen met wie je zelf al maanden heen en weer schrijft. Verwijder iemand met ×.

Je krijgt alleen een herinnering als je veel langer dan gewoonlijk geen contact hebt gehad en er iets concreets is om te zeggen: nieuws dat die persoon heeft gedeeld, ook uit het overzicht op diens pagina, een belofte die nog openstaat of een bericht waarop je nooit hebt geantwoord.

Nieuws met een datum in de toekomst, zoals een verhuizing volgende maand, wordt vlak na die datum opnieuw bekeken, samen met de nieuwste berichten. De herinnering komt in één to-do met de reden en een kort bericht als concept, op de plek waar je meestal praat en in de taal van die persoon. Het bericht wordt pas verstuurd als jij dat doet. Als er niets te zeggen is, wordt er geen to-do gemaakt.

Er worden maximaal twee herinneringen per week verstuurd, hoogstens één per persoon per maand, en geen herinneringen aan iemand met wie je onlangs nog hebt gepraat. Met **Niet nodig** bij een herinnering wacht de routine langer voordat hij die persoon opnieuw voorstelt. Elke keer wordt die periode langer.

De routine stuurt nooit meldingen en blijft privé. Hij wordt nooit gedeeld met een Werk-Fleet, is nooit gebaseerd op werk (wat binnenkomt op je werkaccounts, of een belofte of feit over werk) en wordt opgesteld in een gesprek buiten het werk als je dat hebt.

Met **Tweedehandsvondsten** volgt de routine zoekopdrachten op tweedehandssites zoals Marktplaats, Vinted, eBay of Facebook Marketplace. Voer daar een zoekopdracht uit met de filters die je wilt, kopieer het adres van de resultaten en plak het na **Toevoegen**. Je kunt filters in je eigen woorden toevoegen, bijvoorbeeld “onder 300, binnen 30 km, geen ‘voor onderdelen’”. Elke zoekopdracht is een eigen routine, dus voeg de routine opnieuw toe voor een volgende zoekopdracht.

Elke 3 uur opent The Machine de zoekopdracht in zijn eigen browser en zoekt hij naar advertenties die hij nog niet heeft gezien. Prijs, afstand en woorden die je hebt uitgesloten, worden eerst gecontroleerd met gewone code.

Elke nieuwe advertentie die aan je filters voldoet, wordt geopend. Je AI beoordeelt de staat aan de hand van de foto en beschrijving, en de verkoper aan de hand van reviews, beoordeling en hoe oud het account is. De goede advertenties komen samen in één to-do, elk met een foto, titel, prijs en oordeel in één regel. Tik op een advertentie om hem in de browser van The Machine te openen.

Zolang de to-do openstaat, worden nieuwe vondsten bovenaan toegevoegd, loopt het aantal op en krijg je opnieuw een melding, omdat goede aanbiedingen snel weg zijn. Als je de to-do als gedaan markeert, begint de volgende vondst een nieuwe to-do. Een uitvoering zonder goede vondsten verandert niets.

De routine houdt het netjes en goedkoop: per uitvoering wordt de zoekopdracht één keer uitgelezen, worden maximaal 6 advertenties geopend met een pauze ertussen en worden maximaal 40 advertenties per dag gecontroleerd voor al je zoekopdrachten samen. Voor elke controle stelt je AI één korte vraag met één foto. Tijdens de eerste uitvoering worden de nieuwste advertenties gecontroleerd en de rest als gezien gemarkeerd. Latere uitvoeringen tonen daardoor alleen nieuwe advertenties.

Als de site vraagt om in te loggen, een robotcontrole toont of het uitlezen blokkeert, krijg je een to-do met **Openen** om de pagina in de browser van The Machine te bekijken. Log zelf in of voer de controle uit. Bij de volgende uitvoering wordt de pagina opnieuw uitgelezen. The Machine logt nooit voor je in en lost nooit een controle voor je op. Hij neemt ook nooit contact op met een verkoper, doet geen bod en koopt niets.

Met **Zoekopdracht wijzigen** op de kaart van de routine kun je een nieuw adres of andere filters instellen. Met **Wanneer wijzigen** kies je een ander ritme, zoals “elke 6 uur”.

Met **Nabestellingen** leest de routine orderbevestigingen van webwinkels in je mail en merkt hij op wat je steeds opnieuw koopt, zoals koffie, dierenvoer of vitamines. Als je iets waarschijnlijk weer nodig hebt, wordt er een to-do gemaakt met het product, de winkel, de laatste prijs en wanneer je het voor het laatst hebt gekocht. Met **Openen in de winkel** ga je naar de productpagina om het zelf te kopen. Er wordt niets voor je gekocht.

De routine heeft minstens drie bestellingen van hetzelfde product met een regelmatig interval nodig. Daardoor wordt er geen to-do gemaakt voor een eenmalige bestelling of een ongewoon lange pauze. Voorlopig leest de routine bestellingen bij winkels die Shopify gebruiken. Je AI leest alleen nieuwe bestelbevestigingen van die winkels, met één korte vraag per uitvoering. Deze to-do’s sturen nooit een melding. Als je het product opnieuw bestelt, wordt de openstaande to-do gesloten.

Zolang een routinesjabloon de tekst van het sjabloon gebruikt, wordt de routine uitgevoerd met eigen code, zonder je AI-abonnement. (Spam opruimen toont eerst met code nieuwe mails van onbekende afzenders en stelt je AI alleen een korte vraag als dat nodig is. Contact houden vraagt alleen naar de één of twee mensen die de routine heeft gekozen.) Als je de tekst wijzigt, werkt de routine zoals elke andere routine op basis van jouw tekst.

Nieuwsbrieven opruimen en Spam opruimen leveren nog steeds één to-do op met een keuze per mail. Een aangepaste routine voor Verjaardagen toont het resultaat en hoogstens één concept, geen aparte to-do per persoon. Met **Terug naar het sjabloon** in **Bewerken** zet je de oorspronkelijke tekst terug.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat hij nodig heeft, zoals je berichten, meetings en de Graph. Het resultaat komt op de pagina Routines te staan. Elk resultaat is **Klaargezet**, **Niets nieuws** (met uitleg) of **Lukte niet** (met uitleg). Een uitvoering die eindigt zonder resultaat telt als mislukt, nooit als voltooid.

Routines lezen alleen: je berichten, webpagina’s, GitHub en sites zoals X in de browser. Ze versturen, beantwoorden of plaatsen niets en veranderen niets. Ze openen pagina’s die ze hebben gevonden in wat ze lezen of in een zoekopdracht, gewone webadressen en bekende sites, maar nooit een adres dat is verzonnen om de gelezen informatie mee te sturen. Alleen een sjabloon verandert mails, en alleen wat je via de to-do bevestigt.

Als een taak van een routine eindigt met een bericht of post, voert de routine alles uit tot die stap en toont hij het concept, zoals **Zou op X plaatsen:**. Na een echte uitvoering krijg je dit als to-do om goed te keuren. Bij een testuitvoering wordt het alleen getoond.

De naam geeft aan waar de routine over gaat en waar het resultaat terechtkomt. Met **Van je routine** eronder open je de routine. De knop benoemt de stap, zoals **Bericht voorbereiden**. Daarmee wordt het bericht klaargezet, maar niet geplaatst. Je plaatst het zelf vanuit het resultaat. Als The Machine het niet voor je kan plaatsen, opent de knop daar de pagina waar je dat kunt doen.

De to-do staat eerst bij het onderdeel van het account waarmee het resultaat wordt verstuurd, zoals Werk voor het X-account van je bedrijf. Je hoeft de to-do dus nooit te verplaatsen.

Een uitvoering kan je ingeschakelde [skills](skills.md) volgen, gekozen op basis van wat de routine doet. Alleen skills die van toepassing zijn, worden volledig uitgelezen. Het resultaat vermeldt ze onder **Gebruikt:**. Een skill zorgt er nooit voor dat een routine iets verstuurt of verandert.

Je routines staan onder **Je routines**, onder eventuele suggesties. Een lang resultaat wordt ingeklapt tot een korte preview. Met **Meer tonen** of door erop te tikken, open je het.

Elke uitvoering onthoudt het vorige resultaat, zodat de routine kan aangeven wat er sindsdien is veranderd.

Na een geslaagde uitvoering kan je Machine zelf een recept maken voor leeswerk dat telkens hetzelfde is, zoals welke mails of GitHub-wijzigingen moeten worden bekeken. Bij de volgende uitvoeringen worden die eerst met gewone code uitgelezen. De AI kiest alleen wat belangrijk is en schrijft het resultaat, met minder tokens. Een recept leest alleen. Als het niet meer werkt, wordt de uitvoering zelfstandig uitgelezen en aangepast. Het recept staat onder **Geavanceerd: scriptstappen** in het ⋯-menu.

## Gemiste dagen

Als je Machine uitstaat of bezet is, worden gemiste uitvoeringen niet opgestapeld. Alleen de nieuwste wordt één keer uitgevoerd. Elke datum wordt één keer uitgevoerd, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als je AI-abonnement weinig gebruiksruimte heeft, net als al het werk op de achtergrond. Met **Nu uitvoeren** start je de routine meteen. Het resultaat verschijnt op de kaart zodra het klaar is.

## Wijzigen of stoppen

Deze opties staan in het ⋯-menu van de routine. Met **Bewerken** wijzig je de naam en wat de routine doet. Het tijdstip en de eerdere resultaten blijven behouden. Met **Wanneer wijzigen** stel je een nieuw ritme in je eigen woorden in, zoals "elke werkdag om 8 uur". Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het venster klikken om te annuleren.

Met **Probeer het** in **Bewerken** voer je de nieuwe tekst één keer uit en zie je het resultaat daar. De routine blijft ongewijzigd totdat je op **Opslaan** tikt.

Met **Pauzeren** stop je de uitvoeringen totdat je op de kaart **Hervatten** kiest. Gepauzeerde routines staan onder **Gepauzeerd**, onder je routines. Gemiste uitvoeringen tijdens de pauze worden daarna niet alsnog uitgevoerd. Met **Stoppen** beëindig je een routine definitief.

Je kunt maximaal 20 routines hebben, inclusief gepauzeerde routines. Stop er een om een andere toe te voegen.

Als je **Wijzigingen vragen** kiest bij de to-do van een routine, of iets in de chat van de routine schrijft, en je opmerking geldt voor elke uitvoering, zoals "gebruik nooit emoji's", biedt de to-do **Ook de routine aanpassen** aan. Die optie staat op de to-do en in de chat onder het antwoord. Je ziet wat er in de tekst van de routine verandert. De routine wordt pas aangepast als je op **Aanpassen** tikt. Met **Zo laten** blijft alles hetzelfde. Een aanpassing die alleen voor dat concept geldt, levert geen optie op.

## Geavanceerd: scriptstappen

Je hebt geen script nodig. Beschrijf in je eigen woorden wat een routine moet doen en je Machine regelt de rest.

Ervaren gebruikers kunnen ook eigen opdrachten op hun Machine uitvoeren: kies **Geavanceerd: scriptstappen** in het ⋯-menu. **Bewerken** toont de stappen alleen als de routine er al heeft. Met **Gegevens ophalen** voer je eerst een opdracht uit, in de map van de opdracht (je thuismap als die leeg is), gedurende maximaal het opgegeven aantal seconden. De uitvoer wordt aan de uitvoering doorgegeven. Zonder tekst wordt de uitvoer zelf het resultaat.

Met **Controle** controleer je de uitvoer na de uitvoering. Als de opdracht met een fout stopt, toont de uitvoering **Lukte niet** met de melding van de controle. Als een opdracht voor Gegevens ophalen mislukt, wordt dat op dezelfde manier getoond.

Een opdracht bestaat uit één regel en wordt zonder shell uitgevoerd: geen pipes of variabelen. Scriptstappen zijn van jou en worden alleen op je dashboard ingesteld. Een testuitvoering en **Probeer het** voeren ook Gegevens ophalen uit en vermelden dat. Ze versturen of bewaren nog steeds niets. Een routine verstuurt nooit iets, dus een scriptstap mag alleen lezen.

## Vanuit je OpenClaw-taken

Als je eerder geplande taken in OpenClaw hebt gemaakt, leest je Machine die uit (hij verandert ze nooit) en stelt hij de taken die geschikt zijn voor als routines onder **Voorgesteld**. Elke taak is één keer uitgevoerd, zodat je een echt resultaat ziet.

Je Machine behoudt je aanpassingen aan de taak en laat weg wat de taak heeft verstuurd of geplaatst. Een taak die een script uitvoerde of las wat een scripttaak had verzameld, neemt dat script mee als Gegevens ophalen. Met **Toevoegen** wordt de taak een routine. Met **Nee, bedankt** wordt er nooit meer naar die taak gevraagd. Een taak die je eraan herinnerde iets te doen, verschijnt op To-do’s als een aanbod voor een terugkerende to-do.

Voordat je een suggestie toevoegt, kun je die aanpassen in het ⋯-menu, net als elke andere routine. Met **Bewerken** en **Wanneer wijzigen** pas je de taak aan. Met **Opnieuw uitvoeren** voer je de taak nu uit met de huidige tekst, zodat je nieuwere resultaten ziet, bijvoorbeeld na een rustig weekend. De taak leest alleen en wordt één keer per tik uitgevoerd. Het nieuwe resultaat vervangt het oude.

Er staan maximaal drie suggesties tegelijk klaar. Na een week met geslaagde uitvoeringen vraagt de routine **De oude OpenClaw-taak uitzetten?**. De taak wordt alleen uitgezet als je op **Uitzetten** tikt. Je kunt hem in OpenClaw weer aanzetten. Met **Houden** blijven beide taken actief.

## Op basis van wat je doet

Je Machine merkt ook werk op dat je regelmatig doet en stelt dat als routine voor onder **Voorgesteld**, ook als je OpenClaw niet gebruikt. De routine let op:

- dezelfde vraag die je minstens drie keer achter elkaar stelt, zoals "geef elke maandag een overzicht van de openstaande supporttickets";
- een mail die je regelmatig verstuurt, zoals een wekelijks rapport aan je team;
- nieuwsbrieven en update-mails die elke week binnenkomen;
- een druk Slack-kanaal waar anderen elke week in schrijven;
- mails die je één voor één naar dezelfde persoon doorstuurt, zoals mails van school en de club naar je partner. Een wekelijks overzicht voor die persoon scheelt het doorsturen;
- dezelfde vraag die je regelmatig beantwoordt, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Bij elke suggestie staat wat de routine heeft gezien, zoals "4 keer achter elkaar gevraagd" of "6 mails naar Sam doorgestuurd in 3 weken". De routine is één keer uitgevoerd, zodat je een echt resultaat ziet. Denk bijvoorbeeld aan een overzicht voor je team, een briefing voor een wekelijks gesprek, een overzicht van support of ontwikkeling, een update over je cijfers of een overzicht van de nieuwsbrieven die je ontvangt.

De routine stelt alleen iets voor als het specifiek voor jou is en duidelijk nuttig is: een nieuwsoverzicht bevat alleen je eigen nieuwsbrieven, nooit een algemeen overzicht. Als niets geschikt is, verschijnt er geen suggestie.

De routine controleert dit hoogstens één keer per dag en toont maximaal één nieuwe suggestie per week, zonder melding. Met **Nee, bedankt** wordt die suggestie niet opnieuw getoond. Doorgestuurde mails en antwoorden blijven bij het account waarmee ze zijn verstuurd, zodat Werk en Privé gescheiden blijven. Alles blijft op je Machine. Een to-do die je regelmatig afsluit, verschijnt in plaats daarvan als aanbod voor een terugkerende to-do.

## Routines en terugkerende to-do’s

Een [terugkerende to-do](recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelfstandig uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor "de huur betalen op de eerste" en een routine voor "vertel me elke vrijdag welke deals stil zijn gevallen".
