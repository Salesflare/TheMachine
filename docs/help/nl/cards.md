---
title: To-do's
area: cards
summary: Eén to-do per ding dat je aandacht nodig heeft, klaar voor jouw akkoord. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e1656daff6fc566a
---
Je Machine leest alles wat nieuw is en maakt alleen een to-do als iets je aandacht nodig heeft. Eén to-do per onderwerp, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem dat is opgelost terwijl je weg was. Hij blijft staan tot je op **Begrepen** tikt, maximaal één dag. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (eerst is je beslissing of antwoord nodig; als het werk niet verder kan of niet gebruikt kan worden zonder iets wat alleen jij hebt, zoals een prijs, feit of keuze, staat er onder de titel wat dat is), **Aan het voorbereiden…** (je Machine werkt eraan) of **Om te lezen** (een overzicht of briefing, zonder dat je iets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws bij is gekomen (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarvoor iemand anders aan zet is (zie hieronder).
- **Komt later terug**: to-do's die gesnoozed zijn en to-do's waarop je niet hebt gereageerd op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, zoals '5 minuten geleden gedaan'. To-do's die al afgerond lijken, hebben het label **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is verplaatst, zoals 'Verstuurd. Verplaatst naar Gedaan.' of 'Verstuurd. Verplaatst naar Later tot ma.'. Een antwoord waarin je alleen belooft het werk te doen, zoals 'Ik stuur het dinsdag', laat de to-do open: 'Verstuurd. Open gelaten.' Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of morgen valt, daarna vragen van je Fleet, dan vervolgacties van een bord en vervolgens de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine eraan werkt en wanneer hij klaar is. Alleen de markering verandert. In de andere open groepen staan eerst to-do's waarvan de deadline is verstreken of morgen valt, gevolgd door de rest, met de nieuwste bovenaan. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals 'PR #3451 samengevoegd', maar dat het nog niet is gesloten. Met **Heropenen** zet je de to-do terug op je lijst. Je Machine leert ervan. Deze to-do's worden nooit als te laat weergegeven. Als een bericht laat zien dat de to-do is afgerond, sluit hij na een dag vanzelf, met **Ongedaan maken**. Anders wacht hij tot je op **Als gedaan markeren** tikt. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf gesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: 'Dit is niet Sam Lee.' De afzender wordt weergegeven met zijn eigen adres, nooit met de naam die hij heeft opgegeven. Je Machine controleert zo'n bericht bij de persoon van wie je het adres al hebt, nooit bij de afzender.

Bij een to-do waarvoor je nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, staat **Wacht op:** die stap. De to-do staat ingeklapt onder **Wacht op anderen**, boven Komt later terug, tot er een nieuw bericht binnenkomt. Hetzelfde geldt nadat je een vraag hebt teruggestuurd: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later vandaag valt, of de volgende ochtend als de deadline al voorbij is. Er staat bij op wie je nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Als jij jouw deel verstuurt, wordt de to-do niet gesloten. Hij blijft onder **Wacht op anderen** staan tot een bericht het resultaat laat zien. Daarna wordt hij vanzelf gesloten, met **Ongedaan maken**. Als er niets binnenkomt tegen de tijd dat je diegene een herinnering moet sturen, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als er een week niets nieuws bij een to-do komt, verhuist hij van Voor jou naar **Ouder**. Zo staan nieuwe to-do's bovenaan als je na een paar dagen weer terugkomt. Niets nieuws betekent dat er geen nieuw bericht over is en dat jij er niets aan hebt gedaan, zoals een chatbericht sturen, iets bewerken of snoozen. Alleen de to-do bekijken telt niet mee.

Dringende to-do's, to-do's met een naderende deadline en to-do's waarvan iets onderweg is om verstuurd te worden, blijven onder Voor jou staan. Met **Alles afwijzen** markeer je na één bevestiging alle to-do's onder Ouder als niet nodig. Dat doet hetzelfde als **Niet nodig**, maar dan één voor één, met **Ongedaan maken**. Als er iets nieuws gebeurt bij een to-do, komt hij terug onder Voor jou.

Bij een to-do waar een week lang niemand iets mee heeft gedaan, verschijnt één keer de vraag **Nog nodig?** Met **Niet nodig** sluit je hem, met **Ongedaan maken**. Met **Houden** houd je hem en wordt de vraag nooit meer gesteld. Als je nog een week niet reageert, wordt de to-do ingeklapt onder Komt later terug. Het aantal op het appicoon en in het ochtendoverzicht telt hem dan niet meer mee. De to-do komt terug als je hem opent, een chatbericht stuurt, iets bewerkt of snoozet, of als er een nieuw bericht binnenkomt.

Een project waar een week lang niets is gebeurd en geen open to-do's heeft, kan één keer per week een to-do krijgen met een specifieke volgende stap. Dat gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als niets je aandacht nodig heeft, rust je Machine uit met een lege lijst. Terwijl hij controleert, wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen to-do's van één soort. Op je telefoon en computer wordt dezelfde keuze getoond. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en wordt alleen onder Alle weergegeven.

Met de regel bovenaan de lijst schakel je ook meteen over naar de andere weergave: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst vermeldt de naam van je laatste ochtend- of avondoverzicht en wat erin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** plak je het ergens anders. Zodra je het overzicht opent of op **×** tikt, staat het op al je apparaten tot het volgende overzicht.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de naam van het project onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Zie [To-do's voor een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die hij mag lezen en versturen, verhuist mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij vandaan komt daar staan, wordt hij vanzelf daarheen verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je zelf hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een ander bedrijf van je komt bij de to-do's van dat bedrijf terecht. Een to-do over je eigen leven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant op WhatsApp, een bestelling in je persoonlijke mailbox of een [belofte](promises.md) over werk, valt vanaf het begin onder Werk.

Een to-do die je zelf hebt verplaatst of geplaatst, blijft altijd staan waar je hem hebt gezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, nooit waar hij op antwoordt. Een antwoord gaat altijd naar de plek waar het gesprek plaatsvindt, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de mail is binnengekomen. Hij verschijnt nooit in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's op je wachten, loopt **Doorlopen** in de kop van Voor jou ze één voor één langs, in de volgorde van de lijst. Je ziet elk concept helemaal, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat er op het scherm staat, met `S` snooze je, met `→` sla je over en met Esc stop je. In de kop staat hoelang het duurt als je jouw tempo aanhoudt, zoals 'ongeveer 2 min'.

Aan het einde zie je hoeveel to-do's zijn verstuurd of gesloten en hoeveel er nog worden klaargezet.

Een to-do met een vraag aan jou wordt bij allebei niet meegenomen: daarvoor is je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten wachten of het oudste bericht van een persoon 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden meegenomen bij de volgende controle, binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat 'Nachtpauze, haalt om 06:30 in'. Klik, typ of scroll in de app, schrijf in de chat of tik 's nachts op een to-do en de controles lopen weer zoals gewoonlijk tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen alle bronnen. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat de regel bovenaan op een computer. Een korte regel wordt daar alleen weergegeven terwijl er een controle loopt, of als die is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden uit alle gelezen bronnen, zoals '13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's' of '· 2 nieuwe to-do's'. De regel gaat alleen over die controle: to-do's die al op je lijst staan, blijven zoals ze zijn. Als een nieuwe to-do op een beter moment wacht, zoals je ochtendoverzicht, staat erbij tot wanneer: '1 to-do uitgesteld tot morgen 08:30'.

Tik op de regel om elke e-mailthread, chat en melding te zien, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de bijbehorende nieuwe to-do of waarom er niets nodig was, zoals 'Alleen in cc, een teamgenoot antwoordt' of 'Afspraak staat al voor donderdag'. Bij een thread wordt geen reden getoond als de controle alleen een vage reden gaf. Tik op een bericht om het te lezen, met de rest van het gesprek erbij.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine zelf aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt zoals gewoonlijk gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan of, zodra er een concept klaarstaat, wat erin moet veranderen. **Als gedaan markeren** betekent dat je het hebt afgehandeld. Bij een klaargezette to-do zonder concept of bij een to-do met een vraag aan jou staat deze optie meteen in beeld. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in het bericht. Veeg het bericht weg of sleep het met de muis van de lijst om het eerder te sluiten. De wijziging blijft behouden.

Wil je dat het op een andere manier wordt gedaan, zeg dat dan in de **Chat**. In het antwoord staat alleen wat er is veranderd, zoals een snooze en tot wanneer. Als iets niet kon worden aangepast, bijvoorbeeld een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om de to-do te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt optioneel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt dit ook in de chat vragen, bijvoorbeeld: 'Hernoem dit naar …'. De titel die je kiest, blijft behouden.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van diegene, maar niet na je eigen antwoord. Je ziet dan wanneer hij is teruggekomen en hij wordt gerangschikt als nieuw. De chat gaat verder waar hij gebleven was, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die alleen tot een bepaald tijdstip van belang is, zoals een bevestiging vóór een meeting, wordt na dat tijdstip vanzelf gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding 'Niet meer nodig'. Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de mensen die erbij betrokken zijn, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand erom werd gevraagd en ja zei, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als iemand anders na het maken van je concept iets in hetzelfde gesprek heeft geschreven, houdt **Versturen** het concept tegen: 'Niet verstuurd: nieuw bericht in de thread'. Bij de to-do wordt dat bericht getoond met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept te versturen zoals het is.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, past The Machine zijn to-do's zelf aan. Een to-do die nog steeds nodig is, volgt het nieuwe plan. Een to-do waarvoor niets meer hoeft te gebeuren, wordt verplaatst naar **Gedaan / afgewezen** met de melding 'Niet nodig'. In de chat staat 'Bijgewerkt:' met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's zie je een korte tip over de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en dat er niets wordt verstuurd tot je op **Versturen** drukt. De tip verdwijnt voorgoed zodra je de knop gebruikt of op × drukt.

Op je eerste dag heet de kop van To-do's je welkom en vermeldt hij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je terugkomt.

Elke to-do begint met de titel. De regel eronder vermeldt op wie de to-do betrekking heeft, de organisatie als die relevant is (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij namen en organisaties wordt een foto of logo getoond als de Graph dat heeft, anders de initialen. Als een logo op dat formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook de initiaal getoond.

Soms staat er in een rustige regel wat niet bekend is, zoals 'Laatste contact 12 dagen geleden via e-mail; sindsdien niets.' Deze regel verschijnt als het laatste contact met diegene oud is of nog geen antwoord heeft gekregen. Ook kan hij kanalen noemen die niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van iets te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel zegt wat er moet gebeuren en verandert alleen als dat ook verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, zoals 'Gedaan: Sam heeft dinsdag getekend'.

Boven het concept staat in een vage regel van welk bericht het afkomstig is, met het logo van de dienst. Tik erop om de thread te lezen. Bij het concept staat het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het om een Slack-antwoord of e-mail gaat.

Als het concept is gebaseerd op iemands input elders, zoals een suggestie van een teamgenoot in Slack, staat dat erbij, zoals 'Gebaseerd op Sam in #ops'. Tik erop om dat bericht te lezen. Het bericht verdwijnt zodra er een update is die het concept vervangt.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek weergegeven, van oud naar nieuw: de berichten van vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan jouw berichten rechts, net als in de app. Het bericht van de to-do is gemarkeerd met 'Deze to-do' en wordt geopend in beeld. Met **Eerdere berichten tonen** voeg je oudere berichten toe. De rest van een e-mailthread wordt boven en onder de e-mail ingeklapt weergegeven.

Een bericht wordt op dezelfde manier geopend vanuit Zoeken, de Graph, antwoorden van Ask of de laatste controle, met de markering 'Dit bericht' (of 'Nieuwe berichten').

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt de Gmail-app geopend als je die hebt.

Bij **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige cc-adressen, bcc of een ander antwoordadres. Als er niets extra's is, wordt er niets weergegeven.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link bij de to-do open je het bijbehorende bericht hier ook, met onderaan **Openen in Slack**.

Bij **Details** staan de naam, het project en het gebied (tik erop om het te wijzigen), je laatste notitie en het resultaat van een codeeragent. Met de titel open je de chat. Een afgeronde to-do blijft kort; het bericht waar hij vandaan komt, staat onder **Details**.

Bij een to-do met 'Wacht op' staat een link naar je laatste bericht aan diegene, waarop je wacht: 'E-mail aan Pat · di'.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Een to-do maken verstuurt niets. Als je geen **Werk** of **Privé** kiest, komt hij terecht waar hij thuishoort, op basis van wie en wat erbij hoort. Je Machine zoekt ook de e-mail op waar de to-do op aansluit, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals 'morgen', 'volgende vr', '3 nov', '14:00' of 'over 2 uur'. Dat kan ook in je eigen taal. Met het kalendericoon zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de mensen of bedrijven bij wie de to-do hoort, maximaal 5.
- Berichticoon: voeg het bericht toe waar de to-do over gaat, zoals een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en je Machine leest ze wanneer hij eraan werkt. Je kunt ook alleen bestanden toevoegen: je Machine maakt de to-do dan op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te zien.
