---
title: Routines
area: cards
summary: Werk dat The Machine zelfstandig en volgens een vast ritme doet, zoals elke maandag een overzicht van je openstaande deals. Hij leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: ed2171ef31eb6213
---
## Een routine maken

Open **Routines** in de zijbalk en beschrijf in één regel wat hij moet doen en wanneer: "elke maandag om 9 uur, geef een overzicht van mijn openstaande deals" of "elke ochtend op werkdagen, geef een lijst van de e-mails waarop ik nog moet reageren". Klik daarna op **Toevoegen**.

Zonder opgegeven tijd voert hij de routine om 8:00 uit. De tijd is gebaseerd op de klok van je Machine. De eerste keer krijgt de routine een korte naam.

Met **Toevoegen** wordt eerst een test uitgevoerd, zodat je ziet wat de routine oplevert voordat je hem bewaart. Er wordt niets verstuurd of opgeslagen. Met **Toevoegen** blijft de routine daarna volgens het ingestelde ritme draaien, met **Wijzigen** probeer je andere woorden of een nieuwe naam en met **Annuleren** verwijder je hem.

## Sjablonen

Onder **Sjablonen**, onderaan bij Routines, zet **Toevoegen** een kant-en-klare routine aan. Hij wordt meteen één keer uitgevoerd en daarna elke ochtend om 7:30 (Spam opruimen elk uur, Abonnementen en proefperiodes één keer per maand). Op de kaart staan de woorden van de routine, net als bij elke andere routine. Met **Bewerken** kun je de woorden of de naam wijzigen.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen uitstaat (25 of meer per week, van minstens 5 afzenders), zie je boven je to-do's een regel met het aantal nieuwsbrieven en wat de routine ermee zou doen, met **Zet het aan** en **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier aangeboden wanneer je in een week 5 of meer e-mails handmatig naar spam hebt verplaatst. Met **Zet het aan** voeg je de routine toe, net als met **Toevoegen** hier. Met **Nee, bedankt** wordt de routine niet opnieuw aangeboden. Een sjabloon dat je eerder hebt gehad, wordt nooit opnieuw aangeboden.

**Nieuwsbrieven opruimen** maakt één to-do per gebied (werk en privé) met de nieuwsbrieven van de afgelopen dag. Voor elke nieuwsbrief kun je kiezen uit **Houden** en **Afmelden**. Afmelden gebeurt via de een-kliklink van de mailinglijst of, als verzenden is ingeschakeld, via een afmeldmail vanaf jouw adres. Anders meldt The Machine je af op de pagina van de mailinglijst, in zijn eigen browser. Een aanmelding, captcha of keuzes op die pagina moet je zelf afhandelen. In de regel staat waarom, met **Afmeldpagina openen**.

Bonnetjes, bestellingen en betalingsmeldingen worden weggelaten. E-mail die via een groepsadres is binnengekomen, zoals een Google Group, wordt vermeld bij de afzender en meldt je nooit af van de groep. Als de afzender geen eigen afmeldmogelijkheid heeft, staat er bij de e-mail **Zelf afmelden**.

**Spam opruimen** maakt één to-do per gebied met e-mail van onbekende afzenders die op spam lijkt. Voor elke e-mail kun je kiezen uit **Spam** en **Geen spam**. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert het als spam. De routine controleert elk uur, dus spam staat er meestal al voordat je eraan toekomt. Nieuwe spam wordt aan dezelfde to-do toegevoegd zolang die openstaat.

Gmail dat alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan e-mail niet naar spam verplaatsen. Daar geeft **Spam** een link waarmee je de e-mail in Gmail als spam markeert. The Machine onthoudt de afzender dan als spam. Als er geen e-mailaccount is gekoppeld, staat in het sjabloon **Mail koppelen** in plaats van **Toevoegen**.

Onbekend betekent dat je nooit eerder naar die afzender hebt geschreven. Een "Re:" telt alleen als gesprek in een thread waarin jij hebt geschreven. Als er opnieuw e-mail binnenkomt van een afzender die je als spam hebt gemarkeerd, in de to-do of in je mailbox, staat die in de volgende to-do met **Eerder als spam gemarkeerd**. E-mail die je zelf naar spam hebt verplaatst, helpt de routine ook om vergelijkbare e-mail te herkennen.

Er verandert niets totdat je je keuze in de to-do bevestigt. Tik op een afzender om eerst de e-mail te lezen: hij blijft ongelezen en er verandert niets. In Spam opruimen worden afbeeldingen van internet niet geladen, zodat de afzender niet kan zien dat je de e-mail hebt geopend. Je krijgt geen nieuwe vraag meer over afzenders waarover je al een keuze hebt gemaakt. Op een dag zonder nieuwsbrieven of spam wordt er geen to-do gemaakt. Deze to-do's sturen nooit een melding.

Zodra je voor elke afzender een keuze hebt gemaakt, geeft de to-do aan dat hij klaar is en staat **Markeer als gedaan** erbij.

**Dagelijks overzicht** kiest één keer per dag in één to-do de paar nieuwsbrieven die je tijd waard zijn. Bij elk item staat in één regel waarom het voor jou relevant is. Tik erop om de e-mail te lezen of gebruik **Openen in je mail**. De routine bekijkt alleen nieuwsbrieven, nooit e-mail van mensen, bonnetjes of afzenders waarvoor je je hebt afgemeld, en nooit iets wat je al hebt gelezen. Als er niets uitspringt, wordt er geen to-do gemaakt.

De routine leert wat je belangrijk vindt aan de hand van wat je opent, met een ster markeert of ongeopend archiveert, en van **Meer zoals dit** en **Minder zoals dit** bij elk item. De onderwerpen waarop hij zoekt, staan op de kaart van de routine onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg zelf onderwerpen toe. Onderwerpen met een stippellijn heeft de routine zelf geleerd. Een nieuw overzicht vervangt het vorige zolang dat nog openstaat. De routine stuurt nooit een melding.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief. Hij stelt je AI er één korte vraag over, met een dagelijkse limiet om de kosten laag te houden. Met **Wanneer wijzigen** pas je het tijdstip aan. Zodra je de woorden van de routine wijzigt, wordt hij uitgevoerd zoals elke routine, op basis van jouw woorden.

**Verjaardagen** maakt een to-do voor elk contact met wie je close bent en die vandaag jarig is: mensen aan wie je zelf schrijft, zoals vrienden, familie en vaste contacten. Bij elke verjaardag staat een korte felicitatie als concept, op de plek waar je meestal met die persoon praat, zoals de WhatsApp-chat of e-mailthread. De felicitatie wordt pas verstuurd als jij hem verstuurt. Op een dag zonder verjaardagen wordt er geen to-do gemaakt.

Verjaardagen komen uit je agenda's (de verjaardagsevenementen en verjaardagsagenda van Google, die elke ochtend worden gelezen, ook als ze niet gesynchroniseerd zijn, en de verjaardagsagenda van Outlook), uit je Google-contacten op een zelfgehoste Machine en uit een datumveld met de naam Birthday bij een persoon in de Graph. Als nergens een verjaardag staat, vermeldt het resultaat **Nog geen verjaardagsgegevens** en hoe je die kunt toevoegen.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen aanstaat, biedt een to-do aan om de verjaardagenpagina van Facebook te lezen. Tik op **Importeren**. The Machine opent de pagina in zijn browser, scrolt totdat alle maanden zijn geladen en leest de naam en verjaardag van elke vriend. De routine toont hoeveel verjaardagen hij heeft gevonden en welke mensen overeenkomen met personen in je Graph op basis van hun voor- en achternaam. Namen die bij meerdere personen horen, worden overgeslagen en vermeld.

Alleen met **Opslaan** worden de gegevens bewaard, op de pagina van elke persoon: de verjaardag en, voor iemand die nog geen foto heeft, de profielfoto van Facebook. Een verjaardag of foto die je daar instelt, blijft staan. Een bestaande foto wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

De routine leest de pagina niet automatisch opnieuw. Dat gebeurt alleen met **Opnieuw importeren** in de to-do. In de browser moet je bij Facebook zijn aangemeld. Zo niet, tik dan in de to-do op **Aanmelden bij Facebook** en meld je daar aan. Zodra je bent aangemeld, leest de routine de pagina vanzelf. The Machine meldt je nooit aan.

Vrienden die niemand in je Graph kent, worden geteld en er worden een paar namen getoond. Met **Als privécontacten toevoegen** voeg je ze allemaal tegelijk toe, ook na Opslaan: elk contact met een naam en verjaardag, nooit gedeeld met een Work Fleet. Personen met een naam die al in je Graph voorkomt, of die je eerder definitief hebt verwijderd, worden overgeslagen. Je krijgt alleen verjaardagsherinneringen voor mensen aan wie je schrijft.

Met **Ongedaan maken** in de to-do verwijder je precies die mensen weer, ook na **Opnieuw importeren**.

**Abonnementen en proefperiodes** leest één keer per maand je bonnetjes, facturen en verlengingsberichten en zet je abonnementen in één to-do. Daarin staat wat elk abonnement kost, wanneer het volgende bedrag wordt afgeschreven en of een proefperiode afloopt of de prijs stijgt. Alleen abonnementen waar de routine zeker van is, worden vermeld. Als hij niets vindt, wordt er geen to-do gemaakt.

Kies voor elk abonnement **Houden** of **Opzeggen**. Naar een abonnement dat je houdt, wordt niet opnieuw gevraagd, tenzij de prijs verandert. Met **Opzeggen** krijg je de opzegpagina of een concept waarin je vraagt om het abonnement op te zeggen. Dat wordt pas verstuurd als jij het verstuurt. Tussen de maandelijkse controles door controleert de routine elke dag of er binnen 7 dagen een proefperiode afloopt of een verlenging wordt afgeschreven. In dat geval maakt hij een to-do.

Zolang een routine uit een sjabloon de woorden van dat sjabloon gebruikt, draait hij op eigen code en gebruikt hij je AI-abonnement niet. (Spam opruimen haalt met code eerst nieuwe e-mail van onbekende afzenders op en stelt je AI alleen één korte vraag als er zulke e-mail is.) Zodra je de woorden wijzigt, wordt de routine uitgevoerd zoals elke andere routine, op basis van jouw woorden.

Nieuwsbrieven opruimen en Spam opruimen leveren nog steeds dezelfde to-do op, met een keuze per e-mail. Een aangepaste Verjaardagen-routine geeft het resultaat en hooguit één concept, geen aparte to-do per persoon. Met **Terug naar het sjabloon** in **Bewerken** herstel je de oorspronkelijke woorden.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat nodig is, zoals je berichten, afspraken en de Graph, en zet hij het resultaat op de pagina Routines. Elk resultaat vermeldt **Klaargezet**, **Niets nieuws** (met uitleg) of **Lukte niet** (met uitleg). Een run die eindigt zonder resultaat geldt als mislukt, nooit als voltooid.

Routines lezen alleen: je berichten, webpagina's, GitHub en sites zoals X in de browser. Ze versturen niets, beantwoorden geen berichten, plaatsen niets en veranderen niets. Alleen een sjabloon verandert e-mail, en alleen wat je in de bijbehorende to-do bevestigt.

Als een routine aan het eind iets moet plaatsen of versturen, voert hij alles tot die stap uit en toont hij het concept, bijvoorbeeld **Zou op X plaatsen:**. Na een echte run krijg je dit als to-do ter goedkeuring. Een testrun toont het alleen. De naam beschrijft waar het over gaat en waar het naartoe gaat. De knop noemt de stap, zoals **Plaatsen**, en met **Vanuit je routine** eronder open je de routine.

De to-do staat eerst in het gebied van het account waarmee hij wordt verstuurd, bijvoorbeeld Werk voor het X-account van je bedrijf. Je hoeft hem dus nooit te verplaatsen.

Een run kan de ingeschakelde [skills](skills.md) volgen die bij de taak van de routine passen. Alleen relevante skills worden volledig gelezen. Het resultaat vermeldt ze onder **Gebruikt:**. Een skill zorgt er nooit voor dat een routine iets verstuurt of verandert.

Je routines staan onder **Je routines**, onder eventuele suggesties. Een lang resultaat wordt ingeklapt tot een korte voorvertoning. Met **Meer tonen** of door erop te tikken, open je het.

Elke run kent het vorige resultaat en kan daardoor aangeven wat er sindsdien is veranderd.

Na een geslaagde run kan je Machine zelf een recept maken voor de terugkerende leesstappen, zoals welke e-mails of wijzigingen in GitHub hij moet bekijken. Bij volgende runs worden die stappen eerst uitgevoerd in gewone code. De AI kiest dan alleen wat relevant is en schrijft het resultaat, met minder tokens. Een recept leest alleen. Als het niet meer werkt, voert de run de stappen zelf uit en herstelt hij het recept. Het staat onder **Geavanceerd: scriptstappen** in het menu ⋯.

## Gemiste dagen

Als je Machine uitstaat of bezig is, worden gemiste runs niet opgestapeld. Alleen de meest recente run wordt één keer uitgevoerd. Elke datum wordt één keer uitgevoerd, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als je AI-abonnement weinig gebruik over heeft, net als al het andere achtergrondwerk. Met **Nu uitvoeren** start je de routine meteen. Het resultaat staat op de kaart zodra het klaar is.

## Een routine wijzigen of stoppen

Deze opties staan in het menu ⋯ van de routine. Met **Bewerken** wijzig je de naam en wat de routine doet. Het tijdstip en eerdere resultaten blijven hetzelfde. Met **Wanneer wijzigen** stel je in je eigen woorden een nieuw ritme in, bijvoorbeeld "elke werkdag om 8 uur". Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het menu klikken om te annuleren.

Met **Probeer het** in **Bewerken** voer je de nieuwe woorden één keer uit en zie je het resultaat daar. De routine blijft ongewijzigd totdat je op **Opslaan** tikt.

Met **Pauzeren** worden runs stopgezet totdat je op de kaart van de routine **Hervatten** kiest. Gepauzeerde routines staan onder **Gepauzeerd**, onder je routines. Runs die tijdens de pauze zijn gemist, worden daarna niet uitgevoerd. Met **Stoppen** beëindig je een routine definitief.

Je kunt maximaal 20 routines hebben, inclusief gepauzeerde routines. Stop er een om ruimte te maken voor een nieuwe.

Als je bij de to-do van een routine **Wijzigingen vragen** gebruikt of iets in de chat ervan schrijft, en je opmerking voor elke run geldt, zoals "gebruik nooit emoji's", biedt de to-do **Ook de routine aanpassen** aan. Die optie staat in de to-do en in de chat onder het antwoord. Je ziet wat er in de woorden van de routine wordt gewijzigd. De routine verandert pas als je op **Aanpassen** tikt. Met **Laat zo** blijft alles hetzelfde. Als je alleen het concept wilt aanpassen, wordt deze optie niet aangeboden.

## Geavanceerd: scriptstappen

Een script is niet nodig. Beschrijf in je eigen woorden wat een routine moet doen, dan zoekt je Machine de rest uit.

Voor ervaren gebruikers kan een routine ook eigen opdrachten op je Machine uitvoeren. Kies daarvoor **Geavanceerd: scriptstappen** in het menu ⋯. **Bewerken** toont de stappen alleen als de routine er al heeft. Met **Gegevens ophalen** voer je eerst een opdracht uit, in de bijbehorende map (of in je thuismap als die leeg is), voor maximaal het opgegeven aantal seconden. De uitvoer wordt aan de run doorgegeven om mee te werken. Zonder verdere instructies is de uitvoer het resultaat.

Met **Controle** wordt het resultaat na de run als invoer opgehaald. Als de opdracht met een fout eindigt, toont de run **Lukte niet** met de melding van de controle. Een mislukte opdracht voor Gegevens ophalen wordt op dezelfde manier weergegeven.

Een opdracht is één regel die zonder shell wordt uitgevoerd: geen pipes of variabelen. Scriptstappen stel je zelf in, alleen op je dashboard. Ook bij een testrun en **Probeer het** wordt Gegevens ophalen uitgevoerd en zie je dat dit gebeurt. Er wordt nog steeds niets verstuurd of bewaard. Een routine verstuurt nooit iets, dus een scriptstap mag alleen lezen.

## Vanuit je OpenClaw-taken

Als je eerder geplande taken in OpenClaw hebt gemaakt, leest je Machine die (hij verandert ze nooit) en biedt hij de taken die geschikt zijn aan als routines onder **Voorgesteld**. Elke taak is één keer uitgevoerd, zodat je een echt resultaat ziet.

Je correcties op de taak blijven behouden. Wat de taak heeft verstuurd of geplaatst, wordt weggelaten. Als een taak een script heeft uitgevoerd of iets heeft gelezen dat door een script is verzameld, wordt dat als Gegevens ophalen meegenomen. Met **Toevoegen** maak je er een routine van. Met **Nee, bedankt** wordt er niet opnieuw naar die taak gevraagd. Een taak die je eraan herinnerde iets te doen, wordt in plaats daarvan op To-do's aangeboden als een terugkerende to-do.

Voordat je een suggestie toevoegt, kun je hem wijzigen, net als elke andere routine, met **Bewerken** en **Wanneer wijzigen** in het menu ⋯. Met **Opnieuw uitvoeren** voer je hem nu uit met de huidige woorden, zodat je nieuwere resultaten ziet, bijvoorbeeld na een rustig weekend. De routine leest alleen, wordt één keer per tik uitgevoerd en het nieuwe resultaat vervangt het oude.

Er kunnen maximaal drie suggesties tegelijk klaarstaan. Na een week met geslaagde runs vraagt de routine **De oude OpenClaw-taak uitzetten?**. De taak wordt alleen uitgezet als je op **Uitzetten** tikt. Je kunt hem weer aanzetten in OpenClaw. Met **Houden** blijven beide actief.

## Op basis van wat je doet

Je Machine merkt ook werk op dat je volgens een vast ritme doet en biedt het aan als routine onder **Voorgesteld**, ook zonder OpenClaw. Hij zoekt naar:

- dezelfde vraag die je drie of meer keer achter elkaar stelt, zoals "geef elke maandag een overzicht van de openstaande supporttickets";
- e-mail die je volgens een vast ritme verstuurt, zoals een wekelijks verslag aan je team;
- nieuwsbrieven en updateberichten die elke week blijven binnenkomen;
- een druk Slack-kanaal waarin anderen elke week berichten plaatsen;
- e-mail die je één voor één doorstuurt naar dezelfde persoon, zoals e-mail van school en clubs naar je partner. Een wekelijks overzicht voor die persoon scheelt het doorsturen;
- hetzelfde verzoek waarop je volgens een vast ritme antwoordt, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Bij elke suggestie staat wat de routine heeft gezien, zoals "4 keer achter elkaar gevraagd" of "6 e-mails doorgestuurd naar Sam in 3 weken". De routine is één keer uitgevoerd, zodat je een echt resultaat ziet. Denk aan een samenvatting voor je team, een korte briefing vóór een wekelijks gesprek, een overzicht van support of ontwikkeling, een update over je cijfers of een overzicht van de nieuwsbrieven die je krijgt.

De routine stelt alleen iets voor als het specifiek voor jou is en duidelijk nuttig: een nieuwsoverzicht bevat alleen je eigen nieuwsbrieven, nooit algemene nieuwsberichten. Als er niets geschikts is, wordt er niets voorgesteld.

De routine controleert hooguit één keer per dag en voegt maximaal één nieuwe suggestie per week toe, zonder melding. Met **Nee, bedankt** wordt die suggestie nooit opnieuw getoond. Doorgestuurde berichten en antwoorden blijven bij het account waarmee ze zijn verstuurd, zodat Werk en Privé niet door elkaar lopen. Alles blijft op je Machine. Een to-do die je volgens een vast ritme afsluit, wordt in plaats daarvan aangeboden als terugkerende to-do.

## Routines en terugkerende to-do's

Een [terugkerende to-do](recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelfstandig uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor "betaal de huur op de eerste dag van de maand" en een routine voor "vertel me elke vrijdag welke deals zijn stilgevallen".
