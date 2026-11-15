---
title: Routines
area: cards
summary: Werk dat je Machine zelfstandig en op vaste momenten uitvoert, zoals elke maandag een overzicht van je openstaande deals. Hij leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in
translated: 2be351a9cef42215
---
## Een routine maken

Open **Routines** in de zijbalk en zeg in één regel wat de routine moet doen en wanneer: "elke maandag om 9 uur, geef een overzicht van mijn openstaande deals" of "elke werkdag ’s ochtends, geef een lijst van de mails waarop ik nog moet antwoorden". Klik daarna op **Toevoegen**.

Zonder tijdstip wordt de routine om 8.00 uur uitgevoerd. De tijd is gebaseerd op de klok van je Machine. De eerste keer krijgt de routine een korte naam.

Met **Toevoegen** wordt eerst een test uitgevoerd, zodat je ziet wat de routine oplevert voordat je hem bewaart. Er wordt niets verstuurd of opgeslagen. Daarna zorgt **Toevoegen** ervoor dat de routine op vaste momenten wordt uitgevoerd. Met **Wijzigen** kun je andere woorden of een nieuwe naam proberen, en met **Annuleren** verwijder je de routine.

## Sjablonen

Onder **Sjablonen** onderaan Routines kun je met **Toevoegen** een kant-en-klare routine inschakelen. Die wordt meteen één keer uitgevoerd en daarna elke ochtend om 7.30 uur. Spam opruimen wordt elk uur uitgevoerd en Abonnementen en proefperiodes één keer per maand. Op de kaart staan de woorden van de routine, net als bij elke andere routine. Met **Bewerken** kun je die woorden of de naam aanpassen.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen uitstaat (25 of meer in een week, van minstens 5 afzenders), staat er boven je to-do's een regel met het aantal nieuwsbrieven en wat de routine ermee zou doen, met **Zet het aan** en **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier aangeboden wanneer je in een week 5 of meer mails handmatig naar spam hebt verplaatst. Met **Zet het aan** voeg je de routine toe, net als met **Toevoegen** hier. Als je op **Nee, bedankt** klikt, wordt de routine niet opnieuw aangeboden. Een sjabloon dat je eerder hebt gehad, wordt ook nooit opnieuw aangeboden.

**Nieuwsbrieven opruimen** maakt één to-do per gebied (werk en persoonlijk) met de nieuwsbrieven van de afgelopen dag. Bij elke nieuwsbrief kun je **Houden** of **Afmelden** kiezen. Met Afmelden gebruikt de routine de eenkliklink van de mailinglijst, of verstuurt hij een afmeldmail vanaf jouw adres als mail versturen is ingeschakeld. Anders meldt The Machine je af via de pagina van de mailinglijst in zijn eigen browser. Als je daar moet inloggen, een captcha moet invullen of keuzes moet maken, moet je dat zelf doen. In de regel staat waarom, met **Afmeldpagina openen**.

Bonnetjes, bestellingen en betaalmeldingen worden overgeslagen. Mails die via een groepsadres zijn binnengekomen, zoals een Google Group, worden weergegeven onder de naam van de afzender. Je wordt nooit afgemeld voor de groep. Als de afzender geen eigen afmeldmogelijkheid heeft, staat bij de mail **Zelf afmelden**.

**Spam opruimen** maakt één to-do per gebied met mails van onbekende afzenders die op spam lijken. Bij elke mail kun je **Spam** of **Geen spam** kiezen. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert die als spam. De routine controleert elk uur, dus spam staat er meestal al voordat jij eraan toekomt. Nieuwe spam wordt aan dezelfde to-do toegevoegd zolang die openstaat.

Als Gmail alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan de routine geen mail naar spam verplaatsen. Daar geeft **Spam** een link waarmee je de mail in Gmail kunt markeren, en onthoudt The Machine de afzender als spam. Als er geen mailaccount is gekoppeld, staat bij het sjabloon **Mail koppelen** in plaats van **Toevoegen**.

Een afzender is onbekend als je diegene nooit hebt gemaild. Een "Re:" telt alleen als een gesprek in een thread waaraan jij hebt geschreven. Als er toch weer mail binnenkomt van een afzender die je als spam hebt gemarkeerd, in de to-do of in je mailbox, staat die in de volgende to-do met **Eerder als spam gemarkeerd**. Mail die je zelf naar spam hebt verplaatst, helpt de routine ook vergelijkbare mail te herkennen.

Er verandert niets totdat je je keuze in de to-do bevestigt. Tik op een afzender om eerst de mail te lezen: de mail blijft ongelezen en er verandert niets. In Spam opruimen worden afbeeldingen van het web niet geladen, zodat de afzender niet kan zien dat de mail is geopend. Er wordt niet opnieuw naar afzenders gevraagd waarover je al een keuze hebt gemaakt. Op een dag zonder nieuwsbrieven of spam wordt er geen to-do gemaakt. Deze to-do's sturen nooit een melding.

Als je voor elke afzender een keuze hebt gemaakt, staat er in de to-do dat je klaar bent en staat **Markeer als gedaan** erbij.

Met **Dagelijks overzicht** krijg je één keer per dag één to-do met de paar nieuwsbriefartikelen die je tijd waard zijn. Bij elk artikel staat in één regel waarom het voor jou relevant is. Tik erop om de mail te lezen of gebruik **Openen in je mail**. De routine bekijkt alleen nieuwsbrieven, nooit mails van mensen, bonnetjes of afzenders van wie je je hebt afgemeld, en nooit mails die je al hebt gelezen. Als niets opvalt, wordt er geen to-do gemaakt.

De routine leert wat je belangrijk vindt op basis van wat je opent, markeert met een ster of archiveert zonder te lezen, en van **Meer zoals dit** en **Minder zoals dit** bij elk artikel. De onderwerpen waarop de routine let, staan op de kaart onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg er zelf een toe. Onderwerpen met een stippellijn zijn door de routine zelf geleerd. Een nieuw overzicht vervangt het openstaande overzicht. De routine stuurt nooit een melding.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief en stelt je AI er één korte vraag over, met een dagelijks maximum om de kosten laag te houden. Met **Wanneer wijzigen** stel je het tijdstip in. Zodra je de woorden aanpast, wordt de routine net als elke andere routine uitgevoerd op basis van jouw woorden.

Met **Verjaardagen** wordt er een to-do gemaakt voor elk dierbaar contact dat vandaag jarig is: mensen met wie je zelf contact hebt, zoals vrienden, familie en mensen met wie je regelmatig praat. Voor elk contact staat er een korte felicitatie klaar in de plek waar je meestal met diegene praat, zoals hun WhatsApp-chat of jullie e-mailthread, in hun taal. De felicitatie wordt pas verstuurd als jij hem verstuurt. Op een dag zonder verjaardagen wordt er geen to-do gemaakt.

Verjaardagen komen uit je agenda's (de verjaardagsafspraken en verjaardagsagenda van Google, die elke ochtend worden gelezen, ook als ze niet zijn gesynchroniseerd, en de verjaardagsagenda van Outlook), je Google-contacten op een zelfgehoste Machine en een datumveld met de naam Birthday bij een persoon in de Graph. Als nergens een verjaardag is opgeslagen, staat er in het resultaat **Nog geen verjaardagsgegevens** met uitleg over hoe je die kunt toevoegen.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen is ingeschakeld, biedt een to-do aan de verjaardagenpagina van Facebook te lezen. Tik op **Importeren**. The Machine opent de pagina in zijn browser, scrolt tot alle maanden zijn geladen en leest de namen en verjaardagen van je vrienden. Je ziet hoeveel verjaardagen zijn gevonden en wie er op basis van voor- en achternaam overeenkomt met mensen in je Graph. Namen die bij meer dan één persoon horen, worden overgeslagen en vermeld.

Alleen met **Opslaan** worden de gegevens bewaard op de pagina van elke persoon: de verjaardag en de Facebook-profielfoto voor iemand die nog geen foto heeft. Een verjaardag of foto die je daar hebt ingesteld, blijft staan. Een bestaande foto wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

De routine leest de pagina niet vanzelf opnieuw. Dat gebeurt wel als je op de to-do op **Opnieuw importeren** tikt. Je moet in Facebook zijn ingelogd in de browser. Als dat niet zo is, tik je op de to-do op **Aanmelden bij Facebook** en log je daar in. Zodra je bent ingelogd, leest de routine de pagina vanzelf. The Machine logt nooit voor je in.

Vrienden die niemand in je Graph heeft, worden meegeteld en er worden een paar namen getoond. Met **… toevoegen als persoonlijke contacten** voeg je ze allemaal tegelijk toe, ook nadat je op Opslaan hebt getikt. Ze worden toegevoegd met hun naam en verjaardag en nooit gedeeld met een Work Fleet. Iemand met een naam die al in je Graph voorkomt, of die je eerder permanent hebt verwijderd, wordt overgeslagen. Je krijgt nog steeds alleen verjaardagsherinneringen voor mensen met wie je zelf contact hebt.

Met **Ongedaan maken** in de to-do verwijder je precies die mensen weer, ook nadat je op **Opnieuw importeren** hebt getikt.

**Abonnementen en proefperiodes** leest één keer per maand je bonnetjes, facturen en verlengingsberichten en zet je abonnementen in één to-do. Je ziet wat elk abonnement kost, wanneer de volgende afschrijving is en een melding als een proefperiode afloopt of de prijs stijgt. Alleen abonnementen waar de routine zeker van is, worden vermeld. Als er niets wordt gevonden, wordt er geen to-do gemaakt.

Kies voor elk abonnement **Houden** of **Opzeggen**. Er wordt niet opnieuw naar een abonnement gevraagd als je het wilt houden, tenzij de prijs verandert. Met **Opzeggen** krijg je de opzegpagina of een concept waarin je om opzegging vraagt. Dat wordt pas verstuurd als jij het verstuurt. Tussen de maandelijkse controles door wordt elke dag gecontroleerd. Als een proefperiode of verlenging binnen 7 dagen wordt afgeschreven, wordt er een to-do gemaakt.

**Contact houden** herinnert je af en toe eraan contact op te nemen met iemand die je na aan het hart ligt, maar alleen als daar een goede reden voor is. Kies op de kaart wie erbij hoort uit een korte lijst van mensen met wie je zelf over een langere periode regelmatig heen en weer hebt geschreven. Verwijder iemand met ×.

Je krijgt alleen een herinnering als je veel langer dan gewoonlijk geen contact hebt gehad en er iets specifieks is om te zeggen: nieuws dat diegene heeft gedeeld, een belofte die nog openstaat of een bericht waarop je nooit hebt geantwoord. Er wordt één to-do gemaakt met de reden en een kort bericht als concept op de plek waar je meestal met diegene praat, in diens taal. Het wordt pas verstuurd als jij het verstuurt. Als er niets te zeggen is, wordt er geen to-do gemaakt.

Er worden maximaal twee herinneringen per week verstuurd en maximaal één per persoon per maand. Iemand met wie je onlangs contact had, krijgt er geen. Met **Niet nodig** bij een herinnering wacht de routine langer voordat je die persoon weer een herinnering krijgt. Dat wordt elke keer langer. De routine stuurt nooit een melding en blijft persoonlijk: hij wordt nooit gedeeld met een Work Fleet.

Zolang de routine van een sjabloon de woorden van het sjabloon gebruikt, wordt hij uitgevoerd met eigen code, zonder je AI-abonnement. Spam opruimen zet nieuwe mail van onbekende afzenders eerst in code op een rij en stelt je AI alleen één korte vraag als er mail is. Contact houden vraagt alleen naar de een of twee mensen die de routine heeft gekozen. Een nieuwe naam behoudt die instellingen. Zodra je de woorden aanpast, wordt de routine net als elke andere routine uitgevoerd op basis van jouw woorden.

Nieuwsbrieven opruimen en Spam opruimen eindigen nog steeds met dezelfde to-do, met een keuze voor elke mail. Een aangepaste Verjaardagen geeft het resultaat en maximaal één concept, geen aparte to-do per persoon. Met **Terug naar het sjabloon** in **Bewerken** zet je de oorspronkelijke woorden terug.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat hij nodig heeft, zoals je berichten, vergaderingen en de Graph, en zet hij het resultaat op de pagina Routines. Bij elk resultaat staat **Klaargezet**, **Niets nieuws** (met uitleg) of **Lukte niet** (met uitleg). Een uitvoering die eindigt zonder resultaat, telt als mislukt en nooit als voltooid.

Routines lezen alleen: je berichten, webpagina's, GitHub en sites zoals X in de browser. Ze versturen, beantwoorden of plaatsen niets en veranderen niets. Alleen een sjabloon kan mail aanpassen, en alleen wat je in de bijbehorende to-do bevestigt.

Als een routine eindigt met een bericht of post, voert hij alles tot die stap uit en toont hij het concept, bijvoorbeeld **Zou plaatsen op X:**. Na een echte uitvoering krijg je het als to-do om goed te keuren. Bij een testrun wordt het alleen getoond. De naam geeft aan waar het over gaat en waar het naartoe gaat. De knop vermeldt de stap, zoals **Plaatsen**, en met **Van je routine** eronder open je de routine.

De to-do staat eerst in het gebied van het account waarmee het bericht wordt verstuurd, zoals Werk voor het X-account van je bedrijf. Zo hoef je nooit te kiezen waar de to-do naartoe moet.

Een uitvoering kan de ingeschakelde [skills](skills.md) volgen die bij de taak van de routine passen. Alleen passende skills worden volledig gelezen. In het resultaat staan ze onder **Gebruikt:**. Een skill zorgt er nooit voor dat een routine iets verstuurt of verandert.

Je routines staan onder **Je routines**, onder eventuele suggesties. Een lang resultaat wordt ingeklapt tot een korte preview. Met **Meer tonen** of door erop te tikken, open je het resultaat.

Elke uitvoering kent het vorige resultaat en kan dus aangeven wat er sindsdien is veranderd.

Na een geslaagde uitvoering kan je Machine zelf een recept maken voor leeswerk dat elke keer hetzelfde is, zoals welke mails of GitHub-wijzigingen bekeken moeten worden. Bij volgende uitvoeringen worden die eerst in gewone code gelezen. De AI kiest dan alleen wat relevant is en schrijft het op, met minder tokens. Een recept leest alleen. Als het niet meer werkt, leest de uitvoering zelfstandig en herstelt hij het. Het recept staat onder **Geavanceerd: scriptstappen** in het ⋯-menu.

## Gemiste dagen

Als je Machine uitgeschakeld was of het druk had, wordt een gemiste uitvoering niet opgestapeld. Alleen de meest recente wordt één keer uitgevoerd. Elke datum wordt één keer uitgevoerd, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als er weinig gebruiksruimte over is in je AI-abonnement, net als al het andere achtergrondwerk. Met **Nu uitvoeren** start je de routine meteen. Zodra het resultaat klaar is, staat het op de kaart.

## Een routine wijzigen of stoppen

Deze opties staan in het ⋯-menu van de routine. Met **Bewerken** wijzig je de naam en wat de routine doet. Wanneer de routine wordt uitgevoerd en de resultaten tot nu toe blijven behouden. Met **Wanneer wijzigen** stel je in je eigen woorden een nieuw ritme in, zoals "elke werkdag om 8 uur". Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het venster klikken om te annuleren.

Met **Probeer het** in **Bewerken** voer je de nieuwe woorden één keer uit en zie je het resultaat daar. De routine blijft zoals hij was totdat je op **Opslaan** tikt.

Met **Pauzeren** stop je de uitvoeringen totdat je op de kaart op **Hervatten** tikt. Gepauzeerde routines staan onder **Gepauzeerd**, onder je routines. Gemiste uitvoeringen worden niet alsnog uitgevoerd. Met **Stoppen** beëindig je een routine definitief.

Je kunt maximaal 20 routines hebben, inclusief gepauzeerde routines. Stop een routine om er nog een toe te voegen.

Als je bij de to-do van een routine **Wijzigingen vragen** gebruikt of iets in de chat schrijft dat voor elke uitvoering geldt, zoals "gebruik nooit emoji's", biedt de to-do **Ook de routine aanpassen** aan, zowel in de to-do als in de chat onder het antwoord. Je ziet wat er in de woorden van de routine verandert. De routine wordt pas aangepast als je op **Aanpassen** tikt. Met **Laat zo** blijft alles hetzelfde. Als je alleen het concept wilt aanpassen, wordt deze optie niet aangeboden.

## Geavanceerd: scriptstappen

Je hebt geen script nodig. Beschrijf in je eigen woorden wat een routine moet doen, dan zoekt je Machine uit hoe.

Gevorderde gebruikers kunnen ook eigen opdrachten uitvoeren op hun Machine. Kies daarvoor **Geavanceerd: scriptstappen** in het ⋯-menu. **Bewerken** wordt pas getoond als een routine scriptstappen heeft. Met **Gegevens ophalen** voer je eerst een opdracht uit, in de map van de opdracht (of je thuismap als die leeg is), voor maximaal het opgegeven aantal seconden. Wat de opdracht weergeeft, wordt aan de uitvoering doorgegeven. Als er geen woorden zijn opgegeven, wordt die uitvoer het resultaat.

Met **Controle** wordt het resultaat na de uitvoering als invoer gebruikt. Als de opdracht met een fout eindigt, toont de uitvoering **Lukte niet** met de melding van de controle. Een mislukte opdracht voor Gegevens ophalen wordt op dezelfde manier getoond.

Een opdracht bestaat uit één regel en wordt zonder shell uitgevoerd: geen pipes of variabelen. Scriptstappen zijn van jou en worden alleen op je dashboard ingesteld. Bij een testrun en met **Probeer het** wordt Gegevens ophalen ook uitgevoerd en staat dat erbij. Er wordt nog steeds niets verstuurd of bewaard. Een routine verstuurt nooit iets, dus een scriptstap mag alleen lezen.

## Van je OpenClaw-taken

Als je eerder geplande taken hebt gemaakt in OpenClaw, leest je Machine die (hij verandert ze nooit) en biedt hij passende taken als routines aan onder **Voorgesteld**. Elke taak is één keer uitgevoerd, zodat je een echt resultaat ziet.

De correcties die je op de taak hebt aangebracht, blijven behouden. Wat de taak heeft verstuurd of geplaatst, wordt weggelaten. Een taak die een script heeft uitgevoerd of de resultaten van een scripttaak heeft gelezen, neemt dat script mee als Gegevens ophalen. Met **Toevoegen** maak je er een routine van. Met **Nee, bedankt** wordt er nooit meer naar die taak gevraagd. Een taak die je ergens aan herinnerde, wordt in plaats daarvan op To-do's aangeboden als een terugkerende to-do.

Voordat je een suggestie toevoegt, kun je die aanpassen zoals elke andere routine met **Bewerken** en **Wanneer wijzigen** in het ⋯-menu. Met **Opnieuw uitvoeren** voer je de taak nu uit met de huidige woorden, zodat je nieuwere resultaten ziet, bijvoorbeeld na een rustig weekend. De taak leest alleen, wordt één keer per tik uitgevoerd en het nieuwe resultaat vervangt het oude.

Er kunnen maximaal drie suggesties tegelijk klaarstaan. Na een week met geslaagde uitvoeringen vraagt de routine **De oude OpenClaw-taak uitzetten?**. De taak wordt alleen uitgezet als je op **Uitzetten** tikt. Je kunt hem daarna weer inschakelen in OpenClaw. Met **Houden** blijven beide taken actief.

## Op basis van wat je doet

Je Machine merkt ook werk op dat je regelmatig doet en biedt dat als routine aan onder **Voorgesteld**, ook zonder OpenClaw. Hij kijkt naar:

- dezelfde vraag die je drie keer of vaker achter elkaar hebt gesteld, zoals "geef een overzicht van de openstaande supporttickets" elke maandag;
- een mail die je regelmatig verstuurt, zoals een wekelijks rapport aan je team;
- nieuwsbrieven en updates die elke week blijven binnenkomen;
- een druk Slack-kanaal waarin anderen elke week schrijven;
- mails die je één voor één naar dezelfde persoon doorstuurt, zoals mails over school en clubs naar je partner. Een wekelijks overzicht voor diegene scheelt het doorsturen;
- hetzelfde verzoek waarop je regelmatig reageert, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Bij elke suggestie staat wat de routine heeft opgemerkt, zoals "4 keer achter elkaar gevraagd" of "6 mails in 3 weken doorgestuurd naar Sam". De routine is één keer uitgevoerd, zodat je een echt resultaat ziet. Denk aan een samenvatting voor je team, een briefing voor een wekelijks gesprek, een overzicht van support of development, een update over je cijfers of een overzicht van de nieuwsbrieven die je ontvangt.

De routine stelt alleen iets voor als het specifiek voor jou is en duidelijk nuttig: een nieuwsoverzicht gaat alleen over je eigen nieuwsbrieven, nooit over algemeen nieuws. Als niets past, wordt er geen suggestie gedaan.

De routine kijkt maximaal één keer per dag en doet maximaal één nieuwe suggestie per week, zonder melding. Met **Nee, bedankt** wordt die suggestie nooit opnieuw getoond. Doorgestuurde mails en antwoorden blijven bij het account waarmee ze zijn verstuurd, zodat Werk en Persoonlijk niet door elkaar lopen. Alles blijft op je Machine. Een to-do die je regelmatig afsluit, wordt in plaats daarvan aangeboden als terugkerende to-do.

## Routines en terugkerende to-do's

Een [terugkerende to-do](recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelf uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor "betaal de huur op de eerste" en een routine voor "vertel me elke vrijdag welke deals zijn stilgevallen".
