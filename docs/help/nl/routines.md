---
title: Routines
area: cards
summary: Werk dat je Machine zelfstandig en volgens een vast schema doet, zoals elke maandag een overzicht van je openstaande deals. Je Machine leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: 9c3559a910b9dd37
---
## Een routine maken

Open **Routines** in de zijbalk en beschrijf in één regel wat de routine moet doen en wanneer: "elke maandag om 9 uur, vat mijn openstaande deals samen" of "elke werkdag ’s ochtends, geef een lijst van de e-mails waarop ik nog moet antwoorden". Klik daarna op **Toevoegen**.

Zonder tijdstip wordt de routine om 8:00 uitgevoerd. De tijd is gebaseerd op de klok van je Machine. Bij de eerste uitvoering krijgt de routine een korte naam.

Met **Toevoegen** wordt eerst een test uitgevoerd, zodat je ziet wat de routine oplevert voordat je hem bewaart. Er wordt niets verstuurd of opgeslagen. Daarna zorgt **Toevoegen** ervoor dat de routine volgens schema blijft draaien. Met **Wijzigen** probeer je andere woorden of een nieuwe naam. Met **Annuleren** verwijder je de routine.

## Sjablonen

Bij **Sjablonen** onderaan Routines zet je met **Toevoegen** een kant-en-klare routine aan. Hij wordt meteen één keer uitgevoerd en daarna elke ochtend om 7:30 (Spam opruimen elk uur, Abonnementen en proefperiodes één keer per maand). Op de kaart staat de beschrijving, net als bij elke routine. Met **Bewerken** pas je de beschrijving of de naam aan.

Als je veel nieuwsbrieven ontvangt en Nieuwsbrieven opruimen uitstaat (25 of meer in een week, van minstens 5 afzenders), staat er boven je to-do's hoeveel nieuwsbrieven er zijn binnengekomen en wat de routine zou doen. Je kunt kiezen voor **Zet het aan** of **Nee, bedankt**.

Spam opruimen wordt op dezelfde manier aangeboden als er in een week minstens 5 e-mails handmatig naar spam zijn verplaatst. Met **Zet het aan** voeg je de routine toe, net als met **Toevoegen** hier. Met **Nee, bedankt** wordt de routine niet opnieuw aangeboden. Een sjabloon dat je eerder hebt gehad, wordt nooit opnieuw aangeboden.

**Nieuwsbrieven opruimen** maakt één to-do per gebied (werk en privé) met de nieuwsbrieven van de afgelopen dag. Bij elke nieuwsbrief kun je kiezen voor **Houden** of **Afmelden**. Afmelden gebruikt de eenkliklink van de mailinglijst of de afmeldmail vanaf jouw adres, als verzenden is ingeschakeld. Anders meldt The Machine je af via de pagina van de mailinglijst in zijn eigen browser. Een eventuele login, captcha of keuzes op die pagina moet je zelf afhandelen. Bij de regel staat waarom, met de optie **Afmeldpagina openen**.

Bonnetjes, bestellingen en betaalberichten worden overgeslagen. E-mails die via een groepsadres binnenkomen, zoals een Google Group, staan onder de naam van de afzender. Je wordt nooit afgemeld voor de groep. Als de afzender geen eigen afmeldoptie heeft, staat er bij de regel **Zelf afmelden**.

**Spam opruimen** maakt één to-do per gebied met e-mails van onbekende afzenders die op spam lijken. Bij elke e-mail kun je kiezen voor **Spam** of **Geen spam**. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert het als spam. De routine controleert elk uur, zodat spam er meestal al staat voordat je erbij bent. Nieuwe spam komt op dezelfde to-do zolang die nog openstaat.

Gmail dat alleen-lezen is gekoppeld, zoals op een gehoste Machine, kan e-mail niet naar spam verplaatsen. Daar geeft **Spam** een link waarmee je de e-mail in Gmail kunt markeren. The Machine onthoudt de afzender dan als spam. Als er geen e-mailaccount is gekoppeld, staat bij het sjabloon **Mail koppelen** in plaats van **Toevoegen**.

Onbekend betekent dat je de afzender nooit zelf hebt gemaild. Een "Re:" telt alleen als gesprek in een thread waarin jij zelf hebt geschreven. Als e-mail van een afzender die je als spam hebt gemarkeerd toch weer binnenkomt, in de to-do of in je mailbox, staat die op de volgende to-do met de aanduiding **Eerder als spam gemarkeerd**. E-mails die je zelf naar spam hebt verplaatst, helpen ook om vergelijkbare e-mails te vinden.

Er verandert niets totdat je iets bevestigt in de to-do. Tik op een afzender om de e-mail eerst te lezen: hij blijft ongelezen en er verandert niets. Bij Spam opruimen worden afbeeldingen van het web niet geladen, zodat de afzender niet kan zien dat de e-mail is geopend. Er wordt niet opnieuw naar afzenders gevraagd waarover je al een keuze hebt gemaakt. Als er een dag geen nieuwsbrieven of spam zijn, wordt er geen to-do gemaakt. Deze to-do's sturen nooit een melding.

Zodra je voor elke afzender een keuze hebt gemaakt, geeft de to-do aan dat hij is afgerond en staat **Markeer als gedaan** erbij.

Met **Dagelijks overzicht** krijg je één keer per dag één to-do met de paar nieuwsbrieven die je tijd waard zijn. Bij elk artikel staat in één regel waarom het voor jou relevant is. Tik erop om de e-mail te lezen of kies **Openen in je mail**. Alleen nieuwsbrieven komen erin, nooit e-mails van mensen, bonnetjes of afzenders voor wie je je hebt afgemeld. Ook e-mails die je al hebt gelezen worden overgeslagen. Als niets eruit springt, wordt er geen to-do gemaakt.

De routine leert waar je in geïnteresseerd bent aan de hand van wat je opent, een ster geeft of ongelezen archiveert, en van **Meer zoals dit** en **Minder zoals dit** bij elk artikel. De onderwerpen waarop hij selecteert, staan op de routinekaart onder **Meer over** en **Minder over**. Verwijder een onderwerp met × of voeg er zelf een toe. Onderwerpen met een stippellijn heeft de routine zelf geleerd. Een nieuw overzicht vervangt het openstaande overzicht. Er wordt nooit een melding verstuurd.

De routine leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief. Hij stelt je AI er één korte vraag over, met een dagelijkse limiet, zodat het weinig kost. Met **Wanneer wijzigen** stel je het tijdstip in. Zodra je de beschrijving wijzigt, werkt de routine op basis van jouw beschrijving, net als elke andere routine.

**Verjaardagen** maakt een to-do voor elke naaste contactpersoon die vandaag jarig is: mensen aan wie je zelf schrijft, zoals vrienden, familie en vaste contacten. Bij elke verjaardag staat een korte begroeting als concept, op de plek waar je meestal met die persoon praat, zoals in hun WhatsApp-chat of je e-mailthread, en in hun taal. De begroeting wordt pas verstuurd als jij dat doet. Op dagen zonder verjaardagen wordt er geen to-do gemaakt.

Verjaardagen komen uit je agenda's (de verjaardagsevenementen en Verjaardagen-agenda van Google, die elke ochtend worden uitgelezen, ook als ze niet zijn gesynchroniseerd, en de Verjaardagen-agenda van Outlook), je Google-contacten op een zelfgehoste Machine en een datumveld met de naam Birthday bij een persoon in de Graph. Als er nergens een verjaardag is opgeslagen, staat er bij het resultaat **Nog geen verjaardagsgegevens** en hoe je verjaardagen kunt toevoegen.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen is ingeschakeld, biedt een to-do aan om de verjaardagenpagina van Facebook uit te lezen. Tik op **Importeren**. The Machine opent de pagina in zijn browser, scrolt totdat alle maanden zijn geladen en leest de namen en verjaardagen van je vrienden uit. Je ziet hoeveel verjaardagen zijn gevonden en wie er op basis van voor- en achternaam is gekoppeld aan personen in je Graph. Namen die bij meer dan één persoon horen, worden overgeslagen en vermeld.

Alleen met **Opslaan** worden de gegevens bewaard, op de pagina van elke persoon: de verjaardag en de Facebook-profielfoto als die persoon nog geen foto heeft. Een verjaardag of foto die je daar zelf instelt, blijft staan. Een foto die iemand al heeft, wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

The Machine leest de pagina niet automatisch opnieuw uit. Dat doe je met **Opnieuw importeren** op de to-do. Je moet in Facebook zijn aangemeld in de browser. Zo niet, tik dan op de to-do op **Aanmelden bij Facebook** en meld je daar aan. Zodra je bent aangemeld, leest The Machine de pagina automatisch uit. The Machine meldt je nooit zelf aan.

Vrienden die nog niet in je Graph staan, worden geteld en er worden een paar namen getoond. Met **Toevoegen … als persoonlijke contacten** voeg je ze allemaal tegelijk toe, ook nadat je op Opslaan hebt getikt. Elk contact krijgt een naam en verjaardag en wordt nooit gedeeld met een Work Fleet. Personen met een naam die al in je Graph voorkomt, of die je eerder permanent hebt verwijderd, worden overgeslagen. Je krijgt nog steeds alleen verjaardagsherinneringen voor mensen aan wie je zelf schrijft.

Met **Ongedaan maken** op de to-do verwijder je precies die personen weer, ook nadat je **Opnieuw importeren** hebt gebruikt.

**Abonnementen en proefperiodes** leest één keer per maand je bonnetjes, facturen en verlengingsberichten uit en zet je abonnementen in één to-do. Daarin staat wat elk abonnement kost, wanneer de volgende betaling plaatsvindt en of een proefperiode afloopt of de prijs omhooggaat. Alleen abonnementen waar de routine zeker van is, worden vermeld. Als er niets wordt gevonden, wordt er geen to-do gemaakt.

Kies voor elk abonnement **Houden** of **Opzeggen**. Je krijgt niet opnieuw een vraag over een abonnement dat je wilt houden, tenzij de prijs verandert. Met **Opzeggen** krijg je de opzegpagina of een concept met het verzoek om het abonnement op te zeggen. Dat wordt pas verstuurd als jij dat doet. Tussen de maandelijkse controles door controleert de routine elke dag of een proefperiode of verlenging binnen 7 dagen betaald moet worden. Zo nodig maakt hij een to-do.

Zolang een sjabloonroutine de beschrijving van het sjabloon gebruikt, wordt hij uitgevoerd met eigen code, zonder je AI-abonnement. Spam opruimen geeft eerst in code een lijst van nieuwe e-mails van onbekende afzenders en stelt je AI alleen één korte vraag als er e-mails zijn. Een nieuwe naam verandert daar niets aan. Zodra je de beschrijving wijzigt, werkt de routine op basis van jouw beschrijving, net als elke andere routine.

Nieuwsbrieven opruimen en Spam opruimen eindigen nog steeds met dezelfde to-do, met een keuze voor elke e-mail. Een aangepaste Verjaardagen-routine geeft het resultaat en hooguit één concept, geen aparte to-do per persoon. Met **Terug naar het sjabloon** in **Bewerken** herstel je de oorspronkelijke beschrijving.

## Wat een routine doet

Op het ingestelde tijdstip leest je Machine wat nodig is, zoals je berichten, vergaderingen en de Graph, en zet het resultaat op de pagina Routines. Bij elk resultaat staat **Klaargezet**, **Niets nieuws** met een toelichting of **Lukte niet** met een toelichting. Een uitvoering die eindigt zonder resultaat telt als mislukt, nooit als voltooid.

Routines lezen alleen gegevens, zoals je berichten, webpagina's, GitHub en websites zoals X in de browser. Ze versturen, beantwoorden of plaatsen niets en veranderen niets. Alleen een sjabloon kan e-mail aanpassen, en alleen wat je op de bijbehorende to-do bevestigt.

Als een routine eindigt met het plaatsen van een bericht of het versturen van een e-mail, voert hij alle stappen tot dat punt uit en toont hij het concept, zoals **Zou plaatsen op X:**. Na een echte uitvoering krijg je het als to-do om goed te keuren. Bij een test wordt het alleen getoond. De naam geeft aan waar het over gaat en waar het naartoe gaat. De knop benoemt de stap, zoals **Plaatsen**, en met **Van je routine** eronder open je de routine.

De to-do begint in het gebied van het account waarmee het bericht wordt verstuurd, zoals Werk voor het X-account van je bedrijf. Je hoeft hem dus nooit te verplaatsen.

Een uitvoering kan gebruikmaken van je ingeschakelde [skills](skills.md), geselecteerd op basis van wat de routine doet. Alleen skills die relevant zijn, worden volledig uitgelezen. De gebruikte skills staan onder **Gebruikt:**. Een skill zorgt er nooit voor dat een routine iets verstuurt of verandert.

Je routines staan onder **Je routines**, onder eventuele suggesties. Een lang resultaat wordt ingeklapt tot een korte voorbeeldweergave. Met **Meer tonen** of door erop te tikken, open je het volledige resultaat.

Elke uitvoering kent het vorige resultaat en kan daardoor aangeven wat er sinds die tijd is veranderd.

Na een succesvolle uitvoering kan je Machine zelf een recept schrijven voor leeswerk dat elke keer hetzelfde is, zoals welke e-mails of GitHub-wijzigingen moeten worden bekeken. Bij volgende uitvoeringen worden die eerst met eenvoudige code uitgelezen. De AI selecteert alleen wat belangrijk is en schrijft het resultaat, met minder tokens. Een recept leest alleen gegevens. Als het niet meer werkt, voert de routine de stappen zelf uit en herstelt hij het recept. Het recept staat onder **Geavanceerd: scriptstappen** in het ⋯-menu.

## Gemiste dagen

Als je Machine uitgeschakeld of bezig was, wordt een gemiste uitvoering niet opgestapeld. Alleen de nieuwste wordt één keer uitgevoerd. Elke datum wordt één keer uitgevoerd, ook na een herstart.

Routines worden één voor één uitgevoerd en wachten als het gebruik van je AI-abonnement laag is, net als al het achtergrondwerk. Met **Nu uitvoeren** start je de routine meteen. Het resultaat verschijnt op de kaart zodra het klaar is.

## Wijzigen of stoppen

Deze opties staan in het ⋯-menu van de routine. Met **Bewerken** wijzig je de naam en wat de routine doet. Het tijdstip en eerdere resultaten blijven behouden. Met **Wanneer wijzigen** stel je een nieuw schema in je eigen woorden in, zoals "elke werkdag om 8 uur". Beide opties hebben **Opslaan** en **Annuleren**. Op een computer kun je ook op Esc drukken of buiten het venster klikken om te annuleren.

In **Bewerken** voert **Probeer het** de nieuwe beschrijving één keer uit en toont het resultaat. De routine blijft ongewijzigd totdat je op **Opslaan** tikt.

Met **Pauzeren** worden uitvoeringen stopgezet tot je op **Hervatten** tikt. Gepauzeerde routines staan onder **Gepauzeerd** onderaan. Gemiste uitvoeringen tijdens de pauze worden niet later alsnog uitgevoerd. Met **Stoppen** beëindig je een routine definitief.

Als je bij de to-do van een routine **Wijzigingen vragen** gebruikt of iets in de chat schrijft dat voor elke uitvoering moet gelden, zoals "gebruik nooit emoji's", biedt de to-do **Ook de routine aanpassen** aan. Die optie staat ook in de chat, onder het antwoord. Je ziet wat er in de beschrijving van de routine verandert. De routine wordt pas aangepast als je op **Aanpassen** tikt. Met **Laat zo** blijft alles ongewijzigd. Voor een aanpassing die alleen voor dat concept geldt, wordt deze optie niet aangeboden.

## Geavanceerd: scriptstappen

Je hebt geen script nodig. Beschrijf in je eigen woorden wat een routine moet doen en je Machine bedenkt de rest.

Voor gevorderde gebruikers kan een routine ook eigen opdrachten uitvoeren op je Machine. Kies daarvoor **Geavanceerd: scriptstappen** in het ⋯-menu. **Bewerken** toont scriptstappen alleen als de routine er al heeft. Met **Gegevens ophalen** voer je eerst een opdracht uit, in de bijbehorende map (of in je thuismap als die leeg is) en maximaal het opgegeven aantal seconden. De uitvoer wordt aan de routine doorgegeven om mee te werken. Zonder beschrijving wordt de uitvoer het resultaat.

Met **Controle** wordt het resultaat na de uitvoering als invoer gecontroleerd. Als de opdracht eindigt met een fout, toont de uitvoering **Lukte niet** met de melding van de controle. Een opdracht voor Gegevens ophalen die mislukt, wordt op dezelfde manier weergegeven.

Een opdracht bestaat uit één regel en wordt zonder shell uitgevoerd: geen pipes of variabelen. Scriptstappen zijn van jou en worden alleen op je dashboard ingesteld. Ook bij een testuitvoering en **Probeer het** wordt Gegevens ophalen uitgevoerd. Dat wordt vermeld; er wordt nog steeds niets verstuurd of bewaard. Een routine verstuurt nooit iets, dus een scriptstap mag alleen gegevens uitlezen.

## Van je OpenClaw-taken

Als je eerder geplande taken in OpenClaw hebt gemaakt, leest je Machine ze uit, maar verandert ze nooit. Taken die geschikt zijn, worden onder **Voorgesteld** als routines aangeboden. Elke taak is één keer uitgevoerd, zodat je een echt resultaat ziet.

Je correcties op de taak blijven behouden, maar wat de taak heeft verstuurd of geplaatst wordt weggelaten. Een taak die een script uitvoerde, of gegevens uitleest die door een scripttaak zijn verzameld, neemt dat script mee als Gegevens ophalen. Met **Toevoegen** maak je er een routine van. Met **Nee, bedankt** wordt die taak niet opnieuw aangeboden. Een taak die je ergens aan herinnerde, wordt in plaats daarvan als terugkerende to-do aangeboden bij To-do's.

Voordat je een suggestie toevoegt, kun je die in het ⋯-menu met **Bewerken** en **Wanneer wijzigen** aanpassen, net als elke routine. Met **Opnieuw uitvoeren** wordt de taak meteen uitgevoerd met de huidige beschrijving, zodat je nieuwere resultaten kunt bekijken, bijvoorbeeld na een rustig weekend. De taak leest alleen gegevens, wordt één keer per tik uitgevoerd en het nieuwe resultaat vervangt het oude.

Er staan maximaal drie suggesties tegelijk klaar. Na een week met succesvolle uitvoeringen vraagt de routine **De oude OpenClaw-taak uitzetten?**. De taak wordt alleen uitgezet als je op **Uitzetten** tikt. Je kunt hem weer aanzetten in OpenClaw.

## Op basis van wat je doet

Je Machine merkt ook terugkerend werk op en biedt dit als routine aan onder **Voorgesteld**, ook zonder OpenClaw. Hij zoekt naar:

- dezelfde vraag die je drie keer of vaker achter elkaar stelt, zoals "vat elke maandag de openstaande supporttickets samen";
- een e-mail die je regelmatig verstuurt, zoals een wekelijks rapport aan je team;
- nieuwsbrieven en updateberichten die elke week terugkomen;
- een druk Slack-kanaal waar anderen elke week berichten in plaatsen;
- e-mails die je één voor één naar dezelfde persoon doorstuurt, zoals e-mails van school en clubs naar je partner. Een wekelijks overzicht voor die persoon scheelt je het doorsturen;
- hetzelfde verzoek waarop je regelmatig reageert, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Bij elke suggestie staat wat de routine heeft opgemerkt, zoals "4 keer achter elkaar gevraagd" of "6 e-mails doorgestuurd naar Sam in 3 weken". De suggestie is één keer uitgevoerd, zodat je een echt resultaat ziet. Denk bijvoorbeeld aan een teamoverzicht, een briefing voor een wekelijks gesprek, een overzicht van support of ontwikkeling, inzicht in je cijfers of een overzicht van je nieuwsbrieven.

Alleen suggesties die specifiek voor jou zijn en duidelijk nuttig zijn, worden getoond. Een nieuwsoverzicht bevat bijvoorbeeld alleen je eigen nieuwsbrieven, nooit een algemeen overzicht. Als niets geschikt is, krijg je geen suggestie.

De routine controleert maximaal één keer per dag en geeft hooguit één nieuwe suggestie per week, zonder melding. Met **Nee, bedankt** wordt die suggestie niet opnieuw getoond. Doorgestuurde e-mails en antwoorden blijven bij het account waarmee ze zijn verstuurd, zodat Werk en Persoonlijk niet door elkaar lopen. Alles blijft op je Machine. Een to-do die je regelmatig afsluit, wordt in plaats daarvan als terugkerende to-do aangeboden.

## Routines en terugkerende to-do's

Een terugkerende to-do (recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelfstandig uitvoert en aan je laat zien. Gebruik een terugkerende to-do voor "de huur betalen op de eerste van de maand" en een routine voor "vertel me elke vrijdag welke deals zijn stilgevallen".
