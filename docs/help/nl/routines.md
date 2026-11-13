---
title: Routines
area: cards
summary: Werk dat je Machine zelf doet, op een ritme, zoals een maandagoverzicht van je open deals. Hij leest alleen.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays
---
## Er een maken

Open **Routines** in de zijbalk en zeg in één regel wat hij moet doen en wanneer: "elke maandag om 9, vat mijn open deals samen" of "elke werkdag 's ochtends, lijst de mails op die ik nog moet beantwoorden". Dan **Toevoegen**.

Zonder tijd draait hij om 8:00. De tijd is die van de klok van je Machine.

## Sjablonen

Onder **Sjablonen** onderaan Routines zet **Toevoegen** een kant-en-klare routine aan. Die draait meteen één keer en daarna elke ochtend om 7:30 (Spam opruimen elk uur). Haar kaart toont haar woorden zoals elke routine, en **Bewerken** past ze of haar naam aan.

Komen er veel nieuwsbrieven binnen terwijl Nieuwsbrieven opruimen uit staat (25 of meer in een week, van minstens 5 afzenders), dan zegt een regel boven je to-do’s hoeveel er kwamen en wat het zou doen, met **Zet het aan** en **Nee, bedankt**.

Spam opruimen wordt zo aangeboden als er in een week 5 of meer mails met de hand naar spam zijn verplaatst. **Zet het aan** voegt het toe zoals **Toevoegen** hier. Na **Nee, bedankt** komt het niet meer terug, en een sjabloon dat je al eens had nooit.

**Nieuwsbrieven opruimen** maakt één to-do per gebied (werk en persoonlijk) met de nieuwsbrieven van de voorbije dag, elk met **Houden** of **Afmelden**. Afmelden gebruikt de afmeldlink met één klik van de lijst, of de afmeldmail vanaf je adres als versturen aanstaat. Anders toont het **Afmeldpagina openen**.

Bonnetjes, bestellingen en betalingsberichten blijven erbuiten. Mail die via een groepsadres binnenkomt, zoals een Google Group, staat onder wie hem schreef en meldt je nooit af bij de groep.

**Spam opruimen** maakt één to-do per gebied met mail van onbekende afzenders die op spam lijkt, elk met **Spam** of **Geen spam**. Outlook verplaatst spam naar Ongewenste e-mail en Gmail markeert het als spam. Het kijkt elk uur, zodat spam er meestal al staat voor jij eraan toekomt. Nieuwe spam komt op dezelfde to-do zolang die open staat.

Het werkt alleen met mail die The Machine mag verplaatsen. Gmail met alleen leesrechten, zoals op een gehoste Machine, kan het niet: het sjabloon zegt dat in plaats van **Toevoegen**.

Onbekend wil zeggen dat je hen nooit schreef, en een “Re:” telt alleen als gesprek in een draad waarin jij schreef. Komt mail van een afzender die je als spam markeerde, op de to-do of in je mailbox, toch weer door, dan staat die op de volgende to-do als **Eerder als spam gemarkeerd**. Wat je zelf naar spam verplaatste, helpt ook om gelijkaardige mail te herkennen.

Er verandert niets tot je bevestigt op de to-do. Tik op een afzender om de mail eerst te lezen: die blijft ongelezen en er verandert niets. Vanuit Spam opruimen laden de afbeeldingen van het web niet, zodat de afzender niet ziet dat de mail geopend is. Afzenders waarover je besliste, komen niet terug. Een dag zonder nieuwsbrieven of spam geeft geen to-do, en deze to-do’s sturen nooit een melding.

Is over elke afzender beslist, dan zegt de to-do dat hij klaar is en staat **Markeer als gedaan** erop.

**Dagelijks overzicht** kiest één keer per dag de paar stukken uit je nieuwsbrieven die je tijd waard zijn, in één to-do. Bij elk staat in één regel waarom het voor jou ertoe doet. Tik erop om de mail te lezen, of gebruik **Openen in je mail**. Alleen nieuwsbrieven: nooit mail van mensen, bonnetjes of afzenders waarvoor je je hebt uitgeschreven, en nooit wat je al gelezen hebt. Springt er niets uit, dan komt er geen to-do.

Het leert wat je belangrijk vindt uit wat je opent, een ster geeft of ongelezen archiveert, en uit **Meer zoals dit** en **Minder zoals dit** bij elk stuk. De onderwerpen waarop het kiest staan op de kaart van de routine onder **Meer over** en **Minder over**. Haal er een weg met ×, of voeg je eigen toe. Gestippelde heeft het zelf geleerd. Een nieuw overzicht vervangt het open overzicht, en het stuurt nooit een melding.

Het leest alleen de afzender, het onderwerp en het begin van elke nieuwe nieuwsbrief, en stelt je AI er één korte vraag over, met een daglimiet, zodat het goedkoop blijft. **Tijdstip wijzigen** zet het tijdstip. Pas je de woorden aan, dan draait het als elke routine op jouw woorden.

**Verjaardagen** maakt een to-do voor elk naast contact dat vandaag jarig is: mensen naar wie je zelf schrijft, zoals vrienden, familie en vaste contacten. Elke to-do heeft een korte felicitatie, opgesteld waar je meestal met hen praat, zoals hun WhatsApp-chat of je mailthread, in hun taal. Die gaat pas weg als jij hem verstuurt. Een dag zonder verjaardagen geeft geen to-do.

Verjaardagen komen uit je agenda’s (de verjaardagen en de agenda Verjaardagen van Google, elke ochtend gelezen, ook als ze niet gesynchroniseerd worden, en de agenda Verjaardagen van Outlook), je Google-contacten op een zelf gehoste Machine en een datumveld Verjaardag bij een persoon in de Graph. Staat er nog nergens een verjaardag, dan zegt het resultaat **Nog geen verjaardagen bekend** en hoe je ze toevoegt.

**Verjaardagen importeren uit Facebook**: zodra Verjaardagen aan staat, biedt een to-do aan om de verjaardagspagina van Facebook te lezen. Tik op **Importeren** en The Machine opent ze in zijn browser, scrolt tot elke maand geladen is en leest de naam en verjaardag van elke vriend. Hij toont hoeveel hij vond en wie op voor- en achternaam overeenkomt met mensen in je Graph. Een naam die meer dan één persoon heeft, wordt overgeslagen en vermeld.

Alleen **Bewaren** houdt ze bij, op de pagina van elke persoon: de verjaardag, en de Facebook-profielfoto voor wie nog geen foto heeft. Een verjaardag of foto die je daar zelf instelde, blijft, en een foto die iemand al heeft, wordt nooit vervangen. Er wordt niets naar Facebook geschreven.

Hij leest nooit vanzelf opnieuw: **Opnieuw importeren** op de to-do doet dat. De browser moet aangemeld zijn bij Facebook. Is hij dat niet, tik dan op **Inloggen bij Facebook** op de to-do en log daar in; daarna leest hij de pagina vanzelf. The Machine meldt zich nooit voor je aan.

Vrienden die niemand in je Graph heeft, worden geteld, met een paar namen. **Voeg … toe als persoonlijke contacten** voegt ze allemaal tegelijk toe, ook na Bewaren: elk met naam en verjaardag, nooit gedeeld met een Work Fleet. Een naam die al iemand in je Graph heeft, of die iemand had die je definitief verwijderde, wordt overgeslagen. Verjaardagsherinneringen komen nog altijd alleen voor mensen naar wie je schrijft.

**Ongedaan maken** op de to-do haalt precies die mensen weer weg, ook na **Opnieuw importeren**.

Zolang haar woorden die van het sjabloon zijn, draait ze op eigen code, zonder je AI-abonnement (Spam opruimen zet nieuwe mail van onbekende afzenders eerst met code op een rij, en stelt je AI alleen een korte vraag als er zulke mail is). Een nieuwe naam houdt dat zo. Pas je haar woorden aan, dan draait ze zoals elke routine op jouw woorden.

Nieuwsbrieven opruimen en Spam opruimen eindigen nog altijd in dezelfde to-do met een keuze per mail. Een aangepaste Verjaardagen geeft haar resultaat en hoogstens één concept, geen to-do per persoon. **Terug naar het sjabloon** in **Bewerken** zet haar woorden terug.

## Wat een routine doet

Op het afgesproken moment leest je Machine wat hij nodig heeft, zoals je berichten, vergaderingen en de Graph, en zet het resultaat op de pagina Routines. Elk resultaat zegt **Klaargezet**, **Niets nieuws** (met waarom) of **Lukte niet** (met waarom). Een run die zonder resultaat eindigt, telt als een run die niet lukte, nooit als klaar.

Routines lezen alleen: je berichten, webpagina’s, GitHub en sites zoals X in de browser. Ze versturen, beantwoorden, posten of wijzigen niets. Alleen een sjabloon wijzigt mail, en alleen wat je op zijn to-do bevestigt.

Eindigt de taak van een routine in een post of bericht, dan doet ze alles tot die stap en toont ze het concept, zoals **Zou op X posten:**. Na een echte run krijg je het als to-do om goed te keuren; een testrun toont het alleen. De naam zegt waarover het gaat en waar het naartoe gaat, de knop noemt de stap, zoals **Plaatsen**, en **Van je routine** eronder opent de routine.

De to-do begint in het gebied van het account waar hij vandaan gaat, zoals Werk voor het X-account van je bedrijf, dus hij vraagt nooit om te verhuizen.

Elke run kent het vorige resultaat, zodat hij kan zeggen wat er sindsdien veranderde.

Na een goede run kan je Machine zelf een recept schrijven voor het lezen dat elke keer hetzelfde is, zoals welke mails of GitHub-wijzigingen hij bekijkt. De volgende runs lezen dat eerst, in gewone code, en de AI kiest alleen wat telt en schrijft het op, met minder tokens. Een recept leest alleen; werkt het niet meer, dan leest de run zelf en herstelt hij het. Je ziet het onder **Geavanceerd: scriptstappen** in het ⋯-menu.

## Gemiste dagen

Stond je Machine uit of had hij het druk, dan stapelen gemiste runs zich niet op: alleen de nieuwste draait, één keer. Elke datum draait één keer, ook na een herstart.

Routines draaien één voor één en wachten als het gebruik van je AI-abonnement laag staat, zoals al het werk op de achtergrond. **Nu uitvoeren** draait hem meteen.

## Wijzigen of stoppen

Dit staat in het ⋯-menu van de routine. **Wanneer wijzigen** neemt een nieuw ritme in je eigen woorden, zoals "elke werkdag om 8". **Pauzeren** stopt de runs tot **Hervatten**; wat tijdens de pauze gemist werd, draait niet achteraf. **Stoppen** beëindigt een routine voorgoed.

Gebruik je **Wijzigingen vragen** op een to-do van een routine, of schrijf je in de chat ervan, en geldt je opmerking voor elke run, zoals "nooit emoji", dan biedt de to-do **Ook de routine aanpassen** aan, op de to-do en in de chat onder het antwoord. Die toont wat er in de woorden van de routine verandert, en de routine verandert pas als je op **Aanpassen** tikt. **Laat zo** laat de routine ongemoeid. Een correctie van alleen dat concept biedt niets aan.

## Geavanceerd: scriptstappen

Een script heb je nooit nodig: zeg in je eigen woorden wat een routine moet doen.

Voor gevorderden kan een routine ook je eigen commando's op je Machine draaien: kies in het ⋯-menu **Geavanceerd: scriptstappen**. **Bewerken** toont ze alleen als een routine er al heeft. **Gegevens ophalen** draait eerst een commando, in zijn map (leeg: je thuismap) en hoogstens zijn aantal seconden. Wat het afdrukt, krijgt de run om mee te werken. Zonder woorden is wat het afdrukt het resultaat.

**Controle** krijgt na de run het resultaat als invoer. Eindigt die met een fout, dan toont de run **Lukte niet** met wat de controle zei. Een commando bij Gegevens ophalen dat faalt, toont zich net zo.

Een commando is één regel en draait zonder shell: geen pipes of variabelen. Scriptstappen stel alleen jij in, op je dashboard. Een testrun en **Probeer het** draaien Gegevens ophalen ook en zeggen dat; ze versturen en bewaren nog steeds niets. Een routine verstuurt nooit, dus een scriptstap leest best alleen.

## Uit je OpenClaw-taken

Maakte je eerder geplande taken in OpenClaw, dan leest je Machine ze (hij wijzigt ze nooit) en stelt de passende voor als routine onder **Voorgesteld**. Elke liep één keer, zodat je een echt resultaat ziet.

Je correcties op de taak blijven, wat hij verstuurde of postte valt weg. Een taak die een script draaide, of las wat een scripttaak verzamelde, neemt dat mee als Gegevens ophalen. **Toevoegen** maakt er een routine van, **Nee, bedankt** vraagt nooit meer naar die taak. Een taak die je aan iets herinnerde, komt in plaats daarvan als aanbod voor een terugkerende to-do bij To-do's.

Voor je een voorstel toevoegt, pas je het aan met **Bewerken** en **Wanneer wijzigen** in het ⋯-menu, zoals elke routine. **Opnieuw uitvoeren** voert het nu uit met de huidige woorden, zodat je nieuwere resultaten ziet, bijvoorbeeld na een rustig weekend. Het leest alleen, loopt één keer per tik, en het nieuwe resultaat vervangt het oude.

Er wachten hoogstens drie voorstellen tegelijk. Na een week goede runs vraagt de routine **De oude OpenClaw-taak uitzetten?** Hij gaat pas uit als je op **Uitzetten** tikt, en je kunt hem in OpenClaw weer aanzetten.

## Uit wat je doet

Je Machine merkt ook werk op dat je op een ritme doet en stelt het voor als routine onder **Voorgesteld**, ook zonder OpenClaw. Hij let op:

- dezelfde vraag, drie keer of meer op rij, zoals "vat de open supporttickets samen" elke maandag;
- een mail die je op een ritme verstuurt, zoals een weekrapport aan je team;
- nieuwsbrieven en updatemails die elke week terugkomen;
- een druk Slack-kanaal waar anderen elke week in schrijven;
- mails die je één voor één doorstuurt naar dezelfde persoon, zoals mails van school en de club naar je partner: een wekelijks overzicht voor hen bespaart het doorsturen;
- dezelfde vraag die je op een ritme beantwoordt, zoals een maandelijkse goedkeuring voor dezelfde persoon.

Elk voorstel zegt wat hij zag, zoals "4 keer op rij gevraagd" of "6 mails doorgestuurd naar Sam in 3 weken", en liep één keer, zodat je een echt resultaat ziet. Denk aan een teamoverzicht, een briefing voor een wekelijkse call, een support- of dev-overzicht, een stand van je cijfers of een samenvatting van de nieuwsbrieven die je krijgt.

Hij stelt alleen voor wat bij jou past en duidelijk helpt: een nieuwsoverzicht alleen over je eigen nieuwsbrieven, nooit een algemeen. Past er niets, dan is er geen voorstel.

Hij kijkt hoogstens één keer per dag en brengt hoogstens één nieuw voorstel per week, zonder melding. **Nee, bedankt** brengt dat voorstel nooit terug. Doorgestuurde mails en antwoorden blijven bij het account waarvan ze vertrokken, zodat Werk en Privé niet mengen. Alles blijft op je Machine. Een to-do die je op een ritme afvinkt, komt in plaats daarvan als aanbod voor een terugkerende to-do.

## Routines en terugkerende to-do's

Een terugkerende to-do (recurring.md) herinnert je eraan iets te doen. Een routine is werk dat je Machine zelf doet en je laat zien. Neem een terugkerende to-do voor "de huur betalen op de eerste", en een routine voor "elke vrijdag zeggen welke deals stilvielen".
