---
title: Routines
area: cards
summary: Werk dat je Machine zelfstandig op vaste momenten doet, zoals elke maandag een overzicht van je openstaande deals. Hij leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: e0d519d5927cdde0
---
## Een routine maken

Open **Routines** in de zijbalk en beschrijf in één regel wat de routine moet doen en wanneer: "elke maandag om 9 uur mijn openstaande deals samenvatten" of "elke werkdag 's ochtends de mails opsommen waarop ik nog moet reageren". Klik daarna op **Toevoegen**.

Zonder tijdstip wordt de routine om 8:00 uitgevoerd. De tijd volgt de klok van je Machine. De eerste keer dat de routine wordt uitgevoerd, krijgt hij een korte naam.

**Toevoegen** voert eerst een test uit, zodat je ziet wat de routine oplevert voordat je hem bewaart. Er wordt niets verstuurd of opgeslagen. Daarna zorgt **Toevoegen** ervoor dat de routine op vaste momenten wordt uitgevoerd, probeert **Wijzigen** andere woorden of een nieuwe naam en verwijdert **Annuleren** de routine.

## Sjablonen

Onderaan Routines kun je bij **Sjablonen** met **Toevoegen** een kant-en-klare routine inschakelen. Die wordt meteen één keer uitgevoerd en daarna elke ochtend om 7:30 (Spam opruimen elk uur, Tweedehandsvondsten elke 3 uur, Abonnementen en proefperiodes één keer per maand). De kaart toont de beschrijving, net als bij elke andere routine. Met **Bewerken** pas je de beschrijving of de naam aan.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen uitstaat (25 of meer in een week, van minstens 5 afzenders), verschijnt er boven je to-do's een melding met hoeveel nieuwsbrieven je hebt gekregen en wat de routine ermee zou doen. Je kunt kiezen voor **Aanzetten** of **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier voorgesteld als je in een week 5 of meer mails zelf naar spam hebt verplaatst. Met **Aanzetten** voeg je de routine toe, net als met **Toevoegen** hierboven. Kies je **Nee, bedankt**, dan wordt de routine niet meer voorgesteld. Dat geldt ook voor een sjabloon dat je eerder hebt gehad.

**Nieuwsbrieven opruimen** maakt één to-do per gebied (werk en privé) met de nieuwsbrieven van de afgelopen dag. Je kunt per nieuwsbrief kiezen voor **Houden** of **Afmelden**. Afmelden gebeurt via de eenkliklink van de mailinglijst, of via een afmeldmail vanaf jouw adres als versturen is ingeschakeld. Anders meldt The Machine je af op de pagina van de mailinglijst in zijn eigen browser. Een login, captcha of eventuele keuzes op die pagina moet je zelf afhandelen. Bij de nieuwsbrief staat waarom, met **Afmeldpagina openen**.

Ontvangstbewijzen, bestellingen en betalingsmeldingen worden overgeslagen. Mails die via een groepsadres zijn binnengekomen, zoals een Google Group, staan onder de naam van de afzender. Je wordt nooit afgemeld voor de groep. Heeft de afzender geen eigen afmeldmogelijkheid, dan staat er **Zelf afmelden**.

**Spam opruimen** maakt één to-do per gebied met mails van onbekende afzenders die op spam lijken. Je kunt per mail kiezen voor **Spam** of **Geen spam**. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert het als spam. De routine controleert elk uur, dus spam staat er meestal al voordat je erbij bent. Nieuwe spam wordt aan dezelfde to-do toegevoegd zolang die openstaat.

Gmail dat alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan geen mail naar spam verplaatsen. Daar geeft **Spam** een link waarmee je de mail in Gmail kunt markeren, en onthoudt The Machine de afzender als spam. Als er geen mailaccount is gekoppeld, toont het sjabloon **Mail koppelen** in plaats van **Toevoegen**.

Onbekend betekent dat je de afzender nooit hebt gemaild. Een “Re:” telt alleen als gesprek in een thread waarin je zelf hebt geschreven. Als je opnieuw mail ontvangt van een afzender die je als spam hebt gemarkeerd, op de to-do of in je mailbox, staat die mail op de volgende to-do met de melding **Eerder als spam gemarkeerd**. Mails die je zelf naar spam hebt verplaatst, helpen ook om vergelijkbare mails te herkennen.

Er verandert niets totdat je je keuze op de to-do bevestigt. Tik op een afzender om eerst de mail te lezen. Die blijft ongelezen en er verandert niets. In Spam opruimen worden afbeeldingen van het web niet geladen, zodat de afzender niet kan zien dat je de mail hebt geopend. Je krijgt geen nieuwe vraag over afzenders waarover je al hebt beslist. Op een dag zonder nieuwsbrieven of spam wordt er geen to-do gemaakt. Deze to-do's sturen nooit een melding.

Als je voor alle afzenders een keuze hebt gemaakt, staat er op de to-do dat die is afgerond en verschijnt **Als gedaan markeren**.

**Dagelijks overzicht** kiest één keer per dag de nieuwsbrieven die je tijd waard zijn en zet ze samen in één to-do. Bij elke nieuwsbrief staat in één regel waarom die voor jou relevant is. Tik erop om de mail te lezen of kies **Openen in je mail**. Alleen nieuwsbrieven worden meegenomen, nooit mails van mensen, ontvangstbewijzen of afzenders waarvoor je je hebt afgemeld. Ook mails die je al hebt gelezen worden overgeslagen. Als er niets uitspringt, wordt er geen to-do gemaakt.

De routine leert wat je belangrijk vindt op basis van wat je opent, met een ster markeert of ongelezen archiveert, en van **Meer zoals dit** en **Minder zoals dit** bij elke keuze. De onderwerpen waarop de routine let, staan op de kaart onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg er zelf een toe. Gestippelde onderwerpen heeft de routine zelf geleerd. Een nieuw overzicht vervangt het vorige zolang dat nog openstaat. Er wordt nooit een melding verstuurd.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief. Daarna stelt hij je AI één korte vraag over de nieuwsbrieven, met een dagelijks maximum om de kosten laag te houden. Met **Wanneer wijzigen** stel je het tijdstip in. Zodra je de beschrijving wijzigt, wordt de routine uitgevoerd zoals elke andere routine, op basis van jouw beschrijving.

**Verjaardagen** maakt een to-do voor elke dierbare contactpersoon die vandaag jarig is: mensen met wie je zelf contact hebt, zoals vrienden, familie en mensen met wie je regelmatig praat. Voor elke persoon staat er een korte felicitatie klaar in de app waarin je meestal met diegene praat, zoals diens WhatsApp-chat of jullie mailthread. De felicitatie is in de taal van die persoon. De felicitatie wordt alleen verstuurd als jij dat doet. Op een dag zonder verjaardagen wordt er geen to-do gemaakt.

Verjaardagen komen uit je agenda's (de verjaardagsevenementen en verjaardagsagenda van Google, die elke ochtend worden gelezen, ook als ze niet zijn gesynchroniseerd, en de verjaardagsagenda van Outlook), je Google-contacten op een zelf gehoste Machine en een datumveld met de naam Birthday bij een persoon in de Graph. Als nergens een verjaardag is opgeslagen, staat er bij het resultaat **Nog geen verjaardagsgegevens** en lees je hoe je die kunt toevoegen.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen is ingeschakeld, verschijnt er een to-do waarin je kunt kiezen om de verjaardagenpagina van Facebook te lezen. Tik op **Importeren**. The Machine opent de pagina in zijn browser, scrolt totdat alle maanden zijn geladen en leest de namen en verjaardagen van je vrienden. Je ziet hoeveel verjaardagen zijn gevonden en wie op basis van voor- en achternaam overeenkomt met mensen in je Graph. Namen die bij meer dan één persoon horen, worden overgeslagen en vermeld.

Alleen **Opslaan** bewaart de gegevens, op de pagina van elke persoon: de verjaardag en, als iemand nog geen foto heeft, diens Facebook-profielfoto. Een verjaardag of foto die je daar hebt ingesteld, blijft staan. Een foto die iemand al heeft, wordt nooit vervangen. Er wordt niets op Facebook opgeslagen.

De verjaardagen worden niet vanzelf opnieuw ingelezen. Daarvoor tik je op **Opnieuw importeren** op de to-do. Je moet in Facebook zijn ingelogd in de browser. Is dat niet zo, tik dan op **Inloggen bij Facebook** op de to-do en log daar in. Zodra je bent ingelogd, leest The Machine de pagina vanzelf. The Machine logt nooit voor je in.

Vrienden die niet in je Graph staan, worden geteld en er worden enkele namen getoond. Met **… toevoegen als privécontacten** voeg je ze allemaal tegelijk toe, ook nadat je op Opslaan hebt getikt. Iedereen wordt toegevoegd met diens naam en verjaardag, en nooit gedeeld met een Werk-Fleet. Een naam die al bij iemand in je Graph hoort, of die van iemand die je definitief hebt verwijderd, wordt overgeslagen. Je krijgt nog steeds alleen verjaardagsherinneringen voor mensen met wie je zelf contact hebt.

Met **Ongedaan maken** op de to-do verwijder je precies deze mensen weer, ook nadat je **Opnieuw importeren** hebt gebruikt.

**Abonnementen en proefperiodes** leest één keer per maand je ontvangstbewijzen, facturen en verlengingsberichten en zet je abonnementen in één to-do. Je ziet de prijs, wanneer er weer wordt afgeschreven en een melding als een proefperiode afloopt of de prijs stijgt. Alleen abonnementen waar de routine zeker van is, worden getoond. Als er niets wordt gevonden, wordt er geen to-do gemaakt.

Kies per abonnement **Houden** of **Opzeggen**. Naar een abonnement dat je houdt, wordt niet opnieuw gevraagd, tenzij de prijs verandert. Met **Opzeggen** krijg je de opzegpagina of een conceptbericht waarin je om opzegging vraagt. Dat bericht wordt alleen verstuurd als jij dat doet. Tussen de maandelijkse controles door controleert de routine elke dag of een proefperiode afloopt of een verlenging binnen 7 dagen plaatsvindt. In dat geval wordt er een to-do gemaakt.

**Contact houden** herinnert je af en toe eraan contact op te nemen met iemand die je dierbaar is, maar alleen als daar een goede reden voor is. Kies op de kaart wie erbij hoort uit een korte lijst van mensen met wie je zelf over en weer contact hebt gehad, verspreid over meerdere maanden. Verwijder iemand met ×.

Je krijgt alleen een herinnering als het veel langer dan gewoonlijk geleden is dat jullie contact hadden en er iets specifieks is om over te praten: nieuws dat die persoon heeft gedeeld, een belofte die nog openstaat of een bericht waarop je nooit hebt gereageerd. Er komt één to-do met de reden en een kort bericht dat is opgesteld in de app waarin je meestal praat, in de taal van die persoon. Het bericht wordt alleen verstuurd als jij dat doet. Is er niets om over te praten, dan wordt er geen to-do gemaakt.

De routine stuurt hooguit twee herinneringen per week en één per persoon per maand. Iemand met wie je onlangs contact had, krijgt geen herinnering. Met **Niet nodig** bij een herinnering wacht de routine langer voordat hij die persoon opnieuw voorstelt. Elke keer wordt die wachttijd langer. De routine stuurt nooit een melding en blijft privé. Hij wordt nooit gedeeld met een Werk-Fleet.

**Tweedehandsvondsten** houdt een zoekopdracht op een tweedehandssite in de gaten, zoals Marktplaats, Vinted, eBay of Facebook Marketplace. Zoek op de site met de gewenste filters, kopieer het adres van de resultaten en plak het na **Toevoegen**. Je kunt desgewenst filters in je eigen woorden toevoegen, zoals “onder 300, binnen 30 km, geen ‘voor onderdelen’”. Elke zoekopdracht is een eigen routine. Voeg de routine dus opnieuw toe voor een volgende zoekopdracht.

Elke 3 uur opent The Machine de zoekopdracht in zijn eigen browser en zoekt hij naar advertenties die hij nog niet eerder heeft gezien. Prijs, afstand en woorden die je hebt uitgesloten, worden eerst gecontroleerd met gewone code.

Elke nieuwe advertentie die aan de filters voldoet, wordt geopend. Je AI beoordeelt de staat aan de hand van de foto en beschrijving, en de verkoper op basis van diens recensies, beoordeling en accountleeftijd. De interessante advertenties komen samen in één to-do, elk met een foto, titel, prijs en oordeel van één regel. Tik op een advertentie om die in de browser van The Machine te openen.

Zolang de to-do openstaat, worden nieuwe vondsten bovenaan toegevoegd, loopt het aantal op en krijg je opnieuw een melding, omdat goede deals snel weg zijn. Markeer de to-do als gedaan en de volgende vondst start een nieuwe to-do. Een controle zonder interessante vondsten verandert niets.

De routine houdt het eenvoudig en betaalbaar: per uitvoering wordt de zoekopdracht één keer gelezen. Er worden per uitvoering hooguit 6 advertenties geopend, met een pauze ertussen, en per dag worden er hooguit 40 advertenties gecontroleerd voor al je zoekopdrachten samen. Elke controle bestaat uit één korte vraag aan je AI met één foto. De eerste uitvoering controleert de nieuwste advertenties en markeert de rest als gezien. Volgende uitvoeringen tonen alleen wat nieuw is.

Als de site je vraagt om in te loggen, een robotcontrole toont of het lezen blokkeert, staat dat op een to-do met **Openen** om de pagina in de browser van The Machine te bekijken. Log zelf in of voltooi daar de controle. Bij de volgende uitvoering probeert de routine de pagina opnieuw te lezen. The Machine logt nooit voor je in en voltooit nooit een controle voor je. Hij neemt nooit contact op met een verkoper, biedt nergens op en koopt niets.

Met **Zoekopdracht wijzigen** op de routinekaart pas je het adres of de filters aan. Met **Wanneer wijzigen** kies je een ander ritme, zoals “elke 6 uur”.

**Nabestellingen** leest orderbevestigingen van webwinkels in je mail en merkt op wat je steeds opnieuw koopt, zoals koffie, dierenvoer of vitamines. Als je waarschijnlijk weer iets nodig hebt, maakt de routine een to-do met het artikel, de winkel, de laatste prijs en wanneer je het voor het laatst hebt gekocht. Met **Openen in de winkel** ga je naar de pagina van het artikel om het zelf te kopen. Er wordt niets voor je gekocht.

De routine heeft minstens drie bestellingen van hetzelfde artikel met regelmatige tussenpozen nodig. Een eenmalige bestelling of een ongebruikelijk lange pauze leidt dus niet tot een to-do. De routine leest voorlopig alleen winkels die Shopify gebruiken. Je AI leest alleen nieuwe bestelberichten van die winkels, met één korte vraag per uitvoering. Deze to-do's sturen nooit een melding. Als je het artikel opnieuw bestelt, wordt de openstaande to-do gesloten.

Zolang de routine van een sjabloon de beschrijving van dat sjabloon gebruikt, wordt hij uitgevoerd met eigen code, zonder je AI-abonnement. (Spam opruimen vermeldt nieuwe mails van onbekende afzenders eerst met code en stelt je AI alleen één korte vraag als er mails zijn. Contact houden vraagt alleen naar de een of twee personen die de routine heeft geselecteerd.) Een nieuwe naam verandert dat niet. Zodra je de beschrijving wijzigt, wordt de routine uitgevoerd zoals elke andere routine, op basis van jouw beschrijving.

Nieuwsbrieven opruimen en Spam opruimen blijven dezelfde to-do maken, met een keuze voor elke mail. Een aangepaste Verjaardagen-routine geeft het resultaat en hooguit één concept, niet één to-do per persoon. Met **Terug naar het sjabloon** in **Bewerken** zet je de oorspronkelijke beschrijving terug.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat hij nodig heeft, zoals je berichten, meetings en de Graph, en zet hij het resultaat op de pagina Routines. Elk resultaat heeft de status **Klaargezet**, **Niets nieuws** (met uitleg) of **Lukte niet** (met uitleg). Een uitvoering die eindigt zonder resultaat telt als mislukt, nooit als geslaagd.

Routines lezen alleen: je berichten, webpagina's, GitHub en sites zoals X in de browser. Ze versturen niets, beantwoorden niets, plaatsen niets en veranderen niets. Ze openen pagina's die ze hebben gevonden in wat ze lezen of in een zoekopdracht, gewone webadressen en bekende sites. Ze openen nooit een adres dat is verzonnen om de gelezen inhoud mee te geven. Alleen een sjabloon verandert mails, en alleen wat je op de bijbehorende to-do bevestigt.

Als een routine iets moet plaatsen of een bericht moet versturen, doet hij alles tot aan die stap en toont hij het concept, bijvoorbeeld **Zou plaatsen op X:**. Na een echte uitvoering krijg je dat als to-do ter goedkeuring. Bij een testuitvoering wordt het alleen getoond.

De naam geeft aan waar de routine over gaat en waar de uitvoer terechtkomt. Met **Van je routine** eronder open je de routine. De knop geeft de stap aan, zoals **Bericht voorbereiden**. Daarmee wordt het bericht klaargezet, maar niet geplaatst. Je plaatst het zelf vanuit het resultaat. Als The Machine het niet voor je kan plaatsen, opent de knop de pagina waarop je dat kunt doen.

De to-do wordt gemaakt in het gebied van het account waarmee de actie wordt uitgevoerd, bijvoorbeeld Werk voor het X-account van je bedrijf. Je hoeft de to-do dus nooit naar een ander gebied te verplaatsen.

Een uitvoering kan de ingeschakelde [skills](skills.md) volgen die bij de taak van de routine passen. Alleen relevante skills worden volledig gelezen. Het resultaat vermeldt ze onder **Gebruikt:**. Een skill zorgt er nooit voor dat een routine iets verstuurt of verandert.

Je routines staan onder **Je routines**, onder eventuele suggesties. Lange resultaten worden ingeklapt tot een korte preview. Met **Meer tonen** of door erop te tikken open je het volledige resultaat.

Elke uitvoering weet wat het vorige resultaat was, zodat de routine kan aangeven wat er sindsdien is veranderd.

Na een geslaagde uitvoering kan je Machine zelf een recept opstellen voor het leeswerk dat elke keer hetzelfde is, zoals welke mails of GitHub-wijzigingen moeten worden bekeken. Bij volgende uitvoeringen wordt dat eerst met gewone code gelezen. De AI kiest alleen wat belangrijk is en schrijft het resultaat op, met minder tokens. Een recept leest alleen. Als het niet meer werkt, voert de routine het leeswerk zelf uit en past het recept aan. Het recept staat onder **Geavanceerd: scriptstappen** in het ⋯-menu.

## Gemiste dagen

Als je Machine uitstaat of bezet is, worden gemiste uitvoeringen niet opgestapeld. Alleen de nieuwste wordt één keer uitgevoerd. Elke datum wordt één keer uitgevoerd, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als je AI-abonnement weinig gebruiksruimte over heeft, net als ander achtergrondwerk. Met **Nu uitvoeren** start je de routine meteen. Het resultaat verschijnt op de kaart zodra het klaar is.

## Wijzigen of stoppen

Je vindt deze opties in het ⋯-menu van de routine. Met **Bewerken** pas je de naam en de taak aan. Het tijdstip en de resultaten tot nu toe blijven hetzelfde. Met **Wanneer wijzigen** kies je in je eigen woorden een ander ritme, zoals “elke werkdag om 8 uur”. Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het venster klikken om te annuleren.

Met **Probeer het** in **Bewerken** voer je de nieuwe beschrijving één keer uit en bekijk je het resultaat daar. De routine blijft ongewijzigd totdat je op **Opslaan** tikt.

Met **Pauzeren** stop je de uitvoeringen totdat je op de kaart op **Hervatten** tikt. Gepauzeerde routines staan onder **Gepauzeerd**, onder je routines. Gemiste uitvoeringen worden niet alsnog gedaan. Met **Stoppen** beëindig je een routine definitief.

Je kunt maximaal 20 routines hebben, inclusief gepauzeerde routines. Stop een routine om een nieuwe toe te voegen.

Als je bij de to-do van een routine **Wijzigingen vragen** kiest of iets in de chat schrijft, en je opmerking voor elke uitvoering geldt, zoals “gebruik nooit emoji's”, stelt de to-do **Ook de routine aanpassen** voor. Die optie staat op de to-do en in de chat onder het antwoord. Je ziet welke delen van de beschrijving veranderen. De routine wordt pas aangepast als je op **Aanpassen** tikt. Met **Zo laten** blijft alles hetzelfde. Als je alleen dat ene concept wilt aanpassen, wordt deze optie niet aangeboden.

## Geavanceerd: scriptstappen

Een script is niet nodig. Beschrijf in je eigen woorden wat een routine moet doen en je Machine zoekt uit hoe.

Voor gevorderde gebruikers kan een routine ook eigen opdrachten op je Machine uitvoeren. Kies daarvoor **Geavanceerd: scriptstappen** in het ⋯-menu. **Bewerken** toont de scriptstappen zodra een routine er een heeft. Met **Gegevens ophalen** voer je eerst een opdracht uit in de map van die opdracht (of in je thuismap als er geen map is ingesteld), gedurende maximaal het opgegeven aantal seconden. De uitvoer wordt aan de routine doorgegeven. Als er geen beschrijving is, vormt de uitvoer het resultaat.

Met **Controle** gebruik je de uitvoer als invoer nadat de routine klaar is. Als de opdracht eindigt met een fout, toont de uitvoering **Lukte niet** met de melding van de controle. Een mislukte opdracht voor Gegevens ophalen wordt op dezelfde manier getoond.

Een opdracht bestaat uit één regel en wordt zonder shell uitgevoerd: pipes en variabelen zijn niet toegestaan. Scriptstappen zijn van jou en worden alleen op je dashboard ingesteld. Ook een testuitvoering en **Probeer het** voeren Gegevens ophalen uit en vermelden dat. Ze versturen en bewaren nog steeds niets. Een routine verstuurt nooit iets, dus een scriptstap mag alleen lezen.

## Vanuit je OpenClaw-taken

Als je eerder geplande taken in OpenClaw hebt gemaakt, leest je Machine die in (hij verandert ze nooit) en stelt hij geschikte taken voor als routines onder **Voorgesteld**. Elke taak is één keer uitgevoerd, zodat je een echt resultaat ziet.

Je Machine behoudt je aanpassingen aan de taak en laat weg wat de taak heeft verstuurd of geplaatst. Een taak die een script heeft uitgevoerd, of de uitvoer van een scripttaak heeft gelezen, neemt dat mee als Gegevens ophalen. Met **Toevoegen** maak je er een routine van. Met **Nee, bedankt** wordt er niet opnieuw naar die taak gevraagd. Een taak die je ergens aan herinnerde, wordt op To-do's aangeboden als terugkerende to-do.

Voordat je een suggestie toevoegt, kun je die aanpassen zoals elke routine. Kies daarvoor **Bewerken** of **Wanneer wijzigen** in het ⋯-menu. Met **Opnieuw uitvoeren** voer je de taak meteen uit met de huidige beschrijving, zodat je nieuwere resultaten ziet, bijvoorbeeld na een rustig weekend. De taak leest alleen, wordt één keer per tik uitgevoerd en het nieuwe resultaat vervangt het oude.

Er staan maximaal drie suggesties tegelijk klaar. Na een week met geslaagde uitvoeringen vraagt de routine **De oude OpenClaw-taak uitzetten?** De oude taak wordt alleen uitgezet als je op **Uitzetten** tikt. Je kunt hem daarna weer aanzetten in OpenClaw. Met **Houden** blijven beide taken actief.

## Op basis van wat je doet

Je Machine merkt ook werk op dat je regelmatig doet en stelt dat voor als routine onder **Voorgesteld**, ook als je OpenClaw niet gebruikt. Hij kijkt naar:

- dezelfde vraag die je drie keer of vaker achter elkaar stelt, zoals elke maandag “vat de openstaande supporttickets samen”;
- een mail die je regelmatig verstuurt, zoals een wekelijks rapport aan je team;
- nieuwsbrieven en updatemails die elke week terugkomen;
- een druk Slack-kanaal waarin anderen elke week schrijven;
- mails die je één voor één naar dezelfde persoon doorstuurt, zoals school- en clubmails naar je partner. Een wekelijks overzicht bespaart je het doorsturen;
- dezelfde vraag die je regelmatig beantwoordt, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Elke suggestie vermeldt wat de routine heeft opgemerkt, zoals “4 keer achter elkaar gevraagd” of “6 mails in 3 weken doorgestuurd naar Sam”. De routine is één keer uitgevoerd, zodat je een echt resultaat ziet. Denk aan een teamoverzicht, een briefing voor een wekelijks gesprek, een samenvatting van support of ontwikkeling, een overzicht van je cijfers of een overzicht van je nieuwsbrieven.

De routine stelt alleen iets voor als het specifiek voor jou is en duidelijk nuttig: een nieuwsoverzicht bevat alleen je eigen nieuwsbrieven, nooit algemene nieuwsbrieven. Als niets past, krijg je geen suggestie.

De routine kijkt hooguit één keer per dag en voegt maximaal één nieuwe suggestie per week toe, zonder melding. Met **Nee, bedankt** wordt die suggestie niet opnieuw getoond. Doorgestuurde mails en antwoorden blijven bij het account waarmee ze zijn verstuurd. Werk en privé worden dus niet gemengd. Alles blijft op je Machine. Een to-do die je regelmatig afsluit, wordt in plaats daarvan aangeboden als terugkerende to-do.

## Routines en terugkerende to-do's

Een [terugkerende to-do](recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelfstandig uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor “de huur betalen op de eerste dag van de maand” en een routine voor “vertel me elke vrijdag welke deals stil zijn gevallen”.
