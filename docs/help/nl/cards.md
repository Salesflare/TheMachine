---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak waarbij je iets moet doen, klaar om door jou goedgekeurd te worden. Dit betekenen de verschillende onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 16f31364b3da3827
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als er iets van je nodig is. Eén to-do per kwestie, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze per groep:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een melding, die is afgehandeld terwijl je weg was. Hij blijft hier staan tot je op **Begrepen** tikt, maximaal één dag. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing, zonder dat je iets hoeft te beslissen).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop je niet hebt gereageerd bij **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, nieuwste eerst, met het tijdstip waarop ze zijn afgerond, zoals "5 minuten geleden afgerond". To-do's die al afgerond lijken, krijgen het label **Lijkt gedaan**.

Nadat je iets hebt verstuurd, staat er een korte melding met waar de to-do naartoe is gegaan, zoals "Verstuurd. Verplaatst naar Gedaan." of "Verstuurd. Verplaatst naar Later tot ma." Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de naam van de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of morgen valt, dan vragen van je Fleet, vervolgens vervolgacties van een bord en daarna de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij klaar is. Alleen het label verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of morgen valt bovenaan, gevolgd door de nieuwste. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat de to-do is afgerond, bijvoorbeeld "PR #3451 samengevoegd", maar dat hij nog niet is gesloten. Met **Heropenen** zet je hem terug op je lijst. Je Machine leert hiervan. Deze to-do's worden nooit als te laat weergegeven. Na een dag wordt de to-do automatisch gesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch gesloten.

Komt een bericht van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, dan staat dat duidelijk bij de to-do: "Dit is niet Sam Lee." De persoon wordt weergegeven met het eigen e-mailadres, nooit met de naam die in het bericht staat. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, vermeldt die stap bij **Wacht op**. Hij staat ingeklapt in **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer laat verschijnen. Hetzelfde geldt nadat jij een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die vandaag valt, of de volgende ochtend als de deadline al voorbij is. Er staat dan op wie hij nog wacht.

Gaat een to-do over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, dan staat dat bij **Details** onder **Klaar als**. Als je jouw deel verstuurt, wordt de to-do niet gesloten. Hij blijft in **Wacht op anderen** tot een bericht laat zien dat het resultaat binnen is. Daarna wordt hij automatisch gesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Is het tijd om diegene eraan te herinneren, maar is er nog niets binnen, dan komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond geldt om dit aan te passen.

Een to-do waar een week lang niemand iets mee heeft gedaan, vraagt één keer **Nog nodig?**. Met **Niet nodig** sluit je hem. Je kunt dat ongedaan maken met **Ongedaan maken**. Met **Houden** blijft hij staan en wordt het nooit nog eens gevraagd. Krijgt hij nog een week geen antwoord, dan wordt hij ingeklapt onder Komt later terug. Hij telt dan niet meer mee voor het aantal op het appicoon en het ochtendoverzicht. Als je hem opent, een chatbericht stuurt, hem bewerkt of snoozet, of als er een nieuw bericht binnenkomt, verschijnt hij weer.

Eén keer per week kan een stilgevallen project zonder openstaande to-do's een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als er niets is waarbij je iets moet doen, rust je Machine uit en blijft je lijst leeg. Tijdens een controle wordt hij actief en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je aan of je alle to-do's wilt zien of alleen één soort. Je telefoon en computer gebruiken dezelfde keuze. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en verschijnt alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook direct over naar de andere selectie. Tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De balk bovenaan de lijst vermeldt je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, zie je **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de selectie die je hebt gemaakt.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten om te lezen en te versturen verhuist mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij vandaan komt daar staan, wordt hij automatisch verplaatst en gaat hij verder. Anders zie je **Naar Werk verplaatsen**. Er wordt niets verplaatst tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gelabeld, telt als Privé. Mail voor een ander bedrijf van je komt bij de to-do's van dat bedrijf terecht. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, valt vanaf het begin onder Privé.

Werk dat binnenkomt op een privéaccount, zoals een klant via WhatsApp of een bestelling in je privémailbox, valt vanaf het begin onder Werk. Een to-do die je zelf hebt verplaatst of toegewezen, blijft altijd staan waar je hem hebt gezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, nooit waar hij op antwoordt. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n to-do onder Privé antwoordt nog steeds vanaf het werkadres waarop de mail binnenkwam. Hij verschijnt nooit in een Work Fleet of de Team Graph.

Als er twee of meer to-do's wachten, loop je er met **Doorlopen** in de kop van Voor jou één voor één doorheen, in de volgorde van de lijst. Je ziet elk concept helemaal, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. Onder de titel staat in de kop ook hoe lang het ongeveer duurt als je je eigen tempo aanhoudt, bijvoorbeeld "ongeveer 2 min".

Een to-do die je iets vraagt, staat niet in deze lijst. Daarvoor moet je antwoorden, niet tikken.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Zodra er 40 berichten klaarstaan of het oudste bericht van iemand 15 minuten heeft gewacht, controleert hij wat er is binnengekomen. Nieuwsbrieven, meldingen en ontvangstbewijzen worden meegenomen bij de volgende controle, uiterlijk binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 in één keer gecontroleerd. Zo zijn je to-do's klaar voordat je ochtendoverzicht binnenkomt. Onder Koppelingen staat bij controles: "'s Nachts gepauzeerd, haalt om 06:30 de achterstand in". Typ, klik of scrol in de app, schrijf in de chat of tik 's nachts op een to-do, dan worden controles weer zoals gewoonlijk uitgevoerd tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** worden alle bronnen meteen gelezen. Staat er niets open, tik dan op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat die regel bovenaan op een computer. Daar verschijnt een korte melding alleen als er een controle loopt, is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden in elke gelezen bron, bijvoorbeeld "13 berichten gecontroleerd om 16:11 · niets nodig" of "· 2 nieuwe to-do's". Als een nieuwe to-do op een beter moment wacht, zoals je ochtendoverzicht, staat erbij tot wanneer: "1 to-do uitgesteld tot morgen 08:30".

Tik op de regel om alle e-mailthreads, chats en meldingen te zien, met het icoon van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of de reden waarom er niets nodig was, zoals "Alleen in cc, een teamgenoot antwoordt" of "Vergadering staat al voor donderdag gepland". Bij een thread wordt geen reden weergegeven als de controle alleen een vage reden opleverde. Tik erop om het bericht te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat bevat. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle zichtbaar.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails die je Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of in de lijst gezet. Mail over facturering, je proefperiode of een uitnodiging wordt wel gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe het moet worden gedaan, of, zodra een concept klaarstaat, wat daarin moet veranderen. **Markeer als gedaan** betekent dat de to-do is afgehandeld. Bij een klaargezette to-do zonder concept staat deze knop in beeld. Anders staat hij bovenaan onder **…**, ook bij een to-do waarvoor je een beslissing moet nemen. De to-do verdwijnt meteen van de lijst. In de melding staat **Ongedaan maken**. Veeg de melding weg of sleep hem met de muis opzij om hem sneller te sluiten. De wijziging blijft staan.

Wil je dat de to-do op een andere manier wordt gedaan, vertel dat dan in **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om hem te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel aangeven waarom: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert hiervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. De titel die je kiest, blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van die persoon, maar niet na je eigen antwoord. Je ziet dan wanneer hij is teruggekomen en hij wordt als nieuw gesorteerd. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals een automatische incasso of een opgeslagen betaalkaart, worden dat niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender dat je betaling is ontvangen, wordt de to-do automatisch gesloten. Je kunt hem een dag lang terugzetten met **Ongedaan maken**.

Een to-do die maar tot een bepaald tijdstip relevant was, zoals een bevestiging vóór een vergadering, wordt na dat tijdstip automatisch gesloten. Hij komt bij **Gedaan / afgewezen** te staan als "Niet meer nodig". Je kunt hem een dag lang terugzetten met **Ongedaan maken**.

Voordat een bericht of overdracht aan iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokkenen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat iets al is geregeld, bijvoorbeeld omdat iemand erom was gevraagd en ja heeft gezegd, wordt de to-do automatisch gesloten. Je kunt hem een dag lang terugzetten met **Ongedaan maken**.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, past The Machine zijn to-do's zelf aan. Een to-do die nog relevant is, volgt het nieuwe plan. Als er niets meer hoeft te gebeuren, komt hij bij **Gedaan / afgewezen** te staan als "Niet nodig". In de chat staat dan "Bijgewerkt:" met de reden. Je kunt hem een dag lang terugzetten met **Ongedaan maken**.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Er staat ook in dat er niets wordt verstuurd tot je op **Versturen** drukt. Een tip verdwijnt voorgoed zodra je de knop gebruikt of op × drukt.

Op je eerste dag heet de tekst bovenaan To-do's je welkom en noemt hij wie het langst op je antwoord heeft gewacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je aankomt.

Elke to-do begint met de titel. De regel eronder vermeldt op wie hij betrekking heeft, de organisatie als die relevant is (niet alleen omdat iemand er werkt), het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om die persoonspagina in Graph te openen.

Bij een naam en organisatie wordt een foto of logo getoond als Graph die heeft, anders de initialen. Een logo dat op dat formaat niet goed leesbaar is, zoals witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook met initialen weergegeven.

Soms staat er een korte melding met wat niet bekend is, zoals "Laatste contact 12 dagen geleden via e-mail; sindsdien niets." Die verschijnt als het laatste contact met die persoon oud of onbeantwoord is. Ook worden niet-gekoppelde kanalen genoemd, zoals WhatsApp. Je Machine vertelt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, open je die koppeling met **Koppelen** ernaast.

De titel vermeldt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, zoals "Gedaan: Sam heeft het dinsdag ondertekend".

Boven het concept staat op een lichte regel van welk bericht het afkomstig is, met het logo van de dienst. Tik erop om de thread te lezen. Bij het concept staat het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het om een Slack-antwoord of een e-mail gaat.

Als het concept voortkomt uit iemands input ergens anders, zoals een suggestie van een teamgenoot in Slack, staat dat op een regel, bijvoorbeeld "Gebaseerd op Sam in #ops". Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten van vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je eigen berichten rechts, net als in de app. Bij het bericht van de to-do staat "Deze to-do" en het wordt open weergegeven. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mail wordt de rest van de thread ingeklapt erboven en eronder getoond.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt hij geopend in de Gmail-app als je die hebt.

Onder **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige cc-adressen, bcc of een ander antwoordadres. Als er niets extra's is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link van een to-do naar het eigen bericht open je het hier ook, met onderaan **Openen in Slack**.

Onder **Details** staan de naam, het project en het gebied (tik erop om ze te wijzigen), je laatste notitie en het resultaat van een codeeragent. Met de titel open je de chat. Een afgeronde to-do blijft kort. Het bericht waar hij vandaan komt, staat onder **Details**.

Een to-do met de status "Wacht op" linkt naar je laatste bericht aan die persoon, waarop je wacht: "E-mail aan Pat · di".

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Als je er een maakt, wordt er niets verstuurd. Als je geen **Werk** of **Privé** kiest, komt de to-do terecht waar hij thuishoort, op basis van wie en wat erbij horen. Je Machine vindt ook de e-mail waarop de to-do volgt, zelfs als die al ouder is.

- **Deadline**: typ een dag of tijd, zoals "morgen", "volgende vr", "3 nov", "14:00" of "over 2 uur". Dat kan ook in je eigen taal. Met het kalendericoon zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waarop de to-do betrekking heeft, maximaal 5.
- Berichticoon: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × haal je een bestand weer weg.

De bestanden blijven bij de to-do staan en The Machine leest ze als hij eraan werkt. Alleen bestanden zijn genoeg: de to-do wordt automatisch ingevuld op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding getoond. Tik erop om hem op ware grootte te bekijken.
