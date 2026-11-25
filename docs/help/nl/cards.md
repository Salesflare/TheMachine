---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak die je aandacht nodig heeft, klaar voor jouw akkoord. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 43d9497d3a1c4a86
---
Je Machine leest alles wat nieuw is en maakt alleen een to-do als iets je aandacht nodig heeft. Eén to-do per zaak, ongeacht hoeveel berichten erbij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem dat is afgehandeld terwijl je weg was. De melding blijft staan tot je op **Begrepen** tikt, maximaal één dag, en je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met eerst wat uiterlijk morgen moet gebeuren. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst iets beslissen of beantwoorden; als het werk niet verder kan of gebruikt kan worden zonder iets wat alleen jij weet, zoals een prijs, feit of keuze, staat er onder de titel wat er nodig is), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing waarover je niets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws bij is gekomen (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's, berichten die [later worden verstuurd](send-later.md) en to-do's zonder antwoord op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Lees meer bij [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, zoals '5 minuten geleden gedaan'. To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Nadat je iets hebt verstuurd, staat er kort waar de to-do naartoe is verplaatst, zoals 'Verstuurd. Verplaatst naar Gedaan.' of 'Verstuurd. Verplaatst naar Later tot ma.'. Een antwoord waarin je alleen belooft het werk te doen, zoals 'Ik stuur het dinsdag', laat de to-do openstaan: 'Verstuurd. Open gelaten.' Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de naam van de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of die uiterlijk morgen moeten gebeuren, daarna vragen uit je Fleet, vervolgens vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij is afgerond. Alleen de markering verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of die uiterlijk morgen moeten gebeuren bovenaan, gevolgd door de rest, met de nieuwste eerst. In de zijbalk staat alles in dezelfde volgorde.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals 'PR #3451 samengevoegd', maar dat het nog niet is gesloten. Met **Heropenen** zet je de to-do terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Als de melding bij een bericht staat, sluit hij na een dag vanzelf, met **Ongedaan maken**. Anders wacht hij tot je **Als gedaan markeren** kiest.

Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf gesloten. Een antwoord waarin staat dat er een bestand is bijgevoegd terwijl dat niet zo is, sluit de to-do niet.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: 'Dit is Sam Lee niet.' De afzender wordt weergegeven met zijn eigen adres, nooit met de naam die hij heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, zoals een beoordeling of antwoord, staat bij **Wacht op** welke stap dat is. De to-do staat ingeklapt onder **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer naar voren haalt. Hetzelfde geldt nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later vandaag valt, of de volgende ochtend als de deadline verstreken is. Er staat dan bij op wie hij nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet aanleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Als je jouw deel verstuurt, wordt de to-do niet gesloten. Hij blijft onder **Wacht op anderen** staan tot een bericht laat zien dat het resultaat er is. Daarna wordt hij vanzelf gesloten, met **Ongedaan maken**. Als er niets binnenkomt tegen de tijd dat je erachteraan moet, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als er een week niets nieuws bij een to-do is gekomen, verhuist hij van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je na een paar dagen terugkomt. Niets nieuws betekent dat er geen nieuw bericht bij is gekomen en dat je er zelf niets mee hebt gedaan, zoals een chatbericht sturen, iets bewerken of snoozen. Alleen de to-do bekijken telt niet.

Dringende to-do's, to-do's met een naderende deadline en to-do's waarvan iets wordt verstuurd, blijven onder Voor jou staan. Met **Alles afwijzen** markeer je na één bevestiging alle to-do's onder Ouder als niet nodig. Je kunt ze ook één voor één als **Niet nodig** markeren. Met **Ongedaan maken** maak je dit ongedaan. Zodra er iets nieuws gebeurt bij een to-do, komt hij weer onder Voor jou te staan.

Bij een to-do waar niemand een week iets mee heeft gedaan, verschijnt één keer de vraag **Nog nodig?** Met **Niet nodig** sluit je de to-do, met **Ongedaan maken** als optie. Met **Houden** behoud je de to-do en wordt deze vraag niet opnieuw gesteld. Als je nog een week niet antwoordt, wordt de to-do ingeklapt onder Komt later terug en telt hij niet meer mee voor het aantal op het appicoon of het ochtendoverzicht. Als je de to-do opent, een chatbericht stuurt, iets bewerkt of snoozet, of als er een nieuw bericht binnenkomt, komt hij weer terug.

Eén keer per week kan een project waar het stil is geworden en geen openstaande to-do's heeft, een to-do met één specifieke volgende stap krijgen. Dat gebeurt maximaal drie keer per week. Lees meer bij [Projecten](projects.md).

Als niets je aandacht nodig heeft, rust je Machine uit met een lege lijst. Tijdens een controle wordt hij even wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer wordt dezelfde keuze gebruikt. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst kun je ook meteen naar de andere weergave. Tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat erin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om het overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op de **×** tikt, staat het op al je apparaten tot het volgende overzicht.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do van een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Lees meer bij [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die hij kan lezen en versturen verhuist mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en de berichten waar hij vandaan komt daar allemaal staan, wordt hij vanzelf naar dat gebied verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt aangemerkt, telt als Privé. Mail voor een ander bedrijf van je komt bij de to-do's van dat bedrijf terecht. Een to-do over je eigen leven, zoals familie die naar je werkadres schrijft, is vanaf het begin Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant op WhatsApp, een bestelling in je persoonlijke mailbox of een [belofte](promises.md) over werk, is vanaf het begin Werk.

Een to-do die je zelf hebt verplaatst of aangemaakt, blijft altijd staan waar je hem hebt gezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, niet waar hij op antwoorden reageert. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do reageert nog steeds vanaf het werkadres waarop de e-mail is binnengekomen en verschijnt nooit in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's wachten, doorloopt **Doorlopen** in de kop van Voor jou ze één voor één, in de volgorde van de lijst. Je ziet elk concept volledig, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. In de kop staat hoe lang het duurt als je je eigen tempo aanhoudt, zoals 'ongeveer 2 min'.

Aan het einde zie je hoeveel to-do's zijn verstuurd of gesloten en hoeveel er nog worden voorbereid.

Een to-do met een vraag aan jou wordt overgeslagen: hij heeft je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert nieuwe berichten zodra er 40 berichten klaarstaan of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden bij de volgende controle meegenomen, binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat 'Nachtpauze. Inhalen om 06:30'. Klikken, typen of scrollen in de app, iets schrijven in de chat of 's nachts op een to-do tikken, zorgt ervoor dat controles weer gewoon doorgaan tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, vind je deze optie bovenaan op een computer. Er staat alleen een korte melding zolang een controle bezig is of als er een is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden, uit elke gelezen bron. Bijvoorbeeld: '13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's' of '· 2 nieuwe to-do's'. De regel gaat alleen over die controle. To-do's die al op je lijst stonden, blijven staan zoals ze zijn. Als een nieuwe to-do op een beter moment wacht, zoals je ochtendoverzicht, staat erbij tot wanneer: '1 to-do uitgesteld tot morgen 08:30'.

Tik op de regel om alle e-mailthreads, chats en meldingen te bekijken, met het pictogram van de bron. Je ziet wie het bericht schreef, het onderwerp of de eerste woorden en de nieuwe to-do of waarom er niets nodig was, zoals 'Alleen in cc, een teamgenoot antwoordt' of 'Meeting voor donderdag staat al gepland'. Bij een thread wordt geen reden getoond als de controle alleen een vage reden gaf. Tik op een item om het bericht en de bijbehorende berichten te lezen.

De eerste 10 items worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat bevat. Een Android-melding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen e-mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails die The Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of getoond. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Lees meer bij [Doe het](do-it.md) en [Snooze](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan of, zodra een concept klaarstaat, wat je eraan wilt wijzigen. Als je je bericht niet afmaakt, staat het er nog als je terugkomt. Met **Annuleren** verwijder je het.

**Als gedaan markeren** betekent dat de to-do is afgehandeld. Op een computer staat deze optie bij de andere knoppen als alles op één regel past. Op een telefoon is hij direct zichtbaar bij een klaargezette to-do zonder concept of bij een to-do met een vraag aan jou. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen uit de lijst, met **Ongedaan maken** in de melding. Veeg de melding weg of sleep hem met de muis uit beeld om hem sneller te sluiten. De wijziging blijft staan.

Wil je dat de to-do op een andere manier wordt afgehandeld, zeg dat dan in de **Chat**. Het antwoord noemt alleen wat er is veranderd, zoals een snooze en tot wanneer. Als iets niet kon worden aangepast, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: draag de to-do over aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om hem te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt regelmatig terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de to-do een andere naam te geven. Je kunt dat ook in de chat vragen, bijvoorbeeld: 'Hernoem deze naar …'. De titel blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander, maar niet na je eigen antwoord. Je ziet dan wanneer hij is teruggekomen en hij wordt als nieuw gesorteerd. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een geregistreerde kaart, niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld doordat de afzender bevestigt dat de betaling binnen is, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die maar tot een bepaald tijdstip relevant is, zoals een bevestiging vóór een meeting, wordt na dat tijdstip vanzelf gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding 'Niet meer nodig'. Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht aan iemand als klaar wordt getoond, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand om iets is gevraagd en ja heeft gezegd, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als iemand anders in hetzelfde gesprek heeft geschreven nadat je concept is gemaakt, wordt **Versturen** tijdelijk geblokkeerd: 'Niet verstuurd: nieuw bericht in de thread'. Bij de to-do staat dat bericht, met **Lezen** en **Opnieuw voor dit bericht**. Druk opnieuw op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld doordat een feest naar een andere locatie is verplaatst of een reservering is geannuleerd, werkt The Machine zijn to-do's zelf bij. Een to-do die nog relevant is, volgt het nieuwe plan. Als er niets meer te doen is, wordt hij verplaatst naar **Gedaan / afgewezen** met de melding 'Niet nodig'. In de chat staat 'Bijgewerkt:' met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en de uitleg dat er niets wordt verstuurd tot je op **Versturen** drukt. De tip verdwijnt definitief zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat er wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat zodra je er bent.

Elke to-do begint met de titel. De regel eronder vermeldt over wie de to-do gaat, de organisatie als die relevant is, het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie wordt een foto of logo getoond als de Graph die heeft. Anders zie je de initialen. Als een logo op dat formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een brede woordmarkering, worden ook de initialen getoond.

Soms staat er een korte, gedempte regel met iets wat onbekend is, zoals 'Laatste contact 12 dagen geleden per e-mail; sindsdien niets.' Die regel verschijnt als het laatste contact met die persoon lang geleden of onbeantwoord is, en noemt kanalen die niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet, in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

De titel zegt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, zoals 'Gedaan: Sam heeft dinsdag getekend'.

Boven het concept staat een subtiele regel met het bericht waar het vandaan komt en het logo van die dienst. Tik erop om de thread te lezen. Het concept toont het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een Slack-antwoord of e-mail is.

Als het concept is gebaseerd op iemands input ergens anders, zoals de suggestie van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld 'Gebaseerd op Sam in #ops'. Tik erop om dat bericht te lezen. De regel verdwijnt wanneer een update het concept vervangt.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, met de oudste berichten eerst: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je eigen berichten rechts, net als in de app. Bij het bericht waar de to-do over gaat, staat 'Deze to-do' en het wordt geopend. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Een e-mailthread wordt ingeklapt boven en onder het bericht getoond.

Een bericht wordt op dezelfde manier geopend vanuit Zoeken, de Graph, antwoorden van Ask of de laatste controle. Het is gemarkeerd als 'Dit bericht' of 'Nieuwe berichten'.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android opent hij in de Gmail-app als je die hebt.

Bij **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets aan toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link van een to-do naar het bijbehorende bericht open je het hier ook. Onderaan staat **Openen in Slack**.

Bij **Details** staan de naam, het project en het gebied van de to-do. Tik erop om iets te wijzigen. Je vindt er ook je laatste notitie en het resultaat van een programmeeragent. Tik op de titel om de chat te openen. Een afgeronde to-do blijft kort. Het bericht waar hij vandaan komt, staat onder **Details**.

Bij een to-do met 'Wacht op' staat een link naar je laatste bericht aan de ander en het bericht waarop je wacht, bijvoorbeeld: 'E-mail aan Pat · di'.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat je maar wilt. Door een to-do aan te maken, wordt niets verstuurd. Als je **Werk** of **Privé** niet kiest, komt de to-do terecht waar hij thuishoort, op basis van wie en wat de to-do betreft. Je Machine vindt ook de e-mail op waar de to-do een vervolg op is, zelfs als die ouder is.

Als je de to-do sluit voordat je hem toevoegt, blijven je tekst en keuzes bewaard tot de volgende keer. Bestanden worden niet bewaard. Met **Weggooien** in de melding verwijder je ze.

- **Deadline**: typ een dag of tijd, zoals 'morgen', 'volgende vr', '3 nov', '14:00' of 'over 2 uur'. Dat kan ook in je eigen taal. Het kalenderpictogram bevat snelle opties en **Kies een datum**.
- **Herhaalt**: de to-do komt regelmatig terug. Lees meer bij [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichtpictogram: voeg het bericht toe waar de to-do over gaat. Dat kan een e-mail, bericht in Slack, Teams, WhatsApp, Telegram of een ander bericht zijn dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft gestuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een schermafbeelding of sleep bestanden naar het formulier. Op een telefoon maakt de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en je Machine leest ze wanneer hij eraan werkt. Alleen bestanden zijn genoeg: je Machine vult de to-do in op basis van een pdf of tekstbestand. Een foto wordt als kleine afbeelding getoond. Tik erop om hem op ware grootte te bekijken.
