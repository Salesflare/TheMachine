---
title: Routines
area: cards
summary: Werk dat je Machine zelfstandig en volgens een vast ritme uitvoert, zoals elke maandag een overzicht van je openstaande deals. Hij leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: b5704836b00227a5
---
## Een routine maken

Open **Routines** in de zijbalk en beschrijf in één regel wat de routine moet doen en wanneer: ‘elke maandag om 9 uur mijn openstaande deals samenvatten’ of ‘elke werkdag ’s ochtends de mails opsommen waarop ik nog moet antwoorden’. Klik daarna op **Toevoegen**.

Als je geen tijd opgeeft, wordt de routine om 8.00 uur uitgevoerd. De tijd is gebaseerd op de klok van je Machine. De eerste keer dat de routine wordt uitgevoerd, krijgt hij een korte naam.

Met **Toevoegen** wordt eerst een test uitgevoerd, zodat je kunt zien wat de routine oplevert voordat je hem bewaart. Er wordt niets verstuurd of opgeslagen. Daarna zorgt **Toevoegen** ervoor dat de routine volgens het ritme wordt uitgevoerd. Met **Wijzigen** probeer je andere woorden of een nieuwe naam. Met **Annuleren** verwijder je de routine.

## Sjablonen

Onder **Sjablonen** onderaan bij Routines kun je met **Toevoegen** een kant-en-klare routine inschakelen. Hij wordt meteen één keer uitgevoerd en daarna elke ochtend om 7.30 uur (Spam opruimen elk uur, Tweedehandsvondsten elke 3 uur, Abonnementen en proefperiodes één keer per maand). Op de kaart staat de tekst van de routine, net als bij andere routines. Met **Bewerken** wijzig je de tekst of de naam.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen uitstaat (25 of meer in een week, van minstens 5 afzenders), staat er boven je to-do's hoeveel nieuwsbrieven je hebt ontvangen en wat de routine ermee zou doen. Je kunt kiezen voor **Aanzetten** of **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier aangeboden als er in een week minstens 5 mails handmatig naar spam zijn verplaatst. Met **Aanzetten** voeg je de routine toe, net als met **Toevoegen** hierboven. Als je **Nee, bedankt** kiest, wordt de routine niet meer aangeboden. Een sjabloon dat je al eerder had, wordt nooit aangeboden.

**Nieuwsbrieven opruimen** maakt één to-do per onderdeel (werk en privé) met de nieuwsbrieven van de afgelopen dag. Bij elke nieuwsbrief kun je kiezen voor **Houden** of **Afmelden**. Afmelden gebeurt via de afmeldlink van de mailinglijst, of via een afmeldmail vanaf jouw adres als versturen aanstaat. Anders meldt The Machine zich af via de pagina van de mailinglijst in zijn eigen browser. Een eventuele login, captcha of keuze op die pagina moet je zelf afhandelen. In de regel staat waarom, met de optie **Afmeldpagina openen**.

Ontvangstbewijzen, bestellingen en betaalmeldingen worden overgeslagen. Mails die via een groepsadres zijn binnengekomen, zoals een Google Group, staan op naam van de afzender en leiden nooit tot afmelding van de groep. Als de afzender geen eigen afmeldmogelijkheid heeft, staat er **Zelf afmelden** in de regel.

**Spam opruimen** maakt één to-do per onderdeel met mails van onbekende afzenders die op spam lijken. Je kunt per mail kiezen voor **Spam** of **Geen spam**. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert de mail als spam. De routine controleert elk uur, zodat spam er meestal al staat voordat je erbij bent. Nieuwe spam wordt toegevoegd aan dezelfde to-do zolang die openstaat.

Gmail dat alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan geen mails naar spam verplaatsen. Daar geeft **Spam** een link waarmee je de mail in Gmail kunt markeren. The Machine onthoudt de afzender dan als spam. Als er geen mailaccount is gekoppeld, staat er **Mail koppelen** in plaats van **Toevoegen**.

Een afzender is onbekend als je die persoon nooit hebt gemaild. Een ‘Re:’ telt alleen als gesprek in een thread waarin jij zelf hebt geschreven. Als er opnieuw mail binnenkomt van een afzender die je als spam hebt gemarkeerd, op de to-do of in je mailbox, staat die op de volgende to-do met de melding **Eerder als spam gemarkeerd**. Mails die je zelf naar spam hebt verplaatst, helpen de routine ook om vergelijkbare mails te herkennen.

Er verandert pas iets als je het bevestigt op de to-do. Tik op een afzender om eerst de mail te lezen: hij blijft ongelezen en er verandert niets. Bij Spam opruimen worden afbeeldingen van internet niet geladen, zodat de afzender niet kan zien dat de mail is geopend. Er wordt je niet opnieuw gevraagd wat je met afzenders hebt gedaan. Op een dag zonder nieuwsbrieven of spam wordt er geen to-do gemaakt. Deze to-do's sturen nooit een melding.

Als je voor alle afzenders een keuze hebt gemaakt, staat op de to-do dat je klaar bent en verschijnt **Als gedaan markeren**.

Met **Dagelijks overzicht** krijg je één keer per dag één to-do met de paar onderdelen uit nieuwsbrieven die je tijd waard zijn. Bij elk onderdeel staat in één regel waarom het voor jou belangrijk is. Tik erop om de mail te lezen of kies **Openen in je mail**. Alleen nieuwsbrieven: nooit mails van mensen, ontvangstbewijzen of afzenders waarvoor je je hebt afgemeld. Ook wat je al hebt gelezen, wordt overgeslagen. Als niets opvalt, wordt er geen to-do gemaakt.

De routine leert waar je interesse in hebt op basis van wat je opent, met een ster markeert of als ongelezen archiveert, en van je keuzes voor **Meer zoals dit** en **Minder zoals dit** bij elk onderdeel. De onderwerpen waarop hij let, staan op de routinekaart onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg er zelf een toe. Onderwerpen met een stippellijn heeft de routine zelf geleerd. Een nieuw overzicht vervangt het overzicht dat nog openstaat. Er wordt nooit een melding verstuurd.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief. Daarna stelt hij je AI er één korte vraag over, met een dagelijkse limiet, zodat het goedkoop blijft. Met **Wanneer wijzigen** stel je het tijdstip in. Zodra je de tekst wijzigt, werkt de routine zoals elke andere routine op basis van jouw tekst.

Met **Verjaardagen** wordt voor elke goede bekende die vandaag jarig is een to-do gemaakt: mensen aan wie je zelf schrijft, zoals vrienden, familie en vaste contacten. Bij elke persoon staat een korte felicitatie, opgesteld op de plek waar je meestal met diegene praat, zoals diens WhatsApp-chat of jullie e-mailthread, en in diens taal. De felicitatie wordt pas verstuurd als jij dat doet. Op een dag zonder verjaardagen wordt er geen to-do gemaakt.

Verjaardagen komen uit je agenda’s (de verjaardagsevenementen en verjaardagskalender van Google, die elke ochtend worden gelezen, ook als ze niet zijn gesynchroniseerd, en de verjaardagskalender van Outlook), je Google-contacten op een zelf gehoste Machine en een datumveld met de naam Verjaardag bij een persoon in de Graph. Als er nog nergens een verjaardag staat, vermeldt het resultaat **Nog geen verjaardagen bekend** en hoe je die kunt toevoegen.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen is ingeschakeld, biedt een to-do aan om de verjaardagenpagina van Facebook te lezen. Tik op **Importeren**. The Machine opent de pagina in zijn browser, scrolt totdat alle maanden zijn geladen en leest de namen en verjaardagen van je vrienden. Je ziet hoeveel verjaardagen zijn gevonden en wie overeenkomt met mensen in je Graph op basis van voor- en achternaam. Namen die bij meer dan één persoon horen, worden overgeslagen en vermeld.

Alleen met **Opslaan** worden de gegevens bewaard, op de pagina van elke persoon: de verjaardag en de profielfoto van Facebook voor iemand die nog geen foto heeft. Een verjaardag of foto die je daar instelt, blijft staan. Een foto die iemand al heeft, wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

De routine leest de gegevens niet vanzelf opnieuw. Dat gebeurt wel als je op de to-do **Opnieuw importeren** kiest. In de browser moet je bij Facebook zijn ingelogd. Zo niet, tik dan op de to-do op **Inloggen bij Facebook** en log daar in. Zodra je bent ingelogd, leest de routine de pagina vanzelf. The Machine logt nooit voor je in.

Vrienden die niet in je Graph staan, worden geteld en er worden een paar namen getoond. Met **Voeg … toe als privécontacten** voeg je ze allemaal tegelijk toe, ook nadat je op Opslaan hebt getikt. Voor elke persoon worden de naam en verjaardag opgeslagen. Ze worden nooit gedeeld met een Werk-Fleet. Mensen met een naam die al voorkomt in je Graph, of die je definitief hebt verwijderd, worden overgeslagen. Je krijgt alleen verjaardagsherinneringen voor mensen aan wie je zelf schrijft.

Met **Ongedaan maken** op de to-do verwijder je precies die mensen weer, ook nadat je **Opnieuw importeren** hebt gebruikt.

**Abonnementen en proefperiodes** leest één keer per maand je ontvangstbewijzen, facturen en verlengingsberichten en zet je abonnementen bij elkaar in één to-do. Je ziet per abonnement wat het kost, wanneer het opnieuw wordt afgeschreven en een melding als een proefperiode eindigt of de prijs stijgt. Alleen abonnementen waarover de routine zeker is, worden vermeld. Als er niets wordt gevonden, wordt er geen to-do gemaakt.

Kies per abonnement **Houden** of **Opzeggen**. Je wordt niet opnieuw gevraagd naar een abonnement dat je wilt houden, tenzij de prijs verandert. Met **Opzeggen** krijg je de opzeggingspagina of een conceptbericht waarin je om opzegging vraagt. Dat bericht wordt pas verstuurd als jij dat doet. Tussen de maandelijkse controles door wordt elke dag gecontroleerd. Er wordt een to-do gemaakt als een proefperiode of verlenging binnen 7 dagen wordt afgeschreven.

**Contact houden** herinnert je af en toe eraan om contact op te nemen met iemand die je na aan het hart ligt, maar alleen als daar een goede reden voor is. Kies op de routinekaart wie erbij hoort uit een korte lijst met mensen met wie je zelf al maandenlang over en weer schrijft. Verwijder iemand met ×.

Je krijgt alleen een herinnering als je veel langer dan gebruikelijk geen contact hebt gehad én er iets specifieks is om te zeggen: nieuws dat iemand heeft gedeeld, een belofte die nog openstaat of een bericht waarop je nooit hebt geantwoord. De herinnering is één to-do met de reden en een kort bericht, opgesteld op de plek waar je meestal met diegene praat en in diens taal. Het bericht wordt pas verstuurd als jij dat doet. Als er niets te zeggen is, wordt er geen to-do gemaakt.

Je krijgt hooguit twee herinneringen per week, maximaal één per persoon per maand, en geen over iemand met wie je onlangs contact had. Met **Niet nodig** bij een herinnering wacht de routine langer voordat hij die persoon opnieuw voorstelt. Elke keer wordt die wachttijd langer. Er wordt nooit een melding verstuurd en de routine blijft privé. Hij wordt nooit gedeeld met een Werk-Fleet.

**Tweedehandsvondsten** houdt een zoekopdracht op een tweedehandssite in de gaten, zoals Marktplaats, Vinted, eBay of Facebook Marketplace. Zoek daar met de gewenste filters, kopieer het adres van de resultaten en plak het na **Toevoegen**. Voeg desgewenst filters in je eigen woorden toe, zoals ‘onder 300, binnen 30 km, geen “voor onderdelen”’. Elke zoekopdracht is een eigen routine. Voeg de routine dus opnieuw toe voor een volgende zoekopdracht.

Elke 3 uur opent de routine de zoekopdracht in de eigen browser van The Machine en zoekt hij naar advertenties die hij nog niet heeft gezien. Prijs, afstand en woorden die je hebt uitgesloten, worden eerst gecontroleerd met gewone code.

Elke nieuwe advertentie die aan de voorwaarden voldoet, wordt geopend. Je AI beoordeelt de staat aan de hand van de foto en beschrijving, en de verkoper aan de hand van diens reviews, beoordeling en accountleeftijd. De beste advertenties komen in één to-do te staan, elk met een foto, titel, prijs en oordeel in één regel. Tik op een advertentie om die in de browser van The Machine te openen.

Zolang de to-do openstaat, worden nieuwe vondsten bovenaan toegevoegd, loopt het aantal op en krijg je opnieuw een melding, omdat goede deals snel weg zijn. Markeer de to-do als gedaan en de volgende vondst komt in een nieuwe to-do. Als een uitvoering niets goeds oplevert, verandert er niets.

De routine blijft netjes en goedkoop: één keer per uitvoering wordt de zoekopdracht gelezen, er worden maximaal 6 advertenties per uitvoering geopend met een pauze ertussen en er worden maximaal 40 advertenties per dag gecontroleerd voor al je zoekopdrachten samen. Elke controle is één korte vraag aan je AI met één foto. Bij de eerste uitvoering worden de nieuwste advertenties gecontroleerd en wordt de rest als gezien gemarkeerd, zodat volgende uitvoeringen alleen nieuwe resultaten opleveren.

Als de site je vraagt om in te loggen, een robotcontrole toont of het lezen blokkeert, meldt een to-do dat. Kies **Openen** om de site in de browser van The Machine te bekijken. Log daar zelf in of voer zelf de controle uit. Bij de volgende uitvoering probeert de routine de pagina opnieuw te lezen. The Machine logt nooit voor je in en voert nooit een controle voor je uit. Hij neemt ook nooit contact op met een verkoper, biedt nooit en koopt nooit iets.

Met **Zoekopdracht wijzigen** op de routinekaart geef je een nieuw adres of andere filters op. Met **Wanneer wijzigen** stel je een ander ritme in, zoals ‘elke 6 uur’.

**Nabestellingen** leest orderbevestigingen van webwinkels in je mail en merkt op wat je steeds opnieuw koopt, zoals koffie, dierenvoer of vitamines. Als je iets waarschijnlijk binnenkort weer nodig hebt, maakt de routine een to-do met het artikel, de winkel, de laatste prijs en wanneer je het voor het laatst hebt gekocht. Met **Openen in de winkel** ga je naar de productpagina om het zelf te kopen. Er wordt niets voor je gekocht.

De routine heeft minstens drie bestellingen van hetzelfde artikel met een regelmatig interval nodig. Een eenmalige aankoop of een ongewoon lang interval leidt dus niet tot een to-do. Voorlopig leest de routine alleen webwinkels die Shopify gebruiken. Je AI leest alleen nieuwe bestelberichten van die winkels, met één korte vraag per uitvoering. Deze to-do's sturen nooit een melding. Als je het artikel opnieuw bestelt, wordt de openstaande to-do gesloten.

Zolang een sjabloonroutine de tekst van het sjabloon gebruikt, werkt hij met eigen code, zonder je AI-abonnement. Spam opruimen vermeldt bijvoorbeeld eerst nieuwe mails van onbekende afzenders met code en stelt je AI pas één korte vraag als dat nodig is. Contact houden vraagt alleen naar de één of twee personen die de routine heeft gekozen. Als je de tekst wijzigt, werkt de routine zoals elke andere routine op basis van jouw tekst.

Nieuwsbrieven opruimen en Spam opruimen leveren nog steeds dezelfde to-do op, met een keuze voor elke mail. Een aangepaste routine voor Verjaardagen geeft het resultaat en hooguit één concept, geen aparte to-do voor elke persoon. Met **Terug naar het sjabloon** in **Bewerken** herstel je de oorspronkelijke tekst van het sjabloon.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat nodig is, zoals je berichten, meetings en de Graph, en zet hij het resultaat op de pagina Routines. Elk resultaat heeft de status **Klaargezet**, **Niets nieuws** (met uitleg) of **Lukte niet** (met uitleg). Een uitvoering die eindigt zonder resultaat, telt als mislukt en nooit als voltooid.

Routines lezen alleen: je berichten, webpagina’s, GitHub en sites zoals X in de browser. Ze versturen, beantwoorden of plaatsen niets en veranderen niets. Ze openen pagina’s die ze vinden in wat ze lezen of in een zoekopdracht, gewone webadressen en bekende sites. Ze openen nooit een adres dat is verzonnen om gelezen inhoud mee te sturen. Alleen een sjabloon verandert mail, en alleen wat je bevestigt op de bijbehorende to-do.

Als een taak van een routine eindigt met een bericht of een post, voert de routine alles uit tot die stap en toont hij het concept, bijvoorbeeld **Zou op X plaatsen:**. Na een echte uitvoering krijg je het als to-do om goed te keuren. Bij een testuitvoering wordt het alleen getoond. De naam vermeldt waar de routine over gaat en waar het bericht naartoe gaat. De knop benoemt de stap, bijvoorbeeld **Plaatsen**. Met **Van je routine** eronder open je de routine.

De to-do komt terecht in het onderdeel van het account waarmee het bericht wordt verstuurd, bijvoorbeeld Werk voor het X-account van je bedrijf. Je hoeft hem dus nooit zelf te verplaatsen.

Een uitvoering kan de ingeschakelde [skills](skills.md) volgen die passen bij wat de routine doet. Alleen relevante skills worden volledig gelezen. De gebruikte skills staan onder **Gebruikt:**. Een skill zorgt er nooit voor dat een routine iets verstuurt of verandert.

Je routines staan onder **Je routines**, onder eventuele suggesties. Een lang resultaat wordt ingeklapt tot een korte voorbeeldweergave. Met **Meer tonen** of door erop te tikken, open je het volledige resultaat.

Elke uitvoering kent het vorige resultaat en kan daardoor vertellen wat er sindsdien is veranderd.

Na een geslaagde uitvoering kan je Machine zelf een recept schrijven voor het leeswerk dat elke keer hetzelfde is, zoals welke mails of GitHub-wijzigingen hij moet bekijken. Bij volgende uitvoeringen worden die eerst met gewone code gelezen. Daarna kiest de AI alleen wat belangrijk is en schrijft hij het resultaat, met minder tokens. Een recept leest alleen. Als het niet meer werkt, voert de routine het leeswerk zelf uit en herstelt hij het recept. Het recept staat onder **Geavanceerd: scriptstappen** in het menu ⋯.

## Gemiste dagen

Als je Machine uitstaat of bezig is, worden gemiste uitvoeringen niet opgestapeld. Alleen de nieuwste wordt één keer uitgevoerd. Elke datum wordt één keer uitgevoerd, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als er weinig gebruiksruimte over is in je AI-abonnement, net als al het achtergrondwerk. Met **Nu uitvoeren** start je de routine meteen. Het resultaat verschijnt op de kaart zodra het klaar is.

## Wijzigen of stoppen

Deze opties staan in het menu ⋯ van de routine. Met **Bewerken** wijzig je de naam en wat de routine doet. Het tijdstip en de eerdere resultaten blijven hetzelfde. Met **Wanneer wijzigen** stel je in je eigen woorden een nieuw ritme in, zoals ‘elke werkdag om 8 uur’. Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het venster klikken om te annuleren.

Met **Probeer het** in **Bewerken** voer je de nieuwe tekst één keer uit en zie je het resultaat daar. De routine blijft ongewijzigd totdat je op **Opslaan** tikt.

Met **Pauzeren** stop je de uitvoeringen totdat je op de kaart op **Hervatten** tikt. Gepauzeerde routines staan onder **Gepauzeerd**, onder je routines. Gemiste uitvoeringen tijdens de pauze worden niet later alsnog uitgevoerd. Met **Stoppen** beëindig je een routine definitief.

Je kunt maximaal 20 routines hebben, inclusief gepauzeerde routines. Stop een routine om er een toe te voegen.

Als je **Wijzigingen vragen** gebruikt bij de to-do van een routine, of een bericht schrijft in de chat van de routine, kan het zijn dat je opmerking voor elke uitvoering bedoeld is, zoals ‘gebruik nooit emoji’s’. In dat geval biedt de to-do, en ook de chat onder het antwoord, de optie **Ook de routine aanpassen**. Je ziet wat er in de tekst van de routine verandert. De routine wordt pas aangepast als je op **Aanpassen** tikt. Met **Zo laten** blijft alles ongewijzigd. Als je alleen het concept wilt aanpassen, wordt deze optie niet aangeboden.

## Geavanceerd: scriptstappen

Een script is niet nodig. Beschrijf in je eigen woorden wat de routine moet doen, dan bedenkt je Machine de rest.

Gevorderde gebruikers kunnen een routine ook eigen opdrachten op hun Machine laten uitvoeren. Kies daarvoor in het menu ⋯ **Geavanceerd: scriptstappen**. **Bewerken** toont de stappen alleen als een routine er al heeft. Met **Gegevens ophalen** wordt eerst een opdracht uitgevoerd, in de map van de routine of, als die leeg is, in je thuismap. De opdracht wordt maximaal het ingestelde aantal seconden uitgevoerd. De uitvoer wordt aan de routine doorgegeven. Als er geen tekst is opgegeven, wordt de uitvoer het resultaat.

Met **Controle** wordt het resultaat na de uitvoering als invoer doorgegeven. Als de opdracht eindigt met een fout, geeft de uitvoering **Lukte niet** weer, met de melding van de controle. Als een opdracht voor Gegevens ophalen mislukt, wordt dat op dezelfde manier getoond.

Een opdracht bestaat uit één regel en wordt zonder shell uitgevoerd. Pipes en variabelen zijn niet toegestaan. Scriptstappen zijn van jou en worden alleen op je dashboard ingesteld. Bij een testuitvoering en **Probeer het** wordt Gegevens ophalen ook uitgevoerd en zie je dat. Er wordt nog steeds niets verstuurd of bewaard. Een routine verstuurt nooit iets, dus een scriptstap mag alleen lezen.

## Vanuit je OpenClaw-taken

Als je eerder geplande taken in OpenClaw hebt gemaakt, leest je Machine die in (hij verandert ze nooit) en biedt hij passende taken als routines aan onder **Voorgesteld**. Elke taak is één keer uitgevoerd, dus je ziet een echt resultaat.

Je aanpassingen aan de taak blijven behouden. Wat de taak heeft verstuurd of geplaatst, wordt weggelaten. Een taak die een script uitvoerde of gegevens las die door een scripttaak waren verzameld, neemt dat mee als Gegevens ophalen. Met **Toevoegen** maak je er een routine van. Met **Nee, bedankt** wordt er nooit meer naar die taak gevraagd. Een taak die je eraan herinnerde iets te doen, wordt in plaats daarvan als een terugkerende to-do aangeboden onder To-do's.

Voordat je een suggestie toevoegt, kun je die aanpassen zoals elke andere routine. Gebruik daarvoor **Bewerken** of **Wanneer wijzigen** in het menu ⋯. Met **Opnieuw uitvoeren** voer je de taak meteen uit met de huidige tekst, zodat je nieuwere resultaten kunt bekijken, bijvoorbeeld na een rustig weekend. De taak leest alleen, wordt één keer per tik uitgevoerd en het nieuwe resultaat vervangt het oude.

Er staan maximaal drie suggesties tegelijk klaar. Na een week met geslaagde uitvoeringen vraagt de routine **De oude OpenClaw-taak uitzetten?**. De taak wordt alleen uitgezet als je op **Uitzetten** tikt. Je kunt hem daarna in OpenClaw weer aanzetten. Met **Houden** blijven beide actief.

## Op basis van je werk

Je Machine merkt ook werk op dat je volgens een vast ritme doet en biedt dat als routine aan onder **Voorgesteld**, ook als je OpenClaw niet gebruikt. Hij let op:

- dezelfde opdracht die je drie keer of vaker achter elkaar geeft, zoals ‘de openstaande supporttickets samenvatten’ elke maandag;
- een mail die je volgens een vast ritme verstuurt, zoals een wekelijks rapport aan je team;
- nieuwsbrieven en update-mails die elke week terugkomen;
- een druk Slack-kanaal waarin anderen elke week schrijven;
- mails die je één voor één doorstuurt naar dezelfde persoon, zoals mails van school en een club naar je partner. Een wekelijks overzicht bespaart je het doorsturen;
- hetzelfde verzoek waarop je volgens een vast ritme antwoordt, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Bij elke suggestie staat wat de routine heeft opgemerkt, zoals ‘4 keer achter elkaar gevraagd’ of ‘6 mails in 3 weken doorgestuurd naar Sam’. De routine is één keer uitgevoerd, zodat je een echt resultaat ziet. Denk bijvoorbeeld aan een samenvatting voor je team, een korte voorbereiding op een wekelijks gesprek, een support- of ontwikkeloverzicht, een stand van zaken over je cijfers of een overzicht van je nieuwsbrieven.

De routine stelt alleen iets voor als het specifiek voor jou is en duidelijk nuttig. Een nieuwsoverzicht bevat bijvoorbeeld alleen je eigen nieuwsbrieven, nooit een algemeen overzicht. Als niets past, wordt er geen suggestie gedaan.

De routine controleert dit maximaal één keer per dag en doet maximaal één nieuwe suggestie per week, zonder melding. Met **Nee, bedankt** wordt die suggestie nooit opnieuw getoond. Doorgestuurde mails en antwoorden blijven bij het account waarmee ze zijn verstuurd, zodat Werk en Privé niet door elkaar lopen. Alles blijft op je Machine. Een to-do die je regelmatig afsluit, wordt in plaats daarvan aangeboden als terugkerende to-do.

## Routines en terugkerende to-do's

Een [terugkerende to-do](recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelfstandig uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor ‘huur betalen op de eerste dag van de maand’ en een routine voor ‘vertel me elke vrijdag welke deals zijn stilgevallen’.
