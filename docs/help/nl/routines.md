---
title: Routines
area: cards
summary: Werk dat je Machine zelfstandig en volgens een vast ritme doet, zoals elke maandag een overzicht van je openstaande deals. Hij leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 57b97c44b031845f
---
## Een routine maken

Open **Routines** in de zijbalk en beschrijf in één regel wat de routine moet doen en wanneer: "elke maandag om 9 uur, geef een overzicht van mijn openstaande deals" of "elke werkdag ’s ochtends, geef een lijst van de mails waarop ik nog moet antwoorden". Klik daarna op **Toevoegen**.

Als je geen tijd opgeeft, wordt de routine om 8.00 uur uitgevoerd. De tijd wordt bepaald door de klok van je Machine. De eerste uitvoering geeft de routine een korte naam.

**Toevoegen** voert eerst een testrun uit, zodat je ziet wat de routine oplevert voordat je hem bewaart. Er wordt niets verstuurd of opgeslagen. Daarna zorgt **Toevoegen** ervoor dat de routine volgens het ingestelde ritme wordt uitgevoerd. Met **Wijzigen** kun je andere woorden of een nieuwe naam proberen. Met **Annuleren** verwijder je de routine.

## Sjablonen

Bij **Sjablonen** onderaan Routines zet **Toevoegen** een kant-en-klare routine aan. Hij wordt meteen één keer uitgevoerd en daarna elke ochtend om 7.30 uur. Spam opruimen wordt elk uur uitgevoerd, Tweedehandsvondsten elke 3 uur en Abonnementen en proefperiodes één keer per maand. Op de kaart van de routine staan de woorden die hij gebruikt, net als bij elke andere routine. Met **Bewerken** pas je die woorden of de naam aan.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen uitstaat (25 of meer in een week, van minstens 5 afzenders), staat er boven je to-do's hoeveel nieuwsbrieven er zijn binnengekomen en wat de routine ermee zou doen. Je kunt kiezen voor **Aanzetten** of **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier aangeboden als je in een week 5 of meer mails handmatig naar spam hebt verplaatst. **Aanzetten** voegt de routine toe, net als **Toevoegen** hier. Als je **Nee, bedankt** kiest, wordt de routine niet opnieuw aangeboden. Dat geldt ook voor een sjabloon dat je eerder hebt afgewezen.

**Nieuwsbrieven opruimen** maakt één to-do per gebied aan, voor Werk en Persoonlijk, met de nieuwsbrieven van de afgelopen dag. Voor elke mail kun je kiezen voor **Houden** of **Afmelden**. Met Afmelden gebruikt de routine de afmeldlink voor één klik van de mailinglijst, of verstuurt hij namens jou een afmeldmail als versturen is ingeschakeld. Anders meldt The Machine je af via de pagina van de mailinglijst in zijn eigen browser. Een login, captcha of keuze op die pagina moet je zelf afhandelen. In de regel staat waarom, met **Afmeldpagina openen**.

Wil je geen to-do's meer van een mailinglijst, maar wel de mails blijven ontvangen? Schrijf dan in de chat van een mail van die lijst: "Voor deze lijst hoeft niets op mijn to-do's te staan."

Ontvangstbewijzen, bestellingen en betalingsmeldingen worden overgeslagen. Mails die via een groepsadres binnenkomen, zoals een Google Group, worden vermeld onder de naam van de afzender. Je wordt nooit afgemeld voor de groep. Als de afzender geen eigen afmeldmogelijkheid heeft, staat er **Zelf afmelden** bij de regel.

**Spam opruimen** maakt één to-do per gebied aan met mails van onbekende afzenders die op spam lijken. Voor elke mail kun je kiezen voor **Spam** of **Geen spam**. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert de mail als spam. De routine controleert elk uur, dus spam staat er meestal al voordat je eraan toekomt. Nieuwe spam wordt aan dezelfde to-do toegevoegd zolang die openstaat.

Gmail dat alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan geen mails naar spam verplaatsen. Daar geeft **Spam** een link om de mail in Gmail te markeren. The Machine onthoudt de afzender dan als spam. Als er geen mailaccount is gekoppeld, staat **Mail koppelen** op de plek van **Toevoegen** in het sjabloon.

Een afzender is onbekend als je die nog nooit zelf hebt gemaild. Een “Re:” telt alleen als gesprek als jij iets in de thread hebt geschreven. Als er toch weer een mail binnenkomt van een afzender die je als spam hebt gemarkeerd, in de to-do of in je mailbox, staat die in de volgende to-do met **Eerder als spam gemarkeerd**. Wat je zelf naar spam hebt verplaatst, helpt de routine ook vergelijkbare mails herkennen.

Er verandert niets totdat je dit in de to-do bevestigt. Tik op een afzender om eerst de mail te lezen. De mail blijft ongelezen en er verandert niets. Bij Spam opruimen worden afbeeldingen van internet niet geladen, zodat de afzender niet kan zien dat de mail is geopend. Over afzenders waarover je al een keuze hebt gemaakt, wordt je niet opnieuw gevraagd. Op een dag zonder nieuwsbrieven of spam wordt geen to-do aangemaakt. Deze to-do's sturen nooit een melding.

Zodra je voor alle afzenders een keuze hebt gemaakt, staat er dat de to-do is afgerond en verschijnt **Als gedaan markeren**.

**Dagelijks overzicht** selecteert één keer per dag in één to-do de paar nieuwsbriefartikelen die je tijd waard zijn. Bij elk artikel staat in één regel waarom het voor jou relevant is. Tik erop om de mail te lezen of kies **Openen in je mail**. De routine verwerkt alleen nieuwsbrieven, nooit mails van mensen, ontvangstbewijzen of afzenders waarvoor je je hebt afgemeld. Ook mails die je al hebt gelezen worden overgeslagen. Als niets eruit springt, wordt er geen to-do aangemaakt.

De routine leert waar je om geeft op basis van wat je opent, met een ster markeert of ongelezen archiveert, en van **Meer zoals dit** en **Minder zoals dit** bij elk artikel. De onderwerpen waarop de routine zich richt, staan op de kaart onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg je eigen onderwerpen toe. Onderwerpen met een stippellijn heeft de routine zelf geleerd. Een nieuw overzicht vervangt het openstaande overzicht. Er wordt nooit een melding verstuurd.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief. Daarna stelt hij je AI één korte vraag over de nieuwsbrief, met een dagelijkse limiet om de kosten laag te houden. Met **Wanneer wijzigen** stel je het tijdstip in. Zodra je de woorden aanpast, wordt de routine uitgevoerd zoals elke andere routine, op basis van jouw woorden.

**Verjaardagen** maakt een to-do aan voor elke goede bekende die vandaag jarig is. Dat zijn mensen aan wie je zelf schrijft, zoals vrienden, familie en vaste contacten. Bij elke verjaardag staat een korte felicitatie als concept, op de plek waar je meestal met die persoon praat, bijvoorbeeld in diens WhatsApp-chat of in je e-mailthread, en in diens taal. De felicitatie wordt pas verstuurd als jij hem verstuurt. Op een dag zonder verjaardagen wordt geen to-do aangemaakt.

Verjaardagen komen uit je agenda's (de verjaardagsevenementen en verjaardagsagenda van Google, die elke ochtend worden gelezen, ook als ze niet zijn gesynchroniseerd, en de verjaardagsagenda van Outlook), je Google-contacten op een zelfgehoste Machine en een datumveld met de naam Birthday bij een persoon in de Graph. Als nergens een verjaardag staat, geeft het resultaat **Nog geen verjaardagsgegevens** weer, met uitleg over hoe je verjaardagen kunt toevoegen.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen aanstaat, krijg je een to-do aangeboden om de verjaardagenpagina van Facebook te lezen. Tik op **Importeren**. The Machine opent de pagina in zijn browser, scrolt totdat alle maanden zijn geladen en leest de namen en verjaardagen van je vrienden. Hij laat zien hoeveel verjaardagen hij heeft gevonden en wie overeenkomt met personen in je Graph op basis van voor- en achternaam. Namen die bij meer dan één persoon horen, worden overgeslagen en vermeld.

Alleen met **Opslaan** worden de gegevens bewaard, op de pagina van elke persoon: de verjaardag en de Facebook-profielfoto van iemand die nog geen foto heeft. Een verjaardag of foto die je daar instelt, blijft staan. Een bestaande foto wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

The Machine leest de pagina niet vanzelf opnieuw. Dat gebeurt als je op de to-do **Opnieuw importeren** kiest. Je moet in de browser zijn ingelogd bij Facebook. Is dat niet zo, tik dan op de to-do op **Inloggen bij Facebook** en log daar in. Zodra je bent ingelogd, leest The Machine de pagina vanzelf. The Machine logt nooit voor je in.

Vrienden die niet in je Graph staan, worden geteld en er worden een paar namen getoond. Met **Als persoonlijke contacten toevoegen** voeg je ze allemaal tegelijk toe, ook nadat je op Opslaan hebt gedrukt. Iedereen krijgt een naam en verjaardag en wordt nooit gedeeld met een Werk-Fleet. Personen met een naam die al in je Graph staat, of die je eerder permanent hebt verwijderd, worden overgeslagen. Herinneringen voor verjaardagen krijg je alleen voor mensen aan wie je schrijft.

Met **Ongedaan maken** op de to-do verwijder je precies die personen weer, ook nadat je **Opnieuw importeren** hebt gebruikt.

**Abonnementen en proefperiodes** leest één keer per maand je ontvangstbewijzen, facturen en verlengingsmeldingen en zet je abonnementen in één to-do. Je ziet wat elk abonnement kost, wanneer de volgende betaling plaatsvindt en een waarschuwing als een proefperiode afloopt of de prijs stijgt. Alleen abonnementen waar de routine zeker van is, worden vermeld. Als er niets wordt gevonden, wordt er geen to-do aangemaakt.

Kies per abonnement **Houden** of **Opzeggen**. Over een abonnement dat je houdt, wordt je niet opnieuw gevraagd, tenzij de prijs verandert. Met **Opzeggen** krijg je de pagina om het abonnement op te zeggen of een conceptmail waarin je om opzegging vraagt. Die mail wordt pas verstuurd als jij hem verstuurt. Tussen de maandelijkse controles door controleert de routine elke dag of een proefperiode of verlenging binnen 7 dagen wordt afgeschreven. Zo ja, dan maakt hij een to-do aan.

**Contact houden** herinnert je af en toe eraan om contact op te nemen met iemand die je na aan het hart ligt, maar alleen als daar een goede reden voor is. Op de kaart kies je wie erbij hoort uit een korte lijst van mensen met wie je zelf al maandenlang over en weer schrijft. Verwijder iemand met ×.

Je krijgt alleen een herinnering als je veel langer dan normaal geen contact hebt gehad en er iets specifieks is om over te praten: nieuws dat die persoon heeft gedeeld, ook uit de samenvatting op diens pagina, een openstaande belofte of een bericht waarop je nooit hebt geantwoord.

Bij nieuws met een datum in de toekomst, zoals een verhuizing volgende maand, kijkt de routine vlak na die datum opnieuw naar het nieuws en de meest recente berichten. Het resultaat is één to-do met de reden en een kort bericht als concept op de plek waar je meestal met die persoon praat, in diens taal. Het bericht wordt pas verstuurd als jij het verstuurt. Als er niets te zeggen valt, wordt er geen to-do aangemaakt.

De routine stuurt hooguit twee herinneringen per week en één per persoon per maand. Ook stuurt hij geen herinnering naar iemand met wie je kort geleden contact had. Met **Niet nodig** bij een herinnering wacht de routine langer voordat hij die persoon opnieuw voorstelt. Elke keer wordt die wachttijd langer. Er worden nooit meldingen verstuurd. De routine blijft Persoonlijk: hij wordt nooit gedeeld met een Werk-Fleet en gebruikt nooit informatie uit je Werk-accounts.

**Tweedehandsvondsten** houdt een zoekopdracht op een tweedehandssite in de gaten, zoals Marktplaats, Vinted, eBay of Facebook Marketplace. Zoek daar met de filters die je wilt, kopieer het adres van de resultaten en plak het na **Toevoegen**. Je kunt naar wens filters in je eigen woorden toevoegen, zoals “onder 300, binnen 30 km, geen ‘voor onderdelen’”. Elke zoekopdracht is een aparte routine. Voeg hem opnieuw toe voor een volgende zoekopdracht.

Elke 3 uur opent de routine de zoekopdracht in de eigen browser van The Machine en zoekt hij naar advertenties die hij nog niet eerder heeft gezien. Eerst worden de prijs, afstand en woorden die je hebt uitgesloten gecontroleerd met gewone code.

Elke nieuwe advertentie die door die controle komt, wordt geopend. Je AI beoordeelt de staat aan de hand van de foto en beschrijving, en de verkoper aan de hand van diens reviews, beoordeling en accountleeftijd. De beste advertenties komen in één to-do, elk met een foto, titel, prijs en oordeel van één regel. Tik op een advertentie om die in de browser van The Machine te openen.

Zolang de to-do openstaat, worden nieuwe vondsten bovenaan toegevoegd, loopt het aantal op en krijg je opnieuw een melding. Goede deals zijn vaak snel weg. Markeer de to-do als gedaan en de volgende vondst komt in een nieuwe to-do. Een uitvoering zonder goede vondsten verandert niets.

De routine houdt het beleefd en goedkoop: per uitvoering wordt de zoekopdracht één keer gelezen, worden hooguit 6 advertenties geopend met een pauze ertussen en worden per dag hooguit 40 advertenties gecontroleerd voor al je zoekopdrachten samen. Elke controle bestaat uit één korte vraag aan je AI met één foto. De eerste uitvoering controleert de nieuwste advertenties en markeert de rest als gezien. Latere uitvoeringen tonen daardoor alleen nieuwe advertenties.

Als de site je vraagt om in te loggen, een robotcontrole toont of het lezen blokkeert, staat dat in een to-do. Kies **Openen** om de site te bekijken in de browser van The Machine. Log daar zelf in of voer de controle uit. Bij de volgende uitvoering leest de routine de site opnieuw. The Machine logt nooit voor je in en voert nooit een controle voor je uit. Hij neemt ook nooit contact op met een verkoper, biedt nooit ergens op en koopt nooit iets.

Met **Zoekopdracht wijzigen** op de kaart van de routine pas je het adres of de filters aan. Met **Wanneer wijzigen** stel je een ander ritme in, zoals “elke 6 uur”.

**Nabestellingen** leest de orderbevestigingen van webwinkels in je mail en herkent producten die je steeds opnieuw koopt, zoals koffie, dierenvoer of vitamines. Als je een product waarschijnlijk opnieuw nodig hebt, maakt de routine een to-do aan met het product, de winkel, de laatste prijs en wanneer je het voor het laatst hebt gekocht. **Openen in de winkel** brengt je naar de productpagina, waar je het zelf kunt kopen. Er wordt niets voor je gekocht.

De routine heeft minstens drie bestellingen van hetzelfde product met een regelmatig interval nodig. Daardoor wordt er geen to-do aangemaakt voor een eenmalige aankoop of een ongebruikelijk lange tussenpoos. Voorlopig worden alleen winkels gelezen die Shopify gebruiken. Je AI leest per uitvoering alleen nieuwe bestelmails van die winkels, in één korte vraag. Deze to-do's sturen nooit een melding. Als je het product opnieuw bestelt, wordt de openstaande to-do gesloten.

Zolang de routine van een sjabloon de woorden van het sjabloon gebruikt, draait hij op eigen code, zonder je AI-abonnement. Spam opruimen laat bijvoorbeeld eerst in code nieuwe mails van onbekende afzenders zien en stelt je AI alleen een korte vraag als er mails zijn. Contact houden vraagt alleen iets over de een of twee personen die de routine heeft geselecteerd. Als je een nieuwe naam geeft, blijft dat zo. Zodra je de woorden aanpast, wordt de routine uitgevoerd zoals elke andere routine, op basis van jouw woorden.

Nieuwsbrieven opruimen en Spam opruimen leveren nog steeds dezelfde to-do op, met een keuze per mail. Een aangepaste versie van Verjaardagen geeft het resultaat en hooguit één concept, geen aparte to-do per persoon. Met **Terug naar het sjabloon** in **Bewerken** zet je de oorspronkelijke woorden terug.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat hij nodig heeft, zoals je berichten, meetings en de Graph, en zet hij het resultaat op de pagina Routines. Elk resultaat heeft de status **Klaargezet**, **Niets nieuws** (met uitleg) of **Lukte niet** (met uitleg). Een uitvoering die eindigt zonder resultaat telt als mislukt, nooit als voltooid.

Routines lezen alleen: je berichten, webpagina's, GitHub en sites zoals X in de browser. Ze versturen geen berichten, antwoorden niet, plaatsen niets en veranderen niets. Ze openen pagina's die ze vinden in wat ze lezen of in een zoekopdracht, gewone webadressen en bekende sites. Ze openen nooit een adres dat speciaal is gemaakt om de gelezen informatie mee te geven. Alleen een sjabloon kan mails aanpassen, en alleen wat je bevestigt in de bijbehorende to-do.

Als een routine een bericht of post zou moeten versturen, doet hij alles tot aan die stap en toont hij het concept, bijvoorbeeld **Zou plaatsen op X:**. Na een echte uitvoering krijg je het als to-do om goed te keuren. Bij een testrun wordt het alleen getoond.

De naam beschrijft waar de routine over gaat en waar het resultaat terechtkomt. Met **Van je routine** eronder open je de routine zelf. De knop beschrijft de stap, bijvoorbeeld **Bericht voorbereiden**. Daarmee wordt het bericht klaargezet, maar niet geplaatst. Je plaatst het vanuit het resultaat. Als The Machine het niet voor je kan plaatsen, opent de knop de pagina waar je dat zelf kunt doen.

De to-do begint in het gebied van het account van waaruit het bericht wordt verstuurd, zoals Werk voor het X-account van je bedrijf. Je hoeft hem dus nooit te verplaatsen.

Een uitvoering kan gebruikmaken van je ingeschakelde [skills](skills.md), afhankelijk van wat de routine doet. Alleen passende skills worden helemaal gelezen. Het resultaat vermeldt ze onder **Gebruikt:**. Een skill zorgt er nooit voor dat een routine iets verstuurt of verandert.

Je routines staan onder **Je routines**, onder eventuele suggesties. Lange resultaten worden ingeklapt tot een korte voorbeeldweergave. Met **Meer tonen** of door erop te tikken, open je het hele resultaat.

Elke uitvoering kent het vorige resultaat, zodat de routine kan aangeven wat er sindsdien is veranderd.

Na een geslaagde uitvoering kan je Machine zelf een recept schrijven voor leeswerk dat elke keer hetzelfde is, zoals welke mails of GitHub-wijzigingen hij moet bekijken. Bij volgende uitvoeringen wordt dat eerst met gewone code gelezen. De AI kiest alleen wat belangrijk is en schrijft het resultaat, met minder tokens. Een recept leest alleen. Als het niet meer werkt, voert de routine het leeswerk zelf uit en repareert hij het recept. Je vindt het onder **Geavanceerd: scriptstappen** in het menu ⋯.

## Gemiste dagen

Als je Machine uitstaat of bezig is, worden gemiste uitvoeringen niet opgestapeld. Alleen de meest recente uitvoering wordt één keer uitgevoerd. Elke datum wordt één keer verwerkt, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als er weinig gebruik over is van je AI-abonnement, net als al het achtergrondwerk. Met **Nu uitvoeren** start je de routine meteen. Het resultaat verschijnt op de kaart zodra het klaar is.

## Aanpassen of stoppen

Deze opties staan in het menu ⋯ van de routine. Met **Bewerken** pas je de naam en de werking aan. Wanneer de routine wordt uitgevoerd en de resultaten tot nu toe blijven behouden. Met **Wanneer wijzigen** stel je een nieuw ritme in je eigen woorden in, zoals "elke werkdag om 8 uur". Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het venster klikken om te annuleren.

In **Bewerken** voert **Probeer het** de nieuwe woorden één keer uit en toont het resultaat daar. De routine blijft ongewijzigd totdat je op **Opslaan** drukt.

Met **Pauzeren** worden uitvoeringen stopgezet totdat je op de kaart op **Hervatten** drukt. Gepauzeerde routines staan onder **Gepauzeerd**, onder je routines. Wat tijdens de pauze is overgeslagen, wordt daarna niet alsnog uitgevoerd. Met **Stoppen** beëindig je een routine definitief.

Je kunt maximaal 20 routines hebben, inclusief gepauzeerde routines. Stop een routine om er een toe te voegen.

Als je **Wijzigingen vragen** gebruikt bij de to-do van een routine, of iets in de chat schrijft dat voor elke uitvoering geldt, zoals "gebruik nooit emoji's", stelt de to-do **Ook de routine aanpassen** voor. Die optie staat op de to-do en in de chat onder het antwoord. Je ziet welke woorden van de routine worden aangepast. De routine verandert pas als je op **Aanpassen** drukt. Met **Zo laten** blijft alles hetzelfde. Voor een wijziging die alleen voor dat concept geldt, wordt dit niet voorgesteld.

## Geavanceerd: scriptstappen

Een script is niet nodig. Beschrijf in je eigen woorden wat een routine moet doen, dan bedenkt je Machine de rest.

Voor gevorderde gebruikers kan een routine ook eigen opdrachten op je Machine uitvoeren. Kies daarvoor **Geavanceerd: scriptstappen** in het menu ⋯. **Bewerken** toont de scriptstappen alleen als de routine er al heeft. Met **Gegevens ophalen** voert de routine eerst een opdracht uit in de bijbehorende map, of in je thuismap als er geen map is opgegeven, gedurende maximaal het ingestelde aantal seconden. De uitvoer wordt doorgegeven aan de routine. Als er geen verdere instructies zijn, is de uitvoer het resultaat.

**Controle** ontvangt het resultaat na de uitvoering als invoer. Als de opdracht met een fout eindigt, toont de uitvoering **Lukte niet**, met de melding van de controle. Als een opdracht voor Gegevens ophalen mislukt, wordt dat op dezelfde manier getoond.

Een opdracht bestaat uit één regel en wordt zonder shell uitgevoerd: je kunt geen pipes of variabelen gebruiken. Scriptstappen zijn van jou en worden alleen op je dashboard ingesteld. Een testrun en **Probeer het** voeren ook Gegevens ophalen uit en geven dat aan. Ze versturen of bewaren nog steeds niets. Een routine verstuurt nooit iets, dus een scriptstap mag alleen lezen.

## Van je OpenClaw-taken

Als je eerder geplande taken in OpenClaw hebt gemaakt, leest je Machine ze en laat hij de taken zelf ongemoeid. Hij stelt de taken die geschikt zijn voor als routines onder **Voorgesteld**. Elke taak is één keer uitgevoerd, zodat je een echt resultaat ziet.

Je correcties aan de taak blijven behouden. Wat de taak heeft verstuurd of geplaatst, wordt weggelaten. Als een taak een script uitvoerde of gegevens las die een scripttaak had verzameld, wordt dat als Gegevens ophalen meegenomen. Met **Toevoegen** maak je er een routine van. Met **Nee, bedankt** vraagt The Machine niet opnieuw naar die taak. Een taak die je aan iets herinnerde, wordt op To-do's aangeboden als terugkerende to-do.

Voordat je een suggestie toevoegt, kun je die via **Bewerken** en **Wanneer wijzigen** in het menu ⋯ aanpassen, net als elke andere routine. Met **Opnieuw uitvoeren** voer je de taak nu uit met de huidige woorden, zodat je nieuwere resultaten kunt bekijken, bijvoorbeeld na een rustig weekend. De routine leest alleen, wordt één keer per tik uitgevoerd en het nieuwe resultaat vervangt het oude.

Er staan maximaal drie suggesties tegelijk klaar. Na een week met geslaagde uitvoeringen vraagt de routine **De oude OpenClaw-taak uitzetten?** De taak wordt alleen uitgezet als je op **Uitzetten** drukt. Je kunt hem daarna in OpenClaw weer aanzetten. Met **Houden** blijven beide routines actief.

## Op basis van wat je doet

Je Machine merkt ook werk op dat je regelmatig doet en stelt het voor als routine onder **Voorgesteld**, ook zonder OpenClaw. Hij let op:

- dezelfde opdracht drie keer of vaker achter elkaar, zoals "geef elke maandag een overzicht van de openstaande supporttickets";
- een mail die je regelmatig verstuurt, zoals een wekelijks rapport aan je team;
- nieuwsbrieven en updatemails die elke week binnenkomen;
- een druk Slack-kanaal waarin anderen elke week schrijven;
- mails die je één voor één naar dezelfde persoon doorstuurt, zoals mails van school of de club naar je partner. Een wekelijks overzicht voor die persoon bespaart je het doorsturen;
- hetzelfde verzoek dat je regelmatig beantwoordt, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Bij elke suggestie staat wat de routine heeft gezien, zoals "4 keer achter elkaar gevraagd" of "6 mails in 3 weken doorgestuurd naar Sam". De routine is één keer uitgevoerd, zodat je een echt resultaat ziet. Denk bijvoorbeeld aan een samenvatting voor je team, een briefing voor een wekelijks gesprek, een overzicht van support of development, een stand van zaken over je cijfers of een overzicht van nieuwsbrieven die je ontvangt.

Alleen iets specifieks dat duidelijk nuttig voor je is, wordt voorgesteld. Een nieuwsoverzicht gaat bijvoorbeeld alleen over je eigen nieuwsbrieven, nooit over algemeen nieuws. Als niets geschikt is, wordt er geen suggestie getoond.

Je Machine controleert dit hooguit één keer per dag en doet hooguit één nieuwe suggestie per week, zonder melding. Met **Nee, bedankt** wordt die suggestie niet opnieuw getoond. Doorgestuurde mails en antwoorden blijven bij het account waarmee ze zijn verstuurd, zodat Werk en Persoonlijk niet door elkaar lopen. Alles blijft op je Machine. Een to-do die je regelmatig afsluit, wordt in plaats daarvan aangeboden als terugkerende to-do.

## Routines en terugkerende to-do's

Een [terugkerende to-do](recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelfstandig uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor "betaal de huur op de eerste van de maand" en een routine voor "laat me elke vrijdag weten welke deals stil zijn gevallen".
