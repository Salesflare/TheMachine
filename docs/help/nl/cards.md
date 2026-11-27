---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak die je aandacht vraagt, klaar voor jouw akkoord. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: dfbc7ccc7313ecfe
---
Je Machine leest alles wat nieuw is en maakt alleen een to-do als iets je aandacht vraagt. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem dat is afgehandeld terwijl je weg was. Deze blijft staan tot je op **Begrepen** tikt, maximaal een dag. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met eerst wat uiterlijk morgen moet gebeuren. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar, en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven; als het werk niet verder kan of niet gebruikt kan worden zonder iets wat alleen jij hebt, zoals een prijs, een feit of een keuze, staat er onder de titel wat dat is), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing, zonder iets waarover je hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws bij is gekomen (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij iemand anders aan zet is (zie hieronder).
- **Komt later terug**: gesnoozede to-do's, berichten die [later worden verstuurd](send-later.md) en to-do's waarop nog geen antwoord is op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Bekijk [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, zoals "Gedaan 5 minuten geleden". To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is verplaatst, zoals "Verstuurd. Verplaatst naar Gedaan." of "Verstuurd. Verplaatst naar Later tot ma." Een antwoord waarin alleen wordt beloofd dat het werk wordt gedaan, zoals "Ik stuur het dinsdag", laat de to-do openstaan: "Verstuurd. Open gelaten." Met **Openen** ga je ernaartoe. Zoeken vindt een to-do op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst wat te laat is of uiterlijk morgen moet gebeuren, daarna vragen uit je Fleet, dan vervolgacties op een bord en daarna de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en als hij klaar is: alleen de markering verandert. In de andere open groepen staan wat te laat is of uiterlijk morgen moet gebeuren bovenaan, en de rest op volgorde van nieuw naar oud. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals "PR #3451 samengevoegd", maar dat het nog niet is afgesloten. Met **Heropenen** zet je de to-do terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Als een bericht laat zien dat het werk is afgerond, wordt de to-do na een dag automatisch afgesloten, met **Ongedaan maken**. Anders wacht hij op **Als gedaan markeren**.

Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch afgesloten. Een antwoord waarin staat dat er een bestand is bijgevoegd terwijl dat niet zo is, sluit de to-do niet af.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: "Dit is niet Sam Lee." De afzender wordt weergegeven met diens eigen adres, nooit met de naam die diegene heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, zoals een beoordeling of antwoord, staat **Wacht op:** met de stap die nog moet gebeuren. De to-do staat ingeklapt bij **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer naar voren brengt. Hetzelfde geldt nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later vandaag valt, of de volgende ochtend nadat de deadline is verstreken. Er staat dan op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Je eigen deel versturen sluit de to-do niet af: hij blijft bij **Wacht op anderen** staan tot een bericht het resultaat laat zien. Daarna wordt hij automatisch afgesloten met het resultaat en **Ongedaan maken**. Als er niets binnenkomt tegen de tijd dat je erachteraan moet, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond moet tellen als je dat wilt wijzigen.

Als het resultaat zichtbaar wordt op een openbare webpagina die in de berichten wordt genoemd, zoals een artikel waarin jij wordt vermeld, leest je Machine die pagina wanneer het tijd is om erachteraan te gaan. Als het resultaat op de pagina staat en dat nog niet zo was toen de to-do erop begon te wachten, wordt de to-do automatisch afgesloten. Het resultaat en **Ongedaan maken** worden weergegeven. Je Machine leest de pagina alleen, zoals elke bezoeker, en verstuurt nooit iets.

Als het resultaat niet op de pagina staat en de deadline nog niet is verstreken, leest je Machine de pagina de ochtend na de deadline nog een keer. Anders komt de to-do terug zoals hiervoor, met "Gecheckt" of "Kon niet openen" en de pagina in de chat.

Een to-do waar een week niets nieuws bij is gekomen, wordt verplaatst van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je een paar dagen weg bent geweest. Niets nieuws betekent geen nieuw bericht bij de to-do en ook niets wat jij ermee hebt gedaan, zoals een chatbericht, wijziging of snooze. Alleen de to-do bekijken telt niet.

Dringende to-do's, to-do's die binnenkort moeten gebeuren en to-do's waarvoor iets wordt verstuurd, blijven bij Voor jou staan. Met **Alles afwijzen** markeer je na één bevestiging alle to-do's bij Ouder als niet nodig. Dat werkt hetzelfde als **Niet nodig** voor één to-do, met **Ongedaan maken**. Als er iets nieuws gebeurt bij een to-do, komt hij terug bij Voor jou.

Een to-do waar een week lang niemand iets mee heeft gedaan, vraagt één keer: **Nog nodig?** Met **Niet nodig** sluit je hem af, met **Ongedaan maken**. **Houden** laat hem staan en de vraag wordt niet nog een keer gesteld. Als er nog een week geen antwoord komt, wordt de to-do ingeklapt bij Komt later terug. Hij telt dan niet meer mee voor het aantal op het appicoon en het ochtendoverzicht. Als je hem opent, een chatbericht stuurt, iets wijzigt, snoozet of er een nieuw bericht binnenkomt, komt hij weer terug.

Een project waar een week niets is gebeurd en waar geen open to-do's bij staan, kan één keer per week een to-do krijgen met één concrete volgende stap. Dit gebeurt maximaal drie keer per week. Bekijk [Projecten](projects.md).

Als niets je aandacht vraagt, doet je Machine een dutje en blijft de lijst leeg. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je alle to-do's weer of alleen één soort. Op je telefoon en computer wordt dezelfde keuze gebruikt. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen bij Alle.

Met de regel bovenaan de lijst schakel je ook rechtstreeks naar de andere optie: tik bij **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst vermeldt de naam van je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de optie die je hebt geselecteerd.

Bij een to-do voor een project staat de naam van het project onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Bekijk [De to-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die hij mag lezen en versturen, verhuist mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te kunnen en alle berichten waar hij uit voortkomt daar staan, wordt hij automatisch verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij uit voortkomt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gelabeld, telt als Privé. Mail voor een ander bedrijf van je komt terecht bij de to-do's van dat bedrijf. Een to-do over je eigen leven, zoals familie die naar je werkadres schrijft, is vanaf het begin Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant op WhatsApp, een bestelling in je persoonlijke mailbox of een [belofte](promises.md) over werk, valt vanaf het begin onder Werk.

Een to-do die je zelf hebt verplaatst of aangemaakt, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, nooit waar hij op antwoordt: een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij wordt nooit weergegeven in een Werk-Fleet of Team-Graph.

Als er twee of meer to-do's wachten, loop je ze met **Doorlopen** in de kop van Voor jou één voor één door, in de volgorde van de lijst. Je ziet elk concept helemaal, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, met `S` snooze je, met `→` sla je over en met Esc stop je. In de kop staat hoelang je er in jouw tempo over doet, bijvoorbeeld "ongeveer 2 min".

Aan het einde staat hoeveel er zijn verstuurd of afgesloten en hoeveel er nog worden voorbereid.

Een to-do met een vraag aan jou wordt niet meegenomen: daarvoor is een antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke paar minuten alle bronnen, dag en nacht. Hij controleert nieuwe berichten zodra er 40 zijn of zodra het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden meegenomen bij de volgende controle, uiterlijk binnen een uur.

's Nachts, tussen 00:00 en 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat "'s Nachts gepauzeerd, inhalen om 06:30". Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, worden controles weer zoals gewoonlijk uitgevoerd tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat de optie bovenaan op een computer. Een korte regel wordt daar alleen weergegeven zolang er een controle loopt, of als er een is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat er is gevonden, van alle gelezen bronnen. Bijvoorbeeld "13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's" of "· 2 nieuwe to-do's". Dit gaat alleen over die controle: to-do's die al op je lijst staan, blijven staan zoals ze zijn. Als een nieuwe to-do op een beter moment wacht, zoals je ochtendoverzicht, staat erbij tot wanneer: "1 to-do uitgesteld tot morgen 08:30".

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron. Je ziet wie het bericht schreef, het onderwerp of de eerste woorden en de nieuwe to-do of waarom er niets nodig was, zoals "Alleen in Cc, een teamgenoot antwoordt" of "Meeting staat al gepland voor donderdag". Bij een thread staat geen reden als de controle alleen een algemene reden opleverde. Tik op een bericht om het te lezen, met de berichten eromheen.

De eerste 10 worden weergegeven. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een Android-melding over een bericht dat al in de lijst staat, wordt maar één keer weergegeven. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails die The Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of vermeld. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Bekijk [Doe het](do-it.md) en [Snooze](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets wordt gedaan, of, zodra een concept klaarstaat, wat erin moet veranderen. Laat je tekst onafgemaakt staan, dan staat hij er nog als je terugkomt. Met **Annuleren** verwijder je hem.

Met **Als gedaan markeren** geef je aan dat het is afgehandeld. Op een computer staat deze optie tussen de andere knoppen als ze op één regel passen. Op een telefoon is hij zichtbaar bij een to-do die klaarstaat zonder concept of waarbij je een vraag moet beantwoorden. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen uit de lijst, met **Ongedaan maken** in de melding. Veeg het bericht weg of sleep het met de muis uit beeld om het sneller af te sluiten. De wijziging blijft staan.

Als je wilt dat het op een andere manier gebeurt, zeg dat dan in de **Chat**. In het antwoord staat alleen wat er is veranderd, zoals een snooze en tot wanneer. Als iets niet kon worden gewijzigd, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: draag de to-do over aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om het werk na te kijken](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de to-do een andere naam te geven. Je kunt dit ook in de chat vragen, bijvoorbeeld "Hernoem dit naar …". Je titel blijft staan.

Met **Heropenen** zet je een afgesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de andere persoon, maar niet na je eigen antwoord. Je ziet dan wanneer hij is teruggekomen en hij wordt gesorteerd als nieuw. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betalingsgegevens op de rekening. Rekeningen die automatisch worden betaald, bijvoorbeeld via automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender, wordt de to-do automatisch afgesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die alleen tot een bepaald tijdstip relevant is, zoals een bevestiging vóór een meeting, wordt na dat tijdstip automatisch afgesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding "Niet langer nodig". Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand klaar wordt gezet, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al is afgehandeld, bijvoorbeeld omdat iemand is gevraagd en ja heeft gezegd, wordt de to-do automatisch afgesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als iemand anders iets in hetzelfde gesprek heeft geschreven nadat je concept is gemaakt, houdt **Versturen** het tegen: "Niet verstuurd: nieuw bericht in de thread". Bij de to-do staat dat bericht met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is komen te vervallen, past The Machine zijn to-do's zelf aan. Een to-do die nog relevant is, volgt het nieuwe plan. Als er niets meer te doen is, wordt de to-do verplaatst naar **Gedaan / afgewezen** met de melding "Niet nodig". In de chat staat "Bijgewerkt:" met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's staat een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd tot je op **Versturen** drukt. De tip verdwijnt voorgoed zodra je de knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat er wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je er bent.

Elke to-do begint met de titel. De regel eronder vermeldt voor wie of waar de to-do is, de organisatie als het daarover gaat (niet alleen omdat iemand er werkt), het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie wordt de foto of het logo weergegeven als die beschikbaar is in de Graph. Anders staan er initialen. Als een logo op dat formaat niet leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, worden ook de initialen weergegeven.

Soms staat er een subtiele regel met informatie die ontbreekt, zoals "Laatste contact 12 dagen geleden via e-mail; sindsdien niets." Die verschijnt als het laatste contact lang geleden was of nog geen antwoord heeft gekregen. Ook wordt vermeld welke kanalen niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet, in plaats van te gissen.

Als er een kanaal wordt genoemd dat niet is gekoppeld, open je die koppeling met **Koppelen** ernaast.

Een titel geeft aan wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, zoals "Gedaan: Sam heeft dinsdag getekend".

Boven het concept staat een subtiele regel met het bericht waar het uit voortkomt, met het logo van die dienst. Tik erop om de thread te lezen. Bij het concept staat het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een antwoord in Slack of een e-mail is.

Als het concept voortkomt uit iemands bijdrage elders, zoals een suggestie van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld "Gebaseerd op Sam in #ops". Tik erop om dat bericht te lezen. Het bericht verdwijnt zodra een update het concept vervangt.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je eigen berichten rechts, zoals in de app. Bij het bericht van de to-do staat "Deze to-do" en het wordt in beeld geopend. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Een e-mailthread wordt boven en onder het bericht ingeklapt weergegeven.

Een bericht wordt op dezelfde manier geopend vanuit Zoeken, de Graph, antwoorden van Ask of de laatste controle, met de markering "Dit bericht" (of "Nieuwe berichten").

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt hij geopend in de Gmail-app als je die hebt.

Onder **Details** van een e-mail staat alleen informatie die niet al in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link bij de eigen boodschap van een to-do open je die hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik op een ervan om het te wijzigen), je laatste notitie en het resultaat van een codeeragent. Met de titel open je de chat. Een afgeronde to-do blijft compact; het bericht waar hij uit voortkomt staat onder **Details**.

Bij een to-do met "Wacht op" staat een link naar je laatste bericht aan de ander, waarop je wacht: "E-mail aan Pat · di".

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Er wordt niets verstuurd als je er een maakt. Als je geen **Werk** of **Privé** kiest, komt de to-do terecht waar hij thuishoort, op basis van voor wie of waar hij is. De to-do vindt ook de e-mail waar hij op volgt, zelfs als die al ouder is.

Sluit het venster voordat je de to-do toevoegt en je tekst en keuzes staan er de volgende keer weer. Bestanden blijven niet bewaard. Met **Weggooien** in het bericht verwijder je ze.

- **Deadline**: typ een dag of tijd, zoals "morgen", "volgende vr", "3 nov", "14:00" of "over 2 uur", ook in je eigen taal. Met het kalenderpictogram zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Bekijk [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de mensen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichtpictogram: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maakt de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do staan en The Machine leest ze als hij eraan werkt. Alleen bestanden toevoegen is genoeg: The Machine vult de to-do in op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op volledig formaat te bekijken.
